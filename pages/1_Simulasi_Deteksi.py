import os
import sys
import urllib.request

import numpy as np
import cv2
import streamlit as st
from PIL import Image

# Agar bisa import modul `common` dari root project saat dijalankan sebagai
# halaman di dalam folder pages/
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import (
    inject_css,
    sidebar_nav,
    page_header,
    info_box,
    divider,
    metric_card,
    icon,
)

try:
    import torch
    import torch.nn as nn
    from ultralytics import YOLO
    from ultralytics.nn import tasks as ultralytics_tasks

    # ─────────────────────────────────────────────
    # TRIPLET ATTENTION MODULE
    # Paper: "Rotate to Attend: Convolutional Triplet Attention Module" (WACV 2021)
    # HARUS identik dengan definisi yang dipakai saat training, agar:
    #   1. Unpickling checkpoint .pt berhasil (class harus ditemukan & sama strukturnya)
    #   2. Bobot state_dict cocok dengan arsitektur layer yang dibangun ulang di sini
    # ─────────────────────────────────────────────
    class ZPool(nn.Module):
        """Concatenate max-pool and avg-pool along channel dim."""
        def forward(self, x):
            return torch.cat([
                x.max(dim=1, keepdim=True)[0],
                x.mean(dim=1, keepdim=True)
            ], dim=1)

    class AttentionGate(nn.Module):
        """Single branch: spatial attention along one pair of axes."""
        def __init__(self, kernel_size=7):
            super().__init__()
            pad = kernel_size // 2
            self.compress = ZPool()
            self.conv = nn.Conv2d(2, 1, kernel_size, padding=pad, bias=False)
            self.bn = nn.BatchNorm2d(1)

        def forward(self, x):
            attn = torch.sigmoid(self.bn(self.conv(self.compress(x))))
            return x * attn

    class TripletAttention(nn.Module):
        """
        Triplet Attention: three rotated attention branches
          Branch 1: H x W  (standard spatial, C-W-H rotated)
          Branch 2: C x W  (channel-width)
          Branch 3: C x H  (channel-height)
        """
        def __init__(self, kernel_size=7):
            super().__init__()
            self.branch1 = AttentionGate(kernel_size)  # H x W
            self.branch2 = AttentionGate(kernel_size)  # C x W
            self.branch3 = AttentionGate(kernel_size)  # C x H

        def forward(self, x):
            # Branch 1: normal H-W attention
            b1 = self.branch1(x)
            # Branch 2: rotate to C-W plane
            x2 = x.permute(0, 2, 1, 3)
            b2 = self.branch2(x2).permute(0, 2, 1, 3)
            # Branch 3: rotate to C-H plane
            x3 = x.permute(0, 3, 2, 1)
            b3 = self.branch3(x3).permute(0, 3, 2, 1)
            return (b1 + b2 + b3) / 3.0

    # Daftarkan class ke parser Ultralytics agar terbaca saat memuat
    # checkpoint/arsitektur YAML yang memuat layer TripletAttention
    ultralytics_tasks.TripletAttention = TripletAttention

    ULTRALYTICS_OK = True
except ImportError:
    ULTRALYTICS_OK = False

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LungDetection | Deteksi Tumor Paru",
    page_icon=":material/pulmonology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# ─────────────────────────────────────────────
# KONFIGURASI MODEL — SESUAIKAN BAGIAN INI
#    Tidak perlu mendefinisikan nama kelas secara manual:
#    nama kelas otomatis diambil dari file model YOLOv8 (model.names)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_CONFIG = {
    # Path lokal tempat bobot model akan dicari/disimpan
    "local_path": os.path.join(BASE_DIR, "models", "yolov8_lung_tumor_best.pt"),
    # Ganti dengan URL GitHub Release / cloud storage tempat bobot .pt Anda disimpan
    "download_url": "https://github.com/USERNAME/REPO/releases/download/v1.0/yolov8_lung_tumor_best.pt",
    "default_conf": 0.25,
    "default_iou": 0.45,
}

