# Kịch bản demo 5 phút

## Chuẩn bị
- Bật MySQL trong XAMPP.
- Import `sql/schema.sql`, kiểm tra `.env`.
- Tải `creditcard.csv` vào `data/`.
- Chạy `python train_model.py`.
- Chạy `python -m streamlit run app.py`.

## Kịch bản
1. **Giới thiệu (45 giây):** mục tiêu là gắn cờ giao dịch bất thường để người dùng kiểm tra, không kết luận chắc chắn gian lận.
2. **Dashboard (45 giây):** tổng giao dịch, số bị gắn cờ, phân bố mức rủi ro.
3. **Phân tích (75 giây):** tải CSV, bấm chạy AI và lưu MySQL, giải thích nhãn và điểm xếp hạng.
4. **Lịch sử (45 giây):** mở tab Lịch sử và cho xem các bản ghi đã lưu.
5. **Đánh giá (60 giây):** chạy `python evaluate_model.py`, giải thích confusion matrix, Precision/Recall/F1.
6. **Kết luận (30 giây):** nêu hạn chế và hướng phát triển.

## Khi có lỗi
- MySQL: kiểm tra XAMPP, `.env`, port và schema.
- Không có model: chạy `python train_model.py`.
- Không có CSV: tải dataset theo README; không giả vờ có dữ liệu nếu chưa tải.
- Chỉ trình bày metrics thực sự xuất ra từ script.
