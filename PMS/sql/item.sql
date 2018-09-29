/*
Target Server Type    : MYSQL
Target Server Version : 80012
File Encoding         : 65001

Date: 2018-08-30 20:29:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for item
-- ----------------------------
DROP TABLE IF EXISTS `item`;
CREATE TABLE `item` (
  `id` bigint(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `summary` varchar(255) DEFAULT NULL,
  `content` longtext,
  `category` varchar(255) DEFAULT NULL COMMENT '分类',
  `status` int(255) DEFAULT '1' COMMENT '状态：显示、影藏',
  `sequence` int(11) DEFAULT '1',
  `path_file` varchar(255) DEFAULT '',
  `path_thumb` varchar(255) DEFAULT '',
  `path_origin` varchar(255) DEFAULT NULL COMMENT '原始图片地址',
  `attachment_list` text COMMENT '附件',
  `url` varchar(255) DEFAULT NULL,
  `created` varchar(255) DEFAULT NULL,
  `modified` varchar(255) DEFAULT NULL,
  `visit_count` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='条目信息， 条目是文件的使用者';
