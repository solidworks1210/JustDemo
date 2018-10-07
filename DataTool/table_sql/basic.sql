/*
Navicat MySQL Data Transfer

Source Server         : SDN_MySQL
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : jfgm

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-04-17 22:16:29
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for basic
-- ----------------------------
DROP TABLE IF EXISTS `basic`;
CREATE TABLE `basic` (
  `id` bigint(20) NOT NULL,
  `name_full` varchar(255) DEFAULT NULL,
  `name_short` varchar(255) DEFAULT NULL,
  `seo` varchar(255) DEFAULT NULL,
  `copyright` varchar(255) DEFAULT NULL,
  `icp` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `qq` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `created` varchar(255) DEFAULT NULL,
  `modified` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL COMMENT '条目所在分类',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
