CREATE DATABASE IF NOT EXISTS fraud_detection_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE fraud_detection_db;
CREATE TABLE IF NOT EXISTS transactions (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 source_transaction_id VARCHAR(100) NULL,
 transaction_time DOUBLE NULL,
 amount DECIMAL(14,2) NOT NULL DEFAULT 0,
 actual_label TINYINT NULL COMMENT '0=normal, 1=fraud, NULL=unknown',
 predicted_label TINYINT NOT NULL COMMENT '0=normal, 1=anomaly',
 anomaly_score DOUBLE NOT NULL,
 risk_level VARCHAR(20) NOT NULL,
 model_name VARCHAR(100) NOT NULL,
 features_json JSON NULL,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 INDEX idx_created_at(created_at), INDEX idx_predicted_label(predicted_label),
 INDEX idx_risk_level(risk_level), INDEX idx_source_transaction_id(source_transaction_id)
) ENGINE=InnoDB;
CREATE TABLE IF NOT EXISTS model_runs (
 id BIGINT AUTO_INCREMENT PRIMARY KEY, model_name VARCHAR(100) NOT NULL,
 dataset_name VARCHAR(255) NOT NULL, rows_processed INT NOT NULL DEFAULT 0,
 anomalies_found INT NOT NULL DEFAULT 0, notes TEXT NULL,
 created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
