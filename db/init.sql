-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: entrance_database
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `applicant_answers`
--

DROP TABLE IF EXISTS `applicant_answers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant_answers` (
  `Answer_Id` int NOT NULL AUTO_INCREMENT,
  `Attempt_Id` int NOT NULL,
  `Question_Id` int NOT NULL,
  `Selected_Option_Id` varchar(255) DEFAULT NULL,
  `Answer_Text` text,
  PRIMARY KEY (`Answer_Id`),
  KEY `idx_applicant_answers_attempt` (`Attempt_Id`),
  KEY `idx_applicant_answers_question` (`Question_Id`),
  CONSTRAINT `applicant_answers_ibfk_1` FOREIGN KEY (`Attempt_Id`) REFERENCES `applicant_attempt` (`Attempt_Id`),
  CONSTRAINT `applicant_answers_ibfk_2` FOREIGN KEY (`Question_Id`) REFERENCES `entrance_question_bank` (`Question_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=600 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicant_answers`
--

LOCK TABLES `applicant_answers` WRITE;
/*!40000 ALTER TABLE `applicant_answers` DISABLE KEYS */;
INSERT INTO `applicant_answers` VALUES (1,1,33,'A','Stack'),(2,1,34,'A','TRUE'),(3,1,35,NULL,'Central Processing Unit'),(4,1,36,NULL,'101'),(5,1,37,'B','Queue'),(6,2,33,'A','Stack'),(7,2,34,'A','TRUE'),(8,2,35,NULL,'sdfghjkl;'),(9,2,36,NULL,'101'),(10,2,37,'C','Linked List'),(11,3,33,'A','Stack'),(12,3,34,'B','FALSE'),(13,3,35,NULL,'fghjkl.'),(14,3,36,NULL,'101'),(15,3,37,'B','Queue'),(16,4,33,'C','Linked List'),(17,4,34,'A','TRUE'),(18,4,35,NULL,'fghjkl'),(19,4,36,NULL,'454'),(20,4,37,'B','Queue'),(21,5,33,'A','Stack'),(22,5,34,'A','TRUE'),(23,5,35,NULL,'cpu'),(24,5,36,NULL,'414'),(25,5,37,'C','Linked List'),(26,7,33,'A','Stack'),(27,7,34,'A','TRUE'),(28,7,35,NULL,'Central Processing Unit'),(29,7,36,NULL,'101'),(30,7,37,'D','Tree'),(31,8,33,'B','Queue'),(32,8,34,'A','TRUE'),(33,8,35,NULL,'asdfghjk'),(34,8,36,NULL,'101'),(35,8,37,'B','Queue'),(36,9,33,'A','Stack'),(37,9,34,'A','TRUE'),(38,9,35,NULL,'sdfghjk'),(39,9,36,NULL,'101'),(40,9,37,'B','Queue'),(41,10,33,'A','Stack'),(42,10,34,'A','TRUE'),(43,10,35,NULL,'fghjkl'),(44,10,36,NULL,'101'),(45,10,37,'B','Queue'),(46,11,33,'B','Queue'),(47,11,34,'A','TRUE'),(48,11,35,NULL,'cpu'),(49,11,36,NULL,'101'),(50,11,37,'B','Queue'),(51,12,33,'B','Queue'),(52,12,34,'B','FALSE'),(53,12,35,NULL,'fghjkl'),(54,12,36,NULL,'1010'),(55,12,37,'B','Queue'),(56,13,33,'B','Queue'),(57,13,34,'A','TRUE'),(58,13,35,NULL,'asdf'),(59,13,36,NULL,'101'),(60,13,37,'B','Queue'),(61,14,33,'A','Stack'),(62,14,34,'A','TRUE'),(63,14,35,NULL,'central processing unit'),(64,14,36,NULL,'11111'),(65,14,37,'B','Queue'),(66,16,38,'A','300 GSM'),(67,16,39,'A','True'),(68,16,40,NULL,'Round and Brush'),(69,16,41,'C','Lighter Shades '),(70,16,42,NULL,'2:1'),(71,17,38,'A','300 GSM'),(72,17,39,'A','True'),(73,17,40,NULL,'xcfghjkl'),(74,18,38,'B','50 GSM'),(75,18,39,'A','True'),(76,18,40,NULL,'round'),(77,18,41,'C','Lighter Shades '),(78,18,42,NULL,'2:4'),(79,19,38,'C','100 GSM'),(80,19,39,'A','True'),(81,19,40,NULL,'flat'),(82,19,41,'C','Lighter Shades '),(83,19,42,NULL,'2:5'),(84,20,38,'B','50 GSM'),(85,20,39,'A','True'),(86,20,40,NULL,'asdfg'),(87,20,41,'C','Lighter Shades '),(88,20,42,NULL,'dfgh'),(89,21,38,'C','100 GSM'),(90,21,39,'A','True'),(91,21,40,NULL,'ok'),(92,21,41,'A','Dark Shades'),(93,21,42,NULL,'sdfgh'),(94,25,43,'A','Stack'),(95,25,44,'A','True'),(96,25,45,NULL,'Central Processing Unit'),(97,25,46,NULL,'101'),(98,25,47,'A','True'),(101,29,43,'A','Stack'),(102,29,44,'A','True'),(103,30,43,'B','Queue'),(104,30,44,'A','True'),(105,30,45,NULL,'central Processing unit'),(106,30,47,'A','True'),(107,31,43,'A','Stack'),(108,31,44,'A','True'),(109,32,43,'A','Stack'),(110,32,44,'A','True'),(111,32,45,NULL,'CPU'),(112,32,46,NULL,'101'),(113,32,47,'A','True'),(114,33,43,'A','Stack'),(115,35,53,'A','Stack'),(116,35,54,'A','TRUE'),(117,35,55,NULL,'Central Processing Unit'),(118,35,56,NULL,'101'),(119,35,57,'B','Queue'),(120,36,53,'A','Stack'),(121,36,54,'A','TRUE'),(122,36,55,NULL,'sdfghj'),(123,36,56,NULL,'2121'),(124,36,57,'B','Queue'),(125,37,53,'C','Linked List'),(126,37,54,'A','TRUE'),(127,37,55,NULL,'sdfv'),(128,37,56,NULL,'151'),(129,37,57,'B','Queue'),(130,38,53,'B','Queue'),(131,38,54,'A','TRUE'),(132,38,55,NULL,'cpu'),(133,38,56,NULL,'101'),(134,38,57,'B','Queue'),(135,39,53,'C','Linked List'),(136,39,54,'A','TRUE'),(137,39,55,NULL,'sdf'),(138,39,56,NULL,'101'),(139,39,57,'B','Queue'),(140,40,53,'C','Linked List'),(141,40,54,'A','TRUE'),(142,41,58,'A','Stack'),(143,41,59,'A','TRUE'),(144,41,60,NULL,'cpu'),(145,41,61,NULL,'101'),(146,41,62,'B','Queue'),(147,42,58,'A','Stack'),(148,42,59,'A','TRUE'),(149,43,63,'A','Stack'),(150,43,64,'A','TRUE'),(151,43,65,NULL,'Central Processing Unit'),(152,43,66,NULL,'101'),(153,43,67,'B','Queue'),(154,44,63,'C','Linked List'),(155,44,64,'B','FALSE'),(156,44,65,NULL,'asdfghj'),(157,44,66,NULL,'101'),(158,45,63,'B','Queue'),(159,45,64,'A','TRUE'),(160,45,65,NULL,'ghj'),(161,45,66,NULL,'101'),(162,46,63,'B','Queue'),(163,46,64,'A','TRUE'),(164,46,65,NULL,'cpu'),(165,46,66,NULL,'101'),(166,46,67,'B','Queue'),(167,47,63,'A','Stack'),(168,47,64,'A','TRUE'),(169,47,65,NULL,'fghjk'),(170,47,66,NULL,'ghjk'),(171,47,67,'B','Queue'),(172,48,63,'A','Stack'),(173,48,64,'A','TRUE'),(174,48,65,NULL,'sfs'),(175,48,66,NULL,'arg'),(176,48,67,'B','Queue'),(177,49,63,'A','Stack'),(178,49,64,'A','TRUE'),(179,49,65,NULL,'cpu'),(180,49,66,NULL,'101'),(181,49,67,'B','Queue'),(182,50,63,'A','Stack'),(183,50,64,'A','TRUE'),(184,50,65,NULL,'cpu'),(185,50,66,NULL,'101'),(186,51,63,'A','Stack'),(187,51,64,'A','TRUE'),(188,51,65,NULL,'fgh'),(189,51,66,NULL,'101'),(190,51,67,'B','Queue'),(191,52,63,'A','Stack'),(192,52,64,'A','TRUE'),(193,52,65,NULL,'cpu'),(194,52,66,NULL,'101'),(195,52,67,'B','Queue'),(196,52,63,'A','Stack'),(197,52,64,'A','TRUE'),(198,52,65,NULL,'cpu'),(199,52,66,NULL,'101'),(200,52,67,'B','Queue'),(201,52,63,'A','Stack'),(202,52,64,'A','TRUE'),(203,52,65,NULL,'cpu'),(204,52,66,NULL,'101'),(205,52,67,'B','Queue'),(206,52,63,'A','Stack'),(207,52,64,'A','TRUE'),(208,52,65,NULL,'cpu'),(209,52,66,NULL,'101'),(210,52,67,'B','Queue'),(211,52,63,'A','Stack'),(212,52,64,'A','TRUE'),(213,52,65,NULL,'cpu'),(214,52,66,NULL,'101'),(215,52,67,'B','Queue'),(216,52,63,'A','Stack'),(217,52,64,'A','TRUE'),(218,52,65,NULL,'cpu'),(219,52,66,NULL,'101'),(220,52,67,'B','Queue'),(221,52,63,'A','Stack'),(222,52,64,'A','TRUE'),(223,52,65,NULL,'cpu'),(224,52,66,NULL,'101'),(225,52,67,'B','Queue'),(226,52,63,'A','Stack'),(227,52,64,'A','TRUE'),(228,52,65,NULL,'cpu'),(229,52,66,NULL,'101'),(230,52,67,'B','Queue'),(231,52,63,'A','Stack'),(232,52,64,'A','TRUE'),(233,52,65,NULL,'cpu'),(234,52,66,NULL,'101'),(235,52,67,'B','Queue'),(236,53,63,'A','Stack'),(237,53,64,'A','TRUE'),(238,53,65,NULL,'sdf'),(239,53,66,NULL,'101'),(240,53,67,'B','Queue'),(241,53,63,'A','Stack'),(242,53,64,'A','TRUE'),(243,53,65,NULL,'sdf'),(244,53,66,NULL,'101'),(245,53,67,'B','Queue'),(246,53,63,'A','Stack'),(247,53,64,'A','TRUE'),(248,53,65,NULL,'sdf'),(249,53,66,NULL,'101'),(250,53,67,'B','Queue'),(251,53,63,'A','Stack'),(252,53,64,'A','TRUE'),(253,53,65,NULL,'sdf'),(254,53,66,NULL,'101'),(255,53,67,'B','Queue'),(256,53,63,'A','Stack'),(257,53,64,'A','TRUE'),(258,53,65,NULL,'sdf'),(259,53,66,NULL,'101'),(260,53,67,'B','Queue'),(261,53,63,'A','Stack'),(262,53,64,'A','TRUE'),(263,53,65,NULL,'sdf'),(264,53,66,NULL,'101'),(265,53,67,'B','Queue'),(266,53,63,'A','Stack'),(267,53,64,'A','TRUE'),(268,53,65,NULL,'sdf'),(269,53,66,NULL,'101'),(270,53,67,'B','Queue'),(271,53,63,'A','Stack'),(272,53,64,'A','TRUE'),(273,53,65,NULL,'sdf'),(274,53,66,NULL,'101'),(275,53,67,'B','Queue'),(276,53,63,'A','Stack'),(277,53,64,'A','TRUE'),(278,53,65,NULL,'sdf'),(279,53,66,NULL,'101'),(280,53,67,'B','Queue'),(281,53,63,'A','Stack'),(282,53,64,'A','TRUE'),(283,53,65,NULL,'sdf'),(284,53,66,NULL,'101'),(285,53,67,'B','Queue'),(286,53,63,'A','Stack'),(287,53,64,'A','TRUE'),(288,53,65,NULL,'sdf'),(289,53,66,NULL,'101'),(290,53,67,'B','Queue'),(291,53,63,'A','Stack'),(292,53,64,'A','TRUE'),(293,53,65,NULL,'sdf'),(294,53,66,NULL,'101'),(295,53,67,'B','Queue'),(296,53,63,'A','Stack'),(297,53,64,'A','TRUE'),(298,53,65,NULL,'sdf'),(299,53,66,NULL,'101'),(300,53,67,'B','Queue'),(301,53,63,'A','Stack'),(302,53,64,'A','TRUE'),(303,53,65,NULL,'sdf'),(304,53,66,NULL,'101'),(305,53,67,'B','Queue'),(306,53,63,'A','Stack'),(307,53,64,'A','TRUE'),(308,53,65,NULL,'sdf'),(309,53,66,NULL,'101'),(310,53,67,'B','Queue'),(311,53,63,'A','Stack'),(312,53,64,'A','TRUE'),(313,53,65,NULL,'sdf'),(314,53,66,NULL,'101'),(315,53,67,'B','Queue'),(316,53,63,'A','Stack'),(317,53,64,'A','TRUE'),(318,53,65,NULL,'sdf'),(319,53,66,NULL,'101'),(320,53,67,'B','Queue'),(321,53,63,'A','Stack'),(322,53,64,'A','TRUE'),(323,53,65,NULL,'sdf'),(324,53,66,NULL,'101'),(325,53,67,'B','Queue'),(326,53,63,'A','Stack'),(327,53,64,'A','TRUE'),(328,53,65,NULL,'sdf'),(329,53,66,NULL,'101'),(330,53,67,'B','Queue'),(331,53,63,'A','Stack'),(332,53,64,'A','TRUE'),(333,53,65,NULL,'sdf'),(334,53,66,NULL,'101'),(335,53,67,'B','Queue'),(336,53,63,'A','Stack'),(337,53,64,'A','TRUE'),(338,53,65,NULL,'sdf'),(339,53,66,NULL,'101'),(340,53,67,'B','Queue'),(341,53,63,'A','Stack'),(342,53,64,'A','TRUE'),(343,53,65,NULL,'sdf'),(344,53,66,NULL,'101'),(345,53,67,'B','Queue'),(346,53,63,'A','Stack'),(347,53,64,'A','TRUE'),(348,53,65,NULL,'sdf'),(349,53,66,NULL,'101'),(350,53,67,'B','Queue'),(351,53,63,'A','Stack'),(352,53,64,'A','TRUE'),(353,53,65,NULL,'sdf'),(354,53,66,NULL,'101'),(355,53,67,'B','Queue'),(356,53,63,'A','Stack'),(357,53,64,'A','TRUE'),(358,53,65,NULL,'sdf'),(359,53,66,NULL,'101'),(360,53,67,'B','Queue'),(361,53,63,'A','Stack'),(362,53,64,'A','TRUE'),(363,53,65,NULL,'sdf'),(364,53,66,NULL,'101'),(365,53,67,'B','Queue'),(366,53,63,'A','Stack'),(367,53,64,'A','TRUE'),(368,53,65,NULL,'sdf'),(369,53,66,NULL,'101'),(370,53,67,'B','Queue'),(371,53,63,'A','Stack'),(372,53,64,'A','TRUE'),(373,53,65,NULL,'sdf'),(374,53,66,NULL,'101'),(375,53,67,'B','Queue'),(376,53,63,'A','Stack'),(377,53,64,'A','TRUE'),(378,53,65,NULL,'sdf'),(379,53,66,NULL,'101'),(380,53,67,'B','Queue'),(381,53,63,'A','Stack'),(382,53,64,'A','TRUE'),(383,53,65,NULL,'sdf'),(384,53,66,NULL,'101'),(385,53,67,'B','Queue'),(386,53,63,'A','Stack'),(387,53,64,'A','TRUE'),(388,53,65,NULL,'sdf'),(389,53,66,NULL,'101'),(390,53,67,'B','Queue'),(391,53,63,'A','Stack'),(392,53,64,'A','TRUE'),(393,53,65,NULL,'sdf'),(394,53,66,NULL,'101'),(395,53,67,'B','Queue'),(396,53,63,'A','Stack'),(397,53,64,'A','TRUE'),(398,53,65,NULL,'sdf'),(399,53,66,NULL,'101'),(400,53,67,'B','Queue'),(401,53,63,'A','Stack'),(402,53,64,'A','TRUE'),(403,53,65,NULL,'sdf'),(404,53,66,NULL,'101'),(405,53,67,'B','Queue'),(406,53,63,'A','Stack'),(407,53,64,'A','TRUE'),(408,53,65,NULL,'sdf'),(409,53,66,NULL,'101'),(410,53,67,'B','Queue'),(411,53,63,'A','Stack'),(412,53,64,'A','TRUE'),(413,53,65,NULL,'sdf'),(414,53,66,NULL,'101'),(415,53,67,'B','Queue'),(416,53,63,'A','Stack'),(417,53,64,'A','TRUE'),(418,53,65,NULL,'sdf'),(419,53,66,NULL,'101'),(420,53,67,'B','Queue'),(421,53,63,'A','Stack'),(422,53,64,'A','TRUE'),(423,53,65,NULL,'sdf'),(424,53,66,NULL,'101'),(425,53,67,'B','Queue'),(426,53,63,'A','Stack'),(427,53,64,'A','TRUE'),(428,53,65,NULL,'sdf'),(429,53,66,NULL,'101'),(430,53,67,'B','Queue'),(431,53,63,'A','Stack'),(432,53,64,'A','TRUE'),(433,53,65,NULL,'sdf'),(434,53,66,NULL,'101'),(435,53,67,'B','Queue'),(436,53,63,'A','Stack'),(437,53,64,'A','TRUE'),(438,53,65,NULL,'sdf'),(439,53,66,NULL,'101'),(440,53,67,'B','Queue'),(441,53,63,'A','Stack'),(442,53,64,'A','TRUE'),(443,53,65,NULL,'sdf'),(444,53,66,NULL,'101'),(445,53,67,'B','Queue'),(446,53,63,'A','Stack'),(447,53,64,'A','TRUE'),(448,53,65,NULL,'sdf'),(449,53,66,NULL,'101'),(450,53,67,'B','Queue'),(451,53,63,'A','Stack'),(452,53,64,'A','TRUE'),(453,53,65,NULL,'sdf'),(454,53,66,NULL,'101'),(455,53,67,'B','Queue'),(456,53,63,'A','Stack'),(457,53,64,'A','TRUE'),(458,53,65,NULL,'sdf'),(459,53,66,NULL,'101'),(460,53,67,'B','Queue'),(461,53,63,'A','Stack'),(462,53,64,'A','TRUE'),(463,53,65,NULL,'sdf'),(464,53,66,NULL,'101'),(465,53,67,'B','Queue'),(466,53,63,'A','Stack'),(467,53,64,'A','TRUE'),(468,53,65,NULL,'sdf'),(469,53,66,NULL,'101'),(470,53,67,'B','Queue'),(471,53,63,'A','Stack'),(472,53,64,'A','TRUE'),(473,53,65,NULL,'sdf'),(474,53,66,NULL,'101'),(475,53,67,'B','Queue'),(476,53,63,'A','Stack'),(477,53,64,'A','TRUE'),(478,53,65,NULL,'sdf'),(479,53,66,NULL,'101'),(480,53,67,'B','Queue'),(481,53,63,'A','Stack'),(482,53,64,'A','TRUE'),(483,53,65,NULL,'sdf'),(484,53,66,NULL,'101'),(485,53,67,'B','Queue'),(486,53,63,'A','Stack'),(487,53,64,'A','TRUE'),(488,53,65,NULL,'sdf'),(489,53,66,NULL,'101'),(490,53,67,'B','Queue'),(491,53,63,'A','Stack'),(492,53,64,'A','TRUE'),(493,53,65,NULL,'sdf'),(494,53,66,NULL,'101'),(495,53,67,'B','Queue'),(496,53,63,'A','Stack'),(497,53,64,'A','TRUE'),(498,53,65,NULL,'sdf'),(499,53,66,NULL,'101'),(500,53,67,'B','Queue'),(501,53,63,'A','Stack'),(502,53,64,'A','TRUE'),(503,53,65,NULL,'sdf'),(504,53,66,NULL,'101'),(505,53,67,'B','Queue'),(506,53,63,'A','Stack'),(507,53,64,'A','TRUE'),(508,53,65,NULL,'sdf'),(509,53,66,NULL,'101'),(510,53,67,'B','Queue'),(511,53,63,'A','Stack'),(512,53,64,'A','TRUE'),(513,53,65,NULL,'sdf'),(514,53,66,NULL,'101'),(515,53,67,'B','Queue'),(516,53,63,'A','Stack'),(517,53,64,'A','TRUE'),(518,53,65,NULL,'sdf'),(519,53,66,NULL,'101'),(520,53,67,'B','Queue'),(521,53,63,'A','Stack'),(522,53,64,'A','TRUE'),(523,53,65,NULL,'sdf'),(524,53,66,NULL,'101'),(525,53,67,'B','Queue'),(526,53,63,'A','Stack'),(527,53,64,'A','TRUE'),(528,53,65,NULL,'sdf'),(529,53,66,NULL,'101'),(530,53,67,'B','Queue'),(531,53,63,'A','Stack'),(532,53,64,'A','TRUE'),(533,53,65,NULL,'sdf'),(534,53,66,NULL,'101'),(535,53,67,'B','Queue'),(536,53,63,'A','Stack'),(537,53,64,'A','TRUE'),(538,53,65,NULL,'sdf'),(539,53,66,NULL,'101'),(540,53,67,'B','Queue'),(541,54,68,'A','Stack'),(542,54,69,'A','TRUE'),(543,54,70,NULL,'Central Processing Unit'),(544,54,71,NULL,'101'),(545,54,72,'B','Queue'),(546,55,68,'A','Stack'),(547,55,69,'A','TRUE'),(548,55,70,NULL,'sdssdfrs'),(549,55,71,NULL,'121'),(550,55,72,'B','Queue'),(551,56,68,'A','Stack'),(552,56,69,'A','TRUE'),(553,56,70,NULL,'dfgh'),(554,56,72,'C','Linked List'),(555,57,73,'A','Stack'),(556,57,77,'B','Queue'),(557,57,76,NULL,'101'),(558,58,75,NULL,'sdfghjk'),(559,58,76,NULL,'101'),(560,58,73,'A','Stack'),(561,58,77,'B','Queue'),(562,59,73,'A','Stack'),(563,59,76,NULL,'468'),(564,59,75,NULL,'dfghjkl'),(565,60,75,NULL,'xcv'),(566,60,77,'B','Queue'),(567,60,74,'B','FALSE'),(568,60,73,'A','Stack'),(569,60,76,NULL,'101'),(570,61,77,'A','Stack'),(571,61,75,NULL,'central processing unit'),(572,61,73,'A','Stack'),(573,61,74,'A','TRUE'),(574,62,74,'A','TRUE'),(575,62,77,'A','Stack'),(576,62,75,NULL,'dfjinfu'),(577,62,76,NULL,'101'),(578,62,73,'B','Queue'),(579,63,80,NULL,'dskcnds'),(580,63,81,NULL,'101'),(581,63,79,'A','TRUE'),(582,63,78,'B','Queue'),(583,63,82,'A','Stack'),(584,64,78,'A','Stack'),(585,64,81,NULL,'101'),(586,64,80,NULL,'fghj'),(587,64,79,'A','TRUE'),(588,64,82,'B','Queue'),(589,65,84,'A','TRUE'),(590,65,83,'A','Stack'),(591,65,85,NULL,'Central Processing Unit'),(592,65,87,'B','Queue'),(593,65,86,NULL,'101'),(594,66,85,NULL,'sdfg'),(595,66,83,'B','Queue'),(596,66,86,NULL,'101'),(597,66,87,'B','Queue'),(598,66,84,'A','TRUE'),(599,67,85,NULL,'wdgf');
/*!40000 ALTER TABLE `applicant_answers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applicant_attempt`
--

DROP TABLE IF EXISTS `applicant_attempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant_attempt` (
  `Attempt_Id` int NOT NULL AUTO_INCREMENT,
  `Applicant_Id` int NOT NULL,
  `Student_Email` varchar(255) DEFAULT NULL,
  `Exam_Paper_Id` int NOT NULL,
  `Start_Time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `End_Time` datetime DEFAULT NULL,
  `Status` enum('In Progress','Submitted','Timed Out','Restricted') NOT NULL,
  `Marks_Obtained` decimal(5,2) DEFAULT '0.00',
  PRIMARY KEY (`Attempt_Id`),
  KEY `Applicant_Id` (`Applicant_Id`),
  KEY `Exam_Paper_Id` (`Exam_Paper_Id`),
  CONSTRAINT `applicant_attempt_ibfk_1` FOREIGN KEY (`Applicant_Id`) REFERENCES `applicants` (`Applicant_Id`),
  CONSTRAINT `applicant_attempt_ibfk_2` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicant_attempt`
--

LOCK TABLES `applicant_attempt` WRITE;
/*!40000 ALTER TABLE `applicant_attempt` DISABLE KEYS */;
INSERT INTO `applicant_attempt` VALUES (1,1,'kashaf786parkar@gmail.com',5,'2026-02-25 11:42:19','2026-02-25 11:42:53','Submitted',5.00),(2,3,'yasirazimshaikh5440@gmail.com',5,'2026-02-25 11:46:36','2026-02-25 11:46:57','Submitted',3.00),(3,2,'izmashaikh7681@gmail.com',5,'2026-02-25 11:47:56','2026-02-25 11:48:22','Submitted',3.00),(4,65,'sneha.gupta@example.com',5,'2026-02-25 11:48:58','2026-02-25 11:49:09','Submitted',2.00),(5,63,'kavya.nair@example.com',5,'2026-02-25 11:50:36','2026-02-25 11:50:50','Submitted',2.00),(6,64,'aditya.mehta@example.com',5,'2026-02-25 11:51:24','2026-02-25 11:51:47','Restricted',0.00),(7,82,'aiza123tambe@nuv.ac.in',5,'2026-02-25 13:05:23','2026-02-25 13:05:44','Submitted',4.00),(8,91,'alfiya@gmail.com',5,'2026-02-25 13:06:15','2026-02-25 13:06:30','Submitted',3.00),(9,92,'zoya@gmailcom',5,'2026-02-25 13:07:06','2026-02-25 13:07:45','Submitted',4.00),(10,73,'alisha.tambe15@gmail.com',5,'2026-02-25 13:27:56','2026-02-25 13:28:44','Submitted',4.00),(11,80,'zubeda@gmail.com',5,'2026-02-25 13:41:12','2026-02-25 13:41:27','Submitted',3.00),(12,79,'anjali@gmail.com',5,'2026-02-25 13:42:32','2026-02-25 13:42:44','Submitted',1.00),(13,78,'vasudha@gmail.com',5,'2026-02-25 14:08:05','2026-02-25 14:08:18','Submitted',3.00),(14,95,'shafak@gmail.com',5,'2026-02-25 14:17:01','2026-02-25 14:17:24','Submitted',4.00),(15,74,'aiza123@nuv.ac.in',5,'2026-02-25 14:19:34','2026-02-25 14:19:44','Restricted',0.00),(16,1,'kashaf786parkar@gmail.com',6,'2026-02-26 11:57:23','2026-02-26 11:58:07','Submitted',4.00),(17,3,'yasirazimshaikh5440@gmail.com',6,'2026-02-26 11:59:22','2026-02-26 11:59:53','Submitted',2.00),(18,2,'izmashaikh7681@gmail.com',6,'2026-02-26 12:12:09','2026-02-26 12:13:43','Submitted',2.00),(19,63,'kavya.nair@example.com',6,'2026-02-26 12:18:03','2026-02-26 12:19:09','Submitted',2.00),(20,65,'sneha.gupta@example.com',6,'2026-02-26 12:19:49','2026-02-26 12:20:42','Submitted',2.00),(21,64,'aditya.mehta@example.com',6,'2026-02-26 14:36:59','2026-02-26 14:37:24','Submitted',1.00),(22,82,'aiza123tambe@nuv.ac.in',6,'2026-02-26 15:39:18',NULL,'In Progress',0.00),(23,91,'alfiya@gmail.com',6,'2026-02-26 15:50:36',NULL,'In Progress',0.00),(24,92,'zoya@gmailcom',6,'2026-02-26 16:01:02',NULL,'In Progress',0.00),(25,1,'kashaf786parkar@gmail.com',7,'2026-02-27 11:05:46','2026-02-27 11:06:15','Submitted',5.00),(26,3,'yasirazimshaikh5440@gmail.com',7,'2026-02-27 11:06:48','2026-02-27 11:07:07','Restricted',0.00),(27,54,'ansarikaif23604@gmail.com',7,'2026-02-27 11:08:34','2026-02-27 11:09:06','Restricted',0.00),(28,2,'izmashaikh7681@gmail.com',7,'2026-02-27 11:42:53',NULL,'In Progress',0.00),(29,63,'kavya.nair@example.com',7,'2026-02-27 11:52:34','2026-02-27 11:53:07','Restricted',0.00),(30,65,'sneha.gupta@example.com',7,'2026-02-27 11:55:32','2026-02-27 11:56:10','Restricted',0.00),(31,64,'aditya.mehta@example.com',7,'2026-02-27 13:42:14','2026-02-27 13:42:40','Restricted',0.00),(32,82,'aiza123tambe@nuv.ac.in',7,'2026-02-27 13:43:31','2026-02-27 13:44:16','Submitted',4.00),(33,91,'alfiya@gmail.com',7,'2026-02-27 13:44:55','2026-02-27 13:45:08','Restricted',0.00),(34,1,'kashaf786parkar@gmail.com',8,'2026-03-02 14:42:57',NULL,'In Progress',0.00),(35,1,'kashaf786parkar@gmail.com',9,'2026-03-05 15:51:56','2026-03-05 15:52:23','Submitted',5.00),(36,3,'yasirazimshaikh5440@gmail.com',9,'2026-03-05 15:52:56','2026-03-05 15:53:33','Submitted',3.00),(37,54,'ansarikaif23604@gmail.com',9,'2026-03-05 15:53:59','2026-03-05 15:54:45','Submitted',2.00),(38,2,'izmashaikh7681@gmail.com',9,'2026-03-05 15:55:43','2026-03-05 15:55:59','Submitted',3.00),(39,64,'aditya.mehta@example.com',9,'2026-03-05 15:56:33','2026-03-05 15:56:58','Submitted',3.00),(40,65,'sneha.gupta@example.com',9,'2026-03-05 15:57:30','2026-03-05 15:57:43','Restricted',0.00),(41,1,'kashaf786parkar@gmail.com',10,'2026-03-05 16:11:34','2026-03-05 16:12:06','Submitted',4.00),(42,54,'ansarikaif23604@gmail.com',10,'2026-03-05 16:12:28','2026-03-05 16:12:42','Restricted',0.00),(43,1,'kashaf786parkar@gmail.com',11,'2026-03-06 11:50:07','2026-03-06 11:50:26','Submitted',5.00),(44,54,'ansarikaif23604@gmail.com',11,'2026-03-06 11:50:51','2026-03-06 11:51:19','Restricted',0.00),(45,2,'izmashaikh7681@gmail.com',11,'2026-03-06 11:52:00','2026-03-06 11:53:02','Restricted',0.00),(46,65,'sneha.gupta@example.com',11,'2026-03-06 11:56:37','2026-03-06 11:57:10','Submitted',3.00),(47,64,'aditya.mehta@example.com',11,'2026-03-06 12:18:18','2026-03-06 12:18:40','Submitted',3.00),(48,63,'kavya.nair@example.com',11,'2026-03-06 12:26:06','2026-03-06 12:26:19','Submitted',3.00),(49,82,'aiza123tambe@nuv.ac.in',11,'2026-03-06 12:28:19','2026-03-06 12:28:32','Submitted',4.00),(50,94,'zoii@gmail.com',11,'2026-03-06 12:30:30','2026-03-06 12:32:12','Restricted',0.00),(51,92,'zoya@gmailcom',11,'2026-03-06 12:33:04','2026-03-06 12:33:16','Submitted',4.00),(52,91,'alfiya@gmail.com',11,'2026-03-06 13:25:07','2026-03-06 13:25:56','Submitted',4.00),(53,73,'alisha.tambe15@gmail.com',11,'2026-03-06 13:32:18','2026-03-06 13:33:15','Submitted',4.00),(54,1,'kashaf786parkar@gmail.com',12,'2026-03-06 14:10:46','2026-03-06 14:11:26','Submitted',5.00),(55,54,'ansarikaif23604@gmail.com',12,'2026-03-06 14:12:24','2026-03-06 14:13:10','Submitted',3.00),(56,2,'izmashaikh7681@gmail.com',12,'2026-03-06 14:16:21','2026-03-06 14:16:59','Submitted',2.00),(57,1,'kashaf786parkar@gmail.com',13,'2026-03-09 11:30:20','2026-03-09 11:31:23','Restricted',0.00),(58,54,'ansarikaif23604@gmail.com',13,'2026-03-09 11:31:55','2026-03-09 11:32:22','Restricted',0.00),(59,2,'izmashaikh7681@gmail.com',13,'2026-03-09 11:33:41','2026-03-09 11:34:04','Restricted',0.00),(60,63,'kavya.nair@example.com',13,'2026-03-09 11:35:26','2026-03-09 11:35:57','Submitted',3.00),(61,64,'aditya.mehta@example.com',13,'2026-03-09 11:36:53','2026-03-09 11:41:54','Submitted',3.00),(62,65,'sneha.gupta@example.com',13,'2026-03-09 11:46:09','2026-03-09 11:46:51','Submitted',2.00),(63,1,'kashaf786parkar@gmail.com',14,'2026-03-11 11:04:41','2026-03-11 11:05:13','Submitted',2.00),(64,54,'ansarikaif23604@gmail.com',14,'2026-03-11 11:05:52','2026-03-11 11:06:37','Submitted',4.00),(65,1,'kashaf786parkar@gmail.com',15,'2026-03-16 11:55:09','2026-03-16 11:56:02','Submitted',5.00),(66,54,'ansarikaif23604@gmail.com',15,'2026-03-16 11:56:30','2026-03-16 11:57:06','Submitted',3.00),(67,2,'izmashaikh7681@gmail.com',15,'2026-03-16 11:57:36','2026-03-16 11:57:59','Restricted',0.00);
/*!40000 ALTER TABLE `applicant_attempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applicant_exam_assign`
--

DROP TABLE IF EXISTS `applicant_exam_assign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant_exam_assign` (
  `Assign_Id` int NOT NULL AUTO_INCREMENT,
  `Applicant_Id` int NOT NULL,
  `Exam_Id` int NOT NULL,
  `Assigned_On` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Assign_Id`),
  UNIQUE KEY `uniq_applicant_exam` (`Applicant_Id`,`Exam_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `applicant_exam_assign_ibfk_1` FOREIGN KEY (`Applicant_Id`) REFERENCES `applicants` (`Applicant_Id`),
  CONSTRAINT `applicant_exam_assign_ibfk_2` FOREIGN KEY (`Exam_Id`) REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=130 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicant_exam_assign`
--

LOCK TABLES `applicant_exam_assign` WRITE;
/*!40000 ALTER TABLE `applicant_exam_assign` DISABLE KEYS */;
INSERT INTO `applicant_exam_assign` VALUES (1,66,2,'2026-01-27 10:21:50'),(7,73,7,'2026-01-29 06:08:26'),(8,74,7,'2026-01-29 06:08:26'),(9,78,7,'2026-01-29 06:08:26'),(10,79,7,'2026-01-29 06:08:26'),(11,80,7,'2026-01-29 06:08:26'),(12,82,9,'2026-01-29 06:41:08'),(13,82,10,'2026-01-29 06:42:41'),(14,82,11,'2026-01-30 05:17:49'),(15,91,11,'2026-01-30 05:17:49'),(16,92,11,'2026-01-30 05:17:49'),(21,2,21,'2026-02-23 05:45:25'),(22,1,21,'2026-02-23 05:45:25'),(23,3,21,'2026-02-23 05:45:25'),(24,64,23,'2026-02-24 09:54:04'),(25,2,23,'2026-02-24 09:54:04'),(26,54,23,'2026-02-24 09:54:04'),(27,1,23,'2026-02-24 09:54:04'),(28,65,23,'2026-02-24 09:54:04'),(29,3,23,'2026-02-24 09:54:04'),(30,64,24,'2026-02-25 05:36:40'),(31,2,24,'2026-02-25 05:36:40'),(32,1,24,'2026-02-25 05:36:40'),(33,63,24,'2026-02-25 05:36:40'),(34,65,24,'2026-02-25 05:36:40'),(35,3,24,'2026-02-25 05:36:40'),(36,82,24,'2026-02-25 07:32:23'),(37,91,24,'2026-02-25 07:32:23'),(38,92,24,'2026-02-25 07:32:23'),(39,74,24,'2026-02-25 07:57:02'),(40,73,24,'2026-02-25 07:57:02'),(41,79,24,'2026-02-25 07:57:02'),(42,95,24,'2026-02-25 07:57:02'),(43,78,24,'2026-02-25 07:57:02'),(44,80,24,'2026-02-25 07:57:02'),(45,64,25,'2026-02-26 06:21:04'),(46,2,25,'2026-02-26 06:21:04'),(47,1,25,'2026-02-26 06:21:04'),(48,63,25,'2026-02-26 06:21:04'),(49,65,25,'2026-02-26 06:21:04'),(50,3,25,'2026-02-26 06:21:04'),(51,82,25,'2026-02-26 06:21:04'),(52,91,25,'2026-02-26 06:21:04'),(53,92,25,'2026-02-26 06:21:04'),(54,64,26,'2026-02-27 05:33:55'),(55,2,26,'2026-02-27 05:33:55'),(56,1,26,'2026-02-27 05:33:55'),(57,63,26,'2026-02-27 05:33:55'),(58,65,26,'2026-02-27 05:33:55'),(59,3,26,'2026-02-27 05:33:55'),(60,54,26,'2026-02-27 05:34:05'),(61,82,26,'2026-02-27 08:11:39'),(62,91,26,'2026-02-27 08:11:39'),(63,92,26,'2026-02-27 08:11:39'),(64,64,27,'2026-03-02 09:04:42'),(65,2,27,'2026-03-02 09:04:42'),(66,54,27,'2026-03-02 09:04:42'),(67,1,27,'2026-03-02 09:04:42'),(68,63,27,'2026-03-02 09:04:42'),(69,65,27,'2026-03-02 09:04:42'),(70,3,27,'2026-03-02 09:04:42'),(71,64,28,'2026-03-05 10:19:23'),(72,2,28,'2026-03-05 10:19:23'),(73,54,28,'2026-03-05 10:19:23'),(74,1,28,'2026-03-05 10:19:23'),(75,63,28,'2026-03-05 10:19:23'),(76,65,28,'2026-03-05 10:19:23'),(77,3,28,'2026-03-05 10:19:23'),(78,64,29,'2026-03-05 10:39:18'),(79,2,29,'2026-03-05 10:39:18'),(80,54,29,'2026-03-05 10:39:18'),(81,1,29,'2026-03-05 10:39:18'),(82,63,29,'2026-03-05 10:39:18'),(83,65,29,'2026-03-05 10:39:18'),(84,3,29,'2026-03-05 10:39:18'),(85,64,30,'2026-03-06 06:18:34'),(86,2,30,'2026-03-06 06:18:34'),(87,54,30,'2026-03-06 06:18:34'),(88,1,30,'2026-03-06 06:18:34'),(89,63,30,'2026-03-06 06:18:34'),(90,65,30,'2026-03-06 06:18:34'),(91,3,30,'2026-03-06 06:18:34'),(92,82,30,'2026-03-06 06:57:55'),(93,91,30,'2026-03-06 06:57:55'),(94,94,30,'2026-03-06 06:57:55'),(95,92,30,'2026-03-06 06:57:55'),(96,74,30,'2026-03-06 08:01:42'),(97,73,30,'2026-03-06 08:01:42'),(98,79,30,'2026-03-06 08:01:42'),(99,95,30,'2026-03-06 08:01:42'),(100,78,30,'2026-03-06 08:01:42'),(101,80,30,'2026-03-06 08:01:42'),(102,64,31,'2026-03-06 08:39:55'),(103,2,31,'2026-03-06 08:39:55'),(104,54,31,'2026-03-06 08:39:55'),(105,1,31,'2026-03-06 08:39:55'),(106,63,31,'2026-03-06 08:39:55'),(107,65,31,'2026-03-06 08:39:55'),(108,3,31,'2026-03-06 08:39:55'),(109,64,32,'2026-03-09 05:58:31'),(110,2,32,'2026-03-09 05:58:31'),(111,54,32,'2026-03-09 05:58:31'),(112,1,32,'2026-03-09 05:58:31'),(113,63,32,'2026-03-09 05:58:31'),(114,65,32,'2026-03-09 05:58:31'),(115,3,32,'2026-03-09 05:58:31'),(116,64,33,'2026-03-11 05:30:06'),(117,2,33,'2026-03-11 05:30:06'),(118,54,33,'2026-03-11 05:30:06'),(119,1,33,'2026-03-11 05:30:06'),(120,63,33,'2026-03-11 05:30:06'),(121,65,33,'2026-03-11 05:30:06'),(122,3,33,'2026-03-11 05:30:06'),(123,64,34,'2026-03-16 06:23:38'),(124,2,34,'2026-03-16 06:23:38'),(125,54,34,'2026-03-16 06:23:38'),(126,1,34,'2026-03-16 06:23:38'),(127,63,34,'2026-03-16 06:23:38'),(128,65,34,'2026-03-16 06:23:38'),(129,3,34,'2026-03-16 06:23:38');
/*!40000 ALTER TABLE `applicant_exam_assign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applicant_groups`
--

DROP TABLE IF EXISTS `applicant_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicant_groups` (
  `Group_Id` int NOT NULL AUTO_INCREMENT,
  `Group_Name` varchar(100) DEFAULT NULL,
  `Faculty_Email` varchar(100) DEFAULT NULL,
  `Created_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Group_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicant_groups`
--

LOCK TABLES `applicant_groups` WRITE;
/*!40000 ALTER TABLE `applicant_groups` DISABLE KEYS */;
INSERT INTO `applicant_groups` VALUES (1,'BCA 1','dhavalm@nuv.ac.in','2026-01-22 09:49:18',1),(2,'BCA 2','dhavalm@nuv.ac.in','2026-01-22 09:53:09',0),(3,'BCA 3','dhavalm@nuv.ac.in','2026-01-22 10:45:14',0),(5,'__UNASSIGNED__','system@internal','2026-01-28 10:13:34',1),(6,'BCA Entrance','dhavalm@nuv.ac.in','2026-01-28 10:59:13',1),(8,'BCA','kashaf786parkar@gmail.com','2026-01-29 06:40:19',1),(12,'BCA Final','dhavalm@nuv.ac.in','2026-02-23 05:42:38',1);
/*!40000 ALTER TABLE `applicant_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `applicants`
--

DROP TABLE IF EXISTS `applicants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `applicants` (
  `Applicant_Id` int NOT NULL AUTO_INCREMENT,
  `Full_Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Phone` varchar(15) DEFAULT NULL,
  `DOB` date DEFAULT NULL,
  `Gender` enum('Male','Female','Other') DEFAULT NULL,
  `Address` text,
  `Registration_Date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `group_id` int DEFAULT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Applicant_Id`),
  UNIQUE KEY `Email` (`Email`),
  KEY `fk_applicant_group` (`group_id`),
  CONSTRAINT `fk_applicant_group` FOREIGN KEY (`group_id`) REFERENCES `applicant_groups` (`Group_Id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=99 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `applicants`
--

LOCK TABLES `applicants` WRITE;
/*!40000 ALTER TABLE `applicants` DISABLE KEYS */;
INSERT INTO `applicants` VALUES (1,'Kashaf Ahmed Parkar','kashaf786parkar@gmail.com','Kashaf@123','09967535850','2005-11-07','Female','Mumbai Maharashtra','2025-10-13 07:43:10',12,1),(2,'Izma Shaikh','izmashaikh7681@gmail.com','Izma@123','8160026252','2006-02-16','Female','Fatehgunj Vadodara','2025-10-13 07:53:21',12,1),(3,'Yasir Shaikh','yasirazimshaikh5440@gmail.com','Yasir@123','8799132161','2003-12-24','Male','Tandalja Vadodara','2025-10-13 07:55:56',12,1),(54,'Kaif Ansari','ansarikaif23604@gmail.com','Kaif@123','1232654585','2003-06-06','Male','Tandalja, Vadodara','2025-11-12 07:09:56',12,1),(63,'Kavya Nair','kavya.nair@example.com','kavya@123','9898123456',NULL,'Female','17 MG Road','2025-11-12 10:22:59',12,1),(64,'Aditya Mehta','aditya.mehta@example.com','aditya@2025','9988776655','2004-02-11','Male','8 Sunrise Colony','2025-11-12 10:22:59',12,1),(65,'Sneha Gupta','sneha.gupta@example.com','sneha@pwd','9090909090',NULL,'Female','12 Lotus Street','2025-11-12 10:22:59',12,1),(66,'Masira Parkar','masiii@nuv.ac.in','Masi@NUV','07845123265','2006-02-04','Female','Sakhrol Maharashtra','2026-01-22 09:52:26',1,1),(70,'Aay Khan','ayan@gmail.com','ayaan@123','9876543210','2002-05-14','Male','Ahmedabad, Gujarat','2026-01-27 10:48:45',1,0),(71,'Sar Sheikh','sar@gmail.com','sara@123','9123456789','2001-09-22','Female','Vadodara, Gujarat','2026-01-27 10:48:45',1,1),(72,'Zaidddd Patel','zaiddd@gmail.com','zaid@123','9988776655','2003-01-10','Male','Surat, Gujarat','2026-01-27 10:48:45',1,0),(73,'Alisha Tambe','alisha.tambe15@gmail.com','Alisha@123','09879865465','2019-11-15','Female','Karji Maharashtra','2026-01-28 11:00:14',6,1),(74,'Aiza Tambe','aiza123@nuv.ac.in','Aiza@123','07845123265','2020-01-07','Female','Karji Maharashtra','2026-01-29 05:57:03',6,1),(78,'Vasudha Deshpande','vasudha@gmail.com','Vasudha@123','9872243210','2005-12-30','Female','Mumbai, Maharashtra','2026-01-29 06:05:46',6,1),(79,'Anjali Patel','anjali@gmail.com','Anjali@123','9123477789','2001-09-20','Female','Vadodara, Gujarat','2026-01-29 06:05:46',6,1),(80,'Zubeda Tambe','zubeda@gmail.com','Zubeda@123','9988446655','2003-08-03','Female','Dongri, Maharashtra','2026-01-29 06:05:46',6,1),(82,'Aiza Tambe','aiza123tambe@nuv.ac.in','Aiza@123','07845123265','2020-01-07','Female','Karji Maharashtra','2026-01-29 06:40:51',8,1),(91,'Alfiya Tambe','alfiya@gmail.com','Alfiya@123','8754213265','2011-02-21','Female','Karji Maharashtra','2026-01-29 10:25:10',8,1),(92,'Zoya Tambe','zoya@gmailcom','Zoya@123','7845123569','2009-08-26','Female','Sharjah, Dubai','2026-01-29 10:26:18',8,1),(93,'Aaliya','aaliya@gmail.com','Aaliya@123','7856123491','2009-03-20','Female','Tandalja, Vadodara','2026-02-10 06:23:34',1,1),(94,'Zooiii','zoii@gmail.com','Zoii@123','9123265458','2009-09-26','Female','Tandalja, Vadodara','2026-02-10 06:29:01',8,1),(95,'Shafak Tambe','shafak@gmail.com','Shafak@123','9860348353','2008-10-15','Female','Karji Maharashtra','2026-02-10 06:36:22',6,1),(96,'Amrin Parkar','amrin@gmail.com','Amrin@123','1526485973','2009-08-07','Female','Karji Maharashtra','2026-02-10 06:37:27',1,1),(97,'Vanshika Salekar','vanshika@nuv.ac.in','Vanshika@123','7856124253','2004-11-06','Female','Gotri Vadodara','2026-02-10 09:27:30',1,1),(98,'Arshin Chauhan','arshin@nuv.ac.in','Arshin2123','8855221147','2005-03-23','Female','Tandalja, Vadodara','2026-02-10 09:36:49',1,1);
/*!40000 ALTER TABLE `applicants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attempt_key_logs`
--

DROP TABLE IF EXISTS `attempt_key_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attempt_key_logs` (
  `Log_Id` int NOT NULL AUTO_INCREMENT,
  `Attempt_Id` int NOT NULL,
  `Applicant_Id` int NOT NULL,
  `Event_Type` enum('blocked','warning') COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'blocked',
  `Key_Value` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `Ctrl_Key` tinyint(1) NOT NULL DEFAULT '0',
  `Shift_Key` tinyint(1) NOT NULL DEFAULT '0',
  `Alt_Key` tinyint(1) NOT NULL DEFAULT '0',
  `Meta_Key` tinyint(1) NOT NULL DEFAULT '0',
  `Log_Timestamp` datetime NOT NULL,
  `Created_At` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Log_Id`),
  KEY `idx_attempt` (`Attempt_Id`),
  KEY `idx_applicant` (`Applicant_Id`),
  KEY `idx_event_type` (`Event_Type`),
  KEY `idx_timestamp` (`Log_Timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attempt_key_logs`
--

LOCK TABLES `attempt_key_logs` WRITE;
/*!40000 ALTER TABLE `attempt_key_logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `attempt_key_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auto_grading`
--

DROP TABLE IF EXISTS `auto_grading`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auto_grading` (
  `Grading_Id` int NOT NULL AUTO_INCREMENT,
  `Attempt_Id` int NOT NULL,
  `Total_Score` decimal(5,2) NOT NULL,
  `Status` enum('Pass','Fail','Restricted') DEFAULT NULL,
  `Evaluated_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Grading_Id`),
  KEY `Attempt_Id` (`Attempt_Id`),
  CONSTRAINT `auto_grading_ibfk_1` FOREIGN KEY (`Attempt_Id`) REFERENCES `applicant_attempt` (`Attempt_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=134 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auto_grading`
--

LOCK TABLES `auto_grading` WRITE;
/*!40000 ALTER TABLE `auto_grading` DISABLE KEYS */;
INSERT INTO `auto_grading` VALUES (1,1,5.00,'Pass','2026-02-25 06:12:53'),(2,2,3.00,'Pass','2026-02-25 06:16:57'),(3,3,3.00,'Pass','2026-02-25 06:18:22'),(4,4,2.00,'Pass','2026-02-25 06:19:09'),(5,5,2.00,'Pass','2026-02-25 06:20:50'),(6,6,0.00,'Restricted','2026-02-25 06:21:47'),(7,7,4.00,'Pass','2026-02-25 07:35:44'),(8,8,3.00,'Pass','2026-02-25 07:36:30'),(9,9,4.00,'Pass','2026-02-25 07:37:45'),(10,10,4.00,'Pass','2026-02-25 07:58:44'),(11,11,3.00,'Pass','2026-02-25 08:11:27'),(12,12,1.00,'Fail','2026-02-25 08:12:44'),(13,13,3.00,'Pass','2026-02-25 08:38:18'),(14,14,4.00,'Pass','2026-02-25 08:47:24'),(15,15,0.00,'Restricted','2026-02-25 08:49:44'),(16,16,4.00,'Pass','2026-02-26 06:28:07'),(17,17,2.00,'Pass','2026-02-26 06:29:53'),(18,18,2.00,'Pass','2026-02-26 06:43:43'),(19,19,2.00,'Pass','2026-02-26 06:49:09'),(20,20,2.00,'Pass','2026-02-26 06:50:42'),(21,21,1.00,'Fail','2026-02-26 09:07:24'),(25,25,5.00,'Pass','2026-02-27 05:36:15'),(26,26,0.00,'Restricted','2026-02-27 05:37:07'),(27,27,0.00,'Restricted','2026-02-27 05:39:06'),(28,29,0.00,'Restricted','2026-02-27 06:23:07'),(29,30,0.00,'Restricted','2026-02-27 06:26:10'),(30,31,0.00,'Restricted','2026-02-27 08:12:40'),(31,32,4.00,'Pass','2026-02-27 08:14:16'),(32,33,0.00,'Restricted','2026-02-27 08:15:08'),(33,35,5.00,'Pass','2026-03-05 10:22:23'),(34,36,3.00,'Pass','2026-03-05 10:23:33'),(35,37,2.00,'Pass','2026-03-05 10:24:45'),(36,38,3.00,'Pass','2026-03-05 10:25:59'),(37,39,3.00,'Pass','2026-03-05 10:26:58'),(38,40,0.00,'Restricted','2026-03-05 10:27:43'),(39,41,4.00,'Pass','2026-03-05 10:42:06'),(40,42,0.00,'Restricted','2026-03-05 10:42:42'),(41,43,5.00,'Pass','2026-03-06 06:20:26'),(42,44,0.00,'Restricted','2026-03-06 06:21:19'),(43,45,0.00,'Restricted','2026-03-06 06:23:02'),(44,46,3.00,'Pass','2026-03-06 06:27:10'),(45,47,3.00,'Pass','2026-03-06 06:48:40'),(46,48,3.00,'Pass','2026-03-06 06:56:19'),(47,49,4.00,'Pass','2026-03-06 06:58:32'),(48,50,0.00,'Restricted','2026-03-06 07:02:12'),(49,51,4.00,'Pass','2026-03-06 07:03:16'),(50,52,4.00,'Pass','2026-03-06 07:55:50'),(51,52,4.00,'Pass','2026-03-06 07:55:50'),(52,52,0.00,'Restricted','2026-03-06 07:55:50'),(53,52,4.00,'Pass','2026-03-06 07:55:50'),(54,52,4.00,'Pass','2026-03-06 07:55:50'),(55,52,4.00,'Pass','2026-03-06 07:55:55'),(56,52,4.00,'Pass','2026-03-06 07:55:56'),(57,52,4.00,'Pass','2026-03-06 07:55:56'),(58,52,4.00,'Pass','2026-03-06 07:55:56'),(59,53,4.00,'Pass','2026-03-06 08:02:51'),(60,53,4.00,'Pass','2026-03-06 08:02:52'),(61,53,4.00,'Pass','2026-03-06 08:02:53'),(62,53,4.00,'Pass','2026-03-06 08:02:56'),(63,53,4.00,'Pass','2026-03-06 08:02:58'),(64,53,4.00,'Pass','2026-03-06 08:02:59'),(65,53,4.00,'Pass','2026-03-06 08:03:00'),(66,53,4.00,'Pass','2026-03-06 08:03:01'),(67,53,4.00,'Pass','2026-03-06 08:03:01'),(68,53,4.00,'Pass','2026-03-06 08:03:01'),(69,53,4.00,'Pass','2026-03-06 08:03:02'),(70,53,4.00,'Pass','2026-03-06 08:03:02'),(71,53,4.00,'Pass','2026-03-06 08:03:02'),(72,53,4.00,'Pass','2026-03-06 08:03:02'),(73,53,4.00,'Pass','2026-03-06 08:03:02'),(74,53,4.00,'Pass','2026-03-06 08:03:03'),(75,53,4.00,'Pass','2026-03-06 08:03:03'),(76,53,4.00,'Pass','2026-03-06 08:03:03'),(77,53,4.00,'Pass','2026-03-06 08:03:03'),(78,53,4.00,'Pass','2026-03-06 08:03:03'),(79,53,4.00,'Pass','2026-03-06 08:03:04'),(80,53,4.00,'Pass','2026-03-06 08:03:04'),(81,53,4.00,'Pass','2026-03-06 08:03:04'),(82,53,4.00,'Pass','2026-03-06 08:03:04'),(83,53,4.00,'Pass','2026-03-06 08:03:05'),(84,53,4.00,'Pass','2026-03-06 08:03:06'),(85,53,4.00,'Pass','2026-03-06 08:03:06'),(86,53,4.00,'Pass','2026-03-06 08:03:06'),(87,53,4.00,'Pass','2026-03-06 08:03:06'),(88,53,4.00,'Pass','2026-03-06 08:03:07'),(89,53,4.00,'Pass','2026-03-06 08:03:07'),(90,53,4.00,'Pass','2026-03-06 08:03:07'),(91,53,4.00,'Pass','2026-03-06 08:03:07'),(92,53,4.00,'Pass','2026-03-06 08:03:08'),(93,53,4.00,'Pass','2026-03-06 08:03:08'),(94,53,4.00,'Pass','2026-03-06 08:03:08'),(95,53,4.00,'Pass','2026-03-06 08:03:09'),(96,53,4.00,'Pass','2026-03-06 08:03:09'),(97,53,4.00,'Pass','2026-03-06 08:03:09'),(98,53,4.00,'Pass','2026-03-06 08:03:09'),(99,53,4.00,'Pass','2026-03-06 08:03:09'),(100,53,4.00,'Pass','2026-03-06 08:03:09'),(101,53,4.00,'Pass','2026-03-06 08:03:09'),(102,53,4.00,'Pass','2026-03-06 08:03:10'),(103,53,0.00,'Restricted','2026-03-06 08:03:10'),(104,53,4.00,'Pass','2026-03-06 08:03:11'),(105,53,4.00,'Pass','2026-03-06 08:03:11'),(106,53,4.00,'Pass','2026-03-06 08:03:11'),(107,53,4.00,'Pass','2026-03-06 08:03:12'),(108,53,4.00,'Pass','2026-03-06 08:03:13'),(109,53,4.00,'Pass','2026-03-06 08:03:13'),(110,53,4.00,'Pass','2026-03-06 08:03:13'),(111,53,4.00,'Pass','2026-03-06 08:03:13'),(112,53,4.00,'Pass','2026-03-06 08:03:13'),(113,53,4.00,'Pass','2026-03-06 08:03:13'),(114,53,4.00,'Pass','2026-03-06 08:03:14'),(115,53,4.00,'Pass','2026-03-06 08:03:14'),(116,53,4.00,'Pass','2026-03-06 08:03:14'),(117,53,4.00,'Pass','2026-03-06 08:03:15'),(118,53,4.00,'Pass','2026-03-06 08:03:15'),(119,53,4.00,'Pass','2026-03-06 08:03:15'),(120,54,5.00,'Pass','2026-03-06 08:41:26'),(121,55,3.00,'Pass','2026-03-06 08:43:10'),(122,56,2.00,'Pass','2026-03-06 08:46:59'),(123,57,0.00,'Restricted','2026-03-09 06:01:23'),(124,58,0.00,'Restricted','2026-03-09 06:02:22'),(125,59,0.00,'Restricted','2026-03-09 06:04:04'),(126,60,3.00,'Pass','2026-03-09 06:05:57'),(127,61,3.00,'Pass','2026-03-09 06:11:54'),(128,62,2.00,'Pass','2026-03-09 06:16:51'),(129,63,2.00,'Pass','2026-03-11 05:35:13'),(130,64,4.00,'Pass','2026-03-11 05:36:37'),(131,65,5.00,'Pass','2026-03-16 06:26:02'),(132,66,3.00,'Pass','2026-03-16 06:27:06'),(133,67,0.00,'Restricted','2026-03-16 06:27:59');
/*!40000 ALTER TABLE `auto_grading` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrance_exam`
--

DROP TABLE IF EXISTS `entrance_exam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrance_exam` (
  `Exam_Id` int NOT NULL AUTO_INCREMENT,
  `Exam_Name` varchar(100) NOT NULL,
  `Exam_Date` date NOT NULL,
  `Exam_Time` time NOT NULL,
  `Duration_Minutes` int NOT NULL,
  `Total_Questions` int NOT NULL,
  `Max_Marks` int NOT NULL,
  `Faculty_Email` varchar(255) DEFAULT NULL,
  `notify_10min` tinyint DEFAULT '0',
  `exam_status` enum('OFF','ON') DEFAULT 'OFF',
  `was_started` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrance_exam`
--

LOCK TABLES `entrance_exam` WRITE;
/*!40000 ALTER TABLE `entrance_exam` DISABLE KEYS */;
INSERT INTO `entrance_exam` VALUES (1,'Test','2026-01-27','11:50:00',10,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),(2,'Quiz','2026-01-27','16:15:00',2,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),(7,'Testing','2026-01-29','13:05:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(9,'Email Trial','2026-01-29','12:20:00',5,5,5,'kashaf786parkar@gmail.com',1,'OFF',0),(10,'Email Testing','2026-01-29','12:23:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(11,'Exam 1','2026-01-30','17:10:00',5,5,5,'kashaf.a.parkar@nuv.ac.in',1,'OFF',0),(15,'Entrance BCA','2026-02-02','11:35:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(17,'Test','2026-02-02','11:55:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(21,'Test 2','2026-02-23','11:45:00',5,5,5,'dhavalm@nuv.ac.in',1,'OFF',1),(22,'Quiz','2026-02-23','17:00:00',5,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),(23,'Review','2026-02-24','15:45:00',5,5,5,'dhavalm@nuv.ac.in',1,'OFF',1),(24,'Testing','2026-02-25','14:10:00',10,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(25,'Unique','2026-02-26','16:00:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(26,'Testing Restriction','2026-02-27','13:41:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(27,'Storage Check','2026-03-02','14:40:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(28,'Test','2026-03-05','15:50:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(29,'Testing','2026-03-05','16:10:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(30,'Testing','2026-03-06','13:32:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(31,'Quizzz','2026-03-06','14:10:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(32,'Testing','2026-03-09','11:40:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1),(33,'End Sem','2026-03-11','11:00:00',15,5,5,'dhavalm@nuv.ac.in',0,'OFF',1),(34,'Testify','2026-03-16','11:55:00',5,5,5,'kashaf.parkar@nuv.ac.in',1,'OFF',1);
/*!40000 ALTER TABLE `entrance_exam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entrance_question_bank`
--

DROP TABLE IF EXISTS `entrance_question_bank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `entrance_question_bank` (
  `Question_Id` int NOT NULL AUTO_INCREMENT,
  `Exam_Id` int NOT NULL,
  `Question_Type` enum('MCQ','Fill','TF','OneWord') NOT NULL,
  `Question_Text` text NOT NULL,
  `Option_A` varchar(255) DEFAULT NULL,
  `Option_B` varchar(255) DEFAULT NULL,
  `Option_C` varchar(255) DEFAULT NULL,
  `Option_D` varchar(255) DEFAULT NULL,
  `Correct_Answer` varchar(255) NOT NULL,
  `Marks` int DEFAULT '1',
  `Created_At` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Question_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `entrance_question_bank_ibfk_1` FOREIGN KEY (`Exam_Id`) REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=88 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entrance_question_bank`
--

LOCK TABLES `entrance_question_bank` WRITE;
/*!40000 ALTER TABLE `entrance_question_bank` DISABLE KEYS */;
INSERT INTO `entrance_question_bank` VALUES (1,2,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-27 15:52:10'),(2,2,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-27 15:52:10'),(3,2,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-27 15:52:10'),(4,2,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-27 15:52:10'),(5,2,'MCQ','Which is a programming language?','ABC','HTML','JAVA','OOPS','JAVA',1,'2026-01-27 15:53:12'),(6,7,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-29 11:40:12'),(7,7,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-29 11:40:12'),(8,7,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-29 11:40:12'),(9,7,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-29 11:40:12'),(10,7,'Fill','Full Form of ST is ','','','','','Software Testing',1,'2026-01-29 11:40:39'),(11,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 10:48:13'),(12,11,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-30 10:48:13'),(13,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 10:48:13'),(14,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 10:48:13'),(15,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 10:51:47'),(16,11,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-01-30 10:51:47'),(17,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 10:51:47'),(18,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 10:51:47'),(19,11,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-01-30 10:51:47'),(20,11,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-01-30 11:53:05'),(21,11,'TF','Java is a statically typed language','True','False','','','True',1,'2026-01-30 11:53:05'),(22,11,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-01-30 11:53:05'),(23,11,'OneWord','What is the binary of 5?','','','','','101',1,'2026-01-30 11:53:05'),(28,21,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-23 11:16:39'),(29,21,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-02-23 11:16:39'),(30,21,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-23 11:16:39'),(31,21,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-23 11:16:39'),(32,21,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-02-23 11:16:39'),(33,24,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-25 11:06:55'),(34,24,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-02-25 11:06:55'),(35,24,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-25 11:06:55'),(36,24,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-25 11:06:55'),(37,24,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-02-25 11:06:55'),(38,25,'MCQ','Correct GSM of Watercolour Paper','300 GSM','50 GSM','100 GSM','1000 GSM','300 GSM',1,'2026-02-26 11:51:51'),(39,25,'TF','Acrylic Paint is Different from Oil Paint.','True','False','','','True',1,'2026-02-26 11:52:46'),(40,25,'Fill','For One Stroke Painting _______ and _______ brush is used','','','','','Round and Flat',1,'2026-02-26 11:53:29'),(41,25,'MCQ','Colour Tone of Pastel is','Dark Shades','Normal Shades','Lighter Shades ','None of the above','Lighter Shades ',1,'2026-02-26 11:54:39'),(42,25,'OneWord','What is the ratio of Resin and Hardener?','','','','','2:1',1,'2026-02-26 11:56:12'),(43,26,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-02-27 11:04:20'),(44,26,'TF','Java is a statically typed language','True','False','','','True',1,'2026-02-27 11:04:20'),(45,26,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-02-27 11:04:20'),(46,26,'OneWord','What is the binary of 5?','','','','','101',1,'2026-02-27 11:04:20'),(47,26,'TF','HTML is used for frontend','True','False','','','True',1,'2026-02-27 11:05:07'),(48,27,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-02 14:34:59'),(49,27,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-02 14:34:59'),(50,27,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-02 14:34:59'),(51,27,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-02 14:34:59'),(52,27,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-02 14:34:59'),(53,28,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-05 15:49:37'),(54,28,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-05 15:49:37'),(55,28,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-05 15:49:37'),(56,28,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-05 15:49:37'),(57,28,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-05 15:49:37'),(58,29,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-05 16:09:31'),(59,29,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-05 16:09:31'),(60,29,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-05 16:09:31'),(61,29,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-05 16:09:31'),(62,29,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-05 16:09:31'),(63,30,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-06 11:48:48'),(64,30,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-06 11:48:48'),(65,30,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-06 11:48:48'),(66,30,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-06 11:48:48'),(67,30,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-06 11:48:48'),(68,31,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-06 14:10:11'),(69,31,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-06 14:10:11'),(70,31,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-06 14:10:11'),(71,31,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-06 14:10:11'),(72,31,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-06 14:10:11'),(73,32,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-09 11:28:50'),(74,32,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-09 11:28:50'),(75,32,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-09 11:28:50'),(76,32,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-09 11:28:50'),(77,32,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-09 11:28:50'),(78,33,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-11 11:00:23'),(79,33,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-11 11:00:23'),(80,33,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-11 11:00:23'),(81,33,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-11 11:00:23'),(82,33,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-11 11:00:23'),(83,34,'MCQ','Which data structure uses LIFO order?','Stack','Queue','Linked List','Tree','Stack',1,'2026-03-16 11:53:53'),(84,34,'TF','Java is a statically typed language','TRUE','FALSE','','','TRUE',1,'2026-03-16 11:53:53'),(85,34,'Fill','CPU stands for ______.','','','','','Central Processing Unit',1,'2026-03-16 11:53:53'),(86,34,'OneWord','What is the binary of 5?','','','','','101',1,'2026-03-16 11:53:53'),(87,34,'MCQ','Which data structure uses FIFO order?','Stack','Queue','Linked List','Tree','Queue',1,'2026-03-16 11:53:53');
/*!40000 ALTER TABLE `entrance_question_bank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_paper`
--

DROP TABLE IF EXISTS `exam_paper`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_paper` (
  `Exam_Paper_Id` int NOT NULL AUTO_INCREMENT,
  `Exam_Id` int NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Total_Marks` decimal(5,2) NOT NULL,
  `Duration_Minutes` int NOT NULL,
  `Created_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_saved` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`Exam_Paper_Id`),
  KEY `Exam_Id` (`Exam_Id`),
  CONSTRAINT `exam_paper_ibfk_1` FOREIGN KEY (`Exam_Id`) REFERENCES `entrance_exam` (`Exam_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_paper`
--

LOCK TABLES `exam_paper` WRITE;
/*!40000 ALTER TABLE `exam_paper` DISABLE KEYS */;
INSERT INTO `exam_paper` VALUES (1,2,'Quiz',5.00,2,'2026-01-27 10:22:15',0),(2,7,'Testing',5.00,5,'2026-01-29 06:11:08',0),(3,11,'Exam 1',5.00,5,'2026-01-30 09:54:59',0),(4,21,'Test 2',5.00,5,'2026-02-23 05:47:11',0),(5,24,'Testing',5.00,5,'2026-02-25 05:37:02',0),(6,25,'Unique',5.00,5,'2026-02-26 06:24:47',0),(7,26,'Testing Restriction',5.00,5,'2026-02-27 05:34:34',0),(8,27,'Storage Check',5.00,5,'2026-03-02 09:05:05',1),(9,28,'Test',5.00,5,'2026-03-05 10:19:43',1),(10,29,'Testing',5.00,5,'2026-03-05 10:39:37',1),(11,30,'Testing',5.00,5,'2026-03-06 06:18:53',1),(12,31,'Quizzz',5.00,5,'2026-03-06 08:40:17',1),(13,32,'Testing',5.00,5,'2026-03-09 05:58:59',1),(14,33,'End Sem',5.00,15,'2026-03-11 05:30:31',1),(15,34,'Testify',5.00,5,'2026-03-16 06:24:03',1);
/*!40000 ALTER TABLE `exam_paper` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_paper_questions`
--

DROP TABLE IF EXISTS `exam_paper_questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_paper_questions` (
  `Exam_Paper_Id` int NOT NULL,
  `Question_Id` int NOT NULL,
  PRIMARY KEY (`Exam_Paper_Id`,`Question_Id`),
  KEY `Question_Id` (`Question_Id`),
  CONSTRAINT `exam_paper_questions_ibfk_1` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`),
  CONSTRAINT `exam_paper_questions_ibfk_2` FOREIGN KEY (`Question_Id`) REFERENCES `entrance_question_bank` (`Question_Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_paper_questions`
--

LOCK TABLES `exam_paper_questions` WRITE;
/*!40000 ALTER TABLE `exam_paper_questions` DISABLE KEYS */;
INSERT INTO `exam_paper_questions` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(2,6),(2,7),(2,8),(2,9),(2,10),(3,12),(3,13),(3,14),(3,19),(3,20),(4,28),(4,29),(4,30),(4,31),(4,32),(5,33),(5,34),(5,35),(5,36),(5,37),(6,38),(6,39),(6,40),(6,41),(6,42),(7,43),(7,44),(7,45),(7,46),(7,47),(8,48),(8,49),(8,50),(8,51),(8,52),(9,53),(9,54),(9,55),(9,56),(9,57),(10,58),(10,59),(10,60),(10,61),(10,62),(11,63),(11,64),(11,65),(11,66),(11,67),(12,68),(12,69),(12,70),(12,71),(12,72),(13,73),(13,74),(13,75),(13,76),(13,77),(14,78),(14,79),(14,80),(14,81),(14,82),(15,83),(15,84),(15,85),(15,86),(15,87);
/*!40000 ALTER TABLE `exam_paper_questions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_group_assign`
--

DROP TABLE IF EXISTS `faculty_group_assign`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_group_assign` (
  `Assign_Id` int NOT NULL AUTO_INCREMENT,
  `Faculty_Id` int NOT NULL,
  `Group_Id` int NOT NULL,
  `Assigned_On` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Assign_Id`),
  UNIQUE KEY `uniq_faculty_group` (`Faculty_Id`,`Group_Id`),
  KEY `Group_Id` (`Group_Id`),
  CONSTRAINT `faculty_group_assign_ibfk_1` FOREIGN KEY (`Faculty_Id`) REFERENCES `mst_faculty` (`Faculty_Id`),
  CONSTRAINT `faculty_group_assign_ibfk_2` FOREIGN KEY (`Group_Id`) REFERENCES `faculty_groups` (`Group_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_group_assign`
--

LOCK TABLES `faculty_group_assign` WRITE;
/*!40000 ALTER TABLE `faculty_group_assign` DISABLE KEYS */;
INSERT INTO `faculty_group_assign` VALUES (1,2,1,'2026-01-28 11:24:05'),(2,1,1,'2026-01-28 11:24:09'),(6,3,1,'2026-01-28 11:24:23'),(7,5,1,'2026-01-29 05:56:02'),(8,33,1,'2026-01-29 05:56:04'),(9,4,1,'2026-01-29 05:56:06'),(10,8,2,'2026-01-29 06:06:34'),(16,10,1,'2026-01-29 07:17:35'),(17,9,1,'2026-01-29 07:18:51'),(18,14,1,'2026-01-29 07:20:47'),(26,7,2,'2026-02-06 06:44:47');
/*!40000 ALTER TABLE `faculty_group_assign` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty_groups`
--

DROP TABLE IF EXISTS `faculty_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty_groups` (
  `Group_Id` int NOT NULL AUTO_INCREMENT,
  `Group_Name` varchar(100) NOT NULL,
  `Created_On` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Group_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty_groups`
--

LOCK TABLES `faculty_groups` WRITE;
/*!40000 ALTER TABLE `faculty_groups` DISABLE KEYS */;
INSERT INTO `faculty_groups` VALUES (1,'BCA','2026-01-28 11:23:57',1),(2,'BBA','2026-01-29 06:06:27',1),(6,'MSc','2026-02-06 09:23:03',0);
/*!40000 ALTER TABLE `faculty_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `file_uploads`
--

DROP TABLE IF EXISTS `file_uploads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `file_uploads` (
  `File_ID` int NOT NULL AUTO_INCREMENT,
  `Uploaded_By` varchar(100) DEFAULT NULL,
  `Role` enum('Admin','Faculty') DEFAULT NULL,
  `File_Name` varchar(255) DEFAULT NULL,
  `File_Path` text,
  `Upload_Date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`File_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `file_uploads`
--

LOCK TABLES `file_uploads` WRITE;
/*!40000 ALTER TABLE `file_uploads` DISABLE KEYS */;
INSERT INTO `file_uploads` VALUES (1,'kashaf.parkar@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-13 07:48:30'),(2,'shraddha.doshi@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-13 07:53:59'),(3,'shraddha.doshi@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 07:57:24'),(4,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 07:59:03'),(5,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 08:06:33'),(6,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 10:28:52'),(7,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 10:30:37'),(8,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 10:36:38'),(9,'kashaf.parkar@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-10-13 10:38:56'),(10,'kashaf.parkar@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-10-13 10:40:50'),(11,'kashaf.parkar@nuv.ac.in','Faculty','Applicant_Upload.csv','uploads/students\\Applicant_Upload.csv','2025-10-13 10:56:19'),(12,'margie.patoliya@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-14 07:14:40'),(13,'margie.patoliya@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-10-14 07:16:57'),(14,'kashaf.parkar@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-10-14 07:17:54'),(15,'kashaf.parkar@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-10-16 05:03:57'),(16,'kashaf.parkar@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-10-16 05:12:42'),(17,'kashaf.parkar@nuv.ac.in','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2025-10-16 05:14:14'),(18,'margie.patoliya@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-10-16 05:39:13'),(19,'kashaf.parkar@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-10-16 08:23:15'),(20,'kashaf.parkar@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-16 08:30:44'),(21,'margie.patoliya@nuv.ac.in','Faculty','Questionbank.csv','uploads/question_banks\\Questionbank.csv','2025-10-20 09:51:40'),(22,'null','Faculty','Applicants_1.csv','uploads/students\\Applicants_1.csv','2025-10-25 11:58:40'),(23,'null','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-11 05:04:14'),(24,'null','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-11-11 05:14:11'),(25,'megha.patel@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-11-11 05:48:57'),(26,'megha.patel@nuv.ac.in','Faculty','Spring_questions.csv','uploads/question_banks\\Spring_questions.csv','2025-11-11 06:07:53'),(27,'megha.patel@nuv.ac.in','Faculty','Spring_questions.csv','uploads/question_banks\\Spring_questions.csv','2025-11-11 06:10:39'),(28,'megha.patel@nuv.ac.in','Faculty','Spring_questions.csv','uploads/question_banks\\Spring_questions.csv','2025-11-11 06:12:43'),(29,'megha.patel@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-11 06:22:04'),(30,'megha.patel@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-11-12 04:46:14'),(31,'null','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-12 06:29:55'),(32,'megha.patel@nuv.ac.in','Faculty','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2025-11-12 06:39:16'),(33,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-12 06:39:50'),(34,'megha.patel@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-12 06:44:32'),(35,'megha.patel@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-12 07:10:44'),(36,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-12 07:13:33'),(37,'megha.patel@nuv.ac.in','Faculty','Applicants.csv','uploads/students\\Applicants.csv','2025-11-12 10:22:59'),(38,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-12 10:24:29'),(39,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-25 11:38:10'),(40,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-26 09:11:18'),(41,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-27 17:52:23'),(42,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-28 04:44:55'),(43,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-28 04:48:02'),(44,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2025-11-28 06:20:23'),(45,'megha.patel@nuv.ac.in','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-01-16 05:13:24'),(46,'null','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-01-20 10:12:26'),(47,'null','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2026-01-27 10:22:10'),(48,'null','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2026-01-29 06:10:12'),(49,'null','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2026-01-30 05:18:13'),(50,'null','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-01-30 05:21:47'),(51,'null','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2026-01-30 06:23:05'),(52,'null','Faculty','sample_question_bank_1.csv','uploads/question_banks\\sample_question_bank_1.csv','2026-01-30 06:32:04'),(53,'null','Faculty','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-02-23 05:46:39'),(54,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-02-25 05:36:55'),(55,'kashaf.parkar@nuv.ac.in','Admin','sample_question_bank.csv','uploads/question_banks\\sample_question_bank.csv','2026-02-27 05:34:20'),(56,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-02 09:04:59'),(57,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-05 10:19:37'),(58,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-05 10:39:31'),(59,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-06 06:18:48'),(60,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-06 08:40:11'),(61,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-09 05:58:50'),(62,'dhavalm@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-11 05:30:23'),(63,'kashaf.parkar@nuv.ac.in','Admin','question_bank.csv','uploads/question_banks\\question_bank.csv','2026-03-16 06:23:53');
/*!40000 ALTER TABLE `file_uploads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_log`
--

DROP TABLE IF EXISTS `login_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_log` (
  `Log_ID` int NOT NULL AUTO_INCREMENT,
  `User_Email` varchar(100) DEFAULT NULL,
  `User_Id` int DEFAULT NULL,
  `Role` enum('Admin','Faculty','Student') DEFAULT NULL,
  `Login_Time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Logout_Time` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`Log_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=532 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_log`
--

LOCK TABLES `login_log` WRITE;
/*!40000 ALTER TABLE `login_log` DISABLE KEYS */;
INSERT INTO `login_log` VALUES (1,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 07:41:36','2025-10-13 07:49:38'),(2,'shraddha.doshi@nuv.ac.in',NULL,'Faculty','2025-10-13 07:51:25','2025-10-13 07:58:36'),(3,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 07:58:44','2025-10-13 08:12:53'),(4,'shraddha.doshi@nuv.ac.in',NULL,'Faculty','2025-10-13 08:13:01','2025-10-13 08:13:22'),(6,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 08:14:20','2025-10-13 08:15:35'),(7,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-13 08:15:40','2025-10-13 08:16:34'),(8,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 08:16:53','2025-10-13 08:17:17'),(9,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 08:17:52','2025-10-13 08:18:30'),(11,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-13 08:18:39','2025-10-13 08:19:22'),(12,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 08:19:40','2025-10-13 08:21:28'),(13,'shraddha.doshi@nuv.ac.in',NULL,'Faculty','2025-10-13 08:21:35','2025-10-13 08:22:15'),(14,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 10:28:38','2025-10-13 10:42:53'),(15,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-13 10:55:45','2025-10-13 10:59:56'),(16,'shraddha.doshi@nuv.ac.in',NULL,'Faculty','2025-10-13 11:00:01','2025-10-13 11:00:32'),(17,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-14 07:10:41','2025-10-14 07:13:11'),(18,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-14 07:13:16','2025-10-14 07:13:19'),(19,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-14 07:13:24','2025-10-14 07:15:17'),(20,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-14 07:15:23','2025-10-14 07:15:33'),(21,'izmashaikh7681@gmail.com',NULL,'Student','2025-10-14 07:16:05','2025-10-14 07:16:13'),(22,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-14 07:16:30','2025-10-14 07:17:02'),(23,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-14 07:17:06','2025-10-14 07:18:22'),(24,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-14 07:18:25','2025-10-14 07:25:55'),(25,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-15 06:22:21','2025-10-15 06:25:08'),(27,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 04:58:43','2025-10-16 05:16:33'),(28,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-16 05:16:44','2025-10-16 05:18:00'),(33,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 05:23:00','2025-10-16 05:23:43'),(34,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 05:23:50','2025-10-16 05:24:17'),(36,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 05:36:56','2025-10-16 05:37:35'),(37,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-16 05:37:41','2025-10-16 05:40:56'),(38,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-16 05:41:11','2025-10-16 05:42:17'),(39,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-16 05:42:35','2025-10-16 05:46:45'),(42,'yasirazimshaikh5440@gmail.com',NULL,'Student','2025-10-16 05:48:34','2025-10-16 05:50:42'),(43,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-16 05:51:00','2025-10-16 05:51:36'),(45,'izmashaikh7681@gmail.com',NULL,'Student','2025-10-16 05:52:37','2025-10-16 05:54:45'),(46,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 05:55:05','2025-10-16 05:56:52'),(47,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-16 06:20:56','2025-10-16 06:22:09'),(49,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 08:12:58','2025-10-16 08:23:44'),(51,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-16 08:25:56','2025-10-16 08:26:28'),(52,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 08:27:22','2025-10-16 08:31:36'),(53,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-16 09:21:29','2025-10-16 09:26:50'),(55,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-20 07:47:26','2025-10-20 08:02:57'),(59,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-20 09:09:10','2025-10-20 09:09:36'),(62,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 09:29:41','2025-10-20 09:29:45'),(73,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 09:50:34','2025-10-20 09:52:20'),(74,'kashaf786parkar@gmail.com',NULL,'Student','2025-10-20 09:52:27','2025-10-20 09:58:16'),(77,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 10:00:17','2025-10-20 10:00:47'),(78,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 10:09:30','2025-10-20 10:12:11'),(85,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 10:50:13','2025-10-20 10:50:18'),(88,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 11:00:33','2025-10-20 11:01:13'),(91,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 11:40:39','2025-10-20 11:40:52'),(92,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-20 11:41:25','2025-10-20 11:41:47'),(102,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-25 11:13:36','2025-10-25 11:13:54'),(106,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-25 11:19:51','2025-10-25 11:21:53'),(107,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-25 11:31:15','2025-10-25 11:32:13'),(108,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-25 11:32:24','2025-10-25 11:57:03'),(109,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-25 11:57:05','2025-10-25 12:01:08'),(110,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-25 12:01:19','2025-10-25 12:05:16'),(111,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-25 12:05:32','2025-10-25 12:05:58'),(114,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-10-25 12:08:14','2025-10-25 12:08:29'),(115,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-25 12:08:34','2025-10-25 12:08:58'),(117,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-10-25 12:09:24','2025-10-25 12:09:38'),(118,'margie.patoliya@nuv.ac.in',NULL,'Faculty','2025-11-10 05:00:28','2025-11-10 05:00:38'),(120,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2025-11-11 04:52:17','2025-11-11 04:55:34'),(121,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-11 04:56:40','2025-11-11 05:23:50'),(122,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-11 05:24:05','2025-11-11 05:26:22'),(123,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-11 05:30:42','2025-11-11 05:41:43'),(124,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-11 05:41:56','2025-11-11 05:41:59'),(125,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-11 05:42:27','2025-11-11 05:47:20'),(126,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-11 05:47:50','2025-11-11 05:49:24'),(127,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-11 05:49:32','2025-11-11 05:50:12'),(128,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-11 05:50:28','2025-11-11 06:25:04'),(129,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-11 06:25:10','2025-11-11 06:27:24'),(130,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-11 06:28:52','2025-11-11 06:29:51'),(131,'izmashaikh7681@gmail.com',NULL,'Student','2025-11-11 06:30:34','2025-11-11 06:32:03'),(132,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-11 06:32:19','2025-11-11 06:48:13'),(133,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 04:45:08','2025-11-12 04:48:02'),(136,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 06:21:41','2025-11-12 06:32:15'),(137,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 06:32:25','2025-11-12 06:41:57'),(138,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 06:42:01','2025-11-12 06:42:23'),(139,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 06:42:28','2025-11-12 06:44:56'),(140,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-12 06:45:17','2025-11-12 06:47:53'),(144,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 06:51:59','2025-11-12 06:52:06'),(145,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 06:54:04','2025-11-12 06:54:45'),(146,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 06:54:53','2025-11-12 07:08:32'),(147,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 07:08:49','2025-11-12 07:16:01'),(148,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-12 07:16:26','2025-11-12 07:18:02'),(151,'ansarikaif23604@gmail.com',NULL,'Student','2025-11-12 07:20:47','2025-11-12 07:22:15'),(152,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 09:37:57','2025-11-12 09:38:05'),(153,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 10:09:17','2025-11-12 10:09:18'),(154,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-12 10:18:51','2025-11-12 10:20:48'),(155,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 10:20:57','2025-11-12 10:26:44'),(156,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-12 10:29:19','2025-11-12 10:32:07'),(159,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-12 10:34:46','2025-11-12 10:38:36'),(160,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-25 11:36:55','2025-11-25 12:09:14'),(161,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-26 09:02:34','2025-11-26 09:03:25'),(162,'dhavalm@nuv.ac.in',NULL,'Faculty','2025-11-26 09:03:40','2025-11-26 09:04:46'),(163,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-26 09:05:12','2025-11-26 09:07:15'),(164,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-26 09:07:25','2025-11-26 09:26:50'),(165,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-27 17:51:36','2025-11-27 17:53:09'),(167,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-27 17:53:42','2025-11-27 17:54:00'),(170,'ansarikaif23604@gmail.com',NULL,'Student','2025-11-27 18:19:40','2025-11-27 18:19:56'),(171,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-27 18:21:08','2025-11-27 18:22:28'),(172,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-27 18:22:43','2025-11-27 18:23:03'),(173,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-28 04:40:04','2025-11-28 04:42:06'),(174,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-28 04:42:12','2025-11-28 04:50:53'),(175,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-28 04:52:13','2025-11-28 04:53:12'),(177,'ansarikaif23604@gmail.com',NULL,'Student','2025-11-28 04:56:27','2025-11-28 04:58:00'),(178,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-28 04:58:23','2025-11-28 05:00:04'),(179,'dhavalm@nuv.ac.in',NULL,'Admin','2025-11-28 06:15:44','2025-11-28 06:17:04'),(180,'megha.patel@nuv.ac.in',NULL,'Faculty','2025-11-28 06:17:10','2025-11-28 06:21:20'),(181,'kashaf786parkar@gmail.com',NULL,'Student','2025-11-28 06:21:37','2025-11-28 06:22:35'),(183,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-12 06:11:56','2026-01-12 06:15:27'),(184,'dhavalm@nuv.ac.in',NULL,'Faculty','2026-01-12 06:15:55','2026-01-12 07:31:53'),(185,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-16 05:10:56','2026-01-16 05:11:00'),(186,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-16 05:11:09','2026-01-16 05:15:05'),(187,'kashaf786parkar@gmail.com',NULL,'Student','2026-01-16 05:15:17','2026-01-16 05:16:06'),(188,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-16 05:16:32','2026-01-16 05:21:57'),(190,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-16 05:27:48','2026-01-16 06:11:22'),(191,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-19 05:37:03','2026-01-19 05:37:15'),(221,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-19 07:53:39','2026-01-19 07:53:54'),(226,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-19 07:58:00','2026-01-19 08:01:18'),(227,'dhavalm@nuv.ac.in',NULL,'Faculty','2026-01-19 08:01:30','2026-01-19 08:01:40'),(229,'dhavalm@nuv.ac.in',NULL,'Faculty','2026-01-19 08:08:05','2026-01-19 08:16:19'),(231,'dhavalm@nuv.ac.in',NULL,'Faculty','2026-01-19 08:16:27','2026-02-10 10:49:09'),(233,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-19 08:16:42','2026-01-19 08:16:47'),(235,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-19 08:18:22','2026-01-19 08:18:27'),(237,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-20 06:35:58','2026-01-20 06:36:02'),(243,'megha.patel@nuv.ac.in',NULL,'Faculty','2026-01-20 07:08:19','2026-01-20 07:10:49'),(251,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-20 09:44:51','2026-01-20 10:20:32'),(284,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-28 05:00:25','2026-01-28 06:17:21'),(303,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-28 07:19:52','2026-01-28 07:19:59'),(304,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-28 07:20:02','2026-01-28 07:20:11'),(305,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-28 07:20:57','2026-01-28 07:22:22'),(306,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-28 09:15:21','2026-01-28 11:33:46'),(307,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-29 05:35:34','2026-01-29 05:52:36'),(308,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-29 05:52:39','2026-01-29 05:53:06'),(309,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 05:53:14',NULL),(310,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 06:21:30','2026-01-29 06:23:16'),(311,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-29 06:23:22','2026-01-29 06:35:01'),(312,'dhavalm@nuv.ac.in',NULL,'Admin','2026-01-29 06:35:06','2026-01-29 06:36:04'),(313,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 06:38:14','2026-01-29 06:39:25'),(314,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-01-29 06:39:35','2026-01-29 06:41:52'),(315,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 06:41:59','2026-01-29 07:41:55'),(316,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 09:01:32',NULL),(317,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 09:36:28','2026-01-29 10:45:55'),(318,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 10:59:37','2026-01-29 11:00:02'),(319,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-29 11:00:07','2026-01-29 11:01:19'),(320,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 05:12:00','2026-01-30 05:16:18'),(321,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 05:16:21','2026-01-30 05:16:49'),(322,'kashaf.a.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 05:16:59','2026-01-30 06:34:49'),(323,'kashaf786parkar@gmail.com',NULL,'Student','2026-01-30 06:35:03',NULL),(324,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-01-30 06:35:31','2026-01-30 07:08:45'),(325,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 07:08:49','2026-01-30 07:11:41'),(326,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 07:11:44','2026-01-30 07:12:00'),(327,'kashaf.a.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 07:12:08','2026-01-30 07:50:17'),(328,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-01-30 07:50:28','2026-01-30 08:24:05'),(329,'kashaf.a.parkar@nuv.ac.in',NULL,'Admin','2026-01-30 09:52:40',NULL),(330,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 05:08:41',NULL),(331,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 05:52:15','2026-02-02 05:53:02'),(332,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-02-02 05:53:10','2026-02-02 05:53:44'),(333,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 05:53:47','2026-02-02 06:09:00'),(334,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-02-02 06:09:08','2026-02-02 06:12:36'),(335,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 06:12:39','2026-02-02 06:13:23'),(336,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-02 06:13:30','2026-02-02 06:14:24'),(337,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-02-02 06:16:24','2026-02-02 06:30:55'),(338,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 06:30:58','2026-02-02 06:59:05'),(339,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 07:25:55',NULL),(340,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 09:53:12','2026-02-02 10:32:07'),(341,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-02 10:34:06','2026-02-02 11:22:27'),(342,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-03 05:15:35','2026-02-03 05:15:42'),(343,'kashaf.a.parkar@nuv.ac.in',NULL,'Admin','2026-02-03 05:15:51','2026-02-03 07:23:10'),(344,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-03 07:23:22','2026-02-03 08:03:01'),(345,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-03 08:04:14','2026-02-03 08:08:55'),(346,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-03 09:47:38','2026-02-03 10:06:01'),(347,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 05:52:27','2026-02-06 05:55:33'),(348,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 05:56:57','2026-02-06 06:18:27'),(349,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:18:32','2026-02-06 06:19:12'),(350,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:19:17','2026-02-06 06:20:23'),(351,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:24:36','2026-02-06 06:29:48'),(352,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:30:01','2026-02-06 06:30:33'),(353,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:30:41','2026-02-06 06:31:29'),(354,'kashaf786parkar@gmail.com',NULL,'Faculty','2026-02-06 06:31:37','2026-02-06 06:32:13'),(355,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 06:32:16','2026-02-06 06:51:11'),(356,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-06 08:59:56','2026-02-06 09:54:13'),(357,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-09 05:08:23','2026-02-09 05:48:12'),(358,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-10 05:04:34','2026-02-10 06:21:39'),(359,'kashaf.a.parkar@nuv.ac.in',NULL,'Admin','2026-02-10 06:21:51','2026-02-10 06:21:56'),(360,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-10 06:22:12',NULL),(361,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-10 09:25:37',NULL),(362,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-10 09:55:01','2026-02-10 09:55:16'),(363,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-10 09:55:46',NULL),(364,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-23 05:16:41','2026-02-23 06:14:25'),(365,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-23 06:14:31',NULL),(366,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-23 06:16:54','2026-02-23 07:02:59'),(367,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-23 07:03:18','2026-02-23 07:56:25'),(368,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-23 07:56:39',NULL),(369,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-24 05:12:04','2026-02-24 09:48:09'),(370,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-24 09:52:14','2026-02-24 10:09:48'),(371,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-25 05:14:40','2026-02-25 05:15:33'),(372,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-25 05:35:41',NULL),(373,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 05:36:00','2026-02-25 05:52:26'),(374,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-25 05:52:31',NULL),(375,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-25 06:01:38',NULL),(376,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:11:42','2026-02-25 06:12:04'),(377,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-25 06:12:09',NULL),(378,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:13:07','2026-02-25 06:13:14'),(379,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:13:23','2026-02-25 06:16:09'),(380,'yasirazimshaikh5440@gmail.com',NULL,'Student','2026-02-25 06:16:27',NULL),(381,'izmashaikh7681@gmail.com',NULL,'Student','2026-02-25 06:17:49',NULL),(382,'sneha.gupta@example.com',NULL,'Student','2026-02-25 06:18:52',NULL),(383,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:19:55','2026-02-25 06:20:18'),(384,'kavya.nair@example.com',NULL,'Student','2026-02-25 06:20:32',NULL),(385,'aditya.mehta@example.com',NULL,'Student','2026-02-25 06:21:19','2026-02-25 06:21:47'),(386,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:23:00','2026-02-25 06:28:58'),(387,'kashaf786parkar@gmail.com',NULL,'Student','2026-02-25 06:29:02',NULL),(388,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 06:36:34','2026-02-25 07:19:47'),(389,'dhavalm@nuv.ac.in',NULL,'Admin','2026-02-25 07:19:51','2026-02-25 07:31:28'),(390,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 07:31:58','2026-02-25 07:32:31'),(391,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 07:32:50','2026-02-25 07:33:27'),(392,'aiza123tambe@nuv.ac.in',NULL,'Student','2026-02-25 07:35:17',NULL),(393,'alfiya@gmail.com',NULL,'Student','2026-02-25 07:36:09',NULL),(394,'zoya@gmailcom',NULL,'Student','2026-02-25 07:37:01',NULL),(395,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 07:38:04','2026-02-25 07:57:31'),(396,'alisha.tambe15@gmail.com',NULL,'Student','2026-02-25 07:57:52',NULL),(397,'kashaf.parkar@nuv.ac.in',NULL,'Admin','2026-02-25 07:59:01','2026-02-25 08:10:51'),(398,'zubeda@gmail.com',80,'Student','2026-02-25 08:11:08','2026-02-25 08:11:27'),(399,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-25 08:11:42','2026-02-25 08:12:10'),(400,'anjali@gmail.com',79,'Student','2026-02-25 08:12:28','2026-02-25 08:12:44'),(401,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-25 08:12:57','2026-02-25 08:13:15'),(402,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:13:20','2026-02-25 08:13:41'),(403,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:19:32',NULL),(404,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:20:54',NULL),(405,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:21:13',NULL),(406,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:22:45',NULL),(407,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:24:47',NULL),(408,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:27:27',NULL),(409,'shraddha.doshi@nuv.ac.in',3,'Faculty','2026-02-25 08:27:53',NULL),(410,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:28:24','2026-02-25 08:28:34'),(411,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-25 08:28:44','2026-02-25 08:36:45'),(412,'shraddha.doshi@nuv.ac.in',3,'Faculty','2026-02-25 08:36:53',NULL),(413,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:37:05','2026-02-25 08:37:16'),(414,'vasudha@gmail.com',78,'Student','2026-02-25 08:38:00','2026-02-25 08:38:18'),(415,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:38:32','2026-02-25 08:38:54'),(416,'shraddha.doshi@nuv.ac.in',3,'Faculty','2026-02-25 08:39:27',NULL),(417,'shraddha.doshi@nuv.ac.in',3,'Faculty','2026-02-25 08:45:13','2026-02-25 08:45:15'),(418,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:45:19','2026-02-25 08:46:01'),(419,'shafak@gmail.com',95,'Student','2026-02-25 08:46:55','2026-02-25 08:47:24'),(420,'aiza123tambe@nuv.ac.in',82,'Student','2026-02-25 08:47:57',NULL),(421,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:48:29','2026-02-25 08:48:54'),(422,'aiza123@nuv.ac.in',74,'Student','2026-02-25 08:49:20','2026-02-25 08:49:44'),(423,'dhavalm@nuv.ac.in',1,'Admin','2026-02-25 08:50:01','2026-02-25 09:52:42'),(424,'dhavalm@nuv.ac.in',1,'Admin','2026-02-26 05:35:46','2026-02-26 06:01:02'),(425,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-26 06:20:07','2026-02-26 06:27:08'),(426,'kashaf786parkar@gmail.com',1,'Student','2026-02-26 06:27:15','2026-02-26 06:28:07'),(427,'kashaf786parkar@gmail.com',1,'Student','2026-02-26 06:28:59',NULL),(428,'yasirazimshaikh5440@gmail.com',3,'Student','2026-02-26 06:29:18','2026-02-26 06:29:53'),(429,'izmashaikh7681@gmail.com',2,'Student','2026-02-26 06:40:42','2026-02-26 06:43:43'),(430,'kavya.nair@example.com',63,'Student','2026-02-26 06:47:58','2026-02-26 06:49:09'),(431,'sneha.gupta@example.com',65,'Student','2026-02-26 06:49:42','2026-02-26 06:50:42'),(432,'kashaf786parkar@gmail.com',1,'Student','2026-02-26 08:56:31',NULL),(433,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-26 08:56:40','2026-02-26 09:06:07'),(434,'aditya.mehta@example.com',64,'Student','2026-02-26 09:06:45','2026-02-26 09:07:24'),(435,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-26 09:08:45','2026-02-26 10:06:40'),(436,'aiza123tambe@nuv.ac.in',82,'Student','2026-02-26 10:09:13',NULL),(437,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-26 10:10:03','2026-02-26 10:20:06'),(438,'alfiya@gmail.com',91,'Student','2026-02-26 10:20:29','2026-03-06 07:55:50'),(439,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-26 10:21:33','2026-02-26 10:30:14'),(440,'zoya@gmailcom',92,'Student','2026-02-26 10:30:55',NULL),(441,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 05:08:10','2026-02-27 05:35:36'),(442,'kashaf786parkar@gmail.com',1,'Student','2026-02-27 05:35:39','2026-02-27 05:36:15'),(443,'yasirazimshaikh5440@gmail.com',3,'Student','2026-02-27 05:36:42','2026-02-27 05:37:07'),(444,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 05:37:21','2026-02-27 05:37:32'),(445,'ansarikaif23604@gmail.com',54,'Student','2026-02-27 05:38:28','2026-02-27 05:39:06'),(446,'kashaf786parkar@gmail.com',1,'Student','2026-02-27 05:39:24',NULL),(447,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 05:39:39','2026-02-27 06:12:24'),(448,'izmashaikh7681@gmail.com',2,'Student','2026-02-27 06:12:46',NULL),(449,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 06:18:03','2026-02-27 06:21:39'),(450,'kavya.nair@example.com',63,'Student','2026-02-27 06:22:12',NULL),(451,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 06:24:31','2026-02-27 06:25:14'),(452,'sneha.gupta@example.com',65,'Student','2026-02-27 06:25:27',NULL),(453,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 06:26:24','2026-02-27 08:00:37'),(454,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 08:11:16','2026-02-27 08:11:43'),(455,'aditya.mehta@example.com',64,'Student','2026-02-27 08:12:08',NULL),(456,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 08:12:57','2026-02-27 08:13:01'),(457,'aiza123tambe@nuv.ac.in',82,'Student','2026-02-27 08:13:25',NULL),(458,'alfiya@gmail.com',91,'Student','2026-02-27 08:14:48','2026-03-06 07:55:50'),(459,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-02-27 08:19:28','2026-02-27 09:54:32'),(460,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-02 05:49:37','2026-03-02 09:05:52'),(461,'kashaf786parkar@gmail.com',1,'Student','2026-03-02 09:05:58',NULL),(462,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-02 10:04:47','2026-03-02 10:04:56'),(463,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-05 10:17:21','2026-03-05 10:19:54'),(464,'kashaf786parkar@gmail.com',1,'Student','2026-03-05 10:21:50',NULL),(465,'yasirazimshaikh5440@gmail.com',3,'Student','2026-03-05 10:22:51',NULL),(466,'ansarikaif23604@gmail.com',54,'Student','2026-03-05 10:23:53',NULL),(467,'izmashaikh7681@gmail.com',2,'Student','2026-03-05 10:25:37',NULL),(468,'aditya.mehta@example.com',64,'Student','2026-03-05 10:26:29',NULL),(469,'sneha.gupta@example.com',65,'Student','2026-03-05 10:27:25',NULL),(470,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-05 10:28:05','2026-03-05 10:36:07'),(471,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-05 10:36:56','2026-03-05 10:41:22'),(472,'kashaf786parkar@gmail.com',1,'Student','2026-03-05 10:41:26',NULL),(473,'ansarikaif23604@gmail.com',54,'Student','2026-03-05 10:42:23',NULL),(474,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 05:14:21','2026-03-06 06:19:04'),(475,'kashaf786parkar@gmail.com',1,'Student','2026-03-06 06:19:08',NULL),(476,'ansarikaif23604@gmail.com',54,'Student','2026-03-06 06:20:46',NULL),(477,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:21:34','2026-03-06 06:21:42'),(478,'izmashaikh7681@gmail.com',2,'Student','2026-03-06 06:21:55',NULL),(479,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:23:16','2026-03-06 06:26:13'),(480,'sneha.gupta@example.com',65,'Student','2026-03-06 06:26:32',NULL),(481,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:27:25','2026-03-06 06:47:26'),(482,'aditya.mehta@example.com',64,'Student','2026-03-06 06:47:46',NULL),(483,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:48:54','2026-03-06 06:55:35'),(484,'kavya.nair@example.com',63,'Student','2026-03-06 06:56:01',NULL),(485,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:56:32','2026-03-06 06:57:02'),(486,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:57:16','2026-03-06 06:58:00'),(487,'aiza123tambe@nuv.ac.in',82,'Student','2026-03-06 06:58:14','2026-03-06 06:58:32'),(488,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 06:58:55','2026-03-06 07:00:08'),(489,'zoii@gmail.com',94,'Student','2026-03-06 07:00:25','2026-03-06 07:02:12'),(490,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 07:02:25','2026-03-06 07:02:35'),(491,'zoya@gmailcom',92,'Student','2026-03-06 07:02:57','2026-03-06 07:03:16'),(492,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 07:03:33','2026-03-06 07:36:32'),(493,'alfiya@gmail.com',91,'Student','2026-03-06 07:36:52','2026-03-06 07:55:50'),(494,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 07:37:49','2026-03-06 07:38:05'),(495,'alfiya@gmail.com',91,'Student','2026-03-06 07:54:59','2026-03-06 07:55:50'),(496,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 08:01:22','2026-03-06 08:01:49'),(497,'alisha.tambe15@gmail.com',73,'Student','2026-03-06 08:02:08','2026-03-06 08:02:51'),(498,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 08:04:48','2026-03-06 08:10:33'),(499,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 08:36:15','2026-03-06 08:40:25'),(500,'kashaf786parkar@gmail.com',1,'Student','2026-03-06 08:40:30','2026-03-06 08:41:26'),(501,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 08:41:42','2026-03-06 08:41:58'),(502,'alisha.tambe15@gmail.com',73,'Student','2026-03-06 08:42:02',NULL),(503,'ansarikaif23604@gmail.com',54,'Student','2026-03-06 08:42:19','2026-03-06 08:43:10'),(504,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 08:44:08','2026-03-06 08:46:05'),(505,'izmashaikh7681@gmail.com',2,'Student','2026-03-06 08:46:16','2026-03-06 08:46:59'),(506,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-06 10:24:33','2026-03-06 10:25:31'),(507,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-09 05:55:18','2026-03-09 05:59:57'),(508,'kashaf786parkar@gmail.com',1,'Student','2026-03-09 06:00:06','2026-03-09 06:01:23'),(509,'ansarikaif23604@gmail.com',54,'Student','2026-03-09 06:01:49','2026-03-09 06:02:22'),(510,'izmashaikh7681@gmail.com',2,'Student','2026-03-09 06:03:35','2026-03-09 06:04:04'),(511,'kavya.nair@example.com',63,'Student','2026-03-09 06:04:36','2026-03-09 06:05:57'),(512,'aditya.mehta@example.com',64,'Student','2026-03-09 06:06:48','2026-03-09 06:11:54'),(513,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-09 06:12:51','2026-03-09 06:14:25'),(514,'sneha.gupta@example.com',65,'Student','2026-03-09 06:14:40','2026-03-09 06:16:51'),(515,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-09 06:17:08','2026-03-09 08:39:47'),(516,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-10 05:17:12','2026-03-10 05:17:22'),(517,'dhavalm@nuv.ac.in',1,'Admin','2026-03-10 05:17:27','2026-03-10 05:20:35'),(518,'dhavalm@nuv.ac.in',2,'Faculty','2026-03-10 05:20:46','2026-03-10 05:22:33'),(519,'dhavalm@nuv.ac.in',1,'Admin','2026-03-10 05:22:36','2026-03-10 06:13:32'),(520,'dhavalm@nuv.ac.in',1,'Admin','2026-03-11 05:20:28','2026-03-11 05:34:30'),(521,'kashaf786parkar@gmail.com',1,'Student','2026-03-11 05:34:36','2026-03-11 05:35:13'),(522,'ansarikaif23604@gmail.com',54,'Student','2026-03-11 05:35:47','2026-03-11 05:36:37'),(523,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-11 05:39:24','2026-03-11 05:56:41'),(524,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-11 06:00:38','2026-03-11 06:10:09'),(525,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-11 06:17:56','2026-03-11 08:48:53'),(526,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-16 06:21:27','2026-03-16 06:24:50'),(527,'kashaf786parkar@gmail.com',1,'Student','2026-03-16 06:24:55','2026-03-16 06:26:02'),(528,'ansarikaif23604@gmail.com',54,'Student','2026-03-16 06:26:19','2026-03-16 06:27:06'),(529,'izmashaikh7681@gmail.com',2,'Student','2026-03-16 06:27:29','2026-03-16 06:27:59'),(530,'kashaf.parkar@nuv.ac.in',3,'Admin','2026-03-16 06:28:16','2026-03-16 06:32:27'),(531,'dhavalm@nuv.ac.in',1,'Admin','2026-03-16 06:32:33','2026-03-16 06:34:48');
/*!40000 ALTER TABLE `login_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_admin`
--

DROP TABLE IF EXISTS `mst_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mst_admin` (
  `Admin_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Admin_ID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_admin`
--

LOCK TABLES `mst_admin` WRITE;
/*!40000 ALTER TABLE `mst_admin` DISABLE KEYS */;
INSERT INTO `mst_admin` VALUES (1,'Dhaval Mehta','dhavalm@nuv.ac.in','dm123@NUV',1),(2,'Shraddha Doshi','shraddha.doshi@nuv.ac.in','sd123@NUV',1),(3,'Kashaf Parkar','kashaf.parkar@nuv.ac.in','kp123@NUV',1),(8,'Chirag Darji','chirag.darji@nuv.ac.in','Chirag@NUV',1),(9,'Kashaf','kashaf.a.parkar@nuv.ac.in','12345',1);
/*!40000 ALTER TABLE `mst_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_designation`
--

DROP TABLE IF EXISTS `mst_designation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mst_designation` (
  `Designation_Id` int NOT NULL AUTO_INCREMENT,
  `Designation_Name` varchar(150) NOT NULL,
  `Role_Id` int DEFAULT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Designation_Id`),
  UNIQUE KEY `Designation_Name` (`Designation_Name`),
  KEY `Role_Id` (`Role_Id`),
  CONSTRAINT `mst_designation_ibfk_1` FOREIGN KEY (`Role_Id`) REFERENCES `mst_roles` (`Role_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_designation`
--

LOCK TABLES `mst_designation` WRITE;
/*!40000 ALTER TABLE `mst_designation` DISABLE KEYS */;
INSERT INTO `mst_designation` VALUES (1,'Administrator',1,1),(2,'Dean',2,1),(3,'Head',3,1),(4,'Program Chair',4,1),(5,'Professor',5,1),(6,'Teaching Assistant',6,1),(7,'Lecturer',5,1),(8,'Assistant Professor',5,1),(9,'Associate Professor',5,1),(10,'Mentor',6,1),(11,'Professor of Practice',5,0);
/*!40000 ALTER TABLE `mst_designation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_faculty`
--

DROP TABLE IF EXISTS `mst_faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mst_faculty` (
  `Faculty_Id` int NOT NULL AUTO_INCREMENT,
  `F_Name` varchar(50) NOT NULL,
  `F_Email` varchar(50) NOT NULL,
  `School_Id` int NOT NULL,
  `Designation_Id` int DEFAULT NULL,
  `Password` varchar(255) NOT NULL,
  `Role_Id` int DEFAULT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`Faculty_Id`),
  UNIQUE KEY `F_Email` (`F_Email`),
  KEY `School_Id` (`School_Id`),
  CONSTRAINT `mst_faculty_ibfk_1` FOREIGN KEY (`School_Id`) REFERENCES `mst_school` (`School_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_faculty`
--

LOCK TABLES `mst_faculty` WRITE;
/*!40000 ALTER TABLE `mst_faculty` DISABLE KEYS */;
INSERT INTO `mst_faculty` VALUES (1,'Chirag Darji','chirag.darji@nuv.ac.in',1,1,'Chirag@123',1,1),(2,'Dhaval Mehta','dhavalm@nuv.ac.in',1,4,'Dhaval@123',4,1),(3,'Shraddha Doshi','shraddha.doshi@nuv.ac.in',1,5,'Shraddha@123',5,1),(4,'Rupali Shinde','rupali.shinde@nuv.ac.in',1,5,'Rupali@123',5,1),(5,'Megha Patel','megha.patel@nuv.ac.in',1,5,'Megha@123',5,1),(6,'Shardav Bhatt','shardavb@nuv.ac.in',1,4,'Shardav@123',4,1),(7,'Dr. Vivek Bhatt','vivek.bhatt@nuv.ac.in',3,5,'Vivek@123',5,0),(8,'Dharti Parikh','dhartip@nuv.ac.in',3,5,'Dharti@123',5,0),(9,'Humayed Shaikh','humayd.shaikh@nuv.ac.in',1,6,'Humayd@123',6,1),(10,'Aymaan Garasia','aymaan.garasia@nuv.ac.in',1,6,'Aymaan@123',6,0),(14,'Margie Patolia','margie.patoliya@nuv.ac.in',1,6,'Margie@123',6,0),(18,'Vedant Parmar','vedant.j.parmar@nuv.ac.in',1,6,'Vedant@123',6,0),(30,'Mariyam Memom','mariyam.memon@nuv.ac.in',1,6,'Mariyam@123',6,0),(33,'Salma Pirzada','salmap@nuv.ac.in',1,8,'Salma@123',5,1);
/*!40000 ALTER TABLE `mst_faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_roles`
--

DROP TABLE IF EXISTS `mst_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mst_roles` (
  `Role_Id` int NOT NULL AUTO_INCREMENT,
  `Role_Name` varchar(100) NOT NULL,
  `Access_Level` int NOT NULL,
  `Description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Role_Id`),
  UNIQUE KEY `Role_Name` (`Role_Name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_roles`
--

LOCK TABLES `mst_roles` WRITE;
/*!40000 ALTER TABLE `mst_roles` DISABLE KEYS */;
INSERT INTO `mst_roles` VALUES (1,'Administrator',1,'Full access'),(2,'Dean',2,'School-level access'),(3,'Head',3,'Program-level access'),(4,'Program Chair',4,'Program-only'),(5,'Faculty',5,'Faculty-level'),(6,'Teaching Assistant',6,'TA-level');
/*!40000 ALTER TABLE `mst_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mst_school`
--

DROP TABLE IF EXISTS `mst_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mst_school` (
  `School_Id` int NOT NULL AUTO_INCREMENT,
  `School_Name` varchar(50) NOT NULL,
  `School_Short` varchar(50) NOT NULL,
  `Is_Active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`School_Id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mst_school`
--

LOCK TABLES `mst_school` WRITE;
/*!40000 ALTER TABLE `mst_school` DISABLE KEYS */;
INSERT INTO `mst_school` VALUES (1,'School of Engineering & Technology','SET',1),(2,'School of Science','SOS',1),(3,'School of Business & Law','SBL',1),(4,'School of Liberal Studies & Education','SLSE',1),(6,'School of Environmental Design & Architecture','SEDA',1),(7,'School of Computer Applications','SCA',0);
/*!40000 ALTER TABLE `mst_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notification`
--

DROP TABLE IF EXISTS `notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notification` (
  `Notification_ID` int NOT NULL AUTO_INCREMENT,
  `Title` varchar(255) DEFAULT NULL,
  `Message` text,
  `Target_Role` varchar(50) DEFAULT NULL,
  `Created_At` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `Exam_Id` int DEFAULT NULL,
  `Faculty_Email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Notification_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notification`
--

LOCK TABLES `notification` WRITE;
/*!40000 ALTER TABLE `notification` DISABLE KEYS */;
INSERT INTO `notification` VALUES (1,'Exam Reminder','Exam \"Email Try\" will start in 10 minutes.','Faculty','2026-01-29 06:39:07',NULL,NULL),(2,'Exam Reminder','Exam \"Email Try\" will start in 10 minutes.','Faculty','2026-01-29 06:39:08',NULL,NULL),(3,'Exam Reminder','Exam \"Email Trial\" will start in 10 minutes.','Faculty','2026-01-29 06:40:07',NULL,NULL),(4,'Exam Reminder','Exam \"Email Trial\" will start in 10 minutes.','Faculty','2026-01-29 06:40:09',NULL,NULL),(5,'Exam Reminder','Exam \"Email Testing\" will start in 10 minutes.','Faculty','2026-01-29 06:43:07',NULL,NULL),(6,'Exam Reminder','Exam \"Email Testing\" will start in 10 minutes.','Faculty','2026-01-29 06:43:08',NULL,NULL),(7,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-01-29 07:33:07',NULL,NULL),(8,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-01-29 07:33:08',NULL,NULL),(9,'Exam Reminder','Exam \"Exam 1\" will start in 10 minutes.','Faculty','2026-01-30 05:21:00',NULL,NULL),(10,'Exam Reminder','Exam \"Exam 1\" will start in 10 minutes.','Faculty','2026-01-30 05:21:00',NULL,NULL),(11,'Exam Reminder','Exam \"BCA Exam \" will start in 10 minutes.','Faculty','2026-01-30 07:10:43',NULL,NULL),(12,'Exam Reminder','Exam \"Exam 2\" will start in 10 minutes.','Faculty','2026-01-30 07:20:41',NULL,NULL),(13,'Exam Reminder','Exam \"Entrance\" will start in 10 minutes.','Faculty','2026-02-02 05:20:35',14,'kashaf.parkar@nuv.ac.in'),(14,'Exam Reminder','Exam \"Entrance BCA\" will start in 10 minutes.','Faculty','2026-02-02 05:55:07',15,'kashaf.parkar@nuv.ac.in'),(15,'Exam Reminder','Exam \"Entrance BCA\" will start in 10 minutes.','Faculty','2026-02-02 05:55:07',15,'kashaf.parkar@nuv.ac.in'),(16,'Exam Reminder','Exam \"BCA Exam\" will start in 10 minutes.','Faculty','2026-02-02 06:05:11',16,'kashaf786parkar@gmail.com'),(17,'Exam Reminder','Exam \"BCA Exam\" will start in 10 minutes.','Faculty','2026-02-02 06:05:12',16,'kashaf786parkar@gmail.com'),(18,'Exam Reminder','Exam \"Test\" will start in 10 minutes.','Faculty','2026-02-02 06:15:11',17,'kashaf.parkar@nuv.ac.in'),(19,'Exam Reminder','Exam \"sdfghjk\" will start in 10 minutes.','Faculty','2026-02-02 10:22:06',18,'kashaf.parkar@nuv.ac.in'),(20,'Exam Reminder','Exam \"sdfghjk\" will start in 10 minutes.','Faculty','2026-02-02 10:22:07',18,'kashaf.parkar@nuv.ac.in'),(21,'Exam Reminder','Exam \"Test\" will start in 10 minutes.','Faculty','2026-02-06 05:53:19',19,'kashaf.parkar@nuv.ac.in'),(22,'Exam Reminder','Exam \"Test 2\" will start in 10 minutes.','Faculty','2026-02-23 05:45:29',21,'dhavalm@nuv.ac.in'),(23,'Exam Reminder','Exam \"Test 2\" will start in 10 minutes.','Faculty','2026-02-23 05:45:30',21,'dhavalm@nuv.ac.in'),(24,'Exam Reminder','Exam \"Review\" will start in 10 minutes.','Faculty','2026-02-24 10:05:59',23,'dhavalm@nuv.ac.in'),(25,'Exam Reminder','Exam \"Review\" will start in 10 minutes.','Faculty','2026-02-24 10:06:03',23,'dhavalm@nuv.ac.in'),(26,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-02-25 05:36:55',24,'kashaf.parkar@nuv.ac.in'),(27,'Exam Reminder','Exam \"Unique\" will start in 10 minutes.','Faculty','2026-02-26 06:21:19',25,'kashaf.parkar@nuv.ac.in'),(28,'Exam Reminder','Exam \"Unique\" will start in 10 minutes.','Faculty','2026-02-26 06:21:19',25,'kashaf.parkar@nuv.ac.in'),(29,'Exam Reminder','Exam \"Testing Restriction\" will start in 10 minutes.','Faculty','2026-02-27 05:34:00',26,'kashaf.parkar@nuv.ac.in'),(30,'Exam Reminder','Exam \"Storage Check\" will start in 10 minutes.','Faculty','2026-03-02 09:04:45',27,'kashaf.parkar@nuv.ac.in'),(31,'Exam Reminder','Exam \"Test\" will start in 10 minutes.','Faculty','2026-03-05 10:19:27',28,'kashaf.parkar@nuv.ac.in'),(32,'Exam Reminder','Exam \"Test\" will start in 10 minutes.','Faculty','2026-03-05 10:19:28',28,'kashaf.parkar@nuv.ac.in'),(33,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-03-05 10:39:27',29,'kashaf.parkar@nuv.ac.in'),(34,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-03-05 10:39:27',29,'kashaf.parkar@nuv.ac.in'),(35,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-03-06 06:19:03',30,'kashaf.parkar@nuv.ac.in'),(36,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-03-06 06:19:04',30,'kashaf.parkar@nuv.ac.in'),(37,'Exam Reminder','Exam \"Quizzz\" will start in 10 minutes.','Faculty','2026-03-06 08:39:54',31,'kashaf.parkar@nuv.ac.in'),(38,'Exam Reminder','Exam \"Testing\" will start in 10 minutes.','Faculty','2026-03-09 05:58:43',32,'kashaf.parkar@nuv.ac.in'),(39,'Exam Reminder','Exam \"Testify\" will start in 10 minutes.','Faculty','2026-03-16 06:24:09',34,'kashaf.parkar@nuv.ac.in'),(40,'Exam Reminder','Exam \"Testify\" will start in 10 minutes.','Faculty','2026-03-16 06:24:09',34,'kashaf.parkar@nuv.ac.in');
/*!40000 ALTER TABLE `notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restricted_attempts`
--

DROP TABLE IF EXISTS `restricted_attempts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restricted_attempts` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `Attempt_Id` int NOT NULL,
  `Applicant_Id` int NOT NULL,
  `Exam_Paper_Id` int NOT NULL,
  `Reason` text NOT NULL,
  `Restricted_Timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`Id`),
  KEY `Attempt_Id` (`Attempt_Id`),
  KEY `Applicant_Id` (`Applicant_Id`),
  KEY `Exam_Paper_Id` (`Exam_Paper_Id`),
  CONSTRAINT `fk_restricted_applicant` FOREIGN KEY (`Applicant_Id`) REFERENCES `applicants` (`Applicant_Id`) ON DELETE CASCADE,
  CONSTRAINT `fk_restricted_attempt` FOREIGN KEY (`Attempt_Id`) REFERENCES `applicant_attempt` (`Attempt_Id`) ON DELETE CASCADE,
  CONSTRAINT `fk_restricted_exam_paper` FOREIGN KEY (`Exam_Paper_Id`) REFERENCES `exam_paper` (`Exam_Paper_Id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restricted_attempts`
--

LOCK TABLES `restricted_attempts` WRITE;
/*!40000 ALTER TABLE `restricted_attempts` DISABLE KEYS */;
INSERT INTO `restricted_attempts` VALUES (1,6,64,5,'Window lost focus (Alt+Tab detected)','2026-02-25 11:51:46'),(2,15,74,5,'Window lost focus (Alt+Tab detected)','2026-02-25 14:19:43'),(6,26,3,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:07:06'),(7,27,54,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:09:05'),(8,29,63,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:53:07'),(9,30,65,7,'Window lost focus (Alt+Tab detected)','2026-02-27 11:56:10'),(10,31,64,7,'Window lost focus (5s exceeded)','2026-02-27 13:42:40'),(11,33,91,7,'Window lost focus (returned in time)','2026-02-27 13:45:07'),(12,40,65,9,'Window lost focus (returned in time)','2026-03-05 15:57:43'),(13,42,54,10,'Window lost focus (5s exceeded)','2026-03-05 16:12:41'),(14,44,54,11,'Window lost focus (5s exceeded)','2026-03-06 11:51:18'),(15,45,2,11,'Window lost focus (returned in time)','2026-03-06 11:53:01'),(16,50,94,11,'Window lost focus (5s exceeded)','2026-03-06 12:32:11'),(17,52,91,11,'Window lost focus (returned in time)','2026-03-06 13:25:50'),(18,53,73,11,'Window lost focus (5s exceeded)','2026-03-06 13:33:10'),(19,57,1,13,'Exited fullscreen mode (attempted to exit exam)','2026-03-09 11:31:22'),(20,58,54,13,'Exited fullscreen mode (attempted to exit exam)','2026-03-09 11:32:22'),(21,59,2,13,'Window lost focus (5s exceeded)','2026-03-09 11:34:03'),(22,67,2,15,'Window lost focus (returned in time)','2026-03-16 11:57:59');
/*!40000 ALTER TABLE `restricted_attempts` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-16 12:20:15
