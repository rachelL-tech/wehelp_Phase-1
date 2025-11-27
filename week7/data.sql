-- MySQL dump 10.13  Distrib 8.4.7, for macos15.4 (arm64)
--
-- Host: localhost    Database: website
-- ------------------------------------------------------
-- Server version	8.4.7

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
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `member` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `follower_count` int unsigned NOT NULL DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member`
--

LOCK TABLES `member` WRITE;
/*!40000 ALTER TABLE `member` DISABLE KEYS */;
INSERT INTO `member` VALUES (1,'test2','test@test.com','test',3,'2025-11-13 07:43:30'),(2,'Rachel','Rachel@test.com','pw1',4,'2025-11-13 07:43:30'),(3,'Monica','Monica@test.com','pw2',7,'2025-11-13 07:43:30'),(4,'Chandler','Chandler@test.com','pw3',2,'2025-11-13 07:43:30'),(5,'恐龍','Ross@test.com','pw4',1,'2025-11-13 07:43:30'),(8,'王小姐','wang@abc.com','wang',0,'2025-11-21 10:20:17'),(9,'蔡先生','tsai@abc.com','Tsai',0,'2025-11-21 10:25:08');
/*!40000 ALTER TABLE `member` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `message`
--

DROP TABLE IF EXISTS `message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `message` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `member_id` int unsigned NOT NULL,
  `content` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `like_count` int unsigned NOT NULL DEFAULT '0',
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `member_id` (`member_id`),
  CONSTRAINT `message_ibfk_1` FOREIGN KEY (`member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `message`
--

LOCK TABLES `message` WRITE;
/*!40000 ALTER TABLE `message` DISABLE KEYS */;
INSERT INTO `message` VALUES (1,1,'I am just an example.',2,'2025-11-13 09:28:17'),(2,2,'I am Gonna Go Get One Of Those Job Things.',10,'2025-11-13 09:28:17'),(3,2,'Who is FICA? Why is He Getting All My Money?',5,'2025-11-13 09:28:17'),(4,2,'I Can Be Very Generous, Or Very Stingy.',7,'2025-11-13 09:28:17'),(5,3,'Welcome to the real world! It sucks. You are gonna love it.',20,'2025-11-13 09:28:17'),(6,3,'I know!',25,'2025-11-13 09:28:17'),(7,3,'He could hear me!',8,'2025-11-13 09:28:17'),(8,4,'Could we BE more white trash?',9,'2025-11-13 09:28:17'),(9,4,'Ding dong, the psycho is gone!',7,'2025-11-13 09:28:17'),(10,4,'Hi, I am Chandler. I make jokes when I am uncomfortable.',35,'2025-11-13 09:28:17'),(11,5,'Mississipilessly?',33,'2025-11-13 09:28:17'),(12,5,'O is for Oh wow.',24,'2025-11-13 09:28:17'),(13,5,'Pivot! Pivot! Pivot!',34,'2025-11-13 09:28:17'),(15,5,'We were on a break!',0,'2025-11-21 10:06:06'),(16,3,'這是中文',0,'2025-11-21 10:14:03');
/*!40000 ALTER TABLE `message` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `query`
--

DROP TABLE IF EXISTS `query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `query` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `target_member_id` int unsigned NOT NULL,
  `searcher_member_id` int unsigned NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `target_member_id` (`target_member_id`),
  KEY `searcher_member_id` (`searcher_member_id`),
  CONSTRAINT `query_ibfk_1` FOREIGN KEY (`target_member_id`) REFERENCES `member` (`id`),
  CONSTRAINT `query_ibfk_2` FOREIGN KEY (`searcher_member_id`) REFERENCES `member` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `query`
--

LOCK TABLES `query` WRITE;
/*!40000 ALTER TABLE `query` DISABLE KEYS */;
INSERT INTO `query` VALUES (1,4,5,'2025-11-26 23:55:31'),(2,4,5,'2025-11-26 23:59:07'),(3,4,5,'2025-11-26 23:59:11'),(4,5,4,'2025-11-27 00:10:57'),(5,5,4,'2025-11-27 00:11:01'),(6,5,4,'2025-11-27 00:11:02'),(7,5,4,'2025-11-27 00:11:02'),(8,5,4,'2025-11-27 00:11:03'),(9,5,4,'2025-11-27 00:11:04'),(10,5,4,'2025-11-27 00:11:05'),(11,5,4,'2025-11-27 00:11:05'),(12,5,4,'2025-11-27 00:11:05'),(13,5,4,'2025-11-27 00:11:05'),(14,5,4,'2025-11-27 00:11:06'),(15,5,4,'2025-11-27 00:11:06'),(16,5,4,'2025-11-27 00:11:09'),(17,5,4,'2025-11-27 00:11:09'),(18,5,4,'2025-11-27 00:11:09'),(19,5,4,'2025-11-27 00:11:10'),(20,5,4,'2025-11-27 00:11:10');
/*!40000 ALTER TABLE `query` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 16:57:37
