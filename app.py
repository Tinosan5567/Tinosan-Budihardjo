import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

st.set_page_config(
    page_title="Dashboard KP - PT. Gramar Jaya",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-title {
        font-size: 2rem; font-weight: 700; color: #1a3c5e;
        border-bottom: 3px solid #e74c3c; padding-bottom: 8px; margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a3c5e, #2980b9);
        color: white; padding: 20px; border-radius: 12px;
        text-align: center; margin: 5px;
    }
    .metric-value { font-size: 2rem; font-weight: 700; }
    .metric-label { font-size: 0.85rem; opacity: 0.9; margin-top: 5px; }
    .section-header {
        background: #1a3c5e; color: white; padding: 10px 16px;
        border-radius: 8px; font-weight: 600; margin: 20px 0 10px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    np.random.seed(42)
    tanggal = pd.date_range("2024-01-02", periods=26, freq="W")
    produksi = np.random.randint(280, 340, 26)
    jenis_cacat = [
        "Label miring/salah tempel",
        "Tutup bocor/tidak rapat",
        "Volume tidak sesuai",
        "Kaleng penyok",
        "Warna tidak sesuai"
    ]
    cacat_data = {
        jenis_cacat[0]: np.random.randint(3, 12, 26),
        jenis_cacat[1]: np.random.randint(2, 9, 26),
        jenis_cacat[2]: np.random.randint(1, 6, 26),
        jenis_cacat[3]: np.random.randint(1, 5, 26),
        jenis_cacat[4]: np.random.randint(0, 4, 26),
    }
    df_cacat = pd.DataFrame(cacat_data)
    total_cacat = df_cacat.sum(axis=1)
    df = pd.DataFrame({
        "Minggu": [f"W{i+1}" for i in range(26)],
        "Tanggal": tanggal,
        "Jumlah Produksi": produksi,
        "Total Cacat": total_cacat,
    })
    for col in df_cacat.columns:
        df[col] = df_cacat[col].values
    df["% Cacat"] = (df["Total Cacat"] / df["Jumlah Produksi"] * 100).round(2)
    return df

@st.cache_data
def load_fmea():
    df = pd.DataFrame({
        "No": range(1, 6),
        "Jenis Kegagalan": [
            "Label miring/salah tempel",
            "Tutup bocor/tidak rapat",
            "Volume tidak sesuai",
            "Kaleng penyok",
            "Warna tidak sesuai"
        ],
        "Efek Kegagalan": [
            "Tampilan produk buruk, komplain pelanggan",
            "Tumpah saat pengiriman, bahaya",
            "Tidak memenuhi spesifikasi regulasi",
            "Kerusakan fisik, estetika buruk",
            "Produk tidak sesuai pesanan"
        ],
        "Penyebab": [
            "Operator kurang teliti, mesin labeler aus",
            "Setting torsi tutup tidak tepat",
            "Kalibrasi mesin pengisian tidak akurat",
            "Penanganan kasar saat packing",
            "Kesalahan pencampuran pigmen"
        ],
        "Severity": [7, 9, 8, 6, 8],
        "Occurrence": [8, 6, 5, 4, 3],
        "Detection": [6, 7, 6, 5, 6],
    })
    df["RPN"] = df["Severity"] * df["Occurrence"] * df["Detection"]
    return df

df = load_data()
df_fmea = load_fmea()

JENIS_CACAT = [
    "Label miring/salah tempel",
    "Tutup bocor/tidak rapat",
    "Volume tidak sesuai",
    "Kaleng penyok",
    "Warna tidak sesuai"
]

# Sidebar
st.sidebar.title("📋 Menu Navigasi")
halaman = st.sidebar.radio("Pilih Halaman:", [
    "🏠 Home",
    "📊 Data Cacat",
    "📈 P-Chart",
    "📉 Pareto Chart",
    "⚠️ FMEA"
])
st.sidebar.markdown("---")
st.sidebar.markdown("**Filter Data:**")
minggu_range = st.sidebar.slider("Rentang Minggu:", 1, 26, (1, 26))
df_f = df.iloc[minggu_range[0]-1: minggu_range[1]]
st.sidebar.markdown("---")
st.sidebar.markdown("**Mahasiswa KP:**")
st.sidebar.markdown("👤 Teknik Industri - UMAHA")
st.sidebar.markdown("🏭 PT. Gramar Jaya, Wringinanom")
st.sidebar.markdown("📦 Divisi QC - Packing")

# ── HOME ──────────────────────────────────────────────────────────────────────
if halaman == "🏠 Home":
    st.markdown('<div class="main-title">🏭 Dashboard Analisis Kualitas Packing — PT. Gramar Jaya</div>', unsafe_allow_html=True)

    total_prod = df_f["Jumlah Produksi"].sum()
    total_cacat = df_f["Total Cacat"].sum()
    pct_baik = 100 - (total_cacat / total_prod * 100)
    rpn_max = df_fmea["RPN"].max()

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="metric-card"><div class="metric-value">{total_prod:,}</div><div class="metric-label">Total Produksi (unit)</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="metric-card"><div class="metric-value">{total_cacat:,}</div><div class="metric-label">Total Produk Cacat</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="metric-card"><div class="metric-value">{pct_baik:.1f}%</div><div class="metric-label">Tingkat Kualitas</div></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="metric-card"><div class="metric-value">{rpn_max}</div><div class="metric-label">RPN Tertinggi (FMEA)</div></div>', unsafe_allow_html=True)

    st.markdown("")
    st.markdown('<div class="section-header">📊 Tren Produksi & Cacat per Minggu</div>', unsafe_allow_html=True)
    fig, ax1 = plt.subplots(figsize=(12, 4))
    x = range(len(df_f))
    ax1.bar(x, df_f["Jumlah Produksi"], color="#2980b9", alpha=0.7, label="Produksi")
    ax1.set_ylabel("Jumlah Produksi (unit)", color="#2980b9")
    ax2 = ax1.twinx()
    ax2.plot(x, df_f["Total Cacat"], color="#e74c3c", marker="o", linewidth=2, label="Cacat")
    ax2.set_ylabel("Total Cacat (unit)", color="#e74c3c")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_f["Minggu"], rotation=45, fontsize=8)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown('<div class="section-header">📋 Ringkasan Data</div>', unsafe_allow_html=True)
        st.dataframe(df_f[["Minggu", "Tanggal", "Jumlah Produksi", "Total Cacat", "% Cacat"]], use_container_width=True, height=300)
    with col_r:
        st.markdown('<div class="section-header">🥧 Distribusi Jenis Cacat</div>', unsafe_allow_html=True)
        totals = df_f[JENIS_CACAT].sum()
        fig2, ax = plt.subplots(figsize=(5, 4))
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#3498db"]
        wedges, _, autotexts = ax.pie(totals, autopct='%1.1f%%', colors=colors, startangle=90, pctdistance=0.8, labels=None)
        ax.legend(wedges, [c[:22] for c in JENIS_CACAT], loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=7)
        fig2.tight_layout()
        st.pyplot(fig2)
        plt.close()

# ── DATA CACAT ────────────────────────────────────────────────────────────────
elif halaman == "📊 Data Cacat":
    st.markdown('<div class="main-title">📊 Data Cacat Produksi per Jenis</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">📋 Tabel Data Lengkap</div>', unsafe_allow_html=True)
    cols_tampil = ["Minggu", "Tanggal", "Jumlah Produksi"] + JENIS_CACAT + ["Total Cacat", "% Cacat"]
    st.dataframe(df_f[cols_tampil], use_container_width=True, height=400)

    st.markdown('<div class="section-header">📊 Total Cacat per Jenis</div>', unsafe_allow_html=True)
    totals = df_f[JENIS_CACAT].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.barh(totals.index, totals.values, color=["#3498db","#2ecc71","#f1c40f","#e67e22","#e74c3c"])
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.set_xlabel("Jumlah Cacat (unit)")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="section-header">📈 Tren Cacat per Minggu</div>', unsafe_allow_html=True)
    jenis_pilih = st.multiselect("Pilih jenis cacat:", JENIS_CACAT, default=JENIS_CACAT[:3])
    if jenis_pilih:
        fig3, ax = plt.subplots(figsize=(12, 4))
        colors2 = ["#e74c3c","#e67e22","#f1c40f","#2ecc71","#3498db"]
        for i, col in enumerate(jenis_pilih):
            ax.plot(df_f["Minggu"], df_f[col], marker="o", label=col[:30], color=colors2[i % 5], linewidth=1.5)
        ax.set_xlabel("Minggu")
        ax.set_ylabel("Jumlah Cacat")
        ax.legend(fontsize=8)
        ax.set_xticklabels(df_f["Minggu"], rotation=45, fontsize=8)
        fig3.tight_layout()
        st.pyplot(fig3)
        plt.close()

# ── P-CHART ───────────────────────────────────────────────────────────────────
elif halaman == "📈 P-Chart":
    st.markdown('<div class="main-title">📈 P-Chart — Peta Kendali Proporsi Cacat</div>', unsafe_allow_html=True)

    n = df_f["Jumlah Produksi"].values
    np_val = df_f["Total Cacat"].values
    p = np_val / n
    p_bar = np_val.sum() / n.sum()
    ucl = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / n)
    lcl = np.maximum(0, p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / n))

    c1, c2, c3 = st.columns(3)
    c1.metric("P̄ (Rata-rata Proporsi Cacat)", f"{p_bar:.4f}")
    c2.metric("UCL Rata-rata", f"{ucl.mean():.4f}")
    c3.metric("LCL Rata-rata", f"{lcl.mean():.4f}")

    out_of_control = np.where((p > ucl) | (p < lcl))[0]
    if len(out_of_control) > 0:
        st.warning(f"⚠️ {len(out_of_control)} titik di luar batas kendali: Minggu {', '.join(df_f['Minggu'].iloc[out_of_control].tolist())}")
    else:
        st.success("✅ Semua titik berada dalam batas kendali.")

    fig, ax = plt.subplots(figsize=(13, 5))
    x = range(len(df_f))
    ax.plot(x, p, marker="o", color="#2980b9", linewidth=2, label="Proporsi Cacat (p)", zorder=3)
    ax.plot(x, [p_bar]*len(x), color="green", linestyle="--", linewidth=1.5, label=f"CL = {p_bar:.4f}")
    ax.plot(x, ucl, color="red", linestyle="--", linewidth=1.5, label="UCL")
    ax.plot(x, lcl, color="orange", linestyle="--", linewidth=1.5, label="LCL")
    ax.fill_between(x, lcl, ucl, alpha=0.08, color="green")
    for i in out_of_control:
        ax.scatter(i, p[i], color="red", s=120, zorder=5)
        ax.annotate(f"OOC\n{df_f['Minggu'].iloc[i]}", (i, p[i]), textcoords="offset points", xytext=(5, 8), fontsize=7, color="red", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(df_f["Minggu"], rotation=45, fontsize=8)
    ax.set_xlabel("Minggu Pengamatan")
    ax.set_ylabel("Proporsi Cacat (p)")
    ax.set_title("P-Chart — Peta Kendali Proporsi Cacat Packing PT. Gramar Jaya")
    ax.legend(fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.1f}%"))
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="section-header">📋 Tabel Perhitungan P-Chart</div>', unsafe_allow_html=True)
    df_pchart = pd.DataFrame({
        "Minggu": df_f["Minggu"].values,
        "n (Produksi)": n,
        "np (Cacat)": np_val,
        "p": np.round(p, 4),
        "UCL": np.round(ucl, 4),
        "CL": np.round([p_bar]*len(x), 4),
        "LCL": np.round(lcl, 4),
        "Status": ["❌ OOC" if i in out_of_control else "✅ Terkendali" for i in range(len(x))]
    })
    st.dataframe(df_pchart, use_container_width=True, height=350)

    with st.expander("📐 Rumus P-Chart"):
        st.markdown(r"""
**Proporsi cacat:** $p_i = \dfrac{np_i}{n_i}$

**Center Line:** $\bar{p} = \dfrac{\sum np_i}{\sum n_i}$

**UCL:** $\bar{p} + 3\sqrt{\dfrac{\bar{p}(1-\bar{p})}{n_i}}$

**LCL:** $\bar{p} - 3\sqrt{\dfrac{\bar{p}(1-\bar{p})}{n_i}} \geq 0$
        """)

# ── PARETO ────────────────────────────────────────────────────────────────────
elif halaman == "📉 Pareto Chart":
    st.markdown('<div class="main-title">📉 Pareto Chart — Analisis Jenis Cacat</div>', unsafe_allow_html=True)

    totals = df_f[JENIS_CACAT].sum().sort_values(ascending=False)
    kumulatif = totals.cumsum() / totals.sum() * 100
    vital_few = totals[kumulatif <= 80]

    st.info(f"🎯 Prinsip Pareto (80/20): {len(vital_few)} jenis cacat utama menyumbang ≥80% dari total kerusakan.")

    fig, ax1 = plt.subplots(figsize=(11, 5))
    colors = ["#e74c3c" if c in vital_few.index else "#95a5a6" for c in totals.index]
    bars = ax1.bar(range(len(totals)), totals.values, color=colors, edgecolor="white")
    ax1.bar_label(bars, padding=3, fontsize=9, fontweight="bold")
    ax1.set_ylabel("Jumlah Cacat (unit)")
    ax1.set_xticks(range(len(totals)))
    ax1.set_xticklabels([c[:22]+"…" if len(c)>22 else c for c in totals.index], rotation=20, ha="right", fontsize=9)
    ax2 = ax1.twinx()
    ax2.plot(range(len(totals)), kumulatif.values, color="#2c3e50", marker="o", linewidth=2)
    ax2.axhline(80, color="navy", linestyle="--", linewidth=1.2, alpha=0.7)
    ax2.text(len(totals)-0.5, 81.5, "80%", color="navy", fontsize=9)
    ax2.set_ylabel("% Kumulatif")
    ax2.set_ylim(0, 115)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0f}%"))
    red_patch = mpatches.Patch(color='#e74c3c', label='Vital Few (≤80%)')
    grey_patch = mpatches.Patch(color='#95a5a6', label='Useful Many (>80%)')
    ax1.legend(handles=[red_patch, grey_patch], loc="center right")
    ax1.set_title("Pareto Chart — Jenis Cacat Packing PT. Gramar Jaya", fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="section-header">📋 Tabel Analisis Pareto</div>', unsafe_allow_html=True)
    df_pareto = pd.DataFrame({
        "Jenis Cacat": totals.index,
        "Jumlah": totals.values,
        "% Kontribusi": (totals.values / totals.sum() * 100).round(2),
        "% Kumulatif": kumulatif.values.round(2),
        "Kategori": ["🔴 Vital Few" if c in vital_few.index else "⚪ Useful Many" for c in totals.index]
    })
    st.dataframe(df_pareto, use_container_width=True)

# ── FMEA ──────────────────────────────────────────────────────────────────────
elif halaman == "⚠️ FMEA":
    st.markdown('<div class="main-title">⚠️ FMEA — Failure Mode and Effect Analysis</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("RPN Tertinggi", df_fmea["RPN"].max())
    c2.metric("RPN Rata-rata", f"{df_fmea['RPN'].mean():.0f}")
    c3.metric("Risiko Tinggi (RPN ≥ 200)", len(df_fmea[df_fmea["RPN"] >= 200]))

    st.markdown('<div class="section-header">📋 Tabel FMEA</div>', unsafe_allow_html=True)

    def color_rpn(val):
        if val >= 300: return "background-color: #e74c3c; color: white; font-weight: bold"
        elif val >= 200: return "background-color: #e67e22; color: white; font-weight: bold"
        elif val >= 100: return "background-color: #f1c40f"
        return "background-color: #2ecc71"

    st.dataframe(
        df_fmea.style.applymap(color_rpn, subset=["RPN"]),
        use_container_width=True, height=280
    )

    st.markdown('<div class="section-header">📊 Visualisasi RPN</div>', unsafe_allow_html=True)
    df_sorted = df_fmea.sort_values("RPN", ascending=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    bar_colors = ["#e74c3c" if r >= 300 else "#e67e22" if r >= 200 else "#f1c40f" if r >= 100 else "#2ecc71" for r in df_sorted["RPN"]]
    bars = ax.barh(df_sorted["Jenis Kegagalan"].str[:28], df_sorted["RPN"], color=bar_colors)
    ax.bar_label(bars, padding=3, fontsize=9, fontweight="bold")
    ax.axvline(200, color="red", linestyle="--", linewidth=1.2, alpha=0.7)
    ax.text(202, 0.2, "Batas Risiko Tinggi (200)", color="red", fontsize=8)
    ax.set_xlabel("RPN")
    ax.set_title("Nilai RPN per Jenis Kegagalan")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="section-header">📝 Action Plan</div>', unsafe_allow_html=True)
    df_action = pd.DataFrame({
        "Jenis Kegagalan": df_fmea["Jenis Kegagalan"],
        "RPN": df_fmea["RPN"],
        "Prioritas": ["🔴 TINGGI" if r >= 300 else "🟠 SEDANG" if r >= 200 else "🟡 RENDAH" for r in df_fmea["RPN"]],
        "Tindakan Perbaikan": [
            "Training operator + kalibrasi mesin labeler bulanan",
            "SOP torque setting + uji kebocoran 100% sampel",
            "Kalibrasi flowmeter + sampling QC per batch",
            "Perbaikan jalur conveyor + pelatihan handling",
            "SOP pencampuran pigmen + inspeksi warna sampling"
        ],
        "Target": ["1 Bulan","2 Minggu","1 Bulan","3 Bulan","2 Minggu"],
        "PIC": ["QC + Produksi","QC + Maintenance","QC + Produksi","Produksi","QC + Lab"]
    })
    st.dataframe(df_action, use_container_width=True)
