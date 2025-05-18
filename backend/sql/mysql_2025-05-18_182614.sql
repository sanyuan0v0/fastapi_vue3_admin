-- MySQL dump 10.13  Distrib 8.4.3, for macos14.5 (arm64)
--
-- Host: 127.0.0.1    Database: fastapi_vue_admin
-- ------------------------------------------------------
-- Server version	8.4.3

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
-- Table structure for table `system_config`
--

DROP TABLE IF EXISTS `system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(100) NOT NULL COMMENT '网站标题',
  `favicon` varchar(500) NOT NULL COMMENT '网站favicon',
  `logo` varchar(500) NOT NULL COMMENT '网站logo',
  `background` varchar(500) NOT NULL COMMENT '网站背景',
  `copyright` varchar(500) NOT NULL COMMENT '版权信息',
  `keep_record` varchar(500) NOT NULL COMMENT '备案信息',
  `help_url` varchar(500) NOT NULL COMMENT '帮助链接',
  `privacy_url` varchar(500) NOT NULL COMMENT '隐私政策链接',
  `clause_url` varchar(500) NOT NULL COMMENT '服务条款链接',
  `code_url` varchar(500) NOT NULL COMMENT '源码地址',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_config_creator_id` (`creator_id`),
  CONSTRAINT `system_config_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配置表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_config`
--

