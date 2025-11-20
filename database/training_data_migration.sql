-- Migration: إضافة جدول training_data
-- قم بتشغيل هذا الملف في phpMyAdmin أو MySQL

USE blood_pressure_db;

CREATE TABLE IF NOT EXISTS training_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    systolic FLOAT NOT NULL,
    diastolic FLOAT NOT NULL,
    is_verified INT DEFAULT 0 COMMENT '0 = pending, 1 = verified',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_verified (is_verified),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

