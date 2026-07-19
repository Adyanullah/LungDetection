import streamlit as st
from common import (
    inject_css,
    sidebar_nav,
    page_header,
    section_title,
    card,
    info_box,
    divider,
    metric_card,
    result_card,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="PulmoVision | Tentang Model",
    page_icon=":material/pulmonology:",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
sidebar_nav()

# ─────────────────────────────────────────────
# HEADER HALAMAN
# ─────────────────────────────────────────────
page_header(
    "Dokumentasi Model",
    "Tentang Model & Proses Training",
    "Ringkasan singkat arsitektur, dataset, dan konfigurasi training di balik PulmoVision."
)

info_box(
    "Halaman ini menjelaskan secara ringkas bagaimana model deteksi pada aplikasi ini "
    "dilatih &mdash; mulai dari library yang digunakan, arsitektur, sumber data, hingga strategi "
    "augmentasi. Untuk mencoba modelnya secara langsung, buka halaman <b>Simulasi Deteksi</b> "
    "pada menu sebelah kiri."
)

divider()

# ─────────────────────────────────────────────
# HASIL TRAINING TERBAIK (SKENARIO YANG DI-DEPLOY)
# ─────────────────────────────────────────────
section_title("Hasil Training Model yang Digunakan", "trophy")

info_box(
    "Model yang digunakan pada aplikasi ini merupakan hasil dari <b>skenario training terbaik</b> "
    "di antara seluruh eksperimen yang telah dilakukan. Berikut performanya pada data evaluasi:"
)

res_col1, res_col2, res_col3, res_col4 = st.columns(4)
with res_col1:
    result_card("0.9165", "mAP@0.5")
with res_col2:
    result_card("0.6808", "mAP@0.5:0.95")
with res_col3:
    result_card("0.9401", "Precision")
with res_col4:
    result_card("0.8608", "Recall")

divider()

# ─────────────────────────────────────────────
# LIBRARY YANG DIGUNAKAN
# ─────────────────────────────────────────────
section_title("Library yang Digunakan", "wrench")

lib_col1, lib_col2, lib_col3, lib_col4 = st.columns(4)
with lib_col1:
    card("Ultralytics YOLOv8", "Framework utama untuk arsitektur, training loop, dan inferensi model deteksi objek.")
with lib_col2:
    card("PyTorch", "Backend deep learning tempat YOLOv8 dan modul Triplet Attention custom dibangun.")
with lib_col3:
    card("OpenCV", "Preprocessing citra CT-scan (windowing, resize) serta menggambar bounding box hasil deteksi.")
with lib_col4:
    card("Streamlit", "Membangun antarmuka web interaktif untuk mendemonstrasikan hasil deteksi model.")

st.markdown("""
<div style="margin-top:-0.5rem;">
    <span class="tag">NumPy</span>
    <span class="tag">Pillow (PIL)</span>
    <span class="tag">Pandas</span>
    <span class="tag">Matplotlib</span>
    <span class="tag">Pydicom</span>
</div>
""", unsafe_allow_html=True)

divider()

# ─────────────────────────────────────────────
# ARSITEKTUR MODEL
# ─────────────────────────────────────────────
section_title("Arsitektur Model", "layers")

card(
    "YOLOv8 + Triplet Attention",
    "Model dibangun di atas arsitektur <b>YOLOv8</b> sebagai basis deteksi objek, dengan "
    "tambahan modul <b>Triplet Attention</b> (Rotate to Attend, WACV 2021). Modul ini "
    "menangkap interaksi cross-dimension antara channel dan spasial (tinggi &amp; lebar) "
    "melalui tiga cabang perhatian yang saling melengkapi, tanpa menambah parameter yang "
    "signifikan &mdash; bertujuan mempertajam fokus model pada area nodul yang sering berukuran "
    "kecil pada citra CT paru."
)

st.markdown(f"""
<div class="card">
    <h3>Alur Perhatian Triplet Attention</h3>
    <div class="step-row">
        <div class="step-num">1</div>
        <div class="step-text"><b>Branch H&times;W</b><p>Perhatian spasial standar pada bidang tinggi&ndash;lebar dari feature map.</p></div>
    </div>
    <div class="step-row">
        <div class="step-num">2</div>
        <div class="step-text"><b>Branch C&times;W</b><p>Feature map dirotasi ke bidang channel&ndash;lebar untuk menangkap interaksi antar channel dan lebar.</p></div>
    </div>
    <div class="step-row">
        <div class="step-num">3</div>
        <div class="step-text"><b>Branch C&times;H</b><p>Feature map dirotasi ke bidang channel&ndash;tinggi untuk menangkap interaksi antar channel dan tinggi.</p></div>
    </div>
    <div class="step-row" style="border-bottom:none;">
        <div class="step-num">4</div>
        <div class="step-text"><b>Agregasi</b><p>Ketiga cabang dirata-ratakan untuk menghasilkan feature map akhir yang lebih fokus dan informatif.</p></div>
    </div>
</div>
""", unsafe_allow_html=True)

divider()

# ─────────────────────────────────────────────
# DATASET
# ─────────────────────────────────────────────
section_title("Dataset", "database")

card(
    "LIDC-IDRI (Lung Image Database Consortium)",
    "Model dilatih menggunakan dataset publik <b>LIDC-IDRI</b>, berupa citra CT-scan paru "
    "dengan bidang potong <b>axial</b>. Setiap slice diproses dari format DICOM, dilakukan "
    "<i>lung windowing</i>, lalu anotasi nodul (dalam format XML) dikonversi ke format label "
    "YOLO."
)

ds_col1, ds_col2, ds_col3 = st.columns(3)
with ds_col1:
    metric_card("Axial", "Bidang Citra CT")
with ds_col2:
    metric_card("1&ndash;5 &rarr; 1&ndash;3", "Penyederhanaan Skala Keganasan")
with ds_col3:
    metric_card("3 Kelas", "Benign &middot; Indeterminate &middot; Malignant")

info_box(
    "Skala keganasan (malignancy) asli pada LIDC-IDRI yang berskala <b>1&ndash;5</b> "
    "disederhanakan menjadi <b>3 kelas</b> agar lebih relevan secara klinis dan mengurangi "
    "ambiguitas antar kelas yang berdekatan: <b>Benign</b>, <b>Indeterminate</b>, dan "
    "<b>Malignant</b>."
)

divider()

# ─────────────────────────────────────────────
# REBALANCING DATASET
# ─────────────────────────────────────────────
section_title("Penyeimbangan Dataset (Rebalancing)", "scale")

card(
    "Horizontal Flip untuk Menyeimbangkan Kelas",
    "Distribusi jumlah nodul antar tiga kelas malignancy pada dataset awal tidak seimbang. "
    "Untuk mengatasi hal ini, dilakukan <b>rebalancing</b> dengan menambahkan salinan "
    "<i>horizontal flip</i> pada data dari kelas minoritas, sehingga jumlah sampel training "
    "antar kelas menjadi lebih seimbang tanpa perlu mengumpulkan data baru."
)

divider()

# ─────────────────────────────────────────────
# KONFIGURASI AUGMENTASI TRAINING
# ─────────────────────────────────────────────
section_title("Konfigurasi Augmentasi Training", "sliders")

info_box(
    "Sebagian besar augmentasi bawaan (default) dari YOLOv8 <b>dinonaktifkan</b>. "
    "Hal ini dilakukan karena rebalancing kelas sudah ditangani secara manual melalui "
    "horizontal flip, sehingga augmentasi acak tambahan yang berlebihan berpotensi "
    "mendistorsi karakteristik nodul kecil pada citra CT."
)

aug_col1, aug_col2, aug_col3 = st.columns(3)
with aug_col1:
    metric_card("0.05", "Translate")
with aug_col2:
    metric_card("0.05", "Scale")
with aug_col3:
    metric_card("5.0°", "Degrees (Rotasi)")

divider()

st.markdown("""
<div style="text-align:center;padding:1.5rem;color:var(--text-light);font-size:0.85rem;">
    PulmoVision &middot; YOLOv8 + Triplet Attention &mdash; Lung Tumor Detection<br>
    Dataset: LIDC-IDRI
</div>
""", unsafe_allow_html=True)