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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ce`
--

LOCK TABLES `Ce` WRITE;
/*!40000 ALTER TABLE `Ce` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Ce_total`
--

LOCK TABLES `Ce_total` WRITE;
/*!40000 ALTER TABLE `Ce_total` DISABLE KEYS */;
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
  `host_work_status` varchar(64) NOT NULL,
  `host_code` varchar(64) NOT NULL,
  `host_ip_address` varchar(64) NOT NULL,
  PRIMARY KEY (`host_id`),
  KEY `node_id` (`node_id`),
  CONSTRAINT `Host_ibfk_1` FOREIGN KEY (`node_id`) REFERENCES `Node` (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Host`
--

LOCK TABLES `Host` WRITE;
/*!40000 ALTER TABLE `Host` DISABLE KEYS */;
INSERT INTO `Host` VALUES (1,1,'edge','offline','GW01','');
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
  `isp` varchar(64) NOT NULL,
  PRIMARY KEY (`node_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Node`
--

LOCK TABLES `Node` WRITE;
/*!40000 ALTER TABLE `Node` DISABLE KEYS */;
INSERT INTO `Node` VALUES (1,'bj01','cncc');
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
  `pe_work_status` varchar(64) NOT NULL,
  `pe_default_port_ip` varchar(64) NOT NULL,
  `pe_vlan_port_ip` varchar(64) NOT NULL,
  `pe_vpn_server_ip` varchar(64) NOT NULL,
  `pe_vpn_ip_range_start` varchar(64) NOT NULL,
  `pe_vpn_ip_range_end` varchar(64) NOT NULL,
  `pe_vpn_access_port` int(11) NOT NULL,
  `virtual_network_number` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `host_id` (`host_id`),
  CONSTRAINT `Pe_ibfk_1` FOREIGN KEY (`host_id`) REFERENCES `Host` (`host_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pe`
--

LOCK TABLES `Pe` WRITE;
/*!40000 ALTER TABLE `Pe` DISABLE KEYS */;
INSERT INTO `Pe` VALUES (1,1,'PE01','public','error','172.31.254.253','172.30.254.4','172.31.51.2','172.22.1.130','172.22.1.138',10001,1001),(2,1,'PE02','public','error','172.31.254.253','172.30.254.5','172.31.51.3','172.22.1.139','172.22.1.147',10002,1002);
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
  `host_work_status` varchar(64) NOT NULL,
  `host_ip_address` varchar(64) NOT NULL,
  `node_code` varchar(64) NOT NULL,
  `pe_code` varchar(64) NOT NULL,
  `pe_type` varchar(64) NOT NULL,
  `pe_work_status` varchar(64) NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pe_total`
--

LOCK TABLES `Pe_total` WRITE;
/*!40000 ALTER TABLE `Pe_total` DISABLE KEYS */;
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

-- Dump completed on 2017-07-27 18:38:33