/*!40000 ALTER TABLE `system_config` DISABLE KEYS */;
INSERT INTO `system_config` VALUES (1,'FastAPI Vue Admin','http://8.137.99.5:8001/api/v1/static/image/favicon.ico','http://8.137.99.5:8001/api/v1/static/image/logo.png','http://8.137.99.5:8001/api/v1/static/image/background.png','Copyright © 2021-2025 fastapi-vue-admin.com 版权所有','晋ICP备18005113号-3','https://gitee.com/tao__tao/fastapi_vue3_admin.git','https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE','https://gitee.com/tao__tao/fastapi_vue3_admin/blob/master/LICENSE','https://gitee.com/tao__tao/fastapi_vue3_admin.git','FastAPI Vue Admin 是完全开源的权限管理系统','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_config` ENABLE KEYS */;

--
-- Table structure for table `system_dept`
--

DROP TABLE IF EXISTS `system_dept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dept` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '部门名称',
  `order` int NOT NULL COMMENT '显示排序',
  `parent_id` int DEFAULT NULL COMMENT '父级部门ID',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_dept_parent_id` (`parent_id`),
  CONSTRAINT `system_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_dept`
--

/*!40000 ALTER TABLE `system_dept` DISABLE KEYS */;
INSERT INTO `system_dept` VALUES (1,'集团总公司',1,NULL,1,'集团总公司','2025-05-18 18:24:56','2025-05-18 18:24:56'),(2,'西安分公司',1,1,1,'西安分公司','2025-05-18 18:24:56','2025-05-18 18:24:56'),(3,'深圳分公司',2,1,1,'深圳分公司','2025-05-18 18:24:56','2025-05-18 18:24:56'),(4,'开发组',1,2,1,'开发组','2025-05-18 18:24:56','2025-05-18 18:24:56'),(5,'测试组',2,2,1,'测试组','2025-05-18 18:24:56','2025-05-18 18:24:56'),(6,'演示组',3,2,1,'演示组','2025-05-18 18:24:56','2025-05-18 18:24:56'),(7,'销售部',1,3,1,'销售部','2025-05-18 18:24:56','2025-05-18 18:24:56'),(8,'市场部',2,3,1,'市场部','2025-05-18 18:24:56','2025-05-18 18:24:56'),(9,'财务部',3,3,1,'财务部','2025-05-18 18:24:56','2025-05-18 18:24:56'),(10,'研发部',4,3,1,'研发部','2025-05-18 18:24:56','2025-05-18 18:24:56'),(11,'运维部',5,3,1,'研发部','2025-05-18 18:24:56','2025-05-18 18:24:56');
/*!40000 ALTER TABLE `system_dept` ENABLE KEYS */;

--
-- Table structure for table `system_dict_data`
--

DROP TABLE IF EXISTS `system_dict_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dict_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int DEFAULT NULL COMMENT '字典排序',
  `dict_label` varchar(100) DEFAULT NULL COMMENT '字典标签',
  `dict_value` varchar(100) DEFAULT NULL COMMENT '字典键值',
  `dict_type` varchar(100) DEFAULT NULL COMMENT '字典类型',
  `css_class` varchar(100) DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) DEFAULT NULL COMMENT '表格回显样式',
  `is_default` tinyint(1) DEFAULT NULL COMMENT '是否默认（Y是 N否）',
  `available` tinyint(1) DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_dict_data_creator_id` (`creator_id`),
  CONSTRAINT `system_dict_data_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据字典数据表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_dict_data`
--

/*!40000 ALTER TABLE `system_dict_data` DISABLE KEYS */;
INSERT INTO `system_dict_data` VALUES (1,1,'男','0','sys_user_sex','blue',NULL,1,1,'性别男','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,2,'女','1','sys_user_sex','pink',NULL,0,1,'性别女','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(3,3,'未知','2','sys_user_sex','red',NULL,0,1,'性别未知','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(4,4,'显示','0','sys_show_hide','btn btn-success btn-xs','primary',1,1,'显示菜单','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(5,2,'隐藏','1','sys_show_hide','','danger',0,1,'隐藏菜单','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(6,1,'正常','0','sys_normal_disable','','primary',1,1,'正常状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(7,2,'停用','1','sys_normal_disable','','danger',0,1,'停用状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(8,1,'正常','0','sys_job_status','','primary',1,1,'正常状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(9,2,'暂停','1','sys_job_status','','danger',0,1,'停用状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(10,1,'默认(Memory)','default','sys_job_group','',NULL,1,1,'默认分组','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(11,2,'数据库','sqlalchemy','sys_job_group','',NULL,0,1,'数据库分组','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(12,3,'redis','redis','sys_job_group','',NULL,0,1,'reids分组','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(13,1,'默认','default','sys_job_executor','',NULL,0,1,'线程池','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(14,2,'进程池','processpool','sys_job_executor','',NULL,0,1,'进程池','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(15,1,'是','true','sys_yes_no','','primary',1,1,'系统默认是','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(16,2,'否','false','sys_yes_no','','danger',0,1,'系统默认否','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(17,1,'通知','1','sys_notice_type','blue','warning',1,1,'通知','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(18,2,'公告','2','sys_notice_type','orange','success',0,1,'公告','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(19,1,'正常','0','sys_notice_status','','primary',1,1,'正常状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(20,2,'关闭','1','sys_notice_status','','danger',0,1,'关闭状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(21,99,'其他','0','sys_oper_type','','info',0,1,'其他操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(22,1,'新增','1','sys_oper_type','','info',0,1,'新增操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(23,2,'修改','2','sys_oper_type','','info',0,1,'修改操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(24,3,'删除','3','sys_oper_type','','danger',0,1,'删除操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(25,4,'授权','4','sys_oper_type','','primary',0,1,'授权操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(26,5,'导出','5','sys_oper_type','','warning',0,1,'导出操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(27,6,'导入','6','sys_oper_type','','warning',0,1,'导入操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(28,7,'强退','7','sys_oper_type','','danger',0,1,'强退操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(29,8,'生成代码','8','sys_oper_type','','warning',0,1,'生成操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(30,9,'清空数据','9','sys_oper_type','','danger',0,1,'清空操作','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(31,1,'成功','0','sys_common_status','','primary',0,1,'正常状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(32,2,'失败','1','sys_common_status','','danger',0,1,'停用状态','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(33,1,'初始化演示函数','scheduler_test.job','sys_job_function','',NULL,1,1,'演示函数','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(34,1,'指定日期(date)','date','sys_job_trigger','',NULL,1,1,'指定日期任务触发器','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(35,2,'间隔触发器(interval)','interval','sys_job_trigger','',NULL,0,1,'间隔触发器任务触发器','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(36,3,'cron表达式','cron','sys_job_trigger','',NULL,0,1,'间隔触发器任务触发器','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(37,1,'默认(default)','default','sys_dictdata_list_class','',NULL,1,1,'默认表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(38,2,'主要(primary)','primary','sys_dictdata_list_class','',NULL,0,1,'主要表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(39,3,'成功(success)','success','sys_dictdata_list_class','',NULL,0,1,'成功表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(40,4,'信息(info)','info','sys_dictdata_list_class','',NULL,0,1,'信息表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(41,5,'警告(warning)','warning','sys_dictdata_list_class','',NULL,0,1,'警告表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(42,6,'危险(danger)','danger','sys_dictdata_list_class','',NULL,0,1,'危险表格回显样式','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_dict_data` ENABLE KEYS */;

