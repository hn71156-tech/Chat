# Kịch bản demo phỏng vấn (3–5 phút)

## Trước buổi phỏng vấn
1. Cài dependencies.
2. Chạy `python train_model.py` và kiểm tra tạo được `models/` và `reports/`.
3. Chạy `streamlit run app.py`.
4. Mở sẵn trình duyệt tại `http://localhost:8501`.
5. Chuẩn bị giới thiệu hạn chế dữ liệu demo.

## Kịch bản
**0:00–0:30 – Bài toán:** “Em làm công cụ phân loại phản hồi khách hàng thành tích cực, tiêu cực, trung lập.”

**0:30–1:15 – Công nghệ:** Mở cấu trúc project; giải thích pandas, TF-IDF, Logistic Regression, scikit-learn và Streamlit.

**1:15–2:15 – Demo:** Thử:
- “Dịch vụ rất tốt, giao hàng nhanh, tôi rất hài lòng.”
- “Sản phẩm lỗi, giao hàng chậm và hỗ trợ khách hàng rất tệ.”
- “Tôi vừa nhận được đơn hàng sáng nay.”

**2:15–3:15 – Đánh giá:** Mở `reports/classification_report.txt` và `reports/confusion_matrix.csv`. Nói rõ dữ liệu mẫu nhỏ nên chỉ minh họa pipeline; không đại diện hiệu năng thực tế.

**3:15–4:00 – Hạn chế và phát triển:** Nêu dữ liệu ít, câu mỉa mai/teencode khó, hướng phát triển với dataset công khai và PhoBERT.

**4:00–5:00 – Câu hỏi:** Trả lời vì sao TF-IDF, Logistic Regression, train/test, F1-score.

## Nếu demo lỗi
- Nếu chưa có model: chạy `python train_model.py`.
- Nếu thiếu thư viện: `pip install -r requirements.txt`.
- Nếu lệnh `streamlit` không nhận: `python -m streamlit run app.py`.
- Nếu mô hình đoán chưa tốt: nói đây là baseline minh họa và giải thích cách đánh giá/cải thiện; không che giấu giới hạn.
