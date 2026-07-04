-- MySQL dump 10.13  Distrib 8.0.44, for macos15 (arm64)
--
-- Host: localhost    Database: vbcua_db
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '689efb5a-ebe2-11f0-9663-10bf8e8b0c9c:1-340';

--
-- Table structure for table `AUDIO_FEATURE`
--

DROP TABLE IF EXISTS `AUDIO_FEATURE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AUDIO_FEATURE` (
  `feature_id` int NOT NULL AUTO_INCREMENT,
  `audio_id` int DEFAULT NULL,
  `pause_ratio` double DEFAULT NULL,
  `rms_energy` double DEFAULT NULL,
  `zero_crossing_rate` double DEFAULT NULL,
  `duration_sec` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`feature_id`),
  UNIQUE KEY `audio_id` (`audio_id`),
  CONSTRAINT `audio_feature_ibfk_1` FOREIGN KEY (`audio_id`) REFERENCES `AUDIO_FILE` (`audio_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AUDIO_FEATURE`
--

LOCK TABLES `AUDIO_FEATURE` WRITE;
/*!40000 ALTER TABLE `AUDIO_FEATURE` DISABLE KEYS */;
INSERT INTO `AUDIO_FEATURE` VALUES (1,1,0.15,0.045,0.082,45.5,'2026-07-01 12:37:46'),(2,3,0.08,0.062,0.095,120,'2026-07-01 12:37:46');
/*!40000 ALTER TABLE `AUDIO_FEATURE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AUDIO_FILE`
--

DROP TABLE IF EXISTS `AUDIO_FILE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `AUDIO_FILE` (
  `audio_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `file_name` varchar(255) NOT NULL,
  `file_path` varchar(255) NOT NULL,
  `duration_sec` double DEFAULT NULL,
  `uploaded_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`audio_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `audio_file_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USER_PROFILE` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AUDIO_FILE`
--

LOCK TABLES `AUDIO_FILE` WRITE;
/*!40000 ALTER TABLE `AUDIO_FILE` DISABLE KEYS */;
INSERT INTO `AUDIO_FILE` VALUES (1,1,'concept_explanation_v1.mp3','/storage/audio/user_1/file_101.mp3',45.5,'2026-07-01 12:37:46','Processed'),(2,1,'concept_explanation_retry.mp3','/storage/audio/user_1/file_102.mp3',12.2,'2026-07-01 12:37:46','Failed'),(3,3,'networking_basics.wav','/storage/audio/user_3/file_301.wav',120,'2026-07-01 12:37:46','Processed');
/*!40000 ALTER TABLE `AUDIO_FILE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EVALUATION_RESULT`
--

DROP TABLE IF EXISTS `EVALUATION_RESULT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EVALUATION_RESULT` (
  `result_id` int NOT NULL AUTO_INCREMENT,
  `audio_id` int DEFAULT NULL,
  `ref_concept_id` int DEFAULT NULL,
  `overall_score` double DEFAULT NULL,
  `understanding_level` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `notes` text,
  PRIMARY KEY (`result_id`),
  KEY `audio_id` (`audio_id`),
  KEY `ref_concept_id` (`ref_concept_id`),
  CONSTRAINT `evaluation_result_ibfk_1` FOREIGN KEY (`audio_id`) REFERENCES `AUDIO_FILE` (`audio_id`) ON DELETE CASCADE,
  CONSTRAINT `evaluation_result_ibfk_2` FOREIGN KEY (`ref_concept_id`) REFERENCES `REFERENCE_CONCEPT` (`ref_concept_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EVALUATION_RESULT`
--

LOCK TABLES `EVALUATION_RESULT` WRITE;
/*!40000 ALTER TABLE `EVALUATION_RESULT` DISABLE KEYS */;
INSERT INTO `EVALUATION_RESULT` VALUES (1,1,1,85.5,'Strong','2026-07-01 12:37:46','Great coverage of key definitions. Minor points deducted for filler word presence.'),(2,3,2,95,'Strong','2026-07-01 12:37:46','Exemplary technical accuracy and structure.');
/*!40000 ALTER TABLE `EVALUATION_RESULT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FILLER_WORD_STATS`
--

DROP TABLE IF EXISTS `FILLER_WORD_STATS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FILLER_WORD_STATS` (
  `filler_id` int NOT NULL AUTO_INCREMENT,
  `transcript_id` int DEFAULT NULL,
  `filler_word_count` int DEFAULT NULL,
  `total_words` int DEFAULT NULL,
  `filler_ratio` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`filler_id`),
  UNIQUE KEY `transcript_id` (`transcript_id`),
  CONSTRAINT `filler_word_stats_ibfk_1` FOREIGN KEY (`transcript_id`) REFERENCES `TRANSCRIPT` (`transcript_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FILLER_WORD_STATS`
--

LOCK TABLES `FILLER_WORD_STATS` WRITE;
/*!40000 ALTER TABLE `FILLER_WORD_STATS` DISABLE KEYS */;
INSERT INTO `FILLER_WORD_STATS` VALUES (1,1,4,24,0.166,'2026-07-01 12:37:46'),(2,2,0,21,0,'2026-07-01 12:37:46');
/*!40000 ALTER TABLE `FILLER_WORD_STATS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REFERENCE_CONCEPT`
--

DROP TABLE IF EXISTS `REFERENCE_CONCEPT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REFERENCE_CONCEPT` (
  `ref_concept_id` int NOT NULL AUTO_INCREMENT,
  `concept_title` varchar(255) NOT NULL,
  `concept_text` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ref_concept_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REFERENCE_CONCEPT`
--

LOCK TABLES `REFERENCE_CONCEPT` WRITE;
/*!40000 ALTER TABLE `REFERENCE_CONCEPT` DISABLE KEYS */;
INSERT INTO `REFERENCE_CONCEPT` VALUES (1,'Database Normalization','Database normalization is the process of structuring a relational database in accordance with a series of so-called normal forms in order to reduce data redundancy and improve data integrity.','2026-07-01 12:37:46'),(2,'OSI Model Layers','The Open Systems Interconnection model is a conceptual model that characterizes and standardizes the communication functions of a telecommunication or computing system without regard to its underlying internal structure and technology.','2026-07-01 12:37:46');
/*!40000 ALTER TABLE `REFERENCE_CONCEPT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REPORT`
--

DROP TABLE IF EXISTS `REPORT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REPORT` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `result_id` int DEFAULT NULL,
  `pdf_path` varchar(255) DEFAULT NULL,
  `generated_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `file_size_kb` int DEFAULT NULL,
  PRIMARY KEY (`report_id`),
  UNIQUE KEY `result_id` (`result_id`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`result_id`) REFERENCES `EVALUATION_RESULT` (`result_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REPORT`
--

LOCK TABLES `REPORT` WRITE;
/*!40000 ALTER TABLE `REPORT` DISABLE KEYS */;
INSERT INTO `REPORT` VALUES (1,1,'/storage/reports/report_eval_1.pdf','2026-07-01 12:37:46',142),(2,2,'/storage/reports/report_eval_2.pdf','2026-07-01 12:37:46',156);
/*!40000 ALTER TABLE `REPORT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SEMANTIC_SIMILARITY`
--

DROP TABLE IF EXISTS `SEMANTIC_SIMILARITY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SEMANTIC_SIMILARITY` (
  `similarity_id` int NOT NULL AUTO_INCREMENT,
  `transcript_id` int DEFAULT NULL,
  `ref_concept_id` int DEFAULT NULL,
  `similarity_score` double DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`similarity_id`),
  KEY `transcript_id` (`transcript_id`),
  KEY `ref_concept_id` (`ref_concept_id`),
  CONSTRAINT `semantic_similarity_ibfk_1` FOREIGN KEY (`transcript_id`) REFERENCES `TRANSCRIPT` (`transcript_id`) ON DELETE CASCADE,
  CONSTRAINT `semantic_similarity_ibfk_2` FOREIGN KEY (`ref_concept_id`) REFERENCES `REFERENCE_CONCEPT` (`ref_concept_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SEMANTIC_SIMILARITY`
--

LOCK TABLES `SEMANTIC_SIMILARITY` WRITE;
/*!40000 ALTER TABLE `SEMANTIC_SIMILARITY` DISABLE KEYS */;
INSERT INTO `SEMANTIC_SIMILARITY` VALUES (1,1,1,0.89,'2026-07-01 12:37:46'),(2,2,2,0.94,'2026-07-01 12:37:46');
/*!40000 ALTER TABLE `SEMANTIC_SIMILARITY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SESSION`
--

DROP TABLE IF EXISTS `SESSION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SESSION` (
  `session_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `started_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `ended_at` datetime DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`session_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `USER_PROFILE` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SESSION`
--

LOCK TABLES `SESSION` WRITE;
/*!40000 ALTER TABLE `SESSION` DISABLE KEYS */;
INSERT INTO `SESSION` VALUES (1,1,'2026-07-01 12:37:46',NULL,'Completed'),(2,1,'2026-07-01 12:37:46',NULL,'Active'),(3,3,'2026-07-01 12:37:46',NULL,'Completed');
/*!40000 ALTER TABLE `SESSION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRANSCRIPT`
--

DROP TABLE IF EXISTS `TRANSCRIPT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TRANSCRIPT` (
  `transcript_id` int NOT NULL AUTO_INCREMENT,
  `audio_id` int DEFAULT NULL,
  `transcript_text` text NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transcript_id`),
  UNIQUE KEY `audio_id` (`audio_id`),
  CONSTRAINT `transcript_ibfk_1` FOREIGN KEY (`audio_id`) REFERENCES `AUDIO_FILE` (`audio_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRANSCRIPT`
--

LOCK TABLES `TRANSCRIPT` WRITE;
/*!40000 ALTER TABLE `TRANSCRIPT` DISABLE KEYS */;
INSERT INTO `TRANSCRIPT` VALUES (1,1,'So basically database normalization is like structuring a relational database to follow normal forms. It helps reduce data redundancy and fixes data integrity issues, you know?','2026-07-01 12:37:46'),(2,3,'The OSI model has seven layers. It standardizes communication network functions without focusing on the underlying hardware details or internal structural technology.','2026-07-01 12:37:46');
/*!40000 ALTER TABLE `TRANSCRIPT` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USER_PROFILE`
--

DROP TABLE IF EXISTS `USER_PROFILE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USER_PROFILE` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `role` varchar(20) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USER_PROFILE`
--

LOCK TABLES `USER_PROFILE` WRITE;
/*!40000 ALTER TABLE `USER_PROFILE` DISABLE KEYS */;
INSERT INTO `USER_PROFILE` VALUES (1,'Alex Mercer','alex.mercer@example.com','Student','2026-07-01 12:37:46'),(2,'Sarah Connor','sarah.c@example.com','Instructor','2026-07-01 12:37:46'),(3,'David Lightman','david.l@example.com','Student','2026-07-01 12:37:46');
/*!40000 ALTER TABLE `USER_PROFILE` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-01 13:21:05
