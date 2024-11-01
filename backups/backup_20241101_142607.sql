-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: medical_labdb
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.24.04.2

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
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `action` varchar(255) NOT NULL,
  `details` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
INSERT INTO `audit_log` VALUES (1,1,'SUPERADMIN_ACTION','Cleared all audit logs','2024-11-01 10:45:57',NULL);
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_history`
--

DROP TABLE IF EXISTS `backup_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `backup_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `backup_file` varchar(255) NOT NULL,
  `backup_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `backup_size` bigint DEFAULT NULL,
  `created_by` int DEFAULT NULL,
  `status` enum('success','failed') NOT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `backup_history_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_history`
--

LOCK TABLES `backup_history` WRITE;
/*!40000 ALTER TABLE `backup_history` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login_logs`
--

DROP TABLE IF EXISTS `login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_logs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `success` tinyint(1) DEFAULT NULL,
  `role` varchar(50) DEFAULT NULL,
  `error` text,
  `timestamp` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_logs`
--

LOCK TABLES `login_logs` WRITE;
/*!40000 ALTER TABLE `login_logs` DISABLE KEYS */;
INSERT INTO `login_logs` VALUES (1,'allan',0,NULL,'MedicalLabSystem.login_callback() got an unexpected keyword argument \'admin_level\'','2024-11-01 05:53:26'),(2,'allan',1,'admin',NULL,'2024-11-01 06:09:31'),(3,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 06:10:12'),(4,'allan',1,'admin',NULL,'2024-11-01 06:14:28'),(5,'allan',1,'admin',NULL,'2024-11-01 06:15:00'),(6,'allan',1,'admin',NULL,'2024-11-01 06:30:07'),(7,'allan',1,'admin',NULL,'2024-11-01 06:42:25'),(8,'allan',1,'admin',NULL,'2024-11-01 06:42:47'),(9,'allan',1,'admin',NULL,'2024-11-01 06:45:14'),(10,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 06:46:39'),(11,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:08:31'),(12,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:13:39'),(13,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:16:53'),(14,'allan',1,'admin',NULL,'2024-11-01 07:17:13'),(15,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:22:43'),(16,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:27:02'),(17,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:30:54'),(18,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:36:47'),(19,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:37:29'),(20,'allan',1,'admin',NULL,'2024-11-01 07:39:01'),(21,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 07:39:19'),(22,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 10:42:42'),(23,'allan',1,'admin',NULL,'2024-11-01 10:43:42'),(24,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 10:43:54'),(25,'allan',1,'admin',NULL,'2024-11-01 10:49:22'),(26,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 10:51:16'),(27,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 11:00:39'),(28,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 11:21:12'),(29,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 11:24:11'),(30,'SuperAdmin',1,'superadmin',NULL,'2024-11-01 11:26:05');
/*!40000 ALTER TABLE `login_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_tests`
--

DROP TABLE IF EXISTS `patient_tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_tests` (
  `patient_id` varchar(20) NOT NULL,
  `test_id` int NOT NULL,
  PRIMARY KEY (`patient_id`,`test_id`),
  KEY `patient_tests_ibfk_2` (`test_id`),
  CONSTRAINT `patient_tests_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `patient_tests_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`test_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_tests`
--

LOCK TABLES `patient_tests` WRITE;
/*!40000 ALTER TABLE `patient_tests` DISABLE KEYS */;
INSERT INTO `patient_tests` VALUES ('LLP0001',1),('LLP0002',1),('LLP0003',1),('LLP0004',1),('LLP0005',1),('LLP0006',1),('LLP0007',1),('LLP0008',1),('LLP0009',1),('LLP0005',2),('LLP0006',2),('LLP0008',3),('LLP0008',7);
/*!40000 ALTER TABLE `patient_tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` varchar(20) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `dob` date NOT NULL,
  `age` int NOT NULL,
  `address` varchar(255) NOT NULL,
  `medical_history` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`),
  UNIQUE KEY `phone` (`phone_number`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES ('LLP0001','0700000000','Irynn Nakacwa','Female','1992-10-21',32,'Kampala','','2024-10-26 14:59:06'),('LLP0002','0779695589','Monica Mbabazi','Female','2010-10-20',14,'Kyaliwajjala','','2024-10-26 15:13:21'),('LLP0003','1234567890','Demo Patient','Male','1990-01-01',30,'123 Demo Street','Sample medical history data.','2024-10-26 15:29:03'),('LLP0004','0700124564','Juliet Nalukenge','Female','1997-10-24',27,'Buto, Bweyogerere, Wakiso','No Medical History','2024-10-26 16:28:32'),('LLP0005','0779695590','Johnson Alinda Marvin','Male','1991-10-25',33,'Kampala','Normal over the past 5 days.','2024-10-26 18:40:27'),('LLP0006','+256788084498','Ambrose Ssebayiga','Male','1983-10-12',41,'Namboole Central, Wakiso','Sickly in the past 2 weeks, with mild body temperature, runny nose, severe headache and nausea.','2024-10-29 17:01:02'),('LLP0007','0706050044','Hellen Nassiwa','Female','2002-06-19',22,'Kira Municipality','Sickly over the past 3 weeks','2024-10-29 17:32:33'),('LLP0008','0788809890','Alex Mubiru','Male','1965-05-19',59,'Kampala','No medical History','2024-10-29 18:04:36'),('LLP0009','0784567848','Anne Mary','Female','1999-09-10',25,'Namboole','Heavy Headache, Nausea, Vomiting, Blood stained stools','2024-10-29 18:13:53');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`Admin`@`localhost`*/ /*!50003 TRIGGER `format_patient_id` BEFORE INSERT ON `patients` FOR EACH ROW BEGIN
    DECLARE new_id INT;

    
    SELECT COALESCE(MAX(CAST(SUBSTRING(patient_id, 6) AS UNSIGNED)), 0) INTO new_id FROM patients;

    
    SET new_id = new_id + 1;

    
    SET NEW.patient_id = CONCAT('LL-P', LPAD(new_id, 4, '0'));
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`Admin`@`localhost`*/ /*!50003 TRIGGER `before_insert_patients` BEFORE INSERT ON `patients` FOR EACH ROW BEGIN
    DECLARE max_id INT;
    DECLARE next_id INT;
    DECLARE new_patient_id VARCHAR(20);

    
    SELECT COALESCE(MAX(CAST(SUBSTRING(patient_id, LENGTH('LL-P') + 1) AS UNSIGNED)), 0) INTO max_id
    FROM patients;

    
    SET next_id = max_id + 1;

    
    SET new_patient_id = CONCAT('LLP', LPAD(next_id, 4, '0'));

    
    SET NEW.patient_id = new_patient_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `results`
--

DROP TABLE IF EXISTS `results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` varchar(20) DEFAULT NULL,
  `test_id` int NOT NULL,
  `status` varchar(10) NOT NULL,
  `description` text NOT NULL,
  `test_date` date NOT NULL,
  `doctor_technician` varchar(255) NOT NULL,
  `comments` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `results_ibfk_2` (`test_id`),
  KEY `results_ibfk_1` (`patient_id`),
  CONSTRAINT `results_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `results_ibfk_2` FOREIGN KEY (`test_id`) REFERENCES `tests` (`test_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `results`
--

LOCK TABLES `results` WRITE;
/*!40000 ALTER TABLE `results` DISABLE KEYS */;
INSERT INTO `results` VALUES (1,'LLP0002',1,'Normal','Normal Results\n','2024-10-10','Dr. Annet Moses','Follow prescriptions.\n','2024-10-26 15:15:15'),(2,'LLP0004',1,'Positive','High Fever and requires to start medication as soon as possible.\n','2024-10-25','Dr. Annet Kyomuhangi','Please, follow as prescribed on your patient report.\n','2024-10-26 16:30:52'),(3,'LLP0005',1,'Positive','Tests returned positive, but treated as it\'s still early stages.\n','2024-10-17','Dr. Amos W','Take plenty of Water, and follow medical prescriptions.\n','2024-10-26 19:08:53'),(4,'LLP0005',2,'Negative','No typhoid fever signs and virus upon anology.\n','2024-10-17','Dr. Amos W','Follow as prescribed, and please follow checkouts with your Doctor.\n','2024-10-26 19:10:33'),(5,'LLP0006',1,'Positive','Malaria tests were positive after blood sample was tested.\n','2024-10-10','Dr. Anne Kobusingye','Follow doctor\'s prescriptions as described in patient report.\n','2024-10-29 17:02:56'),(6,'LLP0006',2,'Positive','Positive for Typhoid Fever tests.\n','2024-10-10','Dr. Anne Kobusingye','Respond to medication as soon as possible!!\n','2024-10-29 17:04:20'),(7,'LLP0007',1,'Negative','Negative results for malaria tests\n','2024-10-10','Dr. Alfred Moses','Please, follow prescriptions.\n','2024-10-29 17:33:48'),(8,'LLP0008',1,'Negative','Malaria tests returned negative.\n','2024-10-10','Dr. Amos Wekesa','Take enough fluids!!!\n','2024-10-29 18:06:49'),(9,'LLP0008',3,'Positive','HIV/AIDS results positive.\n','2024-10-10','Dr. Anne Kyomuhangi','Please, follow your prescriptions by the doctor. And follow your medication schedule\n','2024-10-29 18:08:42'),(10,'LLP0008',7,'Negative','Results returned negative.\n','2024-10-10','Dr. Amos Wekesa','Carry out regular exercises and have a better diet.\n','2024-10-29 18:10:02');
/*!40000 ALTER TABLE `results` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) NOT NULL,
  `permissions` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Super Administrator','Add, Modify, Delete Users; Configure LIS; Set Policies; Generate Reports; Ensure Compliance; Implement QA Programs'),(2,'Administrator','Add, Modify, Delete Users; Manage Daily Operations; Generate Reports; Implement QA Protocols; Manage Inventory'),(3,'Clinical Officer','Add Patient Records; Modify Patient Records; View Patient Records; Perform Laboratory Tests; Communicate Results; Implement QA Checks');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_settings`
--

DROP TABLE IF EXISTS `system_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_settings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `setting_key` varchar(255) NOT NULL,
  `setting_value` text,
  `description` text,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `updated_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `setting_key` (`setting_key`),
  KEY `updated_by` (`updated_by`),
  CONSTRAINT `system_settings_ibfk_1` FOREIGN KEY (`updated_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_settings`
--

LOCK TABLES `system_settings` WRITE;
/*!40000 ALTER TABLE `system_settings` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tests`
--

DROP TABLE IF EXISTS `tests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tests` (
  `test_id` int NOT NULL AUTO_INCREMENT,
  `test_name` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`test_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tests`
--

LOCK TABLES `tests` WRITE;
/*!40000 ALTER TABLE `tests` DISABLE KEYS */;
INSERT INTO `tests` VALUES (1,'Malaria','Carry out a blood smear microscopy test is where a small sample of blood is taken from a patient and sent to a laboratory to be examined under a microscope.'),(2,'Typhoid Fever','Test patient stools for possible germs and viruses under a microscope.'),(3,'HIV/AIDS','AIDS Virus tests carried out on patient blood samples.'),(7,'STI AB+','Sexually Transmiotted Infections testing and Treatment'),(8,'HBP','HPB disease spreads faster and faster.');
/*!40000 ALTER TABLE `tests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(100) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('superadmin','admin','user') DEFAULT 'user',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `preferences` json DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `email_2` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Super Administrator','superadmin@medlab.com','+256743189126','SuperAdmin','$2y$10$oyDk/ss3IKl7TE5651MYeuH5g8KpQyp1DEgSXbweeXRvmDa0Vu1GO','superadmin',1,'2024-10-31 22:54:16','2024-10-31 22:54:16',NULL,NULL,'456 Admin Ave','{}'),(2,'Allan Patrick','allanpatrick@gmail.com','0704566244','allan','$2b$12$5/5e7mS5gyrg9OEW2AH1eeCyPcRNbdQNRujZCRPm9/bjnMTSLigse','admin',1,'2024-10-31 23:02:42','2024-10-31 23:02:42',NULL,'uploads/profile_pictures/profile_20241031_230128.jpg','Kampala','{\"dark_mode\": true, \"newsletter\": false, \"notifications\": false}');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-01 14:26:08
