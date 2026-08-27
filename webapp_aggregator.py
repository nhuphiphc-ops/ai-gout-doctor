# -*- coding: utf-8 -*-
"""
HỆ THỐNG TỔNG HỢP & PHÂN TÍCH TÀI LIỆU - DỰ ÁN SỨC KHỎE MR PHI
===================================================================
Chạy:  python -m streamlit run webapp.py --server.port 8502
"""

import sys
import os
import io
import time
import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

# Đảm bảo import được module
CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))
from document_aggregator import DocumentAggregator

# ─────────────────────────────────────────────────
# CẤU HÌNH TRANG
# ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Dự Án Sức Khỏe Mr Phi - Hệ Thống Quản Lý Tài Liệu",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────
# CSS GIAO DIỆN HIỆN ĐẠI
# ─────────────────────────────────────────────────
st.markdown("""
<style>
    /* Header Banner */
    .main-banner {
        background: linear-gradient(135deg, #0F766E 0%, #0D9488 50%, #14B8A6 100%);
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .main-banner h1 { color: #FFFFFF !important; margin: 0; font-size: 1.8rem; font-weight: 700; }
    .main-banner p  { color: #CCFBF1 !important; margin: 0.4rem 0 0 0; font-size: 1rem; }

    /* KPI Cards */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0D9488;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        margin-bottom: 0.8rem;
    }
    .kpi-card.info { border-top-color: #0284C7; }
    .kpi-card.warning { border-top-color: #D97706; }
    .kpi-card.success { border-top-color: #059669; }

    .kpi-val { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0.2rem 0; }
    .kpi-lbl { font-size: 0.85rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-sub { font-size: 0.82rem; color: #94A3B8; }

    /* Document Reader View */
    .doc-viewer {
        background: #FAFAFA;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1.2rem;
        font-family: 'Times New Roman', serif;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #1F2937;
        white-space: pre-wrap;
        max-height: 520px;
        overflow-y: auto;
    }

    /* Insights Box */
    .insight-pill {
        display: inline-block;
        background: #F0FDFA;
        border: 1px solid #99F6E4;
        color: #0F766E;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin: 2px 4px 2px 0;
        font-weight: 500;
    }

    /* Tab Headers */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.02rem;
        font-weight: 600;
        padding: 10px 18px;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# BANNER TIÊU ĐỀ
# ─────────────────────────────────────────────────
st.markdown("""
<div class="main-banner">
    <h1>🩺 DỰ ÁN SỨC KHỎE MR PHI – HỆ THỐNG TỔNG HỢP & PHÂN TÍCH HỒ SƠ TÀI LIỆU</h1>
    <p>Tự động bóc tách thông tin, OCR văn bản scan, tra cứu bảng tính Excel và xuất báo cáo đa tầng</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────
# QUẢN LÝ DỮ LIỆU & SESSION STATE
# ─────────────────────────────────────────────────
if "aggregator" not in st.session_state:
    st.session_state.aggregator = DocumentAggregator(project_name="DU AN SUC KHOE MR PHI", verbose=False)
    # Tự động nạp các tệp hiện có trong thư mục nếu có
    try:
        st.session_state.aggregator.read_folder(str(CURRENT_DIR), recursive=False)
    except Exception:
        pass

aggregator = st.session_state.aggregator
summary = aggregator.get_project_summary()
tq = summary["tong_quan"]

# ─────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📌 Thông tin Dự án")
    st.markdown("""
    - **Tên dự án:** `DU AN SUC KHOE MR PHI`
    - **Thư mục:** `E:\\DU AN SUC KHOE MR PHI`
    - **Tính năng:** OCR Scan, Bóc tách thực thể, Tra cứu bảng biểu, Xuất Excel 6 sheet.
    """)
    st.markdown("---")
    st.markdown("### 📊 Thống kê Hồ sơ Hiện tại")
    st.markdown(f"- **Tổng số tệp:** `{tq['tong_so_file']} tệp`")
    st.markdown(f"- **Văn bản & HĐ:** `{tq['tong_trang_van_ban']} trang`")
    st.markdown(f"- **Sheet Excel:** `{tq['tong_sheet_excel']} sheet`")
    st.markdown(f"- **Bảng trong tài liệu:** `{tq['tong_bang_bieu']} bảng`")

    st.markdown("---")
    st.markdown("### 🔍 Quét Thư Mục Mới")
    custom_dir = st.text_input("Đường dẫn thư mục cần quét:", value=str(CURRENT_DIR))
    scan_subdirs = st.checkbox("Quét cả thư mục con (recursive)", value=True)
    if st.button("🚀 Bắt đầu Quét Thư Mục", use_container_width=True, type="primary"):
        if os.path.isdir(custom_dir):
            with st.spinner(f"Đang quét thư mục {custom_dir}..."):
                new_agg = DocumentAggregator(project_name="DU AN SUC KHOE MR PHI", verbose=False)
                new_agg.read_folder(custom_dir, recursive=scan_subdirs)
                st.session_state.aggregator = new_agg
                st.success("✅ Đã quét xong thư mục!")
                st.rerun()
        else:
            st.error("Thư mục không tồn tại!")

    if st.button("🔄 Làm mới dữ liệu", use_container_width=True):
        st.session_state.aggregator = DocumentAggregator(project_name="DU AN SUC KHOE MR PHI", verbose=False)
        st.session_state.aggregator.read_folder(str(CURRENT_DIR), recursive=False)
        st.rerun()

# ─────────────────────────────────────────────────
# TABS CHÍNH
# ─────────────────────────────────────────────────
tab_dash, tab_reader, tab_data, tab_upload = st.tabs([
    "📊 1. Tổng Quan & Báo Cáo Tổng Hợp",
    "📑 2. Trình Đọc Toàn Văn & Trích Yếu OCR",
    "📈 3. Bảng Tính Dữ Liệu Excel",
    "📤 4. Tải Lên & Xử Lý Tệp Mới",
])

# ══════════════════════════════════════════════════
# TAB 1: TỔNG QUAN & BÁO CÁO
# ══════════════════════════════════════════════════
with tab_dash:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-lbl">Tổng số tệp tài liệu</div>
            <div class="kpi-val">{tq['tong_so_file']}</div>
            <div class="kpi-sub">File PDF, Word, Excel</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card info">
            <div class="kpi-lbl">Trang Văn Bản (OCR / Text)</div>
            <div class="kpi-val" style="color:#0284C7;">{tq['tong_trang_van_ban']}</div>
            <div class="kpi-sub">Đã trích xuất toàn văn</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card warning">
            <div class="kpi-lbl">Bảng tính Excel</div>
            <div class="kpi-val" style="color:#D97706;">{tq['tong_sheet_excel']}</div>
            <div class="kpi-sub">Sheet dữ liệu có cấu trúc</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card success">
            <div class="kpi-lbl">Bảng Biểu Trong Tài Liệu</div>
            <div class="kpi-val" style="color:#059669;">{tq['tong_bang_bieu']}</div>
            <div class="kpi-sub">Trích xuất từ Word/PDF</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown("### 📋 Thông Tin Then Chốt Nhận Diện Tự Động")
        
        c_m, c_d = st.columns(2)
        with c_m:
            st.markdown("**💰 Các khoản tiền phát hiện:**")
            if tq["so_tien_phat_hien"]:
                st.write(", ".join([f"`{m}`" for m in tq["so_tien_phat_hien"][:8]]))
            else:
                st.caption("Chưa phát hiện số tiền trong văn bản.")
        
        with c_d:
            st.markdown("**📅 Mốc thời gian quan trọng:**")
            if tq["ngay_thang_phat_hien"]:
                st.write(", ".join([f"`{d}`" for d in tq["ngay_thang_phat_hien"][:6]]))
            else:
                st.caption("Chưa phát hiện mốc thời gian.")

        st.markdown("**🏢 Các bên / Đối tác liên quan:**")
        if tq["cac_ben_lien_quan"]:
            st.write(", ".join([f"**{p}**" for p in tq["cac_ben_lien_quan"][:8]]))
        else:
            st.caption("Chưa phát hiện tên đơn vị/đối tác.")

    with col_r:
        st.markdown("### 💾 Xuất File Báo Cáo Excel Tổng Hợp")
        st.markdown("Xuất toàn bộ dữ liệu đã bóc tách ra file Excel chuyên nghiệp nhiều Sheet:")
        
        buf = io.BytesIO()
        try:
            temp_out = os.path.join(tempfile.gettempdir(), "temp_export_phi.xlsx")
            aggregator.export_excel(temp_out)
            with open(temp_out, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                label="📥 TẢI XUỐNG BÁO CÁO EXCEL (.xlsx)",
                data=excel_bytes,
                file_name="Bao_cao_tong_hop_Du_An_Suc_Khoe_Mr_Phi.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="primary",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Lỗi xuất Excel: {e}")

    # Danh mục trích yếu chi tiết
    st.markdown("---")
    st.markdown("### 📑 Danh Mục Hồ Sơ & Trích Yếu Chi Tiết")
    if aggregator.key_insights:
        rows_ins = []
        for ins in aggregator.key_insights:
            rows_ins.append({
                "Tên văn bản / Tệp": ins.get("file_name", ""),
                "Số tiền ghi nhận": ", ".join(ins.get("moneys", [])[:4]),
                "Mốc ngày tháng": ", ".join(ins.get("dates", [])[:3]),
                "Số HĐ / Quyết định": ", ".join(ins.get("contract_nums", [])[:2]),
                "Đơn vị / Nhân sự": ", ".join(ins.get("parties", [])[:3]),
            })
        df_ins_table = pd.DataFrame(rows_ins).drop_duplicates(subset=["Tên văn bản / Tệp"])
        st.dataframe(df_ins_table, use_container_width=True, hide_index=True)
    else:
        st.info("Chưa có dữ liệu trích yếu. Vui lòng tải lên tệp hoặc quét thư mục chứa tài liệu.")

# ══════════════════════════════════════════════════
# TAB 2: SMART DOCUMENT READER
# ══════════════════════════════════════════════════
with tab_reader:
    st.markdown("### 📑 Trình Đọc & Tra Cứu Toàn Văn Tài Liệu (Word & PDF Scan OCR)")
    st.caption("Xem chi tiết nội dung từng trang của văn bản Word, PDF và PDF scan hình ảnh đã OCR")

    if not aggregator.text_docs:
        st.info("Chưa có văn bản nào trong hệ thống. Hãy dùng tab **Tải Lên** hoặc sidebar để nạp dữ liệu.")
    else:
        df_docs = pd.DataFrame(aggregator.text_docs)
        available_files = sorted(df_docs["file_name"].unique().tolist())

        col_sel1, col_sel2 = st.columns([3, 1])
        with col_sel1:
            selected_file = st.selectbox("📂 Chọn tài liệu cần xem:", available_files)
        with col_sel2:
            file_subset = df_docs[df_docs["file_name"] == selected_file]
            pages_list  = sorted(file_subset["page"].unique().tolist())
            selected_page = st.selectbox("📄 Trang số:", pages_list if len(pages_list) > 1 else [1])

        row_target = file_subset[file_subset["page"] == selected_page]
        if not row_target.empty:
            content_str = row_target.iloc[0]["content"]
            doc_type    = row_target.iloc[0]["type"]

            # Box thông tin then chốt của tài liệu này
            insight_item = next((ins for ins in aggregator.key_insights if ins.get("file_name") == selected_file), None)
            if insight_item:
                st.markdown("##### 🔍 Thông tin then chốt nhận diện:")
                pills_html = []
                for m in insight_item.get("moneys", [])[:5]:
                    pills_html.append(f'<span class="insight-pill">💰 {m}</span>')
                for d in insight_item.get("dates", [])[:4]:
                    pills_html.append(f'<span class="insight-pill">📅 {d}</span>')
                for p in insight_item.get("parties", []):
                    pills_html.append(f'<span class="insight-pill">🏢 {p}</span>')
                st.markdown(" ".join(pills_html), unsafe_allow_html=True)
                st.markdown("")

            st.markdown(f"**Nội dung toàn văn (Trang {selected_page}/{len(pages_list)} — Định dạng: `{doc_type}`):**")
            st.markdown(f'<div class="doc-viewer">{content_str}</div>', unsafe_allow_html=True)

            st.download_button(
                label=f"📥 Tải toàn văn trang này (.txt)",
                data=content_str.encode("utf-8"),
                file_name=f"{Path(selected_file).stem}_Trang_{selected_page}.txt",
                mime="text/plain",
            )

# ══════════════════════════════════════════════════
# TAB 3: BẢNG TÍNH EXCEL
# ══════════════════════════════════════════════════
with tab_data:
    st.markdown("### 📈 Tra Cứu & Lọc Bảng Dữ Liệu Excel")

    if not aggregator.excel_tables:
        st.info("Chưa có bảng tính Excel nào được nạp vào hệ thống.")
    else:
        df_excel_view = pd.concat(aggregator.excel_tables, ignore_index=True)
        kw_excel = st.text_input("🔍 Tìm kiếm trong toàn bộ bảng tính:", placeholder="Nhập từ khóa cần lọc...")

        df_filtered = df_excel_view.copy()
        if kw_excel:
            mask = df_filtered.apply(lambda col: col.astype(str).str.contains(kw_excel, case=False, na=False)).any(axis=1)
            df_filtered = df_filtered[mask]

        st.markdown(f"**Hiển thị {len(df_filtered):,} dòng dữ liệu:**")
        st.dataframe(df_filtered, use_container_width=True, height=450)

        csv_excel = df_filtered.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="📥 Tải xuống dữ liệu lọc (.csv)",
            data=csv_excel.encode("utf-8-sig"),
            file_name="Du_lieu_bang_tinh_loc.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════════
# TAB 4: TẢI LÊN & QUÉT MỚI
# ══════════════════════════════════════════════════
with tab_upload:
    st.markdown("### 📤 Tải Lên Hồ Sơ Mới (PDF, Word, Excel)")
    st.caption("Kéo thả tài liệu để hệ thống tự động nhận diện chữ, OCR trang scan và trích xuất cấu trúc")

    up_files = st.file_uploader(
        "Chọn các tệp cần phân tích",
        type=["pdf", "docx", "xlsx", "xls"],
        accept_multiple_files=True,
    )

    if up_files:
        st.markdown(f"**{len(up_files)} tệp đã được chọn**")
        if st.button("▶ Bắt đầu Phân Tích & OCR", type="primary", use_container_width=True):
            prg = st.progress(0, text="Đang phân tích...")
            with tempfile.TemporaryDirectory() as tmpdir:
                for idx, uf in enumerate(up_files):
                    tmp_fp = os.path.join(tmpdir, uf.name)
                    with open(tmp_fp, "wb") as tf:
                        tf.write(uf.getbuffer())
                    aggregator.read_file(tmp_fp)
                    prg.progress((idx + 1) / len(up_files), text=f"Đã xử lý: {uf.name}")
            prg.empty()
            st.success("✅ Đã xử lý và nạp dữ liệu thành công!")
            st.rerun()
