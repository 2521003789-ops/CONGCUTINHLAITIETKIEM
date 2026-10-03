import streamlit as st
st.image("logo.jpg")
import pandas as pd

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# =========================
# CSS GIAO DIỆN
# =========================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f5f7fa;
        text-align: center;
        border: 1px solid #e0e0e0;
    }

    .result-title {
        font-size: 16px;
        color: #555;
    }

    .result-value {
        font-size: 25px;
        font-weight: bold;
        margin-top: 8px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# TIÊU ĐỀ
# =========================
st.markdown(
    '<div class="main-title">💰 TÍNH LÃI GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Công cụ tính lãi tiền gửi theo lãi đơn hoặc lãi kép</div>',
    unsafe_allow_html=True
)

# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin khoản tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "💵 Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "📅 Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "📈 Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=5.0,
        step=0.1
    )

with col2:
    hinh_thuc_nhan_lai = st.selectbox(
        "💳 Hình thức nhận lãi",
        [
            "Cuối kỳ",
            "Hàng tháng",
            "Hàng quý"
        ]
    )

    loai_lai = st.selectbox(
        "🔄 Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def dinh_dang_tien(so_tien):
    return f"{so_tien:,.0f} VNĐ"


# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 TÍNH LÃI", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r_nam = lai_suat / 100

    # Thời gian tính theo năm
    so_nam = ky_han / 12

    # --------------------------------
    # LÃI ĐƠN
    # --------------------------------
    if loai_lai == "Lãi đơn":

        tong_lai = so_tien * r_nam * so_nam
        tong_tien = so_tien + tong_lai

        # Xác định số kỳ nhận lãi
        if hinh_thuc_nhan_lai == "Hàng tháng":
            so_ky = ky_han
            lai_moi_ky = tong_lai / so_ky

            ky_labels = [
                f"Tháng {i}"
                for i in range(1, so_ky + 1)
            ]

        elif hinh_thuc_nhan_lai == "Hàng quý":
            so_ky = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3
            if ky_han % 3 != 0:
                so_ky += 1

            lai_moi_ky = tong_lai / so_ky

            ky_labels = [
                f"Quý {i}"
                for i in range(1, so_ky + 1)
            ]

        else:
            so_ky = 1
            lai_moi_ky = tong_lai
            ky_labels = ["Cuối kỳ"]

        # --------------------------------
        # BẢNG CHI TIẾT LÃI ĐƠN
        # --------------------------------
        danh_sach = []

        for i, ky in enumerate(ky_labels, start=1):
            if hinh_thuc_nhan_lai == "Hàng tháng":
                thoi_gian = f"Tháng {i}"

            elif hinh_thuc_nhan_lai == "Hàng quý":
                thoi_gian = f"Quý {i}"

            else:
                thoi_gian = "Cuối kỳ"

            danh_sach.append({
                "Kỳ": thoi_gian,
                "Tiền lãi nhận": lai_moi_ky,
                "Lũy kế tiền lãi": lai_moi_ky * i
            })

    # --------------------------------
    # LÃI KÉP
    # --------------------------------
    else:

        # Xác định số kỳ ghép lãi
        if hinh_thuc_nhan_lai == "Hàng tháng":
            so_ky = ky_han
            lai_suat_ky = r_nam / 12

            ky_labels = [
                f"Tháng {i}"
                for i in range(1, so_ky + 1)
            ]

        elif hinh_thuc_nhan_lai == "Hàng quý":
            so_ky = ky_han // 3

            # Nếu kỳ hạn không chia hết cho 3
            if ky_han % 3 != 0:
                so_ky += 1

            lai_suat_ky = r_nam / 4

            ky_labels = [
                f"Quý {i}"
                for i in range(1, so_ky + 1)
            ]

        else:
            # Cuối kỳ: tính theo năm
            so_ky = so_nam
            lai_suat_ky = r_nam

            # Trường hợp kỳ hạn không phải số năm nguyên
            # dùng công thức tăng trưởng theo thời gian
            tong_tien = so_tien * ((1 + r_nam) ** so_nam)
            tong_lai = tong_tien - so_tien

            danh_sach = [{
                "Kỳ": "Cuối kỳ",
                "Tiền lãi nhận": tong_lai,
                "Lũy kế tiền lãi": tong_lai
            }]

        # --------------------------------
        # LÃI KÉP THEO THÁNG / QUÝ
        # --------------------------------
        if hinh_thuc_nhan_lai != "Cuối kỳ":

            so_du = so_tien
            tong_lai = 0
            danh_sach = []

            for i in range(1, so_ky + 1):

                tien_truoc_ky = so_du

                tien_lai_ky = tien_truoc_ky * lai_suat_ky

                so_du += tien_lai_ky

                tong_lai += tien_lai_ky

                if hinh_thuc_nhan_lai == "Hàng tháng":
                    ky_text = f"Tháng {i}"
                else:
                    ky_text = f"Quý {i}"

                danh_sach.append({
                    "Kỳ": ky_text,
                    "Tiền lãi nhận": tien_lai_ky,
                    "Lũy kế tiền lãi": tong_lai
                })

            tong_tien = so_du


    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()

    st.subheader("📊 Kết quả tính toán")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💰 Tiền lãi định kỳ</div>
                <div class="result-value">
                    {dinh_dang_tien(danh_sach[0]["Tiền lãi nhận"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">📈 Tổng tiền lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_lai)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-title">💵 Tổng gốc + lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_tien)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================
    st.divider()

    st.subheader("📝 Thông tin khoản gửi")

    thong_tin = pd.DataFrame({
        "Thông tin": [
            "Số tiền gửi",
            "Kỳ hạn",
            "Lãi suất",
            "Hình thức nhận lãi",
            "Phương pháp tính"
        ],
        "Giá trị": [
            dinh_dang_tien(so_tien),
            f"{ky_han} tháng",
            f"{lai_suat:.2f}%/năm",
            hinh_thuc_nhan_lai,
            loai_lai
        ]
    })

    st.table(thong_tin)

    # =========================
    # CHI TIẾT TỪNG KỲ
    # =========================
    st.divider()

    st.subheader("📅 Chi tiết tiền lãi theo từng kỳ")

    df = pd.DataFrame(danh_sach)

    df["Tiền lãi nhận"] = df["Tiền lãi nhận"].apply(
        dinh_dang_tien
    )

    df["Lũy kế tiền lãi"] = df["Lũy kế tiền lãi"].apply(
        dinh_dang_tien
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # =========================
    # KẾT LUẬN
    # =========================
    st.success(
        f"🎉 Sau {ky_han} tháng, khoản tiền gửi "
        f"{dinh_dang_tien(so_tien)} tạo ra "
        f"{dinh_dang_tien(tong_lai)} tiền lãi. "
        f"Tổng số tiền nhận được là "
        f"{dinh_dang_tien(tong_tien)}."
    )
