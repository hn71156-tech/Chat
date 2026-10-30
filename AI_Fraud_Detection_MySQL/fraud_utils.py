import json
import numpy as np
import pandas as pd

LABELS=["Class","class","label","Label","is_fraud","fraud"]
AMOUNTS=["Amount","amount","transaction_amount","TransactionAmount"]
TIMES=["Time","time","transaction_time","timestamp"]

def find_col(df, candidates):
    return next((c for c in candidates if c in df.columns),None)

def prepare_features(df):
    work=df.copy()
    label=find_col(work,LABELS); amount_col=find_col(work,AMOUNTS); time_col=find_col(work,TIMES)
    actual=pd.to_numeric(work[label],errors="coerce") if label else pd.Series(np.nan,index=work.index)
    amount=pd.to_numeric(work[amount_col],errors="coerce") if amount_col else pd.Series(0.0,index=work.index)
    tm=pd.to_numeric(work[time_col],errors="coerce") if time_col else pd.Series(np.nan,index=work.index)
    features=work.drop(columns=[label] if label else [],errors="ignore").select_dtypes(include=[np.number])
    features=features.replace([np.inf,-np.inf],np.nan)
    features=features.fillna(features.median(numeric_only=True)).fillna(0)
    if features.empty: raise ValueError("Không tìm thấy cột đặc trưng dạng số trong CSV.")
    actual=actual.where(actual.isin([0,1]),np.nan)
    sid=work["transaction_id"].astype(str) if "transaction_id" in work.columns else pd.Series(work.index.astype(str),index=work.index)
    meta=pd.DataFrame({"source_transaction_id":sid,"transaction_time":tm,"amount":amount.fillna(0),"actual_label":actual},index=work.index)
    return features,meta,label

def risk_level(score):
    if score>=.80:return "Cao"
    if score>=.55:return "Trung bình"
    return "Thấp"

def predict_dataframe(model, raw):
    features,meta,label=prepare_features(raw)
    expected=list(getattr(model,"feature_names_in_",features.columns))
    features=features.reindex(columns=expected,fill_value=0)
    if hasattr(model,"predict_proba"):
        p=model.predict_proba(features); classes=list(model.classes_)
        idx=classes.index(1) if 1 in classes else int(np.argmax(classes))
        scores=np.clip(p[:,idx],0,1); pred=(scores>=.5).astype(int)
    else:
        pred=(model.predict(features)==-1).astype(int)
        decision=model.decision_function(features)
        lo,hi=np.percentile(decision,[1,99]) if len(decision)>1 else (decision[0]-1,decision[0]+1)
        scores=np.clip(1-(decision-lo)/(hi-lo+1e-9),0,1)
    out=meta.copy(); out["predicted_label"]=pred; out["anomaly_score"]=scores
    out["risk_level"]=[risk_level(float(s)) for s in scores]
    out["features_json"]=[json.dumps({k:(None if pd.isna(v) else float(v)) for k,v in row.items()},ensure_ascii=False) for row in features.to_dict("records")]
    return out.reset_index(drop=True),label