--
-- Table structure for table `system_dict_type`
--

DROP TABLE IF EXISTS `system_dict_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_dict_type` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) DEFAULT NULL COMMENT '字典名称',
  `dict_type` varchar(100) DEFAULT NULL COMMENT '字典类型',
  `available` tinyint(1) DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_dict_type_creator_id` (`creator_id`),
  CONSTRAINT `system_dict_type_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据字典类型表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_dict_type`
--

/*!40000 ALTER TABLE `system_dict_type` DISABLE KEYS */;
INSERT INTO `system_dict_type` VALUES (1,'用户性别','sys_user_sex',1,'用户性别列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,'菜单状态','sys_show_hide',1,'菜单状态列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(3,'系统开关','sys_normal_disable',1,'系统开关列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(4,'任务状态','sys_job_status',1,'任务状态列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(5,'任务分组','sys_job_group',1,'任务分组列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(6,'任务执行器','sys_job_executor',1,'任务执行器列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(7,'系统是否','sys_yes_no',1,'系统是否列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(8,'通知类型','sys_notice_type',1,'通知类型列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(9,'通知状态','sys_notice_status',1,'通知状态列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(10,'操作类型','sys_oper_type',1,'操作类型列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(11,'系统状态','sys_common_status',1,'登录状态列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(12,'任务函数','sys_job_function',1,'任务函数列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(13,'任务触发器','sys_job_trigger',1,'任务触发器列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(14,'字典配置表格回显样式','sys_dictdata_list_class',1,'字典配置表格回显样式列表','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_dict_type` ENABLE KEYS */;

--
-- Table structure for table `system_job`
--

DROP TABLE IF EXISTS `system_job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_job` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `name` varchar(64) DEFAULT NULL COMMENT '任务名称',
  `jobstore` varchar(64) DEFAULT NULL COMMENT '存储器',
  `executor` varchar(64) DEFAULT NULL COMMENT '执行器:将运行此作业的执行程序的名称',
  `trigger` varchar(64) NOT NULL COMMENT '触发器:控制此作业计划的 trigger 对象',
  `trigger_args` text COMMENT '触发器参数',
  `func` text NOT NULL COMMENT '任务函数',
  `args` text COMMENT '位置参数',
  `kwargs` text COMMENT '关键字参数',
  `coalesce` tinyint(1) DEFAULT NULL COMMENT '是否合并运行:是否在多个运行时间到期时仅运行作业一次',
  `max_instances` int DEFAULT NULL COMMENT '最大实例数:允许的最大并发执行实例数 工作',
  `start_date` text COMMENT '开始时间',
  `end_date` text COMMENT '结束时间',
  `status` tinyint(1) DEFAULT NULL COMMENT '任务状态:正常,停止',
  `message` varchar(500) DEFAULT NULL COMMENT '日志信息',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_job_creator_id` (`creator_id`),
  CONSTRAINT `system_job_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_job`
--

/*!40000 ALTER TABLE `system_job` DISABLE KEYS */;
INSERT INTO `system_job` VALUES (1,'系统默认（无参）','default','default','cron','0 0 12 * * ?','scheduler_test.job',NULL,NULL,0,1,NULL,NULL,0,NULL,NULL,'2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,'系统默认（有参）','default','default','cron','0 0 12 * * ?','scheduler_test.job','test',NULL,0,1,NULL,NULL,0,NULL,NULL,'2025-05-18 18:24:56','2025-05-18 18:24:56',1),(3,'系统默认（多参）','default','default','cron','0 0 12 * * ?','scheduler_test.job','new','{\"test\": 111}',0,1,NULL,NULL,0,NULL,NULL,'2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_job` ENABLE KEYS */;

--
-- Table structure for table `system_menu`
--

