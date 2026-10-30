import os, json, math
from contextlib import contextmanager
import pymysql
from dotenv import load_dotenv
load_dotenv()

def config():
    return dict(host=os.getenv("DB_HOST","127.0.0.1"), port=int(os.getenv("DB_PORT","3306")),
      user=os.getenv("DB_USER","root"), password=os.getenv("DB_PASSWORD",""),
      database=os.getenv("DB_NAME","fraud_detection_db"), charset="utf8mb4",
      cursorclass=pymysql.cursors.DictCursor, autocommit=False, connect_timeout=5)

@contextmanager
def connection():
    conn=pymysql.connect(**config())
    try: yield conn
    finally: conn.close()

def test_connection():
    with connection() as c:
        with c.cursor() as cur:
            cur.execute("SELECT DATABASE() db_name, VERSION() version")
            result=cur.fetchone()
        c.commit()
        return result

def _num(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (ValueError,TypeError): return None

def save_transactions(df, model_name="IsolationForest"):
    rows=[]
    for _,r in df.iterrows():
        actual=r.get("actual_label")
        try: actual=None if actual is None or str(actual).lower() in ("nan","none","") else int(actual)
        except (ValueError,TypeError): actual=None
        features=r.get("features_json")
        if features is not None and not isinstance(features,str):
            features=json.dumps(features,ensure_ascii=False,default=float)
        sid=r.get("source_transaction_id")
        rows.append((str(sid)[:100] if sid is not None else None,_num(r.get("transaction_time")),
          _num(r.get("amount")) or 0,actual,int(r["predicted_label"]),float(r["anomaly_score"]),
          str(r["risk_level"]),model_name,features))
    if not rows: return 0
    sql="""INSERT INTO transactions
    (source_transaction_id,transaction_time,amount,actual_label,predicted_label,anomaly_score,risk_level,model_name,features_json)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    with connection() as c:
        with c.cursor() as cur: cur.executemany(sql,rows); count=cur.rowcount
        c.commit()
    return count

def fetch_history(limit=500):
    limit=max(1,min(int(limit),5000))
    with connection() as c:
        with c.cursor() as cur:
            cur.execute(f"""SELECT id,source_transaction_id,transaction_time,amount,actual_label,
            predicted_label,anomaly_score,risk_level,model_name,created_at
            FROM transactions ORDER BY id DESC LIMIT {limit}""")
            rows=cur.fetchall()
        c.commit()
    return rows

def fetch_stats():
    with connection() as c:
        with c.cursor() as cur:
            cur.execute("""SELECT COUNT(*) total, COALESCE(SUM(predicted_label=1),0) flagged,
            COALESCE(SUM(predicted_label=0),0) normal, COALESCE(AVG(amount),0) avg_amount FROM transactions""")
            summary=cur.fetchone()
            cur.execute("SELECT risk_level,COUNT(*) count FROM transactions GROUP BY risk_level")
            risks=cur.fetchall()
            cur.execute("""SELECT DATE(created_at) day,COUNT(*) total,SUM(predicted_label=1) flagged
            FROM transactions WHERE created_at >= DATE_SUB(CURDATE(),INTERVAL 29 DAY)
            GROUP BY DATE(created_at) ORDER BY day""")
            daily=cur.fetchall()
        c.commit()
    return summary,risks,daily

def save_model_run(name,dataset,rows,anomalies,notes=""):
    with connection() as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO model_runs(model_name,dataset_name,rows_processed,anomalies_found,notes) VALUES(%s,%s,%s,%s,%s)",
              (name,dataset,int(rows),int(anomalies),notes))
        c.commit()
