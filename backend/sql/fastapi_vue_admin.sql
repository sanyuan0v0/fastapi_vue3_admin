/*
 Navicat Premium Dump SQL

 Source Server         : 本地mysql
 Source Server Type    : MySQL
 Source Server Version : 80403 (8.4.3)
 Source Host           : localhost:3306
 Source Schema         : fastapi_vue_admin

 Target Server Type    : MySQL
 Target Server Version : 80403 (8.4.3)
 File Encoding         : 65001

 Date: 05/08/2025 00:30:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for demo_example
-- ----------------------------
DROP TABLE IF EXISTS `demo_example`;
CREATE TABLE `demo_example` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(64) DEFAULT NULL COMMENT '名称',
  `description` text COMMENT '备注说明',
  `status` tinyint(1) DEFAULT NULL COMMENT '任务状态:正常,停止',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_demo_example_creator_id` (`creator_id`),
  CONSTRAINT `demo_example_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='示例表';

-- ----------------------------
-- Records of demo_example
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for monitor_job
-- ----------------------------
DROP TABLE IF EXISTS `monitor_job`;
CREATE TABLE `monitor_job` (
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
  KEY `ix_monitor_job_creator_id` (`creator_id`),
  CONSTRAINT `monitor_job_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='定时任务调度表';

-- ----------------------------
-- Records of monitor_job
-- ----------------------------
BEGIN;
INSERT INTO `monitor_job` (`id`, `name`, `jobstore`, `executor`, `trigger`, `trigger_args`, `func`, `args`, `kwargs`, `coalesce`, `max_instances`, `start_date`, `end_date`, `status`, `message`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '系统默认（无参）', 'default', 'default', 'cron', '0 0 12 * * ?', 'scheduler_test.job', NULL, NULL, 0, 1, NULL, NULL, 0, NULL, NULL, '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `monitor_job` (`id`, `name`, `jobstore`, `executor`, `trigger`, `trigger_args`, `func`, `args`, `kwargs`, `coalesce`, `max_instances`, `start_date`, `end_date`, `status`, `message`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '系统默认（有参）', 'default', 'default', 'cron', '0 0 12 * * ?', 'scheduler_test.job', 'test', NULL, 0, 1, NULL, NULL, 0, NULL, NULL, '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `monitor_job` (`id`, `name`, `jobstore`, `executor`, `trigger`, `trigger_args`, `func`, `args`, `kwargs`, `coalesce`, `max_instances`, `start_date`, `end_date`, `status`, `message`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, '系统默认（多参）', 'default', 'default', 'cron', '0 0 12 * * ?', 'scheduler_test.job', 'new', '{\"test\": 111}', 0, 1, NULL, NULL, 0, NULL, NULL, '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_config
-- ----------------------------
DROP TABLE IF EXISTS `system_config`;
CREATE TABLE `system_config` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `config_name` varchar(500) DEFAULT NULL COMMENT '参数名称',
  `config_key` varchar(500) DEFAULT NULL COMMENT '参数键名',
  `config_value` varchar(500) DEFAULT NULL COMMENT '参数键值',
  `config_type` tinyint(1) NOT NULL COMMENT '系统内置((True:是 False:否))',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `config_name` (`config_name`),
  UNIQUE KEY `config_key` (`config_key`),
  KEY `ix_system_config_creator_id` (`creator_id`),
  CONSTRAINT `system_config_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配置表';

-- ----------------------------
-- Records of system_config
-- ----------------------------
BEGIN;
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '网站名称', 'sys_web_title', 'FastAPI Vue3 Admin', 1, '网站名称', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '网站描述', 'sys_web_description', 'FastAPI Vue3 Admin 是完全开源的权限管理系统', 1, '网站描述', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, '网页图标', 'sys_web_favicon', 'https://service.fastapiadmin.com/api/v1/static/image/favicon.png', 1, '网页图标', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (4, '网站Logo', 'sys_web_logo', 'https://service.fastapiadmin.com/api/v1/static/image/logo.png', 1, '网站Logo', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (5, '登录背景', 'sys_login_background', 'https://service.fastapiadmin.com/api/v1/static/image/background.svg', 1, '登录背景', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (6, '版权信息', 'sys_web_copyright', 'Copyright © 2025-2026 service.fastapiadmin.com 版权所有', 1, '版权信息', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (7, '备案信息', 'sys_keep_record', '陕ICP备2025069493号-1', 1, '备案信息', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (8, '帮助文档', 'sys_help_doc', 'https://service.fastapiadmin.com/docs/index.html', 1, '帮助文档', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (9, '隐私政策', 'sys_web_privacy', 'https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE', 1, '隐私政策', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (10, '用户协议', 'sys_web_clause', 'https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE', 1, '用户协议', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (11, '源码代码', 'sys_git_code', 'https://github.com/1014TaoTao/fastapi_vue3_admin.git', 1, '源码代码', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_config` (`id`, `config_name`, `config_key`, `config_value`, `config_type`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (12, '项目版本', 'sys_web_version', '2.0.0', 1, '项目版本', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_dept
-- ----------------------------
DROP TABLE IF EXISTS `system_dept`;
CREATE TABLE `system_dept` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '部门名称',
  `order` int NOT NULL COMMENT '显示排序',
  `parent_id` int DEFAULT NULL COMMENT '父级部门ID',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_dept_parent_id` (`parent_id`),
  CONSTRAINT `system_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='部门表';

-- ----------------------------
-- Records of system_dept
-- ----------------------------
BEGIN;
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (1, '集团总公司', 1, NULL, 1, '集团总公司', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (2, '西安分公司', 1, 1, 1, '西安分公司', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (3, '深圳分公司', 2, 1, 1, '深圳分公司', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (4, '开发组', 1, 2, 1, '开发组', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (5, '测试组', 2, 2, 1, '测试组', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (6, '演示组', 3, 2, 1, '演示组', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (7, '销售部', 1, 3, 1, '销售部', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (8, '市场部', 2, 3, 1, '市场部', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (9, '财务部', 3, 3, 1, '财务部', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (10, '研发部', 4, 3, 1, '研发部', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_dept` (`id`, `name`, `order`, `parent_id`, `status`, `description`, `created_at`, `updated_at`) VALUES (11, '运维部', 5, 3, 1, '研发部', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
COMMIT;

-- ----------------------------
-- Table structure for system_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `system_dict_data`;
CREATE TABLE `system_dict_data` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int DEFAULT NULL COMMENT '字典排序',
  `dict_label` varchar(100) DEFAULT NULL COMMENT '字典标签',
  `dict_value` varchar(100) DEFAULT NULL COMMENT '字典键值',
  `dict_type` varchar(100) DEFAULT NULL COMMENT '字典类型',
  `css_class` varchar(100) DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) DEFAULT NULL COMMENT '表格回显样式',
  `is_default` tinyint(1) DEFAULT NULL COMMENT '是否默认（Y是 N否）',
  `status` tinyint(1) DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_dict_data_creator_id` (`creator_id`),
  CONSTRAINT `system_dict_data_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据字典数据表';

-- ----------------------------
-- Records of system_dict_data
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, 1, '男', '0', 'sys_user_sex', 'blue', NULL, 1, 1, '性别男', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, 2, '女', '1', 'sys_user_sex', 'pink', NULL, 0, 1, '性别女', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, 3, '未知', '2', 'sys_user_sex', 'red', NULL, 0, 1, '性别未知', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (4, 1, '启用', '1', 'sys_common_status', '', 'primary', 0, 1, '启用状态', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (5, 2, '停用', '0', 'sys_common_status', '', 'danger', 0, 1, '停用状态', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (6, 1, '是', '1', 'sys_yes_no', '', 'primary', 1, 1, '是', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (7, 2, '否', '0', 'sys_yes_no', '', 'danger', 0, 1, '否', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (8, 99, '其他', '0', 'sys_oper_type', '', 'info', 0, 1, '其他操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (9, 1, '新增', '1', 'sys_oper_type', '', 'info', 0, 1, '新增操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (10, 2, '修改', '2', 'sys_oper_type', '', 'info', 0, 1, '修改操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (11, 3, '删除', '3', 'sys_oper_type', '', 'danger', 0, 1, '删除操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (12, 4, '分配权限', '4', 'sys_oper_type', '', 'primary', 0, 1, '授权操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (13, 5, '导出', '5', 'sys_oper_type', '', 'warning', 0, 1, '导出操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (14, 6, '导入', '6', 'sys_oper_type', '', 'warning', 0, 1, '导入操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (15, 7, '强退', '7', 'sys_oper_type', '', 'danger', 0, 1, '强退操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (16, 8, '生成代码', '8', 'sys_oper_type', '', 'warning', 0, 1, '生成操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (17, 9, '清空数据', '9', 'sys_oper_type', '', 'danger', 0, 1, '清空操作', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (18, 1, '通知', '1', 'sys_notice_type', 'blue', 'warning', 1, 1, '通知', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (19, 2, '公告', '2', 'sys_notice_type', 'orange', 'success', 0, 1, '公告', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (20, 1, '默认(Memory)', 'default', 'sys_job_store', '', NULL, 1, 1, '默认分组', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (21, 2, '数据库(Sqlalchemy)', 'sqlalchemy', 'sys_job_store', '', NULL, 0, 1, '数据库分组', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (22, 3, '数据库(Redis)', 'redis', 'sys_job_store', '', NULL, 0, 1, 'reids分组', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (23, 1, '线程池', 'default', 'sys_job_executor', '', NULL, 0, 1, '线程池', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (24, 2, '进程池', 'processpool', 'sys_job_executor', '', NULL, 0, 1, '进程池', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (25, 1, '演示函数', 'scheduler_test.job', 'sys_job_function', '', NULL, 1, 1, '演示函数', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (26, 1, '指定日期(date)', 'date', 'sys_job_trigger', '', NULL, 1, 1, '指定日期任务触发器', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (27, 2, '间隔触发器(interval)', 'interval', 'sys_job_trigger', '', NULL, 0, 1, '间隔触发器任务触发器', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (28, 3, 'cron表达式', 'cron', 'sys_job_trigger', '', NULL, 0, 1, '间隔触发器任务触发器', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (29, 1, '默认(default)', 'default', 'sys_list_class', '', NULL, 1, 1, '默认表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (30, 2, '主要(primary)', 'primary', 'sys_list_class', '', NULL, 0, 1, '主要表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (31, 3, '成功(success)', 'success', 'sys_list_class', '', NULL, 0, 1, '成功表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (32, 4, '信息(info)', 'info', 'sys_list_class', '', NULL, 0, 1, '信息表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (33, 5, '警告(warning)', 'warning', 'sys_list_class', '', NULL, 0, 1, '警告表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_data` (`id`, `dict_sort`, `dict_label`, `dict_value`, `dict_type`, `css_class`, `list_class`, `is_default`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (34, 6, '危险(danger)', 'danger', 'sys_list_class', '', NULL, 0, 1, '危险表格回显样式', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `system_dict_type`;
CREATE TABLE `system_dict_type` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) DEFAULT NULL COMMENT '字典名称',
  `dict_type` varchar(100) DEFAULT NULL COMMENT '字典类型',
  `status` tinyint(1) DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `dict_name` (`dict_name`),
  UNIQUE KEY `dict_type` (`dict_type`),
  KEY `ix_system_dict_type_creator_id` (`creator_id`),
  CONSTRAINT `system_dict_type_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='数据字典类型表';

-- ----------------------------
-- Records of system_dict_type
-- ----------------------------
BEGIN;
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '用户性别', 'sys_user_sex', 1, '用户性别列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '系统是否', 'sys_yes_no', 1, '系统是否列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, '系统状态', 'sys_common_status', 1, '系统状态', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (4, '通知类型', 'sys_notice_type', 1, '通知类型列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (5, '操作类型', 'sys_oper_type', 1, '操作类型列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (6, '任务存储器', 'sys_job_store', 1, '任务分组列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (7, '任务执行器', 'sys_job_executor', 1, '任务执行器列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (8, '任务函数', 'sys_job_function', 1, '任务函数列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (9, '任务触发器', 'sys_job_trigger', 1, '任务触发器列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_dict_type` (`id`, `dict_name`, `dict_type`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (10, '表格回显样式', 'sys_list_class', 1, '表格回显样式列表', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_menu
-- ----------------------------
DROP TABLE IF EXISTS `system_menu`;
CREATE TABLE `system_menu` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) NOT NULL COMMENT '菜单名称',
  `type` int NOT NULL COMMENT '菜单类型',
  `order` int NOT NULL COMMENT '显示排序',
  `permission` varchar(100) DEFAULT NULL COMMENT '权限标识(如：system:user:list)',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `icon` varchar(50) DEFAULT NULL COMMENT '菜单图标',
  `route_name` varchar(100) DEFAULT NULL COMMENT '路由名称',
  `route_path` varchar(200) DEFAULT NULL COMMENT '路由路径',
  `component_path` varchar(200) DEFAULT NULL COMMENT '组件路径',
  `redirect` varchar(200) DEFAULT NULL COMMENT '重定向地址',
  `hidden` tinyint(1) NOT NULL COMMENT '是否隐藏(True:隐藏 False:显示)',
  `keep_alive` tinyint(1) NOT NULL COMMENT '是否缓存(True:是 False:否)',
  `always_show` tinyint(1) NOT NULL COMMENT '是否始终显示(True:是 False:否)',
  `title` varchar(50) DEFAULT NULL COMMENT '菜单标题',
  `params` text COMMENT '路由参数(JSON数组: [{"key": "", "value": ""}])',
  `affix` tinyint(1) NOT NULL COMMENT '是否固定标签页(True:是 False:否)',
  `parent_id` int DEFAULT NULL COMMENT '父级菜单ID',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_menu_parent_id` (`parent_id`),
  CONSTRAINT `system_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=85 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='菜单表';

-- ----------------------------
-- Records of system_menu
-- ----------------------------
BEGIN;
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (1, '仪表盘', 1, 1, '', 1, 'client', 'Dashboard', '/dashboard', NULL, '/dashboard/workplace', 0, 1, 1, '仪表盘', NULL, 0, NULL, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (2, '工作台', 2, 1, 'dashboard:workplace:query', 1, 'homepage', 'Workplace', '/dashboard/workplace', 'dashboard/workplace', NULL, 0, 1, 0, '工作台', NULL, 1, 1, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (3, '分析页', 2, 2, 'dashboard:analysis:query', 1, 'el-icon-PieChart', 'Analysis', '/dashboard/analysis', 'dashboard/analysis', NULL, 0, 1, 0, '分析页', NULL, 0, 1, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (4, '系统管理', 1, 2, NULL, 1, 'system', 'System', '/system', NULL, '/system/menu', 0, 1, 0, '系统管理', NULL, 0, NULL, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (5, '菜单管理', 2, 1, 'system:menu:query', 1, 'menu', 'Menu', '/system/menu', 'system/menu/index', NULL, 0, 1, 0, '菜单管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (6, '部门管理', 2, 2, 'system:dept:query', 1, 'tree', 'Dept', '/system/dept', 'system/dept/index', NULL, 0, 1, 0, '部门管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (7, '岗位管理', 2, 3, 'system:position:query', 1, 'el-icon-Coordinate', 'Position', '/system/position', 'system/position/index', NULL, 0, 1, 0, '岗位管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (8, '角色管理', 2, 4, 'system:role:query', 1, 'role', 'Role', '/system/role', 'system/role/index', NULL, 0, 1, 0, '角色管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (9, '用户管理', 2, 5, 'system:user:query', 1, 'el-icon-User', 'User', '/system/user', 'system/user/index', NULL, 0, 1, 0, '用户管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (10, '日志管理', 2, 6, 'system:log:query', 1, 'el-icon-Aim', 'Log', '/system/log', 'system/log/index', NULL, 0, 1, 0, '日志管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (11, '公告管理', 2, 7, 'system:notice:query', 1, 'bell', 'Notice', '/system/notice', 'system/notice/index', NULL, 0, 1, 0, '公告管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (12, '配置管理', 2, 8, 'system:config:query', 1, 'setting', 'Config', '/system/config', 'system/config/index', NULL, 0, 1, 0, '配置管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (13, '字典管理', 2, 9, 'system:dict_type:query', 1, 'dict', 'Dict', '/system/dict', 'system/dict/index', NULL, 0, 1, 0, '字典管理', NULL, 0, 4, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (14, '创建菜单', 3, 1, 'system:menu:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建菜单', NULL, 0, 5, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (15, '修改菜单', 3, 2, 'system:menu:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改菜单', NULL, 0, 5, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (16, '删除菜单', 3, 3, 'system:menu:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除菜单', NULL, 0, 5, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (17, '批量修改菜单状态', 3, 4, 'system:menu:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改菜单状态', NULL, 0, 5, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (18, '创建部门', 3, 1, 'system:dept:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建部门', NULL, 0, 6, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (19, '修改部门', 3, 2, 'system:dept:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改部门', NULL, 0, 6, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (20, '删除部门', 3, 3, 'system:dept:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除部门', NULL, 0, 6, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (21, '批量修改部门状态', 3, 4, 'system:dept:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改部门状态', NULL, 0, 6, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (22, '创建岗位', 3, 1, 'system:position:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建岗位', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (23, '修改岗位', 3, 2, 'system:position:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改岗位', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (24, '删除岗位', 3, 3, 'system:position:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改岗位', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (25, '批量修改岗位状态', 3, 4, 'system:position:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改岗位状态', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (26, '岗位导出', 3, 5, 'system:position:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '岗位导出', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (27, '创建角色', 3, 1, 'system:role:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建角色', NULL, 0, 8, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (28, '修改角色', 3, 2, 'system:role:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改角色', NULL, 0, 8, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (29, '删除角色', 3, 3, 'system:role:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除角色', NULL, 0, 8, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (30, '批量修改角色状态', 3, 4, 'system:role:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改角色状态', NULL, 0, 8, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (31, '设置角色权限', 3, 8, 'system:role:permission', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '设置角色权限', NULL, 0, 7, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (32, '角色导出', 3, 6, 'system:role:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '角色导出', NULL, 0, 8, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (33, '创建用户', 3, 1, 'system:user:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建用户', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (34, '修改用户', 3, 2, 'system:user:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改用户', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (35, '删除用户', 3, 3, 'system:user:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除用户', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (36, '批量修改用户状态', 3, 4, 'system:user:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改用户状态', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (37, '导出用户', 3, 5, 'system:user:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出用户', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (38, '导入用户', 3, 6, 'system:user:import', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导入用户', NULL, 0, 9, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (39, '日志删除', 3, 1, 'system:operation_log:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '日志删除', NULL, 0, 10, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (40, '日志导出', 3, 2, 'system:operation_log:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '日志导出', NULL, 0, 10, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (41, '公告创建', 3, 1, 'system:notice:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '公告创建', NULL, 0, 11, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (42, '公告修改', 3, 2, 'system:notice:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改用户', NULL, 0, 11, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (43, '公告删除', 3, 3, 'system:notice:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '公告删除', NULL, 0, 11, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (44, '公告导出', 3, 4, 'system:notice:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '公告导出', NULL, 0, 11, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (45, '公告批量修改状态', 3, 5, 'system:notice:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '公告批量修改状态', NULL, 0, 11, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (46, '创建配置', 3, 1, 'system:config:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建配置', NULL, 0, 12, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (47, '修改配置', 3, 2, 'system:config:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改配置', NULL, 0, 12, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (48, '删除配置', 3, 3, 'system:config:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除配置', NULL, 0, 12, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (49, '导出配置', 3, 4, 'system:config:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出配置', NULL, 0, 12, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (50, '配置上传', 3, 5, 'system:config:upload', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '配置上传', NULL, 0, 12, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (51, '创建字典类型', 3, 1, 'system:dict_type:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建字典类型', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (52, '修改字典类型', 3, 2, 'system:dict_type:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改字典类型', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (53, '删除字典类型', 3, 3, 'system:dict_type:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除字典类型', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (54, '导出字典类型', 3, 4, 'system:dict_type:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出字典类型', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (55, '批量修改字典状态', 3, 5, 'system:dict_type:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出字典类型', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (56, '字典数据查询', 3, 6, 'system:dict_data:query', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '字典数据查询', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (57, '创建字典数据', 3, 7, 'system:dict_data:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建字典数据', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (58, '修改字典数据', 3, 8, 'system:dict_data:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改字典数据', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (59, '删除字典数据', 3, 9, 'system:dict_data:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除字典数据', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (60, '导出字典数据', 3, 10, 'system:dict_data:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出字典数据', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (61, '批量修改字典数据状态', 3, 11, 'system:dict_data:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改字典数据状态', NULL, 0, 13, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (62, '监控管理', 1, 3, NULL, 1, 'monitor', 'Monitor', '/monitor', NULL, '/monitor/online', 0, 0, 0, '监控管理', NULL, 0, NULL, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (63, '任务管理', 2, 1, 'monitor:job:query', 1, 'el-icon-DataLine', 'Job', '/monitor/job', 'monitor/job/index', NULL, 0, 1, 0, '任务管理', NULL, 0, 62, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (64, '创建任务', 3, 1, 'monitor:job:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建任务', NULL, 0, 63, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (65, '修改和操作任务', 3, 2, 'monitor:job:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '修改和操作任务', NULL, 0, 63, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (66, '删除和清除任务', 3, 3, 'monitor:job:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除和清除任务', NULL, 0, 63, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (67, '导出定时任务', 3, 4, 'monitor:job:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出定时任务', NULL, 0, 63, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (68, '在线用户', 2, 2, 'monitor:online:query', 1, 'el-icon-Headset', 'MonitorOnline', '/monitor/online', 'monitor/online/index', NULL, 0, 0, 0, '在线用户', NULL, 0, 62, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (69, '在线用户强制下线', 3, 1, 'monitor:online:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, '在线用户强制下线', NULL, 0, 68, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (70, '服务器监控', 2, 3, 'monitor:server:query', 1, 'el-icon-Odometer', 'MonitorServer', '/monitor/server', 'monitor/server/index', NULL, 0, 0, 0, '服务器监控', NULL, 0, 62, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (71, '缓存监控', 2, 4, 'monitor:cache:query', 1, 'el-icon-Stopwatch', 'MonitorCache', '/monitor/cache', 'monitor/cache/index', NULL, 0, 0, 0, '缓存监控', NULL, 0, 62, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (72, '清除缓存', 3, 1, 'monitor:cache:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, '清除缓存', NULL, 0, 71, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (73, '公共模块', 1, 4, NULL, 1, 'document', 'Common', '/common', NULL, '/common/docs', 0, 0, 0, '公共模块', NULL, 0, NULL, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (74, '接口管理', 4, 1, 'common:docs:query', 1, 'api', 'Docs', '/common/docs', 'common/docs/index', NULL, 0, 0, 0, '接口管理', NULL, 0, 73, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (75, '文档管理', 4, 2, 'common:redoc:query', 1, 'el-icon-Document', 'Redoc', '/common/redoc', 'common/redoc/index', NULL, 0, 0, 0, '文档管理', NULL, 0, 73, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (76, '演示模块', 1, 5, NULL, 1, 'el-icon-Document', 'Demo', '/demo', NULL, '/demo/example', 0, 0, 0, '演示模块', NULL, 0, NULL, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (77, '示例管理', 2, 1, 'demo:example:query', 1, 'el-icon-DataLine', 'Example', '/demo/example', 'demo/example/index', NULL, 0, 1, 0, '示例管理', NULL, 0, 76, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (78, '创建示例', 3, 1, 'demo:example:create', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '创建示例', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (79, '更新示例', 3, 2, 'demo:example:update', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '更新示例', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (80, '删除示例', 3, 3, 'demo:example:delete', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '删除示例', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (81, '批量修改示例状态', 3, 4, 'demo:example:patch', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '批量修改示例状态', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (82, '导出示例', 3, 5, 'demo:example:export', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导出示例', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (83, '导入示例', 3, 6, 'demo:example:import', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '导入示例', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
INSERT INTO `system_menu` (`id`, `name`, `type`, `order`, `permission`, `status`, `icon`, `route_name`, `route_path`, `component_path`, `redirect`, `hidden`, `keep_alive`, `always_show`, `title`, `params`, `affix`, `parent_id`, `description`, `created_at`, `updated_at`) VALUES (84, '下载导入示例模版', 3, 7, 'demo:example:download', 1, NULL, NULL, NULL, NULL, NULL, 0, 1, 0, '下载导入示例模版', NULL, 0, 77, '初始化数据', '2025-08-05 00:25:40', '2025-08-05 00:25:40');
COMMIT;

-- ----------------------------
-- Table structure for system_notice
-- ----------------------------
DROP TABLE IF EXISTS `system_notice`;
CREATE TABLE `system_notice` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `notice_title` varchar(50) NOT NULL COMMENT '公告标题',
  `notice_type` varchar(50) NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` text COMMENT '公告内容',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_notice_creator_id` (`creator_id`),
  CONSTRAINT `system_notice_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='通知公告表';

-- ----------------------------
-- Records of system_notice
-- ----------------------------
BEGIN;
INSERT INTO `system_notice` (`id`, `notice_title`, `notice_type`, `notice_content`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '系统更新', '1', '2099年9月9日，晚上12:00，系统更新', 1, '系统更新', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_notice` (`id`, `notice_title`, `notice_type`, `notice_content`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '系统维护', '2', '2099年9月9日，晚上12:00，系统维护', 1, '系统维护', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_notice` (`id`, `notice_title`, `notice_type`, `notice_content`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, '系统更新完成', '1', '2099年9月9日，晚上12:00，系统更新完成', 0, '系统更新完成', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_notice` (`id`, `notice_title`, `notice_type`, `notice_content`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (4, '系统维护完成', '2', '2099年9月9日，晚上12:00，系统维护完成', 0, '系统维护完成', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_operation_log
-- ----------------------------
DROP TABLE IF EXISTS `system_operation_log`;
CREATE TABLE `system_operation_log` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type` int DEFAULT NULL COMMENT '日志类型(1登录日志 2操作日志)',
  `request_path` varchar(255) DEFAULT NULL COMMENT '请求路径',
  `request_method` varchar(10) DEFAULT NULL COMMENT '请求方式',
  `request_payload` text COMMENT '请求体',
  `request_ip` varchar(50) DEFAULT NULL COMMENT '请求IP地址',
  `login_location` varchar(255) DEFAULT NULL COMMENT '登录位置',
  `request_os` varchar(64) DEFAULT NULL COMMENT '操作系统',
  `request_browser` varchar(64) DEFAULT NULL COMMENT '浏览器',
  `response_code` int DEFAULT NULL COMMENT '响应状态码',
  `response_json` text COMMENT '响应体',
  `process_time` varchar(20) DEFAULT NULL COMMENT '处理时间',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  KEY `ix_system_operation_log_type` (`type`),
  KEY `ix_system_operation_log_request_method` (`request_method`),
  KEY `ix_system_operation_log_request_path` (`request_path`),
  KEY `ix_system_operation_log_creator_id` (`creator_id`),
  CONSTRAINT `system_operation_log_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='操作日志表';

-- ----------------------------
-- Records of system_operation_log
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for system_position
-- ----------------------------
DROP TABLE IF EXISTS `system_position`;
CREATE TABLE `system_position` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '岗位名称',
  `order` int NOT NULL COMMENT '显示排序',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_position_creator_id` (`creator_id`),
  CONSTRAINT `system_position_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位表';

-- ----------------------------
-- Records of system_position
-- ----------------------------
BEGIN;
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '董事长岗', 1, 1, '董事长岗位', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '运营岗', 2, 1, '运营岗位', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (3, '销售岗', 3, 1, '销售岗', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (4, '人事行政岗', 4, 1, '人事行政岗', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (5, '开发岗', 5, 1, '开发岗', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (6, '测试岗', 6, 1, '测试岗', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_position` (`id`, `name`, `order`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (7, '演示岗', 7, 1, '演示岗', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_role
-- ----------------------------
DROP TABLE IF EXISTS `system_role`;
CREATE TABLE `system_role` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(40) NOT NULL COMMENT '角色名称',
  `order` int NOT NULL COMMENT '显示排序',
  `data_scope` int NOT NULL COMMENT '数据权限范围',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
  `description` text COMMENT '备注说明',
  `created_at` datetime DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime DEFAULT NULL COMMENT '更新时间',
  `creator_id` int DEFAULT NULL COMMENT '创建人ID',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_system_role_creator_id` (`creator_id`),
  CONSTRAINT `system_role_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色表';

-- ----------------------------
-- Records of system_role
-- ----------------------------
BEGIN;
INSERT INTO `system_role` (`id`, `name`, `order`, `data_scope`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, '管理员角色', 1, 4, 1, '管理员', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
INSERT INTO `system_role` (`id`, `name`, `order`, `data_scope`, `status`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, '普通角色', 2, 1, 1, '普通角色', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

-- ----------------------------
-- Table structure for system_role_depts
-- ----------------------------
DROP TABLE IF EXISTS `system_role_depts`;
CREATE TABLE `system_role_depts` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `dept_id` int NOT NULL COMMENT '部门ID',
  PRIMARY KEY (`role_id`,`dept_id`),
  KEY `ix_system_role_depts_role_id` (`role_id`),
  KEY `ix_system_role_depts_dept_id` (`dept_id`),
  CONSTRAINT `system_role_depts_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_role_depts_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色部门关联表';

-- ----------------------------
-- Records of system_role_depts
-- ----------------------------
BEGIN;
INSERT INTO `system_role_depts` (`role_id`, `dept_id`) VALUES (1, 1);
INSERT INTO `system_role_depts` (`role_id`, `dept_id`) VALUES (2, 1);
INSERT INTO `system_role_depts` (`role_id`, `dept_id`) VALUES (2, 6);
COMMIT;

-- ----------------------------
-- Table structure for system_role_menus
-- ----------------------------
DROP TABLE IF EXISTS `system_role_menus`;
CREATE TABLE `system_role_menus` (
  `role_id` int NOT NULL COMMENT '角色ID',
  `menu_id` int NOT NULL COMMENT '菜单ID',
  PRIMARY KEY (`role_id`,`menu_id`),
  KEY `ix_system_role_menus_role_id` (`role_id`),
  KEY `ix_system_role_menus_menu_id` (`menu_id`),
  CONSTRAINT `system_role_menus_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='角色菜单关联表';

-- ----------------------------
-- Records of system_role_menus
-- ----------------------------
BEGIN;
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 1);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 2);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 3);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 4);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 5);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 6);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 7);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 8);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 9);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 10);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 11);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 12);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 13);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 14);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 15);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 16);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 17);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 18);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 19);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 20);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 21);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 22);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 23);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 24);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 25);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 26);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 27);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 28);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 29);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 30);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 31);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 32);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 33);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 34);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 35);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 36);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 37);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 38);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 39);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 40);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 41);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 42);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 43);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 44);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 45);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 46);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 47);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 48);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 49);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 50);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 51);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 52);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 53);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 54);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 55);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 56);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 57);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 58);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 59);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 60);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 61);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 62);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 63);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 64);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 65);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 66);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 67);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 68);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 69);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 70);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 71);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 72);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 73);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 74);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 75);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 76);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 77);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 78);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 79);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 80);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 81);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 82);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 83);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (1, 84);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (2, 1);
INSERT INTO `system_role_menus` (`role_id`, `menu_id`) VALUES (2, 2);
COMMIT;

-- ----------------------------
-- Table structure for system_user_positions
-- ----------------------------
DROP TABLE IF EXISTS `system_user_positions`;
CREATE TABLE `system_user_positions` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `position_id` int NOT NULL COMMENT '岗位ID',
  PRIMARY KEY (`user_id`,`position_id`),
  KEY `ix_system_user_positions_user_id` (`user_id`),
  KEY `ix_system_user_positions_position_id` (`position_id`),
  CONSTRAINT `system_user_positions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_user_positions_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `system_position` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户岗位关联表';

-- ----------------------------
-- Records of system_user_positions
-- ----------------------------
BEGIN;
INSERT INTO `system_user_positions` (`user_id`, `position_id`) VALUES (1, 5);
INSERT INTO `system_user_positions` (`user_id`, `position_id`) VALUES (2, 7);
COMMIT;

-- ----------------------------
-- Table structure for system_user_roles
-- ----------------------------
DROP TABLE IF EXISTS `system_user_roles`;
CREATE TABLE `system_user_roles` (
  `user_id` int NOT NULL COMMENT '用户ID',
  `role_id` int NOT NULL COMMENT '角色ID',
  PRIMARY KEY (`user_id`,`role_id`),
  KEY `ix_system_user_roles_user_id` (`user_id`),
  KEY `ix_system_user_roles_role_id` (`role_id`),
  CONSTRAINT `system_user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `system_user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户角色关联表';

-- ----------------------------
-- Records of system_user_roles
-- ----------------------------
BEGIN;
INSERT INTO `system_user_roles` (`user_id`, `role_id`) VALUES (1, 1);
INSERT INTO `system_user_roles` (`user_id`, `role_id`) VALUES (2, 2);
COMMIT;

-- ----------------------------
-- Table structure for system_users
-- ----------------------------
DROP TABLE IF EXISTS `system_users`;
CREATE TABLE `system_users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(150) NOT NULL COMMENT '用户名/登录账号',
  `password` varchar(128) NOT NULL COMMENT '密码',
  `name` varchar(40) NOT NULL COMMENT '姓名',
  `mobile` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(255) DEFAULT NULL COMMENT '邮箱',
  `gender` varchar(20) DEFAULT NULL COMMENT '性别(0:男 1:女 2:未知)',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像地址',
  `status` tinyint(1) NOT NULL COMMENT '是否启用(True:启用 False:禁用)',
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

-- ----------------------------
-- Records of system_users
-- ----------------------------
BEGIN;
INSERT INTO `system_users` (`id`, `username`, `password`, `name`, `mobile`, `email`, `gender`, `avatar`, `status`, `is_superuser`, `last_login`, `dept_id`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (1, 'admin', '$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa', '管理员', '15382112222', 'admin@qq.com', '0', 'https://service.fastapiadmin.com/api/v1/static/image/avatar.png', 1, 1, NULL, 1, '超级管理员', '2025-08-05 00:25:40', '2025-08-05 00:25:40', NULL);
INSERT INTO `system_users` (`id`, `username`, `password`, `name`, `mobile`, `email`, `gender`, `avatar`, `status`, `is_superuser`, `last_login`, `dept_id`, `description`, `created_at`, `updated_at`, `creator_id`) VALUES (2, 'demo', '$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa', '演示用户', '15382112121', 'demo@qq.com', '1', 'https://service.fastapiadmin.com/api/v1/static/image/avatar.png', 1, 0, NULL, 6, '演示用户', '2025-08-05 00:25:40', '2025-08-05 00:25:40', 1);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