DROP TABLE IF EXISTS `system_menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_menu` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '菜单类型',
  `order` int NOT NULL COMMENT '显示排序',
  `permission` varchar(100) DEFAULT NULL COMMENT '权限标识(如：system:user:list)',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `route_name` varchar(100) DEFAULT NULL COMMENT '路由名称',
  `route_path` varchar(200) DEFAULT NULL COMMENT '路由路径',
  `component_path` varchar(200) DEFAULT NULL COMMENT '组件路径',
  `redirect` varchar(200) DEFAULT NULL COMMENT '重定向地址',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏(True:隐藏 False:显示)',
  `cache` tinyint(1) NOT NULL COMMENT '是否缓存(True:是 False:否)',
  `parent_id` int DEFAULT NULL COMMENT '父级菜单ID',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_menu_parent_id` (`parent_id`),
  CONSTRAINT `system_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_menu`
--

/*!40000 ALTER TABLE `system_menu` DISABLE KEYS */;
INSERT INTO `system_menu` VALUES (1,'仪表盘',1,1,'',1,'DashboardOutlined','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,NULL,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(2,'系统管理',1,2,NULL,1,'SettingOutlined','System','/system',NULL,'/system/menu',0,1,NULL,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(3,'菜单管理',2,1,'system:menu:query',1,NULL,'Menu','/system/menu','system/menu/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(4,'部门管理',2,2,'system:dept:query',1,NULL,'Dept','/system/dept','system/dept/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(5,'岗位管理',2,3,'system:position:query',1,NULL,'Position','/system/position','system/position/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(6,'角色管理',2,4,'system:role:query',1,NULL,'Role','/system/role','system/role/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(7,'用户管理',2,5,'system:user:query',1,NULL,'User','/system/user','system/user/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(8,'日志管理',2,6,'system:log:query',1,NULL,'Log','/system/log','system/log/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(9,'创建菜单',3,1,'system:menu:create',1,NULL,NULL,NULL,NULL,NULL,0,1,3,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(10,'修改菜单',3,2,'system:menu:update',1,NULL,NULL,NULL,NULL,NULL,0,1,3,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(11,'删除菜单',3,3,'system:menu:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,3,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(12,'批量修改菜单状态',3,4,'system:menu:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,3,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(13,'创建部门',3,1,'system:dept:create',1,NULL,NULL,NULL,NULL,NULL,0,1,4,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(14,'修改部门',3,2,'system:dept:update',1,NULL,NULL,NULL,NULL,NULL,0,1,4,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(15,'删除部门',3,3,'system:dept:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,4,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(16,'批量修改部门状态',3,4,'system:dept:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,4,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(17,'创建岗位',3,1,'system:position:create',1,NULL,NULL,NULL,NULL,NULL,0,1,5,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(18,'修改岗位',3,2,'system:position:update',1,NULL,NULL,NULL,NULL,NULL,0,1,5,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(19,'删除岗位',3,3,'system:position:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,5,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(20,'批量修改岗位状态',3,4,'system:position:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,5,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(21,'岗位导出',3,5,'system:position:export',1,NULL,NULL,NULL,NULL,NULL,0,1,5,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(22,'创建角色',3,1,'system:role:create',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(23,'修改角色',3,2,'system:role:update',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(24,'删除角色',3,3,'system:role:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(25,'批量修改角色状态',3,4,'system:role:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(26,'设置角色权限',3,5,'system:role:permission',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(27,'角色导出',3,6,'system:role:export',1,NULL,NULL,NULL,NULL,NULL,0,1,6,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(28,'创建用户',3,1,'system:user:create',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(29,'修改用户',3,2,'system:user:update',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(30,'删除用户',3,3,'system:user:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(31,'批量修改用户状态',3,4,'system:user:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(32,'导出用户',3,5,'system:user:export',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(33,'导入用户',3,6,'system:user:import',1,NULL,NULL,NULL,NULL,NULL,0,1,7,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(34,'日志删除',3,1,'system:operation_log:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,8,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(35,'日志导出',3,2,'system:operation_log:export',1,NULL,NULL,NULL,NULL,NULL,0,1,8,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(36,'监控管理',1,3,NULL,1,'MonitorOutlined','Monitor','/monitor',NULL,'/monitor/online',0,1,NULL,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(37,'在线用户',2,1,'monitor:online:query',1,NULL,'MonitorOnline','/monitor/online','monitor/online/index',NULL,0,1,36,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(38,'在线用户强制下线',3,1,'monitor:online:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,37,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(39,'服务器监控',2,2,'monitor:server:query',1,NULL,'MonitorServer','/monitor/server','monitor/server/index',NULL,0,1,36,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(40,'缓存监控',2,3,'monitor:cache:query',1,NULL,'MonitorCache','/monitor/cache','monitor/cache/index',NULL,0,1,36,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(41,'清除缓存',3,1,'monitor:cache:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,40,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(42,'公共模块',1,4,NULL,1,'ApiOutlined','Common','/common',NULL,'/common/docs',0,1,NULL,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(43,'接口管理',2,1,'common:docs:query',1,NULL,'Docs','/common/docs','common/docs/index',NULL,0,1,42,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(44,'文档管理',2,2,'common:redoc:query',1,NULL,'Redoc','/common/redoc','common/redoc/index',NULL,0,1,42,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(45,'公告管理',2,7,'system:notice:query',1,NULL,'Notice','/system/notice','system/notice/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(46,'公告创建',3,1,'system:notice:create',1,NULL,NULL,NULL,NULL,NULL,0,1,45,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(47,'公告修改',3,2,'system:notice:update',1,NULL,NULL,NULL,NULL,NULL,0,1,45,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(48,'公告删除',3,3,'system:notice:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,45,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(49,'公告导出',3,4,'system:notice:export',1,NULL,NULL,NULL,NULL,NULL,0,1,45,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(50,'公告批量修改状态',3,5,'system:notice:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,45,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(51,'配置管理',2,8,'system:config:query',1,NULL,'Config','/system/config','system/config/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(52,'创建配置',3,1,'system:config:create',1,NULL,NULL,NULL,NULL,NULL,0,1,51,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(53,'修改配置',3,2,'system:config:update',1,NULL,NULL,NULL,NULL,NULL,0,1,51,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(54,'删除配置',3,3,'system:config:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,51,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(55,'批量更新配置',3,4,'system:config:update',1,NULL,NULL,NULL,NULL,NULL,0,1,51,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(56,'文件上传',3,5,'system:config:upload',1,NULL,NULL,NULL,NULL,NULL,0,1,51,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(57,'字典管理',2,9,'system:dict_type:query',1,NULL,'Dict','/system/dict','system/dict/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(58,'创建字典类型',3,1,'system:dict_type:create',1,NULL,NULL,NULL,NULL,NULL,0,1,57,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(59,'修改字典类型',3,2,'system:dict_type:update',1,NULL,NULL,NULL,NULL,NULL,0,1,57,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(60,'删除字典类型',3,3,'system:dict_type:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,57,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(61,'导出字典类型',3,4,'system:dict_type:export',1,NULL,NULL,NULL,NULL,NULL,0,1,57,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(62,'字典数据',2,10,'system:dict_data:query',1,NULL,'DictData','/system/dict_data','system/dict/data',NULL,1,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(63,'创建字典数据',3,1,'system:dict_data:create',1,NULL,NULL,NULL,NULL,NULL,0,1,62,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(64,'修改字典数据',3,2,'system:dict_data:update',1,NULL,NULL,NULL,NULL,NULL,0,1,62,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(65,'删除字典数据',3,3,'system:dict_data:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,62,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(66,'导出字典数据',3,4,'system:dict_data:export',1,NULL,NULL,NULL,NULL,NULL,0,1,62,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(67,'任务管理',2,11,'system:job:query',1,NULL,'Job','/system/job','system/job/index',NULL,0,1,2,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(68,'创建任务',3,1,'system:job:create',1,NULL,NULL,NULL,NULL,NULL,0,1,67,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(69,'修改和操作任务',3,2,'system:job:update',1,NULL,NULL,NULL,NULL,NULL,0,1,67,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(70,'删除和清除任务',3,3,'system:job:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,67,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(71,'导出定时任务',3,4,'system:job:export',1,NULL,NULL,NULL,NULL,NULL,0,1,67,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(72,'工作台',2,1,'dashboard:workplace:query',1,'','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,1,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56'),(73,'分析页',2,2,'dashboard:analysis:query',1,'','Analysis','/dashboard/analysis','dashboard/analysis',NULL,0,1,1,'初始化数据','2025-05-18 18:24:56','2025-05-18 18:24:56');
/*!40000 ALTER TABLE `system_menu` ENABLE KEYS */;

--
-- Table structure for table `system_notice`
--

DROP TABLE IF EXISTS `system_notice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_notice` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `notice_title` varchar(50) NOT NULL COMMENT '公告标题',
  `notice_type` varchar(50) NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` text COMMENT '公告内容',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_notice_creator_id` (`creator_id`),
  CONSTRAINT `system_notice_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知公告表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_notice`
--

/*!40000 ALTER TABLE `system_notice` DISABLE KEYS */;
INSERT INTO `system_notice` VALUES (1,'系统更新','1','2099年9月9日，晚上12:00，系统更新',1,'系统更新','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,'系统维护','2','2099年9月9日，晚上12:00，系统维护',1,'系统维护','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(3,'系统更新完成','1','2099年9月9日，晚上12:00，系统更新完成',0,'系统更新完成','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(4,'系统维护完成','2','2099年9月9日，晚上12:00，系统维护完成',0,'系统维护完成','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_notice` ENABLE KEYS */;