# Palet warna untuk bounding box, dipilih berputar berdasarkan index kelas
BOX_PALETTE = [
    (220, 38, 38),   # merah
    (37, 99, 235),   # biru
    (217, 119, 6),   # oranye
    (5, 150, 105),   # hijau
    (124, 58, 237),  # ungu
]


# ─────────────────────────────────────────────
# LOAD MODEL YOLOv8 (CACHE RESOURCE)
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    if not ULTRALYTICS_OK:
        raise RuntimeError(
            "Library 'ultralytics' belum terpasang. Jalankan: pip install ultralytics"
        )

    model_dir = os.path.dirname(MODEL_CONFIG["local_path"])
    os.makedirs(model_dir, exist_ok=True)

    if not os.path.exists(MODEL_CONFIG["local_path"]):
        with st.spinner("Mengunduh bobot model YOLOv8 dari server. Mohon tunggu sebentar."):
            try:
                urllib.request.urlretrieve(MODEL_CONFIG["download_url"], MODEL_CONFIG["local_path"])
            except Exception as e:
                raise RuntimeError(
                    f"Gagal mengunduh model. Pastikan 'download_url' pada MODEL_CONFIG sudah benar "
                    f"dan ada koneksi internet. Error: {e}"
                )

    model = YOLO(MODEL_CONFIG["local_path"])
    return model


# ─────────────────────────────────────────────
# SIDEBAR — logo, navigasi, & pengaturan deteksi khusus halaman ini
# ─────────────────────────────────────────────
conf_threshold = MODEL_CONFIG["default_conf"]
iou_threshold = MODEL_CONFIG["default_iou"]


def _detection_controls():
    global conf_threshold, iou_threshold
    st.markdown('<div class="sidebar-section-title">Pengaturan Deteksi</div>', unsafe_allow_html=True)
    conf_threshold = st.slider(
        "Confidence Threshold", min_value=0.05, max_value=0.95,
        value=MODEL_CONFIG["default_conf"], step=0.05
    )
    iou_threshold = st.slider(
        "IoU Threshold (NMS)", min_value=0.05, max_value=0.95,
        value=MODEL_CONFIG["default_iou"], step=0.05
    )


sidebar_nav(extra_controls=_detection_controls)

# ─────────────────────────────────────────────
# KONTEN HALAMAN — SIMULASI / INFERENSI
# ─────────────────────────────────────────────
page_header(
    "Uji Model",
    "Deteksi Tumor Paru",
    "Unggah gambar CT-Scan / X-Ray paru untuk menguji model YOLOv8 secara langsung."
)

info_box(
    "Unggah gambar paru (format JPG/PNG/BMP). Model YOLOv8 akan melakukan inferensi dan "
    "menampilkan bounding box beserta label serta tingkat keyakinan (confidence) untuk setiap "
    "area yang terindikasi tumor."
)

uploaded_file = st.file_uploader(
    "Seret & lepas gambar di sini, atau klik untuk memilih",
    type=["jpg", "jpeg", "png", "bmp"]
)

