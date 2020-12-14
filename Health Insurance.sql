DROP DATABASE IF EXISTS `Health_Insurance`;
CREATE DATABASE `Health_Insurance`; 
USE `Health_Insurance`;

SET NAMES utf8mb4 ;
SET character_set_client = utf8mb4 ;



CREATE TABLE `customers` (
  `Customer_id` int NOT NULL AUTO_INCREMENT,
  `First_name` varchar(50) NOT NULL,
  `Last_name` varchar(50) NOT NULL,
  `Birth_date` date DEFAULT NULL ,
  `Phone` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20201201 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `customers` VALUES (1,'Babara','MacCaffrey','1986-03-28','781-932-9754');
INSERT INTO `customers` VALUES (2,'Ines','Brushfield','1986-04-13','804-427-9456');
INSERT INTO `customers` VALUES (3,'Freddi','Boagey','1955-02-07','719-724-7869');
INSERT INTO `customers` VALUES (4,'Ambur','Roseburgh','1974-04-14','407-231-8017');
INSERT INTO `customers` VALUES (5,'Clemmie','Betchley','1973-11-07',NULL);
INSERT INTO `customers` VALUES (6,'Elka','Twiddell','1991-09-04','312-480-8498');
INSERT INTO `customers` VALUES (7,'Ilene','Dowson','1964-08-30','615-641-4759');
INSERT INTO `customers` VALUES (8,'Thacher','Naseby','1993-07-17','941-527-3977');
INSERT INTO `customers` VALUES (9,'Romola','Rumgay','1992-05-23','559-181-3744');
INSERT INTO `customers` VALUES (10,'Levy','Mynett','1969-10-13','404-246-3370');

CREATE TABLE `Address` (
  `Customer_id` int NOT NULL,
  `DoorNo.` varchar(10) NOT NULL,
  `Street/Area` varchar(50) NOT NULL,
  `City` varchar(50) NOT NULL,
  `State` varchar(3) NOT NULL,
  PRIMARY KEY (`Customer_id`),
  KEY `fk_Address_customers_idx` (`Customer_id`),
  CONSTRAINT `fk_Address_customers` FOREIGN KEY (`Customer_id`) REFERENCES `customers` (`Customer_id`) ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `Insurance_Policy` (
  `PolicyID` varchar(10) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Type` varchar(50) NOT NULL,
  `Premium` int,
  `InsuredAmount` int NOT NULL,
  PRIMARY KEY (`PolicyID`)
  ) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
  
INSERT INTO `Insurance_Policy` VALUES (1,'CardioSure','Health',4000,400000);
INSERT INTO `Insurance_Policy` VALUES (2,'SportFit','Health',2000,200000);
INSERT INTO `Insurance_Policy` VALUES (3,'Medicall','Health',2500,250000);

CREATE TABLE `Holds` (
  `Customer_id` int NOT NULL,
  `PolicyID` varchar(10) NOT NULL,
  `Policy_number` int NOT NULL AUTO_INCREMENT,
  `Start_date` date NOT NULL,
  `Renewal_date` date DEFAULT NULL,
  PRIMARY KEY (`Policy_number`),
  KEY `fk_Holds_customers_idx` (`Customer_id`),
  KEY `fk_Holds_insurance_policy_idx` (`PolicyID`),
  CONSTRAINT `fk_Holds_customers` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`customer_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_Holds_insurance_policy` FOREIGN KEY (`PolicyID`) REFERENCES `insurance_policy` (`PolicyID`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Claims` (
  `Customer_id` int NOT NULL,
  `PolicyID` varchar(10) NOT NULL,
  `Policy_number` int NOT NULL,
  `Issued_amount` int NOT NULL,
  `Issued_year` year,
  PRIMARY KEY (`Policy_number`,`Issued_year`),
  KEY `fk_Claims_customers_idx` (`Customer_id`),
  KEY `fk_Claims_insurance_policy_idx` (`PolicyID`),
  KEY `fk_Claims_Holds_idx` (`Policy_number`),
  CONSTRAINT `fk_Claims_customers` FOREIGN KEY (`Customer_id`) REFERENCES `customers` (`Customer_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_Claims_insurance_policy` FOREIGN KEY (`PolicyID`) REFERENCES `insurance_policy` (`PolicyID`) ON UPDATE CASCADE,
  CONSTRAINT `fk_Claims_Holds` FOREIGN KEY (`Policy_number`) REFERENCES `Holds` (`Policy_number`) ON UPDATE CASCADE
  ) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
  
CREATE TABLE `Hospital` (
  `Name` varchar(20) NOT NULL,
  `Hospital_id` int NOT NULL,
  `Patient_id` int NOT NULL,
  `BillAmount` int NOT NULL,
  PRIMARY KEY (`Hospital_id`),
  KEY `fk_Hospital_customers_idx` (`patient_id`),
  CONSTRAINT `fk_Hospital_customers` FOREIGN KEY (`Patient_id`) REFERENCES `customers` (`Customer_id`) ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `DiagnosedBy` (
  `Disease` varchar(20) NOT NULL,
  `Hospital_id` int NOT NULL,
  `Customer_id` int NOT NULL,
  PRIMARY KEY (`HospItal_id`,`Customer_id`),
  KEY `fk_DiagnosedBy_customers_idx` (`Customer_id`),
  KEY `fk_DiagnosedBy_Hospital_idx` (`Hospital_id`),
  CONSTRAINT `fk_DiagnosedBy_customers` FOREIGN KEY (`Customer_id`) REFERENCES `customers` (`Customer_id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_DiagnosedBy_Hospital` FOREIGN KEY (`Hospital_id`) REFERENCES `Hospital` (`Hospital_id`) ON UPDATE CASCADE
) ENGINE=InnoDB CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
