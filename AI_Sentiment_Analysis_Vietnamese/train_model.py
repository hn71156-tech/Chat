from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data" / "reviews.csv"
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"

def main():
    MODEL_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    required = {"text", "label"}
    if not required.issubset(df.columns):
        raise ValueError("CSV phải có hai cột text và label.")
    df = df.dropna(subset=["text", "label"]).copy()
    df["text"] = df["text"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip()
    df = df[df["text"] != ""].drop_duplicates(subset=["text"])

    if df["label"].nunique() < 2:
        raise ValueError("Cần ít nhất hai nhãn khác nhau để huấn luyện.")

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.25, random_state=42,
        stratify=df["label"]
    )

    model = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=12000,
                                  strip_accents=None, lowercase=True)),
        ("classifier", LogisticRegression(max_iter=1500, class_weight="balanced"))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, pred)
    report = classification_report(y_test, pred, zero_division=0)
    labels = sorted(df["label"].unique())
    matrix = confusion_matrix(y_test, pred, labels=labels)

    joblib.dump(model, MODEL_DIR / "sentiment_pipeline.joblib")
    metrics = {
        "dataset_rows_after_cleaning": int(len(df)),
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "labels": labels,
        "accuracy": float(accuracy),
        "note": "Dữ liệu demo nhỏ; không dùng các chỉ số này làm cam kết chất lượng thực tế."
    }
    (REPORT_DIR / "metrics.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (REPORT_DIR / "classification_report.txt").write_text(report, encoding="utf-8")
    pd.DataFrame(matrix, index=labels, columns=labels).to_csv(
        REPORT_DIR / "confusion_matrix.csv", encoding="utf-8-sig"
    )

    print("Huấn luyện hoàn tất.")
    print(f"Số mẫu: {len(df)} | Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"Accuracy trên tập test demo: {accuracy:.3f}")
    print(report)
    print(f"Đã lưu model tại: {MODEL_DIR / 'sentiment_pipeline.joblib'}")

if __name__ == "__main__":
    main()
