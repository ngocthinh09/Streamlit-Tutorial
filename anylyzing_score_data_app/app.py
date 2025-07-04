import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import io
from PIL import Image

# Hàm tính điểm trung bình
def calculate_average(scores):
    return sum(scores) / len(scores)

# Hàm phân loại điểm số
def percentage_distribution(scores):
    bins = {"90-100": 0,
            "80-89":  0,
            "70-79":  0,
            "60-69":  0,
            "<60":    0}
    for score in scores:
        if score >= 90:
            bins["90-100"] += 1
        elif score >= 80:
            bins["80-89"] += 1
        elif score >= 70:
            bins["70-79"] += 1
        elif score >= 60:
            bins["60-69"] += 1
        else:
            bins["<60"] += 1
    return bins

def main():
    # Header
    st.title("Phân tích dữ liệu điểm số học sinh")

    # Upload file
    uploaded_file = st.file_uploader("Chọn file Excel (có cột\"Điểm số\")", type=["xlsx"])
    
    # Khi có file:
    if uploaded_file:
        # Đọc file
        df = pd.read_excel(uploaded_file)

        # Xử lý danh sách điểm số
        scores = df["Điểm số"].dropna().astype(float).tolist()

        if scores:
            # Hiển thị các chỉ số
            st.write(f"Tổng số học sinh: {len(scores)}")
            st.write(f"Điểm trung bình: {round(calculate_average(scores), 2)}")

            # Phân loại điểm
            dist = percentage_distribution(scores)
            labels = list(dist.keys())
            values = list(dist.values())

            fig, ax = plt.subplots(figsize=(1, 1))
            ax.pie(values, 
                labels=labels, 
                autopct="%1.1f%%", 
                startangle=90,
                textprops={"fontsize": 3.5}
            )
            ax.axis('equal')
            plt.tight_layout(pad=0.1)
            
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300)
            buf.seek(0)
            img = Image.open(buf)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(img, width=300)        # Hiển thị biểu đồ ở cột giữa
                st.markdown(
                    "<p style='text-align: center;'>Biểu đồ phân bố điểm số.</p>",
                    unsafe_allow_html=True
                )
    
        
if __name__ == "__main__":
    main()