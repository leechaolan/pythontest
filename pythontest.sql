-- MySQL dump 10.13  Distrib 5.6.37, for Linux (x86_64)
--
-- Host: localhost    Database: pythontest
-- ------------------------------------------------------
-- Server version	5.6.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Ce`
--

DROP TABLE IF EXISTS `Ce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `virtual_network_number` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `customer_code` varchar(64) NOT NULL,
  `access_instance_id` int(11) NOT NULL,
  `tunnel_type` varchar(64) NOT NULL,
  `vpn_cli_ip` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `work_mode` varchar(64) NOT NULL,
  `pe_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `pe_id` (`pe_id`),
  CONSTRAINT `Ce_ibfk_1` FOREIGN KEY (`pe_id`) REFERENCES `Pe` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ce`
--

LOCK TABLES `Ce` WRITE;
/*!40000 ALTER TABLE `Ce` DISABLE KEYS */;
INSERT INTO `Ce` VALUES (1,1003,1,'algoblu',1,'openvpn','1.2.3.4','u1507604085','ub9vdtdf','master',3),(2,1003,1,'algoblu',2,'openvpn','4.3.2.1','u1507604086','6j6xuy9o','slave',17),(3,1003,1,'algoblu',3,'openvpn','2.2.2.2','u1507604792','07o9x4d7','master',9),(4,1003,1,'algoblu',4,'openvpn','3.3.3.3','u1507604793','5g3up3pt','slave',13);
/*!40000 ALTER TABLE `Ce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Ce_total`
--

DROP TABLE IF EXISTS `Ce_total`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Ce_total` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `virtual_network_number` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `customer_code` varchar(64) NOT NULL,
  `access_instance_id` int(11) NOT NULL,
  `tunnel_type` varchar(64) NOT NULL,
  `vpn_cli_ip` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `work_mode` varchar(64) NOT NULL,
  `pe_code` varchar(64) NOT NULL,
  `ce_table_md5sum` varchar(32) NOT NULL,
  `ce_row_md5sum` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ce_total`
--

LOCK TABLES `Ce_total` WRITE;
/*!40000 ALTER TABLE `Ce_total` DISABLE KEYS */;
INSERT INTO `Ce_total` VALUES (1,1003,1,'algoblu',1,'openvpn','1.2.3.4','u1507604085','ub9vdtdf','master','beijing_gw01_pvt01','1ea5560fd1fad1fa383e5e72a4c2ae81','f4c7133742ba3f157231057351c29aad'),(2,1003,1,'algoblu',2,'openvpn','4.3.2.1','u1507604086','6j6xuy9o','slave','tianjin_gw01_pvt01','1ea5560fd1fad1fa383e5e72a4c2ae81','80f0789664f0f940bd25c334ae9daf29'),(3,1003,1,'algoblu',3,'openvpn','2.2.2.2','u1507604792','07o9x4d7','master','shanghai_gw01_pvt01','1ea5560fd1fad1fa383e5e72a4c2ae81','53215646948699bdf073332bdd9b9e1e'),(4,1003,1,'algoblu',4,'openvpn','3.3.3.3','u1507604793','5g3up3pt','slave','guangzhou_gw01_pvt01','1ea5560fd1fad1fa383e5e72a4c2ae81','18670c1a12a362c89a51f810bfcb54cb');
/*!40000 ALTER TABLE `Ce_total` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Host`
--

DROP TABLE IF EXISTS `Host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Host` (
  `host_id` int(11) NOT NULL AUTO_INCREMENT,
  `node_id` int(11) NOT NULL,
  `host_type` varchar(64) NOT NULL,
  `host_code` varchar(64) NOT NULL,
  `host_ip_address` varchar(1024) NOT NULL DEFAULT '',
  `host_work_status` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`host_id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `Host_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `Node` (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Host`
--

LOCK TABLES `Host` WRITE;
/*!40000 ALTER TABLE `Host` DISABLE KEYS */;
INSERT INTO `Host` VALUES (1,1,'edge','beijing_gw01','[{\"operator_code\": \"CUCC\", \"host_ip_address\": \"201.1.1.2\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"201.1.1.3\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"201.1.1.4\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"201.1.1.5\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"201.1.1.6\"}]',''),(2,2,'edge','shanghai_gw01','[{\"operator_code\": \"CTCC\", \"host_ip_address\": \"202.1.1.2\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"202.1.1.3\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"202.1.1.4\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"202.1.1.5\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"202.1.1.6\"}]',''),(3,3,'edge','guangzhou_gw01','[{\"operator_code\": \"CTCC\", \"host_ip_address\": \"203.1.1.2\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"203.1.1.3\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"203.1.1.4\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"203.1.1.5\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"203.1.1.6\"}]',''),(4,4,'edge','tianjin_gw01','[{\"operator_code\": \"CUCC\", \"host_ip_address\": \"204.1.1.2\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"204.1.1.3\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"204.1.1.4\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"204.1.1.5\"}, {\"operator_code\": \"CUCC\", \"host_ip_address\": \"204.1.1.6\"}]',''),(5,5,'edge','chongqing_gw01','[{\"operator_code\": \"CTCC\", \"host_ip_address\": \"205.1.1.2\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"205.1.1.3\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"205.1.1.4\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"205.1.1.5\"}, {\"operator_code\": \"CTCC\", \"host_ip_address\": \"205.1.1.6\"}]','');
/*!40000 ALTER TABLE `Host` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Node`
--

DROP TABLE IF EXISTS `Node`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Node` (
  `node_id` int(11) NOT NULL AUTO_INCREMENT,
  `node_code` varchar(64) NOT NULL,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Node`
--

LOCK TABLES `Node` WRITE;
/*!40000 ALTER TABLE `Node` DISABLE KEYS */;
INSERT INTO `Node` VALUES (1,'beijing'),(2,'shanghai'),(3,'guangzhou'),(4,'tianjin'),(5,'chongqing');
/*!40000 ALTER TABLE `Node` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pe`
--

DROP TABLE IF EXISTS `Pe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_id` int(11) NOT NULL,
  `pe_code` varchar(64) NOT NULL,
  `pe_type` varchar(64) NOT NULL,
  `pe_default_port_ip` varchar(64) NOT NULL,
  `pe_vlan_port_ip` varchar(64) NOT NULL,
  `pe_vpn_server_ip` varchar(64) NOT NULL,
  `pe_vpn_ip_range_start` varchar(64) NOT NULL,
  `pe_vpn_ip_range_end` varchar(64) NOT NULL,
  `pe_vpn_access_port` int(11) NOT NULL,
  `virtual_network_number` int(11) NOT NULL,
  `pe_work_status` varchar(64) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `Pe_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `Host` (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pe`
--

LOCK TABLES `Pe` WRITE;
/*!40000 ALTER TABLE `Pe` DISABLE KEYS */;
INSERT INTO `Pe` VALUES (1,1,'beijing_gw01_mon','monitor','10.1.1.2','172.30.1.2','','','',0,0,''),(2,1,'beijing_gw01_pub01','public','10.1.1.3','172.30.1.3','201.1.1.2','172.1.1.2','172.1.1.254',10000,1000,''),(3,1,'beijing_gw01_pvt01','private','10.1.1.4','172.30.1.4','201.1.1.3','172.1.2.2','172.1.2.254',10000,1000,''),(4,1,'beijing_gw01_pvt02','private','10.1.1.5','172.30.1.5','201.1.1.4','172.1.3.2','172.1.3.254',10000,1000,''),(5,1,'beijing_gw01_pub02','public','10.1.1.4','172.30.1.1','201.1.1.3','172.25.1.2','172.25.1.254',10001,1000,''),(6,1,'beijing_gw01_pvt03','private','10.1.1.2','172.30.1.4','201.1.1.4','172.1.22.2','172.25.23.254',13000,1000,''),(7,2,'shanghai_gw01_mon','monitor','10.1.2.2','172.30.2.2','','','',0,0,''),(8,2,'shanghai_gw01_pub01','public','10.1.2.3','172.30.2.3','202.1.1.2','172.1.4.2','172.1.4.254',10000,1000,''),(9,2,'shanghai_gw01_pvt01','private','10.1.2.4','172.30.2.4','202.1.1.3','172.1.5.2','172.1.5.254',10000,1000,''),(10,2,'shanghai_gw01_pvt02','private','10.1.2.5','172.30.2.5','202.1.1.4','172.1.6.2','172.1.6.254',10000,1000,''),(11,3,'guangzhou_gw01_mon','monitor','10.1.3.2','172.30.3.2','','','',0,0,''),(12,3,'guangzhou_gw01_pub01','public','10.1.3.3','172.30.3.3','203.1.1.2','172.1.7.2','172.1.7.254',10000,1000,''),(13,3,'guangzhou_gw01_pvt01','private','10.1.3.4','172.30.3.4','203.1.1.3','172.1.8.2','172.1.8.254',10000,1000,''),(14,3,'guangzhou_gw01_pvt02','private','10.1.3.5','172.30.3.5','203.1.1.4','172.1.9.2','172.1.9.254',10000,1000,''),(15,4,'tianjin_gw01_mon','monitor','10.1.4.2','172.30.4.2','','','',0,0,''),(16,4,'tianjin_gw01_pub01','public','10.1.4.3','172.30.4.3','204.1.1.2','172.1.10.2','172.1.10.254',10000,1000,''),(17,4,'tianjin_gw01_pvt01','private','10.1.4.4','172.30.4.4','204.1.1.3','172.1.11.2','172.1.11.254',10000,1000,''),(18,4,'tianjin_gw01_pvt02','private','10.1.4.5','172.30.4.5','204.1.1.4','172.1.12.2','172.1.12.254',10000,1000,''),(19,5,'congqing_gw01_mon','monitor','10.1.5.2','172.30.5.2','','','',0,0,''),(20,5,'congqing_gw01_pub01','public','10.1.5.3','172.30.5.3','205.1.1.2','172.1.13.2','172.1.13.254',10000,1000,''),(21,5,'congqing_gw01_pvt01','private','10.1.5.4','172.30.5.4','205.1.1.3','172.1.14.2','172.1.14.254',10000,1000,''),(22,5,'congqing_gw01_pvt02','private','10.1.5.5','172.30.5.5','205.1.1.4','172.1.15.2','172.1.15.254',10000,1000,'');
/*!40000 ALTER TABLE `Pe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pe_total`
--

DROP TABLE IF EXISTS `Pe_total`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pe_total` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host_type` varchar(64) NOT NULL,
  `host_ip_address` varchar(1024) NOT NULL DEFAULT '',
  `node_code` varchar(64) NOT NULL,
  `pe_code` varchar(64) NOT NULL,
  `pe_type` varchar(64) NOT NULL,
  `pe_default_port_ip` varchar(64) NOT NULL,
  `pe_vlan_port_ip` varchar(64) NOT NULL,
  `pe_vpn_server_ip` varchar(64) NOT NULL,
  `pe_vpn_ip_range_start` varchar(64) NOT NULL,
  `pe_vpn_ip_range_end` varchar(64) NOT NULL,
  `pe_vpn_access_port` int(11) NOT NULL,
  `virtual_network_number` int(11) NOT NULL,
  `pe_table_md5sum` varchar(32) NOT NULL,
  `host_code` varchar(64) NOT NULL,
  `pe_row_md5sum` varchar(32) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pe_total`
--

LOCK TABLES `Pe_total` WRITE;
/*!40000 ALTER TABLE `Pe_total` DISABLE KEYS */;
INSERT INTO `Pe_total` VALUES (1,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_mon','monitor','10.1.1.2','172.30.1.2','','','',0,0,'5b76843f20aeb4f212520178038948cd','beijing_gw01','51546f8899f9b1ffe13e9aa6a2b06608'),(2,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_pub01','public','10.1.1.3','172.30.1.3','201.1.1.2','172.1.1.2','172.1.1.254',10000,1000,'5b76843f20aeb4f212520178038948cd','beijing_gw01','2a25f8becfe170affc47977b07d2fa6d'),(3,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_pvt01','private','10.1.1.4','172.30.1.4','201.1.1.3','172.1.2.2','172.1.2.254',10000,1000,'5b76843f20aeb4f212520178038948cd','beijing_gw01','3cb3e465cbdb24f4e2a90601fda70bfd'),(4,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_pvt02','private','10.1.1.5','172.30.1.5','201.1.1.4','172.1.3.2','172.1.3.254',10000,1000,'5b76843f20aeb4f212520178038948cd','beijing_gw01','75aad9851712599c58589016384185f3'),(5,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_pub02','public','10.1.1.4','172.30.1.1','201.1.1.3','172.25.1.2','172.25.1.254',10001,1000,'5b76843f20aeb4f212520178038948cd','beijing_gw01','d9658128ebd403683ad7f54c216ae13a'),(6,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'201.1.1.6\'}]','beijing','beijing_gw01_pvt03','private','10.1.1.2','172.30.1.4','201.1.1.4','172.1.22.2','172.25.23.254',13000,1000,'5b76843f20aeb4f212520178038948cd','beijing_gw01','d34c6b9f7c2f5f11e80c281b6ee29ecb'),(7,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}]','shanghai','shanghai_gw01_mon','monitor','10.1.2.2','172.30.2.2','','','',0,0,'5b76843f20aeb4f212520178038948cd','shanghai_gw01','2091fb82503b33f41daac279a5d9df16'),(8,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}]','shanghai','shanghai_gw01_pub01','public','10.1.2.3','172.30.2.3','202.1.1.2','172.1.4.2','172.1.4.254',10000,1000,'5b76843f20aeb4f212520178038948cd','shanghai_gw01','653315ca69608d41cca3418cebf02f96'),(9,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}]','shanghai','shanghai_gw01_pvt01','private','10.1.2.4','172.30.2.4','202.1.1.3','172.1.5.2','172.1.5.254',10000,1000,'5b76843f20aeb4f212520178038948cd','shanghai_gw01','ead7e10769005d5e6ba5ebdb80f7a491'),(10,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'202.1.1.6\'}]','shanghai','shanghai_gw01_pvt02','private','10.1.2.5','172.30.2.5','202.1.1.4','172.1.6.2','172.1.6.254',10000,1000,'5b76843f20aeb4f212520178038948cd','shanghai_gw01','e4103b291a749f57ad67954797e22e29'),(11,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}]','guangzhou','guangzhou_gw01_mon','monitor','10.1.3.2','172.30.3.2','','','',0,0,'5b76843f20aeb4f212520178038948cd','guangzhou_gw01','f9fca82b4c80638884ef993554341d54'),(12,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}]','guangzhou','guangzhou_gw01_pub01','public','10.1.3.3','172.30.3.3','203.1.1.2','172.1.7.2','172.1.7.254',10000,1000,'5b76843f20aeb4f212520178038948cd','guangzhou_gw01','972bbcf9f7be2a76dc12a5b00f20e182'),(13,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}]','guangzhou','guangzhou_gw01_pvt01','private','10.1.3.4','172.30.3.4','203.1.1.3','172.1.8.2','172.1.8.254',10000,1000,'5b76843f20aeb4f212520178038948cd','guangzhou_gw01','7091e68787c70f0ec3f3fc5f4f6094ad'),(14,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'203.1.1.6\'}]','guangzhou','guangzhou_gw01_pvt02','private','10.1.3.5','172.30.3.5','203.1.1.4','172.1.9.2','172.1.9.254',10000,1000,'5b76843f20aeb4f212520178038948cd','guangzhou_gw01','b8cc49dad15c77c47c00a23e5705427b'),(15,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}]','tianjin','tianjin_gw01_mon','monitor','10.1.4.2','172.30.4.2','','','',0,0,'5b76843f20aeb4f212520178038948cd','tianjin_gw01','4f33b41c980724f2a4499eadb5965c7e'),(16,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}]','tianjin','tianjin_gw01_pub01','public','10.1.4.3','172.30.4.3','204.1.1.2','172.1.10.2','172.1.10.254',10000,1000,'5b76843f20aeb4f212520178038948cd','tianjin_gw01','0956a4a19c886adc7d09ece90cdba085'),(17,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}]','tianjin','tianjin_gw01_pvt01','private','10.1.4.4','172.30.4.4','204.1.1.3','172.1.11.2','172.1.11.254',10000,1000,'5b76843f20aeb4f212520178038948cd','tianjin_gw01','a1933b75bab8ef55361b9b3fa0f0f2ea'),(18,'edge','[{\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}, {\'operator_code\': u\'CUCC\', \'host_ip_address\': u\'204.1.1.6\'}]','tianjin','tianjin_gw01_pvt02','private','10.1.4.5','172.30.4.5','204.1.1.4','172.1.12.2','172.1.12.254',10000,1000,'5b76843f20aeb4f212520178038948cd','tianjin_gw01','7353fd00da38eb0783bd40345a2538b7'),(19,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}]','chongqing','congqing_gw01_mon','monitor','10.1.5.2','172.30.5.2','','','',0,0,'5b76843f20aeb4f212520178038948cd','chongqing_gw01','0ececc9a115713e0ab01028a5a8e7b29'),(20,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}]','chongqing','congqing_gw01_pub01','public','10.1.5.3','172.30.5.3','205.1.1.2','172.1.13.2','172.1.13.254',10000,1000,'5b76843f20aeb4f212520178038948cd','chongqing_gw01','64d107d13ee246c055ef99bbdb6af43f'),(21,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}]','chongqing','congqing_gw01_pvt01','private','10.1.5.4','172.30.5.4','205.1.1.3','172.1.14.2','172.1.14.254',10000,1000,'5b76843f20aeb4f212520178038948cd','chongqing_gw01','c222fbee04df7f0f38c5a6addb5c1b84'),(22,'edge','[{\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}, {\'operator_code\': u\'CTCC\', \'host_ip_address\': u\'205.1.1.6\'}]','chongqing','congqing_gw01_pvt02','private','10.1.5.5','172.30.5.5','205.1.1.4','172.1.15.2','172.1.15.254',10000,1000,'5b76843f20aeb4f212520178038948cd','chongqing_gw01','c844878e78d3f583c62af969e0dc3de2');
/*!40000 ALTER TABLE `Pe_total` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-31 18:01:49