--
-- Table structure for table `system_operation_log`
--

DROP TABLE IF EXISTS `system_operation_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_operation_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `request_path` varchar(255) DEFAULT NULL COMMENT '请求路径',
  `request_method` varchar(10) DEFAULT NULL COMMENT '请求方式',
  `request_payload` text COMMENT '请求体',
  `request_ip` varchar(50) DEFAULT NULL COMMENT '请求IP地址',
  `login_location` varchar(255) DEFAULT NULL COMMENT '登录位置',
  `request_os` varchar(64) DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) DEFAULT NULL COMMENT '浏览器',
  `response_code` int DEFAULT NULL COMMENT '响应状态码',
  `response_json` text COMMENT '响应体',
  `process_time` float DEFAULT NULL COMMENT '处理时间',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_operation_log_creator_id` (`creator_id`),
  KEY `ix_system_operation_log_request_method` (`request_method`),
  KEY `ix_system_operation_log_request_path` (`request_path`),
  CONSTRAINT `system_operation_log_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='操作日志表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_operation_log`
--

/*!40000 ALTER TABLE `system_operation_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_operation_log` ENABLE KEYS */;

--
-- Table structure for table `system_position`
--

DROP TABLE IF EXISTS `system_position`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_position` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '岗位名称',
  `order` int NOT NULL COMMENT '显示排序',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_position_creator_id` (`creator_id`),
  CONSTRAINT `system_position_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_position`
