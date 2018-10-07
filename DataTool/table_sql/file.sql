/*
Navicat MySQL Data Transfer

Source Server         : SDN_MySQL
Source Server Version : 50717
Source Host           : localhost:3306
Source Database       : jfgm

Target Server Type    : MYSQL
Target Server Version : 50717
File Encoding         : 65001

Date: 2017-04-17 22:16:56
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for file
-- ----------------------------
DROP TABLE IF EXISTS `file`;
CREATE TABLE `file` (
  `id` bigint(20) DEFAULT NULL COMMENT '毫秒时间',
  `user` varchar(255) DEFAULT NULL COMMENT '使用者',
  `title` varchar(255) DEFAULT NULL COMMENT '文件标题',
  `summary` varchar(255) DEFAULT NULL COMMENT '文件描述',
  `size` bigint(11) DEFAULT NULL COMMENT '文件大小，单位？',
  `suffix` varchar(255) DEFAULT NULL COMMENT '后缀',
  `type` varchar(255) DEFAULT NULL COMMENT '文件格式（完整）',
  `type_a` varchar(255) DEFAULT NULL COMMENT '文件类型 前部',
  `category` varchar(255) DEFAULT NULL COMMENT '使用者所在分类',
  `created` varchar(255) DEFAULT NULL COMMENT '创建时间，时间戳字符串',
  `modified` varchar(255) DEFAULT NULL COMMENT '修改时间，时间戳字符串',
  `category_file` varchar(255) DEFAULT NULL COMMENT '文件类型：原始origin、使用use、缩略图 thumb',
  `path` varchar(255) DEFAULT NULL COMMENT '文件路径'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='新闻对应的文件资源';
