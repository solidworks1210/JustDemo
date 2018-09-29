/*
Target Server Type    : MYSQL
Target Server Version : 80012
File Encoding         : 65001

Date: 2018-08-30 20:29:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` bigint(20) AUTO_INCREMENT COMMENT '自增序列',
  `area` varchar(255) DEFAULT NULL COMMENT '地域',
  `first_name` varchar(255) DEFAULT NULL COMMENT '姓',
  `last_name` varchar(255) DEFAULT NULL COMMENT '名',
  `sex` tinyint DEFAULT 0 COMMENT '性别：0男，1女',
  `company_no` char(8) UNIQUE COMMENT '公司工号',
  `password` char(32) DEFAULT 'e10adc3949ba59abbe56e057f20f883e' COMMENT '密码：至少6位, md5加密，默认：123456',
  `hw_no` char(9) DEFAULT NULL COMMENT '华为工号',
  `phone` varchar(11) DEFAULT NULL COMMENT '手机号',
  `identity_no` char(18) DEFAULT NULL COMMENT '身份证号',
  `address_province` varchar(255) DEFAULT NULL COMMENT '现居住地-省',
  `address_city` varchar(255) DEFAULT NULL COMMENT '现居住地-市',
  `address_detail` varchar(255) DEFAULT NULL COMMENT '现居住地-详细',
  `project_id` int(5) DEFAULT NULL COMMENT '项目编号',
  `position` int(3) DEFAULT NULL COMMENT '岗位编号',
  `entry_date` date DEFAULT NULL COMMENT '入职日期',
  `company_email` varchar(255) DEFAULT NULL COMMENT '公司邮箱',
  `hw_email` varchar(255) DEFAULT NULL COMMENT '华为邮箱',
  `tc_no` char(11) DEFAULT NULL COMMENT 'TC编号',
  `display_no` char(11) DEFAULT NULL COMMENT '显示器编号',
  `birthplace_province` varchar(255) DEFAULT NULL COMMENT '籍贯(省)',
  `birthplace_city` varchar(255) DEFAULT NULL COMMENT '籍贯(市)',
  `emergency_contact` varchar(255) DEFAULT NULL COMMENT '紧急联系人',
  `relationship` int(2) DEFAULT NULL COMMENT '紧急联系人关系: 兄、弟、姐',
  `emergency_contact_phone` varchar(11) DEFAULT NULL COMMENT '紧急联系人电话',
  `date_of_graduate` date DEFAULT NULL COMMENT '毕业日期',
  `school_no` int(5) DEFAULT NULL COMMENT '学校编码',
  `field` int(5) DEFAULT NULL COMMENT '专业名称',
  `is_computer` int(1) DEFAULT 0 COMMENT '是否计算机相关专业: 0 否， 1 是',
  `grade` varchar(14) DEFAULT NULL COMMENT '学历: 小学、初中、高中、专科、本科、硕士、博士',
  `unification_recruitment` int(1) DEFAULT 0 COMMENT '是否统招：0 否，1 是',
  `resignation_date` date DEFAULT NULL COMMENT '公司离职日期',
  `competitor` int(1) DEFAULT 0 COMMENT '是否在友商工作过：0 否，1 是',
  `competitor_resignation_date2` date DEFAULT NULL COMMENT '友商离职日期',
  `auth_group_id` int(3) DEFAULT 1 COMMENT '所在的权限组编号',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='人员信息';

-- ----------------------------
-- Table structure for school
-- ----------------------------
DROP TABLE IF EXISTS `school`;
CREATE TABLE `school` (
  `id` bigint(20) AUTO_INCREMENT COMMENT '自增序列',
  `no` varchar(10) NOT NULL COMMENT '学校编号',
  `name` varchar(255) NOT NULL COMMENT '学校名称',
  `province` varchar(255) NOT NULL COMMENT '学校所在省',
  `city` varchar(255) NOT NULL COMMENT '学校所在市',
  `is_211` int(1) DEFAULT 0 COMMENT '是否211：0 不是， 1 是',
  `is_985` int(1) DEFAULT 0 COMMENT '是否985：0 不是， 1 是',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='学校信息';

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` bigint(20) AUTO_INCREMENT COMMENT '自增序列',
  `name` varchar(255) NOT NULL COMMENT '名字',
  `code` varchar(255) NOT NULL COMMENT '权限代码，对应与所装饰的方法的名字',
  `type` varchar(255) DEFAULT NULL COMMENT '权限类型',
  `sort` INT DEFAULT 1 COMMENT '排序，越大越考前',
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限';

-- ----------------------------
-- Table structure for auth_permission_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission_group`;
CREATE TABLE `auth_permission_group` (
  `id` bigint(20) AUTO_INCREMENT COMMENT '自增序列',
  `name` varchar(255) NOT NULL COMMENT '名字',
  `codes` varchar(255) DEFAULT '[]' COMMENT '权限代码族：list的json字符串, 值是auth_permission的id',
  `type` varchar(255) DEFAULT NULL COMMENT '权限类型',
  `sort` INT DEFAULT 1 COMMENT '排序，越大越考前',
   PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='权限组';

-- ----------------------------
-- Records of auth_permission_group
-- ----------------------------
INSERT INTO `auth_user` VALUES ('1', '默认权限组', '[]', '未知', 1);

