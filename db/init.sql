-- ============================================================
-- Fixed init.sql for entrance_database
-- Foreign key checks are disabled during the entire import
-- Tables are created and populated in dependency order
-- ============================================================

SET NAMES utf8mb4;
SET CHARACTER_SET_CLIENT = utf8mb4;
SET CHARACTER_SET_RESULTS = utf8mb4;
SET COLLATION_CONNECTION = utf8mb4_0900_ai_ci;
SET TIME_ZONE = '+00:00';
SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE IF NOT EXISTS entrance_database;
USE entrance_database;

-- Disable FK checks for the whole import
SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- 1. mst_roles  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `mst_roles`;
CREATE TABLE `mst_roles` (
  `Role_Id`      int          NOT NULL AUTO_INCREMENT,
  `Role_Name`    varchar(100) NOT NULL,
  `Access_Level` int          NOT NULL,
  `Description`  varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Role_Id`),
  UNIQUE KEY `Role_Name` (`Role_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mst_roles` VALUES
  (1,'Administrator',1,'Full access'),
  (2,'Dean',2,'School-level access'),
  (3,'Head',3,'Program-level access'),
  (4,'Program Chair',4,'Program-only'),
  (5,'Faculty',5,'Faculty-level'),
  (6,'Teaching Assistant',6,'TA-level');

-- ============================================================
-- 2. mst_school  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `mst_school`;
CREATE TABLE `mst_school` (
  `School_Id`    int         NOT NULL AUTO_INCREMENT,
  `School_Name`  varchar(50) NOT NULL,
  `School_Short` varchar(50) NOT NULL,
  `Is_Active`    tinyint(1)  DEFAULT '1',
  PRIMARY KEY (`School_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mst_school` VALUES
  (1,'School of Engineering & Technology','SET',1),
  (2,'School of Science','SOS',1),
  (3,'School of Business & Law','SBL',1),
  (4,'School of Liberal Studies & Education','SLSE',1),
  (6,'School of Environmental Design & Architecture','SEDA',1),
  (7,'School of Computer Applications','SCA',0);

-- ============================================================
-- 3. mst_designation  (depends on mst_roles)
-- ============================================================
DROP TABLE IF EXISTS `mst_designation`;
CREATE TABLE `mst_designation` (
  `Designation_Id`   int          NOT NULL AUTO_INCREMENT,
  `Designation_Name` varchar(150) NOT NULL,
  `Role_Id`          int          DEFAULT NULL,
  `Is_Active`        tinyint(1)   DEFAULT '1',
  PRIMARY KEY (`Designation_Id`),
  UNIQUE KEY `Designation_Name` (`Designation_Name`),
  KEY `Role_Id` (`Role_Id`),
  CONSTRAINT `mst_designation_ibfk_1` FOREIGN KEY (`Role_Id`) REFERENCES `mst_roles` (`Role_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mst_designation` VALUES
  (1,'Administrator',1,1),
  (2,'Dean',2,1),
  (3,'Head',3,1),
  (4,'Program Chair',4,1),
  (5,'Professor',5,1),
  (6,'Teaching Assistant',6,1),
  (7,'Lecturer',5,1),
  (8,'Assistant Professor',5,1),
  (9,'Associate Professor',5,1),
  (10,'Mentor',6,1),
  (11,'Professor of Practice',5,0);

-- ============================================================
-- 4. mst_admin  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `mst_admin`;
CREATE TABLE `mst_admin` (
  `Admin_ID`    int          NOT NULL AUTO_INCREMENT,
  `Name`        varchar(100) DEFAULT NULL,
  `Email`       varchar(100) DEFAULT NULL,
  `Password`    varchar(255) DEFAULT NULL,
  `Is_Active`   tinyint(1)   DEFAULT '1',
  `Profile_Pic` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Admin_ID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mst_admin` VALUES
  (1,'Dhaval Mehta','dhavalm@nuv.ac.in','dm123@NUV',1,NULL),
  (2,'Shraddha Doshi','shraddha.doshi@nuv.ac.in','sd123@NUV',1,NULL),
  (3,'Kashaf Parkar','kashaf.parkar@nuv.ac.in','kp123@NUV',1,NULL),
  (4,'Izma Shaikh','izma.shaikh@nuv.ac.in','is123@NUV',1,NULL),
  (5,'Yasir Shaikh','yasir.shaikh@nuv.ac.in','ys123@NUV',1,NULL),
  (8,'Chirag Darji','chirag.darji@nuv.ac.in','Chirag@NUV',1,NULL),
  (9,'Kashaf','kashaf.a.parkar@nuv.ac.in','12345',1,NULL);

-- ============================================================
-- 5. mst_faculty  (depends on mst_school)
-- ============================================================
DROP TABLE IF EXISTS `mst_faculty`;
CREATE TABLE `mst_faculty` (
  `Faculty_Id`     int         NOT NULL AUTO_INCREMENT,
  `F_Name`         varchar(50) NOT NULL,
  `F_Email`        varchar(50) NOT NULL,
  `School_Id`      int         NOT NULL,
  `Designation_Id` int         DEFAULT NULL,
  `Password`       varchar(255) NOT NULL,
  `Role_Id`        int         DEFAULT NULL,
  `Is_Active`      tinyint(1)  DEFAULT '1',
  `Profile_Pic`    varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Faculty_Id`),
  UNIQUE KEY `F_Email` (`F_Email`),
  KEY `School_Id` (`School_Id`),
  CONSTRAINT `mst_faculty_ibfk_1` FOREIGN KEY (`School_Id`) REFERENCES `mst_school` (`School_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mst_faculty` VALUES
  (1,'Chirag Darji','chirag.darji@nuv.ac.in',1,1,'Chirag@123',1,1,NULL),
  (2,'Dhaval Mehta','dhavalm@nuv.ac.in',1,4,'Dhaval@123',4,1,NULL),
  (3,'Shraddha Doshi','shraddha.doshi@nuv.ac.in',1,5,'Shraddha@123',5,1,NULL),
  (4,'Rupali Shinde','rupali.shinde@nuv.ac.in',1,5,'Rupali@123',5,1,NULL),
  (5,'Megha Patel','megha.patel@nuv.ac.in',1,5,'Megha@123',5,1,NULL),
  (6,'Shardav Bhatt','shardavb@nuv.ac.in',1,4,'Shardav@123',4,1,NULL),
  (7,'Dr. Vivek Bhatt','vivek.bhatt@nuv.ac.in',3,5,'Vivek@123',5,0,NULL),
  (8,'Dharti Parikh','dhartip@nuv.ac.in',3,5,'Dharti@123',5,0,NULL),
  (9,'Humayed Shaikh','humayd.shaikh@nuv.ac.in',1,6,'Humayd@123',6,1,NULL),
  (10,'Aymaan Garasia','aymaan.garasia@nuv.ac.in',1,6,'Aymaan@123',6,0,NULL),
  (14,'Margie Patolia','margie.patoliya@nuv.ac.in',1,6,'Margie@123',6,0,NULL),
  (18,'Vedant Parmar','vedant.j.parmar@nuv.ac.in',1,6,'Vedant@123',6,0,NULL),
  (30,'Mariyam Memom','mariyam.memon@nuv.ac.in',1,6,'Mariyam@123',6,0,NULL),
  (33,'Salma Pirzada','salmap@nuv.ac.in',1,8,'Salma@123',5,1,NULL);

-- ============================================================
-- 6. faculty_groups  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `faculty_groups`;
CREATE TABLE `faculty_groups` (
  `Group_Id`      int          NOT NULL AUTO_INCREMENT,
  `Group_Name`    varchar(100) NOT NULL,
  `Faculty_Email` varchar(100) NOT NULL,
  `Created_On`    timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  `Is_Active`     tinyint(1)   DEFAULT '1',
  PRIMARY KEY (`Group_Id`),
  UNIQUE KEY `unique_faculty_group` (`Group_Name`, `Faculty_Email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `faculty_groups` VALUES
  (1,'BCA','dhavalm@nuv.ac.in','2026-01-28 11:23:57',1),
  (2,'BBA','dhavalm@nuv.ac.in','2026-01-29 06:06:27',1),
  (6,'MSc','kashaf.parkar@nuv.ac.in','2026-02-06 09:23:03',0);

-- ============================================================
-- 7. faculty_group_assign  (depends on mst_faculty, faculty_groups)
-- ============================================================
DROP TABLE IF EXISTS `faculty_group_assign`;
CREATE TABLE `faculty_group_assign` (
  `Assign_Id`   int       NOT NULL AUTO_INCREMENT,
  `Faculty_Id`  int       NOT NULL,
  `Group_Id`    int       NOT NULL,
  `Assigned_On` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Assign_Id`),
  UNIQUE KEY `uniq_faculty_group` (`Faculty_Id`,`Group_Id`),
  KEY `Group_Id` (`Group_Id`),
  CONSTRAINT `faculty_group_assign_ibfk_1` FOREIGN KEY (`Faculty_Id`) REFERENCES `mst_faculty` (`Faculty_Id`),
  CONSTRAINT `faculty_group_assign_ibfk_2` FOREIGN KEY (`Group_Id`)   REFERENCES `faculty_groups` (`Group_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `faculty_group_assign` VALUES
  (1,2,1,'2026-01-28 11:24:05'),
  (2,1,1,'2026-01-28 11:24:09'),
  (6,3,1,'2026-01-28 11:24:23'),
  (7,5,1,'2026-01-29 05:56:02'),
  (8,33,1,'2026-01-29 05:56:04'),
  (9,4,1,'2026-01-29 05:56:06'),
  (10,8,2,'2026-01-29 06:06:34'),
  (16,10,1,'2026-01-29 07:17:35'),
  (17,9,1,'2026-01-29 07:18:51'),
  (18,14,1,'2026-01-29 07:20:47'),
  (26,7,2,'2026-02-06 06:44:47');

-- ============================================================
-- 8. applicant_groups  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `applicant_groups`;
CREATE TABLE `applicant_groups` (
  `Group_Id`      int          NOT NULL AUTO_INCREMENT,
  `Group_Name`    varchar(100) DEFAULT NULL,
  `Faculty_Email` varchar(100) DEFAULT NULL,
  `Created_At`    timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  `Is_Active`     tinyint(1)   DEFAULT '1',
  PRIMARY KEY (`Group_Id`),
  UNIQUE KEY `unique_group_per_faculty` (`Group_Name`, `Faculty_Email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `applicant_groups` VALUES
  (1,'BCA 1','dhavalm@nuv.ac.in','2026-01-22 09:49:18',1),
  (2,'BCA 2','dhavalm@nuv.ac.in','2026-01-22 09:53:09',0),
  (3,'BCA 3','dhavalm@nuv.ac.in','2026-01-22 10:45:14',0),
  (5,'__UNASSIGNED__','system@internal','2026-01-28 10:13:34',1),
  (6,'BCA Entrance','dhavalm@nuv.ac.in','2026-01-28 10:59:13',1),
  (8,'BCA','kashaf786parkar@gmail.com','2026-01-29 06:40:19',1),
  (12,'BCA Final','dhavalm@nuv.ac.in','2026-02-23 05:42:38',1);

-- ============================================================
-- 9. applicants  (depends on applicant_groups)
-- ============================================================
DROP TABLE IF EXISTS `applicants`;
CREATE TABLE `applicants` (
  `Applicant_Id`      int          NOT NULL AUTO_INCREMENT,
  `Full_Name`         varchar(100) NOT NULL,
  `Email`             varchar(100) NOT NULL,
  `Password`          varchar(100) NOT NULL,
  `Phone`             varchar(15)  DEFAULT NULL,
  `DOB`               date         DEFAULT NULL,
  `Gender`            enum('Male','Female','Other') DEFAULT NULL,
  `Address`           text,
  `Registration_Date` timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  `group_id`          int          DEFAULT NULL,
  `Is_Active`         tinyint(1)   DEFAULT '1',
  PRIMARY KEY (`Applicant_Id`),
  UNIQUE KEY `Email` (`Email`),
  KEY `fk_applicant_group` (`group_id`),
  CONSTRAINT `fk_applicant_group` FOREIGN KEY (`group_id`) REFERENCES `applicant_groups` (`Group_Id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `applicants` VALUES
  (1,'Kashaf Ahmed Parkar','kashaf786parkar@gmail.com','Kashaf@123','09967535850','2005-11-07','Female','Mumbai Maharashtra','2025-10-13 07:43:10',12,1),
  (2,'Izma Shaikh','izmashaikh7681@gmail.com','Izma@123','8160026252','2006-02-16','Female','Fatehgunj Vadodara','2025-10-13 07:53:21',12,1),
  (3,'Yasir Shaikh','yasirazimshaikh5440@gmail.com','Yasir@123','8799132161','2003-12-24','Male','Tandalja Vadodara','2025-10-13 07:55:56',12,1),
  (54,'Kaif Ansari','ansarikaif23604@gmail.com','Kaif@123','1232654585','2003-06-06','Male','Tandalja, Vadodara','2025-11-12 07:09:56',12,1),
  (63,'Kavya Nair','kavya.nair@example.com','kavya@123','9898123456',NULL,'Female','17 MG Road','2025-11-12 10:22:59',12,1),
  (64,'Aditya Mehta','aditya.mehta@example.com','aditya@2025','9988776655','2004-02-11','Male','8 Sunrise Colony','2025-11-12 10:22:59',12,1),
  (65,'Sneha Gupta','sneha.gupta@example.com','sneha@pwd','9090909090',NULL,'Female','12 Lotus Street','2025-11-12 10:22:59',12,1),
  (66,'Masira Parkar','masiii@nuv.ac.in','Masi@NUV','07845123265','2006-02-04','Female','Sakhrol Maharashtra','2026-01-22 09:52:26',1,1),
  (70,'Aay Khan','ayan@gmail.com','ayaan@123','9876543210','2002-05-14','Male','Ahmedabad, Gujarat','2026-01-27 10:48:45',1,0),
  (71,'Sar Sheikh','sar@gmail.com','sara@123','9123456789','2001-09-22','Female','Vadodara, Gujarat','2026-01-27 10:48:45',1,1),
  (72,'Zaidddd Patel','zaiddd@gmail.com','zaid@123','9988776655','2003-01-10','Male','Surat, Gujarat','2026-01-27 10:48:45',1,0),
  (73,'Alisha Tambe','alisha.tambe15@gmail.com','Alisha@123','09879865465','2019-11-15','Female','Karji Maharashtra','2026-01-28 11:00:14',6,1),
  (74,'Aiza Tambe','aiza123@nuv.ac.in','Aiza@123','07845123265','2020-01-07','Female','Karji Maharashtra','2026-01-29 05:57:03',6,1),
  (78,'Vasudha Deshpande','vasudha@gmail.com','Vasudha@123','9872243210','2005-12-30','Female','Mumbai, Maharashtra','2026-01-29 06:05:46',6,1),
  (79,'Anjali Patel','anjali@gmail.com','Anjali@123','9123477789','2001-09-20','Female','Vadodara, Gujarat','2026-01-29 06:05:46',6,1),
  (80,'Zubeda Tambe','zubeda@gmail.com','Zubeda@123','9988446655','2003-08-03','Female','Dongri, Maharashtra','2026-01-29 06:05:46',6,1),
  (82,'Aiza Tambe','aiza123tambe@nuv.ac.in','Aiza@123','07845123265','2020-01-07','Female','Karji Maharashtra','2026-01-29 06:40:51',8,1),
  (91,'Alfiya Tambe','alfiya@gmail.com','Alfiya@123','8754213265','2011-02-21','Female','Karji Maharashtra','2026-01-29 10:25:10',8,1),
  (92,'Zoya Tambe','zoya@gmailcom','Zoya@123','7845123569','2009-08-26','Female','Sharjah, Dubai','2026-01-29 10:26:18',8,1),
  (93,'Aaliya','aaliya@gmail.com','Aaliya@123','7856123491','2009-03-20','Female','Tandalja, Vadodara','2026-02-10 06:23:34',1,1),
  (94,'Zooiii','zoii@gmail.com','Zoii@123','9123265458','2009-09-26','Female','Tandalja, Vadodara','2026-02-10 06:29:01',8,1),
  (95,'Shafak Tambe','shafak@gmail.com','Shafak@123','9860348353','2008-10-15','Female','Karji Maharashtra','2026-02-10 06:36:22',6,1),
  (96,'Amrin Parkar','amrin@gmail.com','Amrin@123','1526485973','2009-08-07','Female','Karji Maharashtra','2026-02-10 06:37:27',1,1),
  (97,'Vanshika Salekar','vanshika@nuv.ac.in','Vanshika@123','7856124253','2004-11-06','Female','Gotri Vadodara','2026-02-10 09:27:30',1,1),
  (98,'Arshin Chauhan','arshin@nuv.ac.in','Arshin2123','8855221147','2005-03-23','Female','Tandalja, Vadodara','2026-02-10 09:36:49',1,1);

-- ============================================================
-- 10. entrance_exam  (no dependencies)
-- ============================================================
DROP TABLE IF EXISTS `entrance_exam`;
CREATE TABLE `entrance_exam` (
  `Exam_Id`          int          NOT NULL AUTO_INCREMENT,
  `Exam_Name`        varchar(100) NOT NULL,
  `Exam_Date`        date         NOT NULL,
  `Exam_Time`        time         NOT NULL,
  `Duration_Minutes` int          NOT NULL,
  `Total_Questions`  int          NOT NULL,
  `Max_Marks`        int          NOT NULL,
  `Faculty_Email`    varchar(255) DEFAULT NULL,
  `notify_10min`     tinyint      DEFAULT '0',
  `exam_status`      enum('OFF','ON') DEFAULT 'OFF',
  `was_started`      tinyint(1)   DEFAULT '0',
  PRIMARY KEY (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `entrance_exam` VALUES
  (1,'Test','2026-01-27','11:50:00',10,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),
  (2,'Quiz','2026-01-27','16:15:00',2,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),
  (7,'Testing','2026-01-29','13:05:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (9,'Email Trial','2026-01-29','12:20:00',5,5,5,'kashaf786parkar@gmail.com',1,'OFF',0),
  (10,'Email Testing','2026-01-29','12:23:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (11,'Exam 1','2026-01-30','17:10:00',5,5,5,'kashaf.a.parkar@nuv.ac.in',1,'OFF',0),
  (15,'Entrance BCA','2026-02-02','11:35:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (17,'Test','2026-02-02','11:55:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (21,'Test 2','2026-02-23','11:45:00',5,5,5,'dhavalm@nuv.ac.in',1,'OFF',1),
  (22,'Quiz','2026-02-23','17:00:00',5,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),
  (23,'Review','2026-02-24','15:45:00',5,5,5,'dhavalm@nuv.ac.in',1,'OFF',1),
  (24,'Testing','2026-02-25','14:10:00',10,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (25,'Unique','2026-02-26','16:00:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (26,'Testing Restriction','2026-02-27','13:41:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (27,'Storage Check','2026-03-02','14:40:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (28,'Test','2026-03-05','15:50:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (29,'Testing','2026-03-05','16:10:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (30,'Testing','2026-03-06','13:32:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (31,'Quizzz','2026-03-06','14:10:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (32,'Testing','2026-03-09','11:40:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),
  (33,'End Sem','2026-03-11','11:00:00',15,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),
  (34,'Testify','2026-03-16','11:55:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1);

-- ============================================================
-- 11. entrance_question_bank  (depends on entrance_exam)
-- ============================================================
DROP TABLE IF EXISTS `entrance_question_bank`;
CREATE TABLE `entrance_question_bank` (
  `Question_Id`   int          NOT NULL AUTO_INCREMENT,
  `Exam_Id`       int          NOT NULL,
  `Question_Type` enum('MCQ','Fill','TF','OneWord') NOT NULL,
  `Question_Text` text         NOT NULL,
  `Option_A`      varchar(255) DEFAULT NULL,
  `Option_B`      varchar(255) DEFAULT NULL,
  `Option_C`      varchar(255) DEFAULT NULL,
  `Option_D`      varchar(255) DEFAULT NULL,
  `Correct_Answer` varchar(255) NOT NULL,
  `Marks`         int          DEFAULT '1',
  `Created_At`    datetime     DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Question_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `entrance_question_bank_ibfk_1` FOREIGN KEY (`Exam_Id`) REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `entrance_question_bank` VALUES
  (1,2,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-27 15:52:10'),
  (2,2,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-27 15:52:10'),
  (3,2,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-27 15:52:10'),
  (4,2,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-27 15:52:10'),
  (5,2,'MCQ','Which is a programming language?','ABC','HTML','JAVA','OOPS','JAVA',1,'2026-01-27 15:53:12'),
  (6,7,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-29 11:40:12'),
  (7,7,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-29 11:40:12'),
  (8,7,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-29 11:40:12'),
  (9,7,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-29 11:40:12'),
  (10,7,'Fill','Full Form of ST is ','','','','','Software Testing',1,'2026-01-29 11:40:39'),
  (11,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 10:48:13'),
  (12,11,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-30 10:48:13'),
  (13,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 10:48:13'),
  (14,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 10:48:13'),
  (15,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 10:51:47'),
  (16,11,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-01-30 10:51:47'),
  (17,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 10:51:47'),
  (18,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 10:51:47'),
  (19,11,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-01-30 10:51:47'),
  (20,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 11:53:05'),
  (21,11,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-30 11:53:05'),
  (22,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 11:53:05'),
  (23,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 11:53:05'),
  (28,21,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-23 11:16:39'),
  (29,21,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-02-23 11:16:39'),
  (30,21,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-23 11:16:39'),
  (31,21,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-23 11:16:39'),
  (32,21,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-02-23 11:16:39'),
  (33,24,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-25 11:06:55'),
  (34,24,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-02-25 11:06:55'),
  (35,24,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-25 11:06:55'),
  (36,24,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-25 11:06:55'),
  (37,24,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-02-25 11:06:55'),
  (38,25,'MCQ','Correct GSM of Watercolour Paper','300 GSM','50 GSM','100 GSM','1000 GSM','300 GSM',1,'2026-02-26 11:51:51'),
  (39,25,'TF','Acrylic Paint is Different from Oil Paint.','True','False','','','True',1,'2026-02-26 11:52:46'),
  (40,25,'Fill','For One Stroke Painting _______ and _______ brush is used','','','','','Round and Flat',1,'2026-02-26 11:53:29'),
  (41,25,'MCQ','Colour Tone of Pastel is','Dark Shades','Normal Shades','Lighter Shades ','None of the above','Lighter Shades ',1,'2026-02-26 11:54:39'),
  (42,25,'OneWord','What is the ratio of Resin and Hardener?','','','','','2:1',1,'2026-02-26 11:56:12'),
  (43,26,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-27 11:04:20'),
  (44,26,'TF','Java is a statically typed language','True','False','','','True',1,'2026-02-27 11:04:20'),
  (45,26,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-27 11:04:20'),
  (46,26,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-27 11:04:20'),
  (47,26,'TF','HTML is used for frontend','True','False','','','True',1,'2026-02-27 11:05:07'),
  (48,27,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-02 14:34:59'),
  (49,27,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-02 14:34:59'),
  (50,27,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-02 14:34:59'),
  (51,27,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-02 14:34:59'),
  (52,27,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-02 14:34:59'),
  (53,28,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-05 15:49:37'),
  (54,28,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-05 15:49:37'),
  (55,28,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-05 15:49:37'),
  (56,28,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-05 15:49:37'),
  (57,28,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-05 15:49:37'),
  (58,29,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-05 16:09:31'),
  (59,29,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-05 16:09:31'),
  (60,29,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-05 16:09:31'),
  (61,29,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-05 16:09:31'),
  (62,29,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-05 16:09:31'),
  (63,30,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-06 11:48:48'),
  (64,30,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-06 11:48:48'),
  (65,30,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-06 11:48:48'),
  (66,30,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-06 11:48:48'),
  (67,30,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-06 11:48:48'),
  (68,31,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-06 14:10:11'),
  (69,31,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-06 14:10:11'),
  (70,31,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-06 14:10:11'),
  (71,31,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-06 14:10:11'),
  (72,31,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-06 14:10:11'),
  (73,32,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-09 11:28:50'),
  (74,32,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-09 11:28:50'),
  (75,32,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-09 11:28:50'),
  (76,32,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-09 11:28:50'),
  (77,32,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-09 11:28:50'),
  (78,33,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-11 11:00:23'),
  (79,33,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-11 11:00:23'),
  (80,33,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-11 11:00:23'),
  (81,33,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-11 11:00:23'),
  (82,33,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-11 11:00:23'),
  (83,34,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-16 11:53:53'),
  (84,34,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-16 11:53:53'),
  (85,34,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-16 11:53:53'),
  (86,34,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-16 11:53:53'),
  (87,34,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-16 11:53:53');

-- ============================================================
-- 12. exam_paper  (depends on entrance_exam)
-- ============================================================
DROP TABLE IF EXISTS `exam_paper`;
CREATE TABLE `exam_paper` (
  `Exam_Paper_Id`    int            NOT NULL AUTO_INCREMENT,
  `Exam_Id`          int            NOT NULL,
  `Title`            varchar(255)   NOT NULL,
  `Total_Marks`      decimal(5,2)   NOT NULL,
  `Duration_Minutes` int            NOT NULL,
  `Created_At`       timestamp      NULL DEFAULT CURRENT_TIMESTAMP,
  `is_saved`         tinyint(1)     DEFAULT '0',
  PRIMARY KEY (`Exam_Paper_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `exam_paper_ibfk_1` FOREIGN KEY (`Exam_Id`) REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `exam_paper` VALUES
  (1,2,'Quiz',5.00,2,'2026-01-27 10:22:15',0),
  (2,7,'Testing',5.00,5,'2026-01-29 06:11:08',0),
  (3,11,'Exam 1',5.00,5,'2026-01-30 09:54:59',0),
  (4,21,'Test 2',5.00,5,'2026-02-23 05:47:11',0),
  (5,24,'Testing',5.00,5,'2026-02-25 05:37:02',0),
  (6,25,'Unique',5.00,5,'2026-02-26 06:24:47',0),
  (7,26,'Testing Restriction',5.00,5,'2026-02-27 05:34:34',0),
  (8,27,'Storage Check',5.00,5,'2026-03-02 09:05:05',1),
  (9,28,'Test',5.00,5,'2026-03-05 10:19:43',1),
  (10,29,'Testing',5.00,5,'2026-03-05 10:39:37',1),
  (11,30,'Testing',5.00,5,'2026-03-06 06:18:53',1),
  (12,31,'Quizzz',5.00,5,'2026-03-06 08:40:17',1),
  (13,32,'Testing',5.00,5,'2026-03-09 05:58:59',1),
  (14,33,'End Sem',5.00,15,'2026-03-11 05:30:31',1),
  (15,34,'Testify',5.00,5,'2026-03-16 06:24:03',1);

-- ============================================================
-- 13. exam_paper_questions  (depends on exam_paper, entrance_question_bank)
-- ============================================================
DROP TABLE IF EXISTS `exam_paper_questions`;
CREATE TABLE `exam_paper_questions` (
  `Exam_Paper_Id` int NOT NULL,
  `Question_Id`   int NOT NULL,
  PRIMARY KEY (`Exam_Paper_Id`,`Question_Id`),
  KEY `Question_Id` (`Question_Id`),
  CONSTRAINT `exam_paper_questions_ibfk_1` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`),
  CONSTRAINT `exam_paper_questions_ibfk_2` FOREIGN KEY (`Question_Id`)   REFERENCES `entrance_question_bank` (`Question_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `exam_paper_questions` VALUES
  (1,1),(1,2),(1,3),(1,4),(1,5),
  (2,6),(2,7),(2,8),(2,9),(2,10),
  (3,12),(3,13),(3,14),(3,19),(3,20),
  (4,28),(4,29),(4,30),(4,31),(4,32),
  (5,33),(5,34),(5,35),(5,36),(5,37),
  (6,38),(6,39),(6,40),(6,41),(6,42),
  (7,43),(7,44),(7,45),(7,46),(7,47),
  (8,48),(8,49),(8,50),(8,51),(8,52),
  (9,53),(9,54),(9,55),(9,56),(9,57),
  (10,58),(10,59),(10,60),(10,61),(10,62),
  (11,63),(11,64),(11,65),(11,66),(11,67),
  (12,68),(12,69),(12,70),(12,71),(12,72),
  (13,73),(13,74),(13,75),(13,76),(13,77),
  (14,78),(14,79),(14,80),(14,81),(14,82),
  (15,83),(15,84),(15,85),(15,86),(15,87);

-- ============================================================
-- 14. applicant_attempt  (depends on applicants, exam_paper)
-- ============================================================
DROP TABLE IF EXISTS `applicant_attempt`;
CREATE TABLE `applicant_attempt` (
  `Attempt_Id`     int            NOT NULL AUTO_INCREMENT,
  `Applicant_Id`   int            NOT NULL,
  `Student_Email`  varchar(255)   DEFAULT NULL,
  `Exam_Paper_Id`  int            NOT NULL,
  `Start_Time`     datetime       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `End_Time`       datetime       DEFAULT NULL,
  `Status`         enum('In Progress','Submitted','Timed Out','Restricted') NOT NULL,
  `Marks_Obtained` decimal(5,2)   DEFAULT '0.00',
  PRIMARY KEY (`Attempt_Id`),
  KEY `Applicant_Id` (`Applicant_Id`),
  KEY `Exam_Paper_Id` (`Exam_Paper_Id`),
  CONSTRAINT `applicant_attempt_ibfk_1` FOREIGN KEY (`Applicant_Id`)  REFERENCES `applicants` (`Applicant_Id`),
  CONSTRAINT `applicant_attempt_ibfk_2` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `applicant_attempt` VALUES
  (1,1,'kashaf786parkar@gmail.com',5,'2026-02-25 11:42:19','2026-02-25 11:42:53','Submitted',5.00),
  (2,3,'yasirazimshaikh5440@gmail.com',5,'2026-02-25 11:46:36','2026-02-25 11:46:57','Submitted',3.00),
  (3,2,'izmashaikh7681@gmail.com',5,'2026-02-25 11:47:56','2026-02-25 11:48:22','Submitted',3.00),
  (4,65,'sneha.gupta@example.com',5,'2026-02-25 11:48:58','2026-02-25 11:49:09','Submitted',2.00),
  (5,63,'kavya.nair@example.com',5,'2026-02-25 11:50:36','2026-02-25 11:50:50','Submitted',2.00),
  (6,64,'aditya.mehta@example.com',5,'2026-02-25 11:51:24','2026-02-25 11:51:47','Restricted',0.00),
  (7,82,'aiza123tambe@nuv.ac.in',5,'2026-02-25 13:05:23','2026-02-25 13:05:44','Submitted',4.00),
  (8,91,'alfiya@gmail.com',5,'2026-02-25 13:06:15','2026-02-25 13:06:30','Submitted',3.00),
  (9,92,'zoya@gmailcom',5,'2026-02-25 13:07:06','2026-02-25 13:07:45','Submitted',4.00),
  (10,73,'alisha.tambe15@gmail.com',5,'2026-02-25 13:27:56','2026-02-25 13:28:44','Submitted',4.00),
  (11,80,'zubeda@gmail.com',5,'2026-02-25 13:41:12','2026-02-25 13:41:27','Submitted',3.00),
  (12,79,'anjali@gmail.com',5,'2026-02-25 13:42:32','2026-02-25 13:42:44','Submitted',1.00),
  (13,78,'vasudha@gmail.com',5,'2026-02-25 14:08:05','2026-02-25 14:08:18','Submitted',3.00),
  (14,95,'shafak@gmail.com',5,'2026-02-25 14:17:01','2026-02-25 14:17:24','Submitted',4.00),
  (15,74,'aiza123@nuv.ac.in',5,'2026-02-25 14:19:34','2026-02-25 14:19:44','Restricted',0.00),
  (16,1,'kashaf786parkar@gmail.com',6,'2026-02-26 11:57:23','2026-02-26 11:58:07','Submitted',4.00),
  (17,3,'yasirazimshaikh5440@gmail.com',6,'2026-02-26 11:59:22','2026-02-26 11:59:53','Submitted',2.00),
  (18,2,'izmashaikh7681@gmail.com',6,'2026-02-26 12:12:09','2026-02-26 12:13:43','Submitted',2.00),
  (19,63,'kavya.nair@example.com',6,'2026-02-26 12:18:03','2026-02-26 12:19:09','Submitted',2.00),
  (20,65,'sneha.gupta@example.com',6,'2026-02-26 12:19:49','2026-02-26 12:20:42','Submitted',2.00),
  (21,64,'aditya.mehta@example.com',6,'2026-02-26 14:36:59','2026-02-26 14:37:24','Submitted',1.00),
  (22,82,'aiza123tambe@nuv.ac.in',6,'2026-02-26 15:39:18',NULL,'In Progress',0.00),
  (23,91,'alfiya@gmail.com',6,'2026-02-26 15:50:36',NULL,'In Progress',0.00),
  (24,92,'zoya@gmailcom',6,'2026-02-26 16:01:02',NULL,'In Progress',0.00),
  (25,1,'kashaf786parkar@gmail.com',7,'2026-02-27 11:05:46','2026-02-27 11:06:15','Submitted',5.00),
  (26,3,'yasirazimshaikh5440@gmail.com',7,'2026-02-27 11:06:48','2026-02-27 11:07:07','Restricted',0.00),
  (27,54,'ansarikaif23604@gmail.com',7,'2026-02-27 11:08:34','2026-02-27 11:09:06','Restricted',0.00),
  (28,2,'izmashaikh7681@gmail.com',7,'2026-02-27 11:42:53',NULL,'In Progress',0.00),
  (29,63,'kavya.nair@example.com',7,'2026-02-27 11:52:34','2026-02-27 11:53:07','Restricted',0.00),
  (30,65,'sneha.gupta@example.com',7,'2026-02-27 11:55:32','2026-02-27 11:56:10','Restricted',0.00),
  (31,64,'aditya.mehta@example.com',7,'2026-02-27 13:42:14','2026-02-27 13:42:40','Restricted',0.00),
  (32,82,'aiza123tambe@nuv.ac.in',7,'2026-02-27 13:43:31','2026-02-27 13:44:16','Submitted',4.00),
  (33,91,'alfiya@gmail.com',7,'2026-02-27 13:44:55','2026-02-27 13:45:08','Restricted',0.00),
  (34,1,'kashaf786parkar@gmail.com',8,'2026-03-02 14:42:57',NULL,'In Progress',0.00),
  (35,1,'kashaf786parkar@gmail.com',9,'2026-03-05 15:51:56','2026-03-05 15:52:23','Submitted',5.00),
  (36,3,'yasirazimshaikh5440@gmail.com',9,'2026-03-05 15:52:56','2026-03-05 15:53:33','Submitted',3.00),
  (37,54,'ansarikaif23604@gmail.com',9,'2026-03-05 15:53:59','2026-03-05 15:54:45','Submitted',2.00),
  (38,2,'izmashaikh7681@gmail.com',9,'2026-03-05 15:55:43','2026-03-05 15:55:59','Submitted',3.00),
  (39,64,'aditya.mehta@example.com',9,'2026-03-05 15:56:33','2026-03-05 15:56:58','Submitted',3.00),
  (40,65,'sneha.gupta@example.com',9,'2026-03-05 15:57:30','2026-03-05 15:57:43','Restricted',0.00),
  (41,1,'kashaf786parkar@gmail.com',10,'2026-03-05 16:11:34','2026-03-05 16:12:06','Submitted',4.00),
  (42,54,'ansarikaif23604@gmail.com',10,'2026-03-05 16:12:28','2026-03-05 16:12:42','Restricted',0.00),
  (43,1,'kashaf786parkar@gmail.com',11,'2026-03-06 11:50:07','2026-03-06 11:50:26','Submitted',5.00),
  (44,54,'ansarikaif23604@gmail.com',11,'2026-03-06 11:50:51','2026-03-06 11:51:19','Restricted',0.00),
  (45,2,'izmashaikh7681@gmail.com',11,'2026-03-06 11:52:00','2026-03-06 11:53:02','Restricted',0.00),
  (46,65,'sneha.gupta@example.com',11,'2026-03-06 11:56:37','2026-03-06 11:57:10','Submitted',3.00),
  (47,64,'aditya.mehta@example.com',11,'2026-03-06 12:18:18','2026-03-06 12:18:40','Submitted',3.00),
  (48,63,'kavya.nair@example.com',11,'2026-03-06 12:26:06','2026-03-06 12:26:19','Submitted',3.00),
  (49,82,'aiza123tambe@nuv.ac.in',11,'2026-03-06 12:28:19','2026-03-06 12:28:32','Submitted',4.00),
  (50,94,'zoii@gmail.com',11,'2026-03-06 12:30:30','2026-03-06 12:32:12','Restricted',0.00),
  (51,92,'zoya@gmailcom',11,'2026-03-06 12:33:04','2026-03-06 12:33:16','Submitted',4.00),
  (52,91,'alfiya@gmail.com',11,'2026-03-06 13:25:07','2026-03-06 13:25:56','Submitted',4.00),
  (53,73,'alisha.tambe15@gmail.com',11,'2026-03-06 13:32:18','2026-03-06 13:33:15','Submitted',4.00),
  (54,1,'kashaf786parkar@gmail.com',12,'2026-03-06 14:10:46','2026-03-06 14:11:26','Submitted',5.00),
  (55,54,'ansarikaif23604@gmail.com',12,'2026-03-06 14:12:24','2026-03-06 14:13:10','Submitted',3.00),
  (56,2,'izmashaikh7681@gmail.com',12,'2026-03-06 14:16:21','2026-03-06 14:16:59','Submitted',2.00),
  (57,1,'kashaf786parkar@gmail.com',13,'2026-03-09 11:30:20','2026-03-09 11:31:23','Restricted',0.00),
  (58,54,'ansarikaif23604@gmail.com',13,'2026-03-09 11:31:55','2026-03-09 11:32:22','Restricted',0.00),
  (59,2,'izmashaikh7681@gmail.com',13,'2026-03-09 11:33:41','2026-03-09 11:34:04','Restricted',0.00),
  (60,63,'kavya.nair@example.com',13,'2026-03-09 11:35:26','2026-03-09 11:35:57','Submitted',3.00),
  (61,64,'aditya.mehta@example.com',13,'2026-03-09 11:36:53','2026-03-09 11:41:54','Submitted',3.00),
  (62,65,'sneha.gupta@example.com',13,'2026-03-09 11:46:09','2026-03-09 11:46:51','Submitted',2.00),
  (63,1,'kashaf786parkar@gmail.com',14,'2026-03-11 11:04:41','2026-03-11 11:05:13','Submitted',2.00),
  (64,54,'ansarikaif23604@gmail.com',14,'2026-03-11 11:05:52','2026-03-11 11:06:37','Submitted',4.00),
  (65,1,'kashaf786parkar@gmail.com',15,'2026-03-16 11:55:09','2026-03-16 11:56:02','Submitted',5.00),
  (66,54,'ansarikaif23604@gmail.com',15,'2026-03-16 11:56:30','2026-03-16 11:57:06','Submitted',3.00),
  (67,2,'izmashaikh7681@gmail.com',15,'2026-03-16 11:57:36','2026-03-16 11:57:59','Restricted',0.00);

-- ============================================================
-- 15. applicant_exam_assign  (depends on applicants, entrance_exam)
-- ============================================================
DROP TABLE IF EXISTS `applicant_exam_assign`;
CREATE TABLE `applicant_exam_assign` (
  `Assign_Id`    int       NOT NULL AUTO_INCREMENT,
  `Applicant_Id` int       NOT NULL,
  `Exam_Id`      int       NOT NULL,
  `Assigned_On`  timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Assign_Id`),
  UNIQUE KEY `uniq_applicant_exam` (`Applicant_Id`,`Exam_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `applicant_exam_assign_ibfk_1` FOREIGN KEY (`Applicant_Id`) REFERENCES `applicants` (`Applicant_Id`),
  CONSTRAINT `applicant_exam_assign_ibfk_2` FOREIGN KEY (`Exam_Id`)      REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `applicant_exam_assign` VALUES
  (1,66,2,'2026-01-27 10:21:50'),(7,73,7,'2026-01-29 06:08:26'),
  (8,74,7,'2026-01-29 06:08:26'),(9,78,7,'2026-01-29 06:08:26'),
  (10,79,7,'2026-01-29 06:08:26'),(11,80,7,'2026-01-29 06:08:26'),
  (12,82,9,'2026-01-29 06:41:08'),(13,82,10,'2026-01-29 06:42:41'),
  (14,82,11,'2026-01-30 05:17:49'),(15,91,11,'2026-01-30 05:17:49'),
  (16,92,11,'2026-01-30 05:17:49'),(21,2,21,'2026-02-23 05:45:25'),
  (22,1,21,'2026-02-23 05:45:25'),(23,3,21,'2026-02-23 05:45:25'),
  (24,64,23,'2026-02-24 09:54:04'),(25,2,23,'2026-02-24 09:54:04'),
  (26,54,23,'2026-02-24 09:54:04'),(27,1,23,'2026-02-24 09:54:04'),
  (28,65,23,'2026-02-24 09:54:04'),(29,3,23,'2026-02-24 09:54:04'),
  (30,64,24,'2026-02-25 05:36:40'),(31,2,24,'2026-02-25 05:36:40'),
  (32,1,24,'2026-02-25 05:36:40'),(33,63,24,'2026-02-25 05:36:40'),
  (34,65,24,'2026-02-25 05:36:40'),(35,3,24,'2026-02-25 05:36:40'),
  (36,82,24,'2026-02-25 07:32:23'),(37,91,24,'2026-02-25 07:32:23'),
  (38,92,24,'2026-02-25 07:32:23'),(39,74,24,'2026-02-25 07:57:02'),
  (40,73,24,'2026-02-25 07:57:02'),(41,79,24,'2026-02-25 07:57:02'),
  (42,95,24,'2026-02-25 07:57:02'),(43,78,24,'2026-02-25 07:57:02'),
  (44,80,24,'2026-02-25 07:57:02'),(45,64,25,'2026-02-26 06:21:04'),
  (46,2,25,'2026-02-26 06:21:04'),(47,1,25,'2026-02-26 06:21:04'),
  (48,63,25,'2026-02-26 06:21:04'),(49,65,25,'2026-02-26 06:21:04'),
  (50,3,25,'2026-02-26 06:21:04'),(51,82,25,'2026-02-26 06:21:04'),
  (52,91,25,'2026-02-26 06:21:04'),(53,92,25,'2026-02-26 06:21:04'),
  (54,64,26,'2026-02-27 05:33:55'),(55,2,26,'2026-02-27 05:33:55'),
  (56,1,26,'2026-02-27 05:33:55'),(57,63,26,'2026-02-27 05:33:55'),
  (58,65,26,'2026-02-27 05:33:55'),(59,3,26,'2026-02-27 05:33:55'),
  (60,54,26,'2026-02-27 05:34:05'),(61,82,26,'2026-02-27 08:11:39'),
  (62,91,26,'2026-02-27 08:11:39'),(63,92,26,'2026-02-27 08:11:39'),
  (64,64,27,'2026-03-02 09:04:42'),(65,2,27,'2026-03-02 09:04:42'),
  (66,54,27,'2026-03-02 09:04:42'),(67,1,27,'2026-03-02 09:04:42'),
  (68,63,27,'2026-03-02 09:04:42'),(69,65,27,'2026-03-02 09:04:42'),
  (70,3,27,'2026-03-02 09:04:42'),(71,64,28,'2026-03-05 10:19:23'),
  (72,2,28,'2026-03-05 10:19:23'),(73,54,28,'2026-03-05 10:19:23'),
  (74,1,28,'2026-03-05 10:19:23'),(75,63,28,'2026-03-05 10:19:23'),
  (76,65,28,'2026-03-05 10:19:23'),(77,3,28,'2026-03-05 10:19:23'),
  (78,64,29,'2026-03-05 10:39:18'),(79,2,29,'2026-03-05 10:39:18'),
  (80,54,29,'2026-03-05 10:39:18'),(81,1,29,'2026-03-05 10:39:18'),
  (82,63,29,'2026-03-05 10:39:18'),(83,65,29,'2026-03-05 10:39:18'),
  (84,3,29,'2026-03-05 10:39:18'),(85,64,30,'2026-03-06 06:18:34'),
  (86,2,30,'2026-03-06 06:18:34'),(87,54,30,'2026-03-06 06:18:34'),
  (88,1,30,'2026-03-06 06:18:34'),(89,63,30,'2026-03-06 06:18:34'),
  (90,65,30,'2026-03-06 06:18:34'),(91,3,30,'2026-03-06 06:18:34'),
  (92,82,30,'2026-03-06 06:57:55'),(93,91,30,'2026-03-06 06:57:55'),
  (94,94,30,'2026-03-06 06:57:55'),(95,92,30,'2026-03-06 06:57:55'),
  (96,74,30,'2026-03-06 08:01:42'),(97,73,30,'2026-03-06 08:01:42'),
  (98,79,30,'2026-03-06 08:01:42'),(99,95,30,'2026-03-06 08:01:42'),
  (100,78,30,'2026-03-06 08:01:42'),(101,80,30,'2026-03-06 08:01:42'),
  (102,64,31,'2026-03-06 08:39:55'),(103,2,31,'2026-03-06 08:39:55'),
  (104,54,31,'2026-03-06 08:39:55'),(105,1,31,'2026-03-06 08:39:55'),
  (106,63,31,'2026-03-06 08:39:55'),(107,65,31,'2026-03-06 08:39:55'),
  (108,3,31,'2026-03-06 08:39:55'),(109,64,32,'2026-03-09 05:58:31'),
  (110,2,32,'2026-03-09 05:58:31'),(111,54,32,'2026-03-09 05:58:31'),
  (112,1,32,'2026-03-09 05:58:31'),(113,63,32,'2026-03-09 05:58:31'),
  (114,65,32,'2026-03-09 05:58:31'),(115,3,32,'2026-03-09 05:58:31'),
  (116,64,33,'2026-03-11 05:30:06'),(117,2,33,'2026-03-11 05:30:06'),
  (118,54,33,'2026-03-11 05:30:06'),(119,1,33,'2026-03-11 05:30:06'),
  (120,63,33,'2026-03-11 05:30:06'),(121,65,33,'2026-03-11 05:30:06'),
  (122,3,33,'2026-03-11 05:30:06'),(123,64,34,'2026-03-16 06:23:38'),
  (124,2,34,'2026-03-16 06:23:38'),(125,54,34,'2026-03-16 06:23:38'),
  (126,1,34,'2026-03-16 06:23:38'),(127,63,34,'2026-03-16 06:23:38'),
  (128,65,34,'2026-03-16 06:23:38'),(129,3,34,'2026-03-16 06:23:38');

-- ============================================================
-- 16. applicant_answers  (depends on applicant_attempt, entrance_question_bank)
-- ============================================================
DROP TABLE IF EXISTS `applicant_answers`;
CREATE TABLE `applicant_answers` (
  `Answer_Id`        int          NOT NULL AUTO_INCREMENT,
  `Attempt_Id`       int          NOT NULL,
  `Question_Id`      int          NOT NULL,
  `Selected_Option_Id` varchar(255) DEFAULT NULL,
  `Answer_Text`      text,
  PRIMARY KEY (`Answer_Id`),
  KEY `idx_applicant_answers_attempt`  (`Attempt_Id`),
  KEY `idx_applicant_answers_question` (`Question_Id`),
  CONSTRAINT `applicant_answers_ibfk_1` FOREIGN KEY (`Attempt_Id`)  REFERENCES `applicant_attempt` (`Attempt_Id`),
  CONSTRAINT `applicant_answers_ibfk_2` FOREIGN KEY (`Question_Id`) REFERENCES `entrance_question_bank` (`Question_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=600 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `applicant_answers` VALUES (1,1,33,'A','Stack'),(2,1,34,'A','TRUE'),(3,1,35,NULL,'Central Processing Unit'),(4,1,36,NULL,'101'),(5,1,37,'B','Queue'),(6,2,33,'A','Stack'),(7,2,34,'A','TRUE'),(8,2,35,NULL,'sdfghjkl;'),(9,2,36,NULL,'101'),(10,2,37,'C','Linked List'),(11,3,33,'A','Stack'),(12,3,34,'B','FALSE'),(13,3,35,NULL,'fghjkl.'),(14,3,36,NULL,'101'),(15,3,37,'B','Queue'),(16,4,33,'C','Linked List'),(17,4,34,'A','TRUE'),(18,4,35,NULL,'fghjkl'),(19,4,36,NULL,'454'),(20,4,37,'B','Queue'),(21,5,33,'A','Stack'),(22,5,34,'A','TRUE'),(23,5,35,NULL,'cpu'),(24,5,36,NULL,'414'),(25,5,37,'C','Linked List'),(26,7,33,'A','Stack'),(27,7,34,'A','TRUE'),(28,7,35,NULL,'Central Processing Unit'),(29,7,36,NULL,'101'),(30,7,37,'D','Tree'),(31,8,33,'B','Queue'),(32,8,34,'A','TRUE'),(33,8,35,NULL,'asdfghjk'),(34,8,36,NULL,'101'),(35,8,37,'B','Queue'),(36,9,33,'A','Stack'),(37,9,34,'A','TRUE'),(38,9,35,NULL,'sdfghjk'),(39,9,36,NULL,'101'),(40,9,37,'B','Queue'),(41,10,33,'A','Stack'),(42,10,34,'A','TRUE'),(43,10,35,NULL,'fghjkl'),(44,10,36,NULL,'101'),(45,10,37,'B','Queue'),(46,11,33,'B','Queue'),(47,11,34,'A','TRUE'),(48,11,35,NULL,'cpu'),(49,11,36,NULL,'101'),(50,11,37,'B','Queue'),(51,12,33,'B','Queue'),(52,12,34,'B','FALSE'),(53,12,35,NULL,'fghjkl'),(54,12,36,NULL,'1010'),(55,12,37,'B','Queue'),(56,13,33,'B','Queue'),(57,13,34,'A','TRUE'),(58,13,35,NULL,'asdf'),(59,13,36,NULL,'101'),(60,13,37,'B','Queue'),(61,14,33,'A','Stack'),(62,14,34,'A','TRUE'),(63,14,35,NULL,'central processing unit'),(64,14,36,NULL,'11111'),(65,14,37,'B','Queue'),(66,16,38,'A','300 GSM'),(67,16,39,'A','True'),(68,16,40,NULL,'Round and Brush'),(69,16,41,'C','Lighter Shades '),(70,16,42,NULL,'2:1'),(71,17,38,'A','300 GSM'),(72,17,39,'A','True'),(73,17,40,NULL,'xcfghjkl'),(74,18,38,'B','50 GSM'),(75,18,39,'A','True'),(76,18,40,NULL,'round'),(77,18,41,'C','Lighter Shades '),(78,18,42,NULL,'2:4'),(79,19,38,'C','100 GSM'),(80,19,39,'A','True'),(81,19,40,NULL,'flat'),(82,19,41,'C','Lighter Shades '),(83,19,42,NULL,'2:5'),(84,20,38,'B','50 GSM'),(85,20,39,'A','True'),(86,20,40,NULL,'asdfg'),(87,20,41,'C','Lighter Shades '),(88,20,42,NULL,'dfgh'),(89,21,38,'C','100 GSM'),(90,21,39,'A','True'),(91,21,40,NULL,'ok'),(92,21,41,'A','Dark Shades'),(93,21,42,NULL,'sdfgh'),(94,25,43,'A','Stack'),(95,25,44,'A','True'),(96,25,45,NULL,'Central Processing Unit'),(97,25,46,NULL,'101'),(98,25,47,'A','True'),(101,29,43,'A','Stack'),(102,29,44,'A','True'),(103,30,43,'B','Queue'),(104,30,44,'A','True'),(105,30,45,NULL,'central Processing unit'),(106,30,47,'A','True'),(107,31,43,'A','Stack'),(108,31,44,'A','True'),(109,32,43,'A','Stack'),(110,32,44,'A','True'),(111,32,45,NULL,'CPU'),(112,32,46,NULL,'101'),(113,32,47,'A','True'),(114,33,43,'A','Stack'),(115,35,53,'A','Stack'),(116,35,54,'A','TRUE'),(117,35,55,NULL,'Central Processing Unit'),(118,35,56,NULL,'101'),(119,35,57,'B','Queue'),(120,36,53,'A','Stack'),(121,36,54,'A','TRUE'),(122,36,55,NULL,'sdfghj'),(123,36,56,NULL,'2121'),(124,36,57,'B','Queue'),(125,37,53,'C','Linked List'),(126,37,54,'A','TRUE'),(127,37,55,NULL,'sdfv'),(128,37,56,NULL,'151'),(129,37,57,'B','Queue'),(130,38,53,'B','Queue'),(131,38,54,'A','TRUE'),(132,38,55,NULL,'cpu'),(133,38,56,NULL,'101'),(134,38,57,'B','Queue'),(135,39,53,'C','Linked List'),(136,39,54,'A','TRUE'),(137,39,55,NULL,'sdf'),(138,39,56,NULL,'101'),(139,39,57,'B','Queue'),(140,40,53,'C','Linked List'),(141,40,54,'A','TRUE'),(142,41,58,'A','Stack'),(143,41,59,'A','TRUE'),(144,41,60,NULL,'cpu'),(145,41,61,NULL,'101'),(146,41,62,'B','Queue'),(147,42,58,'A','Stack'),(148,42,59,'A','TRUE'),(149,43,63,'A','Stack'),(150,43,64,'A','TRUE'),(151,43,65,NULL,'Central Processing Unit'),(152,43,66,NULL,'101'),(153,43,67,'B','Queue'),(154,44,63,'C','Linked List'),(155,44,64,'B','FALSE'),(156,44,65,NULL,'asdfghj'),(157,44,66,NULL,'101'),(158,45,63,'B','Queue'),(159,45,64,'A','TRUE'),(160,45,65,NULL,'ghj'),(161,45,66,NULL,'101'),(162,46,63,'B','Queue'),(163,46,64,'A','TRUE'),(164,46,65,NULL,'cpu'),(165,46,66,NULL,'101'),(166,46,67,'B','Queue'),(167,47,63,'A','Stack'),(168,47,64,'A','TRUE'),(169,47,65,NULL,'fghjk'),(170,47,66,NULL,'ghjk'),(171,47,67,'B','Queue'),(172,48,63,'A','Stack'),(173,48,64,'A','TRUE'),(174,48,65,NULL,'sfs'),(175,48,66,NULL,'arg'),(176,48,67,'B','Queue'),(177,49,63,'A','Stack'),(178,49,64,'A','TRUE'),(179,49,65,NULL,'cpu'),(180,49,66,NULL,'101'),(181,49,67,'B','Queue'),(182,50,63,'A','Stack'),(183,50,64,'A','TRUE'),(184,50,65,NULL,'cpu'),(185,50,66,NULL,'101'),(186,51,63,'A','Stack'),(187,51,64,'A','TRUE'),(188,51,65,NULL,'fgh'),(189,51,66,NULL,'101'),(190,51,67,'B','Queue'),(191,52,63,'A','Stack'),(192,52,64,'A','TRUE'),(193,52,65,NULL,'cpu'),(194,52,66,NULL,'101'),(195,52,67,'B','Queue'),(236,53,63,'A','Stack'),(237,53,64,'A','TRUE'),(238,53,65,NULL,'sdf'),(239,53,66,NULL,'101'),(240,53,67,'B','Queue'),(541,54,68,'A','Stack'),(542,54,69,'A','TRUE'),(543,54,70,NULL,'Central Processing Unit'),(544,54,71,NULL,'101'),(545,54,72,'B','Queue'),(546,55,68,'A','Stack'),(547,55,69,'A','TRUE'),(548,55,70,NULL,'sdssdfrs'),(549,55,71,NULL,'121'),(550,55,72,'B','Queue'),(551,56,68,'A','Stack'),(552,56,69,'A','TRUE'),(553,56,70,NULL,'dfgh'),(554,56,72,'C','Linked List'),(555,57,73,'A','Stack'),(556,57,77,'B','Queue'),(557,57,76,NULL,'101'),(558,58,75,NULL,'sdfghjk'),(559,58,76,NULL,'101'),(560,58,73,'A','Stack'),(561,58,77,'B','Queue'),(562,59,73,'A','Stack'),(563,59,76,NULL,'468'),(564,59,75,NULL,'dfghjkl'),(565,60,75,NULL,'xcv'),(566,60,77,'B','Queue'),(567,60,74,'B','FALSE'),(568,60,73,'A','Stack'),(569,60,76,NULL,'101'),(570,61,77,'A','Stack'),(571,61,75,NULL,'central processing unit'),(572,61,73,'A','Stack'),(573,61,74,'A','TRUE'),(574,62,74,'A','TRUE'),(575,62,77,'A','Stack'),(576,62,75,NULL,'dfjinfu'),(577,62,76,NULL,'101'),(578,62,73,'B','Queue'),(579,63,80,NULL,'dskcnds'),(580,63,81,NULL,'101'),(581,63,79,'A','TRUE'),(582,63,78,'B','Queue'),(583,63,82,'A','Stack'),(584,64,78,'A','Stack'),(585,64,81,NULL,'101'),(586,64,80,NULL,'fghj'),(587,64,79,'A','TRUE'),(588,64,82,'B','Queue'),(589,65,84,'A','TRUE'),(590,65,83,'A','Stack'),(591,65,85,NULL,'Central Processing Unit'),(592,65,87,'B','Queue'),(593,65,86,NULL,'101'),(594,66,85,NULL,'sdfg'),(595,66,83,'B','Queue'),(596,66,86,NULL,'101'),(597,66,87,'B','Queue'),(598,66,84,'A','TRUE'),(599,67,85,NULL,'wdgf');

-- ============================================================
-- 17. auto_grading  (depends on applicant_attempt)
-- ============================================================
DROP TABLE IF EXISTS `auto_grading`;
CREATE TABLE `auto_grading` (
  `Grading_Id`  int          NOT NULL AUTO_INCREMENT,
  `Attempt_Id`  int          NOT NULL,
  `Total_Score` decimal(5,2) NOT NULL,
  `Status`      enum('Pass','Fail','Restricted') DEFAULT NULL,
  `Evaluated_At` timestamp   NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Grading_Id`),
  KEY `Attempt_Id` (`Attempt_Id`),
  CONSTRAINT `auto_grading_ibfk_1` FOREIGN KEY (`Attempt_Id`) REFERENCES `applicant_attempt` (`Attempt_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `auto_grading` VALUES
  (1,1,5.00,'Pass','2026-02-25 06:12:53'),(2,2,3.00,'Pass','2026-02-25 06:16:57'),
  (3,3,3.00,'Pass','2026-02-25 06:18:22'),(4,4,2.00,'Pass','2026-02-25 06:19:09'),
  (5,5,2.00,'Pass','2026-02-25 06:20:50'),(6,6,0.00,'Restricted','2026-02-25 06:21:47'),
  (7,7,4.00,'Pass','2026-02-25 07:35:44'),(8,8,3.00,'Pass','2026-02-25 07:36:30'),
  (9,9,4.00,'Pass','2026-02-25 07:37:45'),(10,10,4.00,'Pass','2026-02-25 07:58:44'),
  (11,11,3.00,'Pass','2026-02-25 08:11:27'),(12,12,1.00,'Fail','2026-02-25 08:12:44'),
  (13,13,3.00,'Pass','2026-02-25 08:38:18'),(14,14,4.00,'Pass','2026-02-25 08:47:24'),
  (15,15,0.00,'Restricted','2026-02-25 08:49:44'),(16,16,4.00,'Pass','2026-02-26 06:28:07'),
  (17,17,2.00,'Pass','2026-02-26 06:29:53'),(18,18,2.00,'Pass','2026-02-26 06:43:43'),
  (19,19,2.00,'Pass','2026-02-26 06:49:09'),(20,20,2.00,'Pass','2026-02-26 06:50:42'),
  (21,21,1.00,'Fail','2026-02-26 09:07:24'),(25,25,5.00,'Pass','2026-02-27 05:36:15'),
  (26,26,0.00,'Restricted','2026-02-27 05:37:07'),(27,27,0.00,'Restricted','2026-02-27 05:39:06'),
  (28,29,0.00,'Restricted','2026-02-27 06:23:07'),(29,30,0.00,'Restricted','2026-02-27 06:26:10'),
  (30,31,0.00,'Restricted','2026-02-27 08:12:40'),(31,32,4.00,'Pass','2026-02-27 08:14:16'),
  (32,33,0.00,'Restricted','2026-02-27 08:15:08'),(33,35,5.00,'Pass','2026-03-05 10:22:23'),
  (34,36,3.00,'Pass','2026-03-05 10:23:33'),(35,37,2.00,'Pass','2026-03-05 10:24:45'),
  (36,38,3.00,'Pass','2026-03-05 10:25:59'),(37,39,3.00,'Pass','2026-03-05 10:26:58'),
  (38,40,0.00,'Restricted','2026-03-05 10:27:43'),(39,41,4.00,'Pass','2026-03-05 10:42:06'),
  (40,42,0.00,'Restricted','2026-03-05 10:42:42'),(41,43,5.00,'Pass','2026-03-06 06:20:26'),
  (42,44,0.00,'Restricted','2026-03-06 06:21:19'),(43,45,0.00,'Restricted','2026-03-06 06:23:02'),
  (44,46,3.00,'Pass','2026-03-06 06:27:10'),(45,47,3.00,'Pass','2026-03-06 06:48:40'),
  (46,48,3.00,'Pass','2026-03-06 06:56:19'),(47,49,4.00,'Pass','2026-03-06 06:58:32'),
  (48,50,0.00,'Restricted','2026-03-06 07:02:12'),(49,51,4.00,'Pass','2026-03-06 07:03:16'),
  (50,52,4.00,'Pass','2026-03-06 07:55:50'),(59,53,4.00,'Pass','2026-03-06 08:02:51'),
  (120,54,5.00,'Pass','2026-03-06 08:41:26'),(121,55,3.00,'Pass','2026-03-06 08:43:10'),
  (122,56,2.00,'Pass','2026-03-06 08:46:59'),(123,57,0.00,'Restricted','2026-03-09 06:01:23'),
  (124,58,0.00,'Restricted','2026-03-09 06:02:22'),(125,59,0.00,'Restricted','2026-03-09 06:04:04'),
  (126,60,3.00,'Pass','2026-03-09 06:05:57'),(127,61,3.00,'Pass','2026-03-09 06:11:54'),
  (128,62,2.00,'Pass','2026-03-09 06:16:51'),(129,63,2.00,'Pass','2026-03-11 05:35:13'),
  (130,64,4.00,'Pass','2026-03-11 05:36:37'),(131,65,5.00,'Pass','2026-03-16 06:26:02'),
  (132,66,3.00,'Pass','2026-03-16 06:27:06'),(133,67,0.00,'Restricted','2026-03-16 06:27:59');

-- ============================================================
-- 18. restricted_attempts  (depends on applicants, applicant_attempt, exam_paper)
-- ============================================================
DROP TABLE IF EXISTS `restricted_attempts`;
CREATE TABLE `restricted_attempts` (
  `Id`                   int      NOT NULL AUTO_INCREMENT,
  `Attempt_Id`           int      NOT NULL,
  `Applicant_Id`         int      NOT NULL,
  `Exam_Paper_Id`        int      NOT NULL,
  `Reason`               text     NOT NULL,
  `Restricted_Timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  KEY `Attempt_Id`    (`Attempt_Id`),
  KEY `Applicant_Id`  (`Applicant_Id`),
  KEY `Exam_Paper_Id` (`Exam_Paper_Id`),
  CONSTRAINT `fk_restricted_applicant`  FOREIGN KEY (`Applicant_Id`)  REFERENCES `applicants` (`Applicant_Id`) ON DELETE CASCADE,
  CONSTRAINT `fk_restricted_attempt`    FOREIGN KEY (`Attempt_Id`)    REFERENCES `applicant_attempt` (`Attempt_Id`) ON DELETE CASCADE,
  CONSTRAINT `fk_restricted_exam_paper` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `restricted_attempts` VALUES
  (1,6,64,5,'Window lost focus (Alt+Tab detected)','2026-02-25 11:51:46'),
  (2,15,74,5,'Window lost focus (Alt+Tab detected)','2026-02-25 14:19:43'),
  (6,26,3,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:07:06'),
  (7,27,54,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:09:05'),
  (8,29,63,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:53:07'),
  (9,30,65,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:56:10'),
  (10,31,64,7,'Window lost focus (5s exceeded)','2026-02-27 13:42:40'),
  (11,33,91,7,'Window lost focus (returned in time)','2026-02-27 13:45:07'),
  (12,40,65,9,'Window lost focus (returned in time)','2026-03-05 15:57:43'),
  (13,42,54,10,'Window lost focus (5s exceeded)','2026-03-05 16:12:41'),
  (14,44,54,11,'Window lost focus (5s exceeded)','2026-03-06 11:51:18'),
  (15,45,2,11,'Window lost focus (returned in time)','2026-03-06 11:53:01'),
  (16,50,94,11,'Window lost focus (5s exceeded)','2026-03-06 12:32:11'),
  (17,52,91,11,'Window lost focus (returned in time)','2026-03-06 13:25:50'),
  (18,53,73,11,'Window lost focus (5s exceeded)','2026-03-06 13:33:10'),
  (19,57,1,13,'Exited fullscreen mode (attempted to exit exam)','2026-03-09 11:31:22'),
  (20,58,54,13,'Exited fullscreen mode (attempted to exit exam)','2026-03-09 11:32:22'),
  (21,59,2,13,'Window lost focus (5s exceeded)','2026-03-09 11:34:03'),
  (22,67,2,15,'Window lost focus (returned in time)','2026-03-16 11:57:59');

-- ============================================================
-- 19. attempt_key_logs  (depends on applicant_attempt, applicants)
-- ============================================================
DROP TABLE IF EXISTS `attempt_key_logs`;
CREATE TABLE `attempt_key_logs` (
  `Log_Id`        int          NOT NULL AUTO_INCREMENT,
  `Attempt_Id`    int          NOT NULL,
  `Applicant_Id`  int          NOT NULL,
  `Event_Type`    enum('blocked','warning') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'blocked',
  `Key_Value`     varchar(50)  COLLATE utf8mb4_unicode_ci NOT NULL,
  `Ctrl_Key`      tinyint(1)   NOT NULL DEFAULT '0',
  `Shift_Key`     tinyint(1)   NOT NULL DEFAULT '0',
  `Alt_Key`       tinyint(1)   NOT NULL DEFAULT '0',
  `Meta_Key`      tinyint(1)   NOT NULL DEFAULT '0',
  `Log_Timestamp` datetime     NOT NULL,
  `Created_At`    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Log_Id`),
  KEY `idx_attempt`    (`Attempt_Id`),
  KEY `idx_applicant`  (`Applicant_Id`),
  KEY `idx_event_type` (`Event_Type`),
  KEY `idx_timestamp`  (`Log_Timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
-- (no data)

-- ============================================================
-- 19b. keystroke_logs  (depends on applicant_attempt, applicants, entrance_question_bank)
-- ============================================================
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
-- (no data)

-- ============================================================
-- 20. file_uploads  (no FK dependencies)
-- ============================================================
DROP TABLE IF EXISTS `file_uploads`;
CREATE TABLE `file_uploads` (
  `File_ID`     int          NOT NULL AUTO_INCREMENT,
  `Uploaded_By` varchar(100) DEFAULT NULL,
  `Role`        enum('Admin','Faculty') DEFAULT NULL,
  `File_Name`   varchar(255) DEFAULT NULL,
  `File_Path`   text,
  `Upload_Date` timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`File_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `file_uploads` VALUES
  (1,'kashaf.parkar@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-13 07:48:30'),
  (2,'shraddha.doshi@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-13 07:53:59'),
  (3,'shraddha.doshi@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 07:57:24'),
  (4,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 07:59:03'),
  (5,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 08:06:33'),
  (54,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-02-25 05:36:55'),
  (55,'kashaf.parkar@nuv.ac.in','Admin','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2026-02-27 05:34:20'),
  (62,'dhavalm@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-11 05:30:23'),
  (63,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-16 06:23:53');

-- ============================================================
-- 21. login_log  (no FK dependencies)
-- ============================================================
DROP TABLE IF EXISTS `login_log`;
CREATE TABLE `login_log` (
  `Log_ID`      int          NOT NULL AUTO_INCREMENT,
  `User_Email`  varchar(100) DEFAULT NULL,
  `User_Id`     int          DEFAULT NULL,
  `Role`        enum('Admin','Faculty','Student') DEFAULT NULL,
  `Login_Time`  timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  `Logout_Time` timestamp    NULL DEFAULT NULL,
  PRIMARY KEY (`Log_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=532 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `login_log` VALUES
  (1,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 07:41:36','2025-10-13 07:49:38'),
  (2,'shraddha.doshi@nuv.ac.in',NULL,'Faculty','2025-10-13 07:51:25','2025-10-13 07:58:36'),
  (3,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 07:58:44','2025-10-13 08:12:53'),
  (398,'zubeda@gmail.com',80,'Student','2026-02-25 08:11:08','2026-02-25 08:11:27'),
  (399,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-25 08:11:42','2026-02-25 08:12:10'),
  (526,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-16 06:21:27','2026-03-16 06:24:50'),
  (527,'kashaf786parkar@gmail.com',1,'Student','2026-03-16 06:24:55','2026-03-16 06:26:02'),
  (528,'ansarikaif23604@gmail.com',54,'Student','2026-03-16 06:26:19','2026-03-16 06:27:06'),
  (529,'izmashaikh7681@gmail.com',2,'Student','2026-03-16 06:27:29','2026-03-16 06:27:59'),
  (530,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-16 06:28:16','2026-03-16 06:32:27'),
  (531,'dhavalm@nuv.ac.in',1,'Admin','2026-03-16 06:32:33','2026-03-16 06:34:48');

-- ============================================================
-- 22. notification  (no FK dependencies)
-- ============================================================
DROP TABLE IF EXISTS `notification`;
CREATE TABLE `notification` (
  `Notification_ID` int          NOT NULL AUTO_INCREMENT,
  `Title`           varchar(255) DEFAULT NULL,
  `Message`         text,
  `Target_Role`     varchar(50)  DEFAULT NULL,
  `Created_At`      timestamp    NULL DEFAULT CURRENT_TIMESTAMP,
  `Exam_Id`         int          DEFAULT NULL,
  `Faculty_Email`   varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Notification_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `notification` VALUES
  (1,'Exam Reminder','Exam "Email Try" will start in 10 minutes.','Faculty','2026-01-29 06:39:07',NULL,NULL),
  (22,'Exam Reminder','Exam "Test 2" will start in 10 minutes.','Faculty','2026-02-23 05:45:29',21,'dhavalm@nuv.ac.in'),
  (26,'Exam Reminder','Exam "Testing" will start in 10 minutes.','Faculty','2026-02-25 05:36:55',24,'kashaf.parkar@nuv.ac.in'),
  (35,'Exam Reminder','Exam "Testing" will start in 10 minutes.','Faculty','2026-03-06 06:19:03',30,'kashaf.parkar@nuv.ac.in'),
  (39,'Exam Reminder','Exam "Testify" will start in 10 minutes.','Faculty','2026-03-16 06:24:09',34,'kashaf.parkar@nuv.ac.in'),
  (40,'Exam Reminder','Exam "Testify" will start in 10 minutes.','Faculty','2026-03-16 06:24:09',34,'kashaf.parkar@nuv.ac.in');

-- ============================================================
-- 23. exam_archived  (placeholder — not in original dump)
-- ============================================================
DROP TABLE IF EXISTS `exam_archived`;
CREATE TABLE `exam_archived` (
  `Archive_Id`  int  NOT NULL AUTO_INCREMENT,
  `Exam_Id`     int  DEFAULT NULL,
  `Archived_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Archive_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ============================================================
-- 24. Schema additions
-- ============================================================
ALTER TABLE entrance_exam ADD COLUMN is_archived TINYINT(1) DEFAULT 0;
UPDATE entrance_exam SET is_archived = 0 WHERE is_archived IS NULL;

-- Super Admin flag
ALTER TABLE mst_admin ADD COLUMN Is_Super_Admin TINYINT DEFAULT 0;
UPDATE mst_admin SET Is_Super_Admin = 1 WHERE Email IN (
  'kashaf.parkar@nuv.ac.in',
  'izma.shaikh@nuv.ac.in',
  'yasir.shaikh@nuv.ac.in'
);

-- Re-enable FK checks
SET FOREIGN_KEY_CHECKS = 1;