if uploaded_file is not None:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">'
            f'<span style="width:20px;height:20px;display:inline-flex;">{icon("camera")}</span>'
            f'<span style="font-weight:600;color:var(--blue-dark);">Gambar Input</span></div>',
            unsafe_allow_html=True,
        )
        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, use_column_width=True)

    boxes, confs, cls_idx, names = [], [], [], {}
    inference_error = None

    with st.spinner("Memproses gambar dengan YOLOv8..."):
        try:
            model = load_model()
            results = model.predict(
                source=np.array(image),
                conf=conf_threshold,
                iou=iou_threshold,
                verbose=False
            )
            r = results[0]
            names = r.names  # dict {index: nama_kelas} sesuai training

            if r.boxes is not None and len(r.boxes) > 0:
                boxes = r.boxes.xyxy.cpu().numpy()
                confs = r.boxes.conf.cpu().numpy()
                cls_idx = r.boxes.cls.cpu().numpy().astype(int)
        except Exception as e:
            inference_error = str(e)

    if inference_error:
        st.markdown(
            f'<div class="info-box" style="border-left-color:#B45309;background:linear-gradient(to right, #FEF3E2, #FFFBF3);">'
            f'<div class="icon-chip" style="background:rgba(180,83,9,0.12);">{icon("warning")}</div>'
            f'<p>Terjadi kesalahan saat inferensi: {inference_error}</p></div>',
            unsafe_allow_html=True,
        )
    else:
        img_result = np.array(image).copy()
        html_details = ""

        for box, label_idx, score in zip(boxes, cls_idx, confs):
            x_min, y_min, x_max, y_max = map(int, box)
            class_name = names.get(int(label_idx), f"Kelas {label_idx}")
            conf_pct = score * 100
            color = BOX_PALETTE[int(label_idx) % len(BOX_PALETTE)]

            cv2.rectangle(img_result, (x_min, y_min), (x_max, y_max), color, 2)
            label_text = f"{class_name}: {conf_pct:.1f}%"
            cv2.putText(
                img_result, label_text, (x_min, max(y_min - 10, 0)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2
            )

            html_details += f"""
            <div style="display:flex;align-items:center;gap:0.75rem;margin-bottom:0.5rem;flex-wrap:wrap;">
                <span class="tag">{class_name}</span>
                <span style="font-size:0.85rem;color:var(--text-dark);font-weight:500;">Confidence: {conf_pct:.1f}%</span>
                <span style="font-size:0.75rem;color:var(--text-light);margin-left:auto;">BBox: [{x_min}, {y_min}, {x_max}, {y_max}]</span>
            </div>
            """

        with col2:
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">'
                f'<span style="width:20px;height:20px;display:inline-flex;">{icon("target")}</span>'
                f'<span style="font-weight:600;color:var(--blue-dark);">Hasil Deteksi</span></div>',
                unsafe_allow_html=True,
            )
            st.image(img_result, use_column_width=True)

            if len(boxes) > 0:
                card_html = (
                    '<div style="background:var(--blue-pale);border:1px solid var(--border);'
                    'border-radius:12px;padding:1rem 1.25rem;margin-top:0.75rem;">'
                    '<div style="font-size:0.75rem;color:var(--text-light);letter-spacing:1px;'
                    'text-transform:uppercase;font-weight:600;margin-bottom:0.75rem;">'
                    'Rincian Prediksi'
                    '</div>'
                    + html_details +
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)

                _, buf = cv2.imencode(".png", cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR))
                st.download_button(
                    "Unduh Gambar Hasil Deteksi",
                    data=buf.tobytes(),
                    file_name="hasil_deteksi_tumor_paru.png",
                    mime="image/png"
                )
            else:
                st.warning("Tidak ada area tumor yang terdeteksi pada confidence threshold saat ini.")

        if len(boxes) > 0:
            divider()
            st.markdown("### Ringkasan Deteksi")
            sum_col1, sum_col2, sum_col3 = st.columns(3)
            with sum_col1:
                metric_card(str(len(boxes)), "Total Objek Terdeteksi")
            with sum_col2:
                metric_card(f"{confs.max() * 100:.1f}%", "Confidence Tertinggi")
            with sum_col3:
                kelas_terbanyak_idx = np.bincount(cls_idx).argmax()
                metric_card(names.get(int(kelas_terbanyak_idx), "-"), "Kelas Terbanyak")

divider()
st.markdown("""
<div style="text-align:center;padding:1.5rem;color:var(--text-light);font-size:0.85rem;">
    LungDetection &middot; YOLOv8 Lung Tumor Detection<br>
    Dibangun dengan Streamlit &amp; Ultralytics YOLOv8
</div>
""", unsafe_allow_html=True)