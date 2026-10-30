from pathlib import Path
import joblib,pandas as pd,plotly.express as px,streamlit as st
from db import test_connection,save_transactions,fetch_history,fetch_stats,save_model_run
from fraud_utils import predict_dataframe
ROOT=Path(__file__).resolve().parent; MODEL=ROOT/"models"/"isolation_forest.joblib"; DATA=ROOT/"data"/"creditcard.csv"
st.set_page_config(page_title="AI Fraud Detection",page_icon="🛡️",layout="wide")
st.title("🛡️ AI Fraud Detection")
st.caption("Phát hiện giao dịch bất thường bằng Machine Learning • Prototype học tập, không dùng để chặn giao dịch thật.")
with st.sidebar:
    st.header("Kết nối")
    st.caption("Cấu hình MySQL trong file .env")
    if st.button("Kiểm tra kết nối MySQL",use_container_width=True):
        try:
            d=test_connection(); st.success(f"Kết nối OK: {d['db_name']} / MySQL {d['version']}")
        except Exception as e: st.error(f"Kết nối thất bại: {e}")
    st.info("Isolation Forest là mô hình không giám sát. Điểm rủi ro là thang xếp hạng, không phải xác suất gian lận.")
if not MODEL.exists():
    st.warning("Chưa có model. Đặt creditcard.csv trong data/ rồi chạy `python train_model.py`.")
    st.stop()
try: model=joblib.load(MODEL)
except Exception as e: st.error(f"Không đọc được model: {e}"); st.stop()
tab1,tab2,tab3,tab4=st.tabs(["📊 Dashboard","🔎 Phân tích","🗂️ Lịch sử","ℹ️ Giới thiệu"])
with tab1:
    st.subheader("Thống kê từ MySQL")
    try:
        summary,risks,daily=fetch_stats(); a,b,c,d=st.columns(4)
        a.metric("Tổng giao dịch",f"{summary['total']:,}"); b.metric("Bị gắn cờ",f"{summary['flagged']:,}")
        c.metric("Bình thường",f"{summary['normal']:,}"); d.metric("Số tiền trung bình",f"{float(summary['avg_amount']):,.2f}")
        if risks: st.plotly_chart(px.pie(pd.DataFrame(risks),names="risk_level",values="count",title="Phân bố mức rủi ro"),use_container_width=True)
        if daily:
            dd=pd.DataFrame(daily); dd["day"]=pd.to_datetime(dd["day"])
            st.plotly_chart(px.line(dd,x="day",y=["total","flagged"],markers=True,title="Giao dịch lưu theo ngày"),use_container_width=True)
        else: st.info("Chưa có lịch sử. Hãy phân tích một file CSV.")
    except Exception as e: st.warning("Chưa đọc được MySQL. Bật MySQL trong XAMPP và import sql/schema.sql."); st.caption(str(e))
with tab2:
    st.subheader("Phân tích CSV")
    st.write("Dữ liệu công khai Kaggle `creditcard.csv` có cột `Class`. Nhãn này không được dùng để huấn luyện Isolation Forest.")
    upload=st.file_uploader("Tải file CSV",type=["csv"])
    use_local=st.checkbox("Dùng data/creditcard.csv nếu có",value=DATA.exists())
    raw=None; source=None
    if upload is not None:
        source=upload.name
        try: raw=pd.read_csv(upload)
        except Exception as e: st.error(f"Không đọc được CSV: {e}")
    elif use_local and DATA.exists():
        source=DATA.name
        try: raw=pd.read_csv(DATA,nrows=50000); st.caption("Nạp tối đa 50.000 dòng cho giao diện phản hồi nhanh.")
        except Exception as e: st.error(str(e))
    if raw is not None:
        st.write(f"**{source}** — {len(raw):,} dòng, {len(raw.columns)} cột")
        st.dataframe(raw.head(8),use_container_width=True)
        if st.button("Chạy AI và lưu vào MySQL",type="primary",use_container_width=True):
            try:
                with st.spinner("Đang phân tích..."):
                    result,label=predict_dataframe(model,raw)
                    result["source_transaction_id"]=result["source_transaction_id"].astype(str)
                    st.session_state["results"]=result
                    inserted=save_transactions(result,"IsolationForest")
                    try: save_model_run("IsolationForest",source,len(result),int(result.predicted_label.sum()),"Unsupervised anomaly detection")
                    except Exception: pass
                st.success(f"Hoàn tất; đã lưu {inserted:,} dòng vào MySQL.")
            except Exception as e: st.error(f"Phân tích/lưu thất bại: {e}")
    result=st.session_state.get("results")
    if result is not None:
        a,b,c=st.columns(3); a.metric("Đã phân tích",f"{len(result):,}"); b.metric("Bị gắn cờ",f"{int(result.predicted_label.sum()):,}"); c.metric("Tỷ lệ gắn cờ",f"{result.predicted_label.mean()*100:.2f}%")
        view=result.rename(columns={"source_transaction_id":"Mã giao dịch","transaction_time":"Thời gian dữ liệu","amount":"Số tiền","predicted_label":"Nhãn AI (1=bất thường)","anomaly_score":"Điểm xếp hạng rủi ro","risk_level":"Mức rủi ro"})
        st.dataframe(view[["Mã giao dịch","Thời gian dữ liệu","Số tiền","Nhãn AI (1=bất thường)","Điểm xếp hạng rủi ro","Mức rủi ro"]],use_container_width=True)
        st.download_button("Tải kết quả CSV",view.to_csv(index=False).encode("utf-8-sig"),"fraud_detection_results.csv","text/csv")
        st.markdown("**Giao dịch bị gắn cờ**")
        st.dataframe(result[result.predicted_label==1][["source_transaction_id","transaction_time","amount","anomaly_score","risk_level"]].head(100),use_container_width=True)
with tab3:
    st.subheader("Lịch sử đã lưu trong MySQL"); limit=st.selectbox("Số bản ghi gần nhất",[100,500,1000,5000],index=1)
    try:
        history=fetch_history(limit)
        if history:
            h=pd.DataFrame(history); st.dataframe(h,use_container_width=True)
            st.download_button("Xuất lịch sử CSV",h.to_csv(index=False).encode("utf-8-sig"),"fraud_history.csv","text/csv")
        else: st.info("Chưa có giao dịch đã lưu.")
    except Exception as e: st.warning(f"Không tải được lịch sử: {e}")
with tab4:
    st.subheader("Thông tin dự án")
    st.markdown("""
- **Mô hình:** Isolation Forest, học không giám sát.
- **Dataset:** Kaggle Credit Card Fraud Detection, tải `creditcard.csv` theo hướng dẫn.
- **Database:** MySQL/XAMPP, các bảng `transactions` và `model_runs`.
- **Metrics:** Precision, Recall, F1-score và confusion matrix qua `python evaluate_model.py`.
- **Giới hạn:** anomaly không đồng nghĩa fraud; điểm hiển thị không phải xác suất hiệu chuẩn. Cần người kiểm tra cảnh báo.
- **An toàn:** chỉ dùng dữ liệu công khai/đã ẩn danh; không nhập dữ liệu thẻ thật.
""")
