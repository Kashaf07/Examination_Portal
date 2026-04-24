-- ============================================================
-- Migration: Add Keystroke Tracking Feature
-- Run this ONCE to add keystroke logging to existing database
-- ============================================================

USE entrance_database;

-- Create keystroke_logs table (with Log_Type column)
DROP TABLE IF EXISTS `keystroke_logs`;
CREATE TABLE `keystroke_logs` (
  `Log_Id`          BIGINT        NOT NULL AUTO_INCREMENT,
  `Attempt_Id`      INT           NOT NULL,
  `Applicant_Id`    INT           NOT NULL,
  `Question_Id`     INT           NOT NULL,
  `Key_Pressed`     VARCHAR(100)  NOT NULL,
  `Key_Code`        VARCHAR(50)   DEFAULT NULL,
  `Is_Ctrl`         TINYINT(1)    DEFAULT 0,
  `Is_Alt`          TINYINT(1)    DEFAULT 0,
  `Is_Shift`        TINYINT(1)    DEFAULT 0,
  `Is_Meta`         TINYINT(1)    DEFAULT 0,
  `Key_Combination` VARCHAR(200)  DEFAULT NULL,
  `Log_Type`        VARCHAR(10)   DEFAULT 'key',
  `Timestamp`       DATETIME      NOT NULL,
  `Created_At`      TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Log_Id`),
  KEY `idx_attempt`          (`Attempt_Id`),
  KEY `idx_applicant`        (`Applicant_Id`),
  KEY `idx_question`         (`Question_Id`),
  KEY `idx_timestamp`        (`Timestamp`),
  KEY `idx_attempt_question` (`Attempt_Id`, `Question_Id`),
  CONSTRAINT `fk_keystroke_attempt`   FOREIGN KEY (`Attempt_Id`)   REFERENCES `applicant_attempt`      (`Attempt_Id`)   ON DELETE CASCADE,
  CONSTRAINT `fk_keystroke_applicant` FOREIGN KEY (`Applicant_Id`) REFERENCES `applicants`             (`Applicant_Id`) ON DELETE CASCADE,
  CONSTRAINT `fk_keystroke_question`  FOREIGN KEY (`Question_Id`)  REFERENCES `entrance_question_bank` (`Question_Id`)  ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

SELECT 'Migration completed successfully! Keystroke tracking table created.' AS Status;
