from pathlib import Path
import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "sentiment_pipeline.joblib"

st.set_page_config(page_title="AI Sentiment Analysis", page_icon="💬", layout="centered")
st.title("💬 AI phân tích cảm xúc đánh giá")
st.write("Nhập một câu đánh giá tiếng Việt để mô hình dự đoán cảm xúc.")

if not MODEL_PATH.exists():
    st.warning("Chưa có mô hình. Hãy mở Terminal tại thư mục project và chạy: `python train_model.py`")
    st.stop()

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()
text = st.text_area(
    "Nội dung đánh giá",
    placeholder="Ví dụ: Sản phẩm đóng gói cẩn thận, giao hàng nhanh và nhân viên nhiệt tình.",
    height=120
)

if st.button("Phân tích cảm xúc", type="primary", use_container_width=True):
    if not text.strip():
        st.error("Vui lòng nhập nội dung đánh giá.")
    else:
        prediction = model.predict([text.strip()])[0]
        labels_vi = {
            "positive": "Tích cực 😊",
            "negative": "Tiêu cực 😞",
            "neutral": "Trung lập 😐"
        }
        st.subheader("Kết quả")
        st.success(labels_vi.get(prediction, prediction))
        st.caption("Đây là dự đoán từ mô hình học máy demo, không phải kết luận chắc chắn.")
        try:
            probabilities = model.predict_proba([text.strip()])[0]
            classes = model.classes_
            st.write("Điểm tin cậy tương đối theo mô hình")
            for label, probability in sorted(zip(classes, probabilities), key=lambda x: x[1], reverse=True):
                st.write(f"{labels_vi.get(label, label)}: {probability:.1%}")
        except Exception:
            pass

with st.expander("Thử câu mẫu"):
    st.code("Dịch vụ rất tốt, giao hàng nhanh, tôi rất hài lòng.")
    st.code("Sản phẩm lỗi, giao hàng chậm và hỗ trợ khách hàng rất tệ.")
    st.code("Sản phẩm đúng như mô tả, đã nhận được hàng.")
st.divider()
st.caption("Demo học tập | Python · scikit-learn · TF-IDF · Logistic Regression · Streamlit")