--

/*!40000 ALTER TABLE `system_position` DISABLE KEYS */;
INSERT INTO `system_position` VALUES (1,'董事长岗',1,1,'董事长岗位','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,'运营岗',2,1,'运营岗位','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(3,'销售岗',3,1,'销售岗','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(4,'人事行政岗',4,1,'人事行政岗','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(5,'开发岗',5,1,'开发岗','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(6,'测试岗',6,1,'测试岗','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(7,'演示岗',7,1,'演示岗','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_position` ENABLE KEYS */;

--
-- Table structure for table `system_role`
--

DROP TABLE IF EXISTS `system_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '角色名称',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_role_creator_id` (`creator_id`),
  CONSTRAINT `system_role_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role`
--

/*!40000 ALTER TABLE `system_role` DISABLE KEYS */;
INSERT INTO `system_role` VALUES (1,'管理员角色',1,4,1,'管理员','2025-05-18 18:24:56','2025-05-18 18:24:56',1),(2,'演示角色',2,5,1,'演示角色','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_role` ENABLE KEYS */;

--
-- Table structure for table `system_role_depts`
--

DROP TABLE IF EXISTS `system_role_depts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role_depts` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `dept_id` int NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`,`dept_id`),
  KEY `ix_system_role_depts_dept_id` (`dept_id`),
  KEY `ix_system_role_depts_role_id` (`role_id`),
  CONSTRAINT `system_role_depts_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_role_depts_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色部门关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role_depts`
--

/*!40000 ALTER TABLE `system_role_depts` DISABLE KEYS */;
INSERT INTO `system_role_depts` VALUES (1,1),(2,1),(2,6);
/*!40000 ALTER TABLE `system_role_depts` ENABLE KEYS */;

--
-- Table structure for table `system_role_menus`
--

DROP TABLE IF EXISTS `system_role_menus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_role_menus` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `ix_system_role_menus_role_id` (`role_id`),
  KEY `ix_system_role_menus_menu_id` (`menu_id`),
  CONSTRAINT `system_role_menus_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色菜单关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_role_menus`
--

/*!40000 ALTER TABLE `system_role_menus` DISABLE KEYS */;
INSERT INTO `system_role_menus` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),(1,13),(1,14),(1,15),(1,16),(1,17),(1,18),(1,19),(1,20),(1,21),(1,22),(1,23),(1,24),(1,25),(1,26),(1,27),(1,28),(1,29),(1,30),(1,31),(1,32),(1,33),(1,34),(1,35),(1,36),(1,37),(1,38),(1,39),(1,40),(1,41),(1,42),(1,43),(1,44),(1,45),(1,46),(1,47),(1,48),(1,49),(1,50),(1,51),(1,52),(1,53),(1,54),(1,55),(1,56),(1,57),(1,58),(1,59),(1,60),(1,61),(1,62),(1,63),(1,64),(1,65),(1,66),(1,67),(1,68),(1,69),(1,70),(1,71),(1,72),(1,73),(2,1),(2,2),(2,3);
/*!40000 ALTER TABLE `system_role_menus` ENABLE KEYS */;

--
-- Table structure for table `system_user_positions`
--

DROP TABLE IF EXISTS `system_user_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user_positions` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `position_id` int NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`,`position_id`),
  KEY `ix_system_user_positions_position_id` (`position_id`),
  KEY `ix_system_user_positions_user_id` (`user_id`),
  CONSTRAINT `system_user_positions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_user_positions_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `system_position` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户岗位关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user_positions`
--

/*!40000 ALTER TABLE `system_user_positions` DISABLE KEYS */;
INSERT INTO `system_user_positions` VALUES (1,5),(2,7);
/*!40000 ALTER TABLE `system_user_positions` ENABLE KEYS */;

--
-- Table structure for table `system_user_roles`
--

DROP TABLE IF EXISTS `system_user_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_user_roles` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `ix_system_user_roles_user_id` (`user_id`),
  KEY `ix_system_user_roles_role_id` (`role_id`),
  CONSTRAINT `system_user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户角色关联表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_user_roles`
--

/*!40000 ALTER TABLE `system_user_roles` DISABLE KEYS */;
INSERT INTO `system_user_roles` VALUES (1,1),(2,2);
/*!40000 ALTER TABLE `system_user_roles` ENABLE KEYS */;

--
-- Table structure for table `system_users`
--

DROP TABLE IF EXISTS `system_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `system_users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(150) NOT NULL COMMENT '用户名/登录账号',
  `password` varchar(128) NOT NULL COMMENT '密码',
  `name` varchar(40) NOT NULL COMMENT '姓名',
  `mobile` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `gender` varchar(20) NOT NULL COMMENT '性别(1:男 2:女 3:未知)',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像地址',
  `available` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `is_superuser` tinyint(1) NOT NULL COMMENT '是否为超级管理员',
  `last_login` datetime DEFAULT NULL COMMENT '最后登录时间',
  `dept_id` int DEFAULT NULL COMMENT '部门ID',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `ix_system_users_creator_id` (`creator_id`),
  KEY `ix_system_users_dept_id` (`dept_id`),
  CONSTRAINT `system_users_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `system_users_ibfk_2` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_users`
--

/*!40000 ALTER TABLE `system_users` DISABLE KEYS */;
INSERT INTO `system_users` VALUES (1,'admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','管理员','15382112222','admin@qq.com','0','https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',1,1,NULL,1,'超级管理员','2025-05-18 18:24:56','2025-05-18 18:24:56',NULL),(2,'demo','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','演示用户','15382112121','demo@qq.com','1','https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png',1,0,NULL,6,'演示用户','2025-05-18 18:24:56','2025-05-18 18:24:56',1);
/*!40000 ALTER TABLE `system_users` ENABLE KEYS */;

--
-- Dumping routines for database 'fastapi_vue_admin'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-18 18:26:27
