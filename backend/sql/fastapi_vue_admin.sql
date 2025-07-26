SET FOREIGN_KEY_CHECKS = 0;
SET NAMES utf8mb4;
-- fastapi_vue_admin DDL
CREATE DATABASE `fastapi_vue_admin`
CHARACTER SET utf8mb4
COLLATE utf8mb4_0900_ai_ci;;
use `fastapi_vue_admin`;
-- fastapi_vue_admin.system_config DDL
CREATE TABLE `fastapi_vue_admin`.`system_config` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`config_name` VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "参数名称",
`config_key` VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "参数键名",
`config_value` VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "参数键值",
`config_type` TINYINT(3) NOT NULL Comment "系统内置((True:是 False:否))",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
UNIQUE INDEX `config_key`(`config_key` ASC) USING BTREE,
UNIQUE INDEX `config_name`(`config_name` ASC) USING BTREE,
INDEX `ix_system_config_creator_id`(`creator_id` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 12 ROW_FORMAT = Dynamic COMMENT = "配置表";
-- fastapi_vue_admin.system_dept DDL
CREATE TABLE `fastapi_vue_admin`.`system_dept` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`name` VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "部门名称",
`order` INT(10) NOT NULL Comment "显示排序",
`parent_id` INT(10) NULL Comment "父级部门ID",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
INDEX `ix_system_dept_parent_id`(`parent_id` ASC) USING BTREE,
UNIQUE INDEX `name`(`name` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 11 ROW_FORMAT = Dynamic COMMENT = "部门表";
-- fastapi_vue_admin.system_dict_data DDL
CREATE TABLE `fastapi_vue_admin`.`system_dict_data` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "字典编码",
`dict_sort` INT(10) NULL Comment "字典排序",
`dict_label` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "字典标签",
`dict_value` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "字典键值",
`dict_type` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "字典类型",
`css_class` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "样式属性（其他样式扩展）",
`list_class` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "表格回显样式",
`is_default` TINYINT(3) NULL Comment "是否默认（Y是 N否）",
`status` TINYINT(3) NULL Comment "状态（0正常 1停用）",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_dict_data_creator_id`(`creator_id` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 42 ROW_FORMAT = Dynamic COMMENT = "数据字典数据表";
-- fastapi_vue_admin.system_dict_type DDL
CREATE TABLE `fastapi_vue_admin`.`system_dict_type` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "字典主键",
`dict_name` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "字典名称",
`dict_type` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "字典类型",
`status` TINYINT(3) NULL Comment "状态（0正常 1停用）",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
UNIQUE INDEX `dict_name`(`dict_name` ASC) USING BTREE,
UNIQUE INDEX `dict_type`(`dict_type` ASC) USING BTREE,
INDEX `ix_system_dict_type_creator_id`(`creator_id` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 14 ROW_FORMAT = Dynamic COMMENT = "数据字典类型表";
-- fastapi_vue_admin.system_job DDL
CREATE TABLE `fastapi_vue_admin`.`system_job` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "任务ID",
`name` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "任务名称",
`jobstore` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "存储器",
`executor` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "执行器:将运行此作业的执行程序的名称",
`trigger` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "触发器:控制此作业计划的 trigger 对象",
`trigger_args` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "触发器参数",
`func` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "任务函数",
`args` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "位置参数",
`kwargs` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "关键字参数",
`coalesce` TINYINT(3) NULL Comment "是否合并运行:是否在多个运行时间到期时仅运行作业一次",
`max_instances` INT(10) NULL Comment "最大实例数:允许的最大并发执行实例数 工作",
`start_date` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "开始时间",
`end_date` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "结束时间",
`status` TINYINT(3) NULL Comment "任务状态:正常,停止",
`message` VARCHAR(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "日志信息",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_job_creator_id`(`creator_id` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 3 ROW_FORMAT = Dynamic COMMENT = "定时任务调度表";
-- fastapi_vue_admin.system_menu DDL
CREATE TABLE `fastapi_vue_admin`.`system_menu` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`name` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "菜单名称",
`type` INT(10) NOT NULL Comment "菜单类型",
`order` INT(10) NOT NULL Comment "显示排序",
`permission` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "权限标识(如：system:user:list)",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`icon` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "菜单图标",
`route_name` VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "路由名称",
`route_path` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "路由路径",
`component_path` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "组件路径",
`redirect` VARCHAR(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "重定向地址",
`hidden` TINYINT(3) NOT NULL Comment "是否隐藏(True:隐藏 False:显示)",
`keep_alive` TINYINT(3) NOT NULL Comment "是否缓存(True:是 False:否)",
`always_show` TINYINT(3) NOT NULL Comment "是否始终显示(True:是 False:否)",
`title` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "菜单标题",
`params` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "路由参数(JSON数组: [{\"key\": \"\", \"value\": \"\"}])",
`affix` TINYINT(3) NOT NULL Comment "是否固定标签页(True:是 False:否)",
`parent_id` INT(10) NULL Comment "父级菜单ID",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
INDEX `ix_system_menu_parent_id`(`parent_id` ASC) USING BTREE,
UNIQUE INDEX `name`(`name` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 75 ROW_FORMAT = Dynamic COMMENT = "菜单表";
-- fastapi_vue_admin.system_notice DDL
CREATE TABLE `fastapi_vue_admin`.`system_notice` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`notice_title` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "公告标题",
`notice_type` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "公告类型（1通知 2公告）",
`notice_content` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "公告内容",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_notice_creator_id`(`creator_id` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 4 ROW_FORMAT = Dynamic COMMENT = "通知公告表";
-- fastapi_vue_admin.system_operation_log DDL
CREATE TABLE `fastapi_vue_admin`.`system_operation_log` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`type` INT(10) NULL Comment "日志类型(1登录日志 2操作日志)",
`request_path` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "请求路径",
`request_method` VARCHAR(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "请求方式",
`request_payload` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "请求体",
`request_ip` VARCHAR(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "请求IP地址",
`login_location` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "登录位置",
`request_os` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "操作系统",
`request_browser` VARCHAR(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "浏览器",
`response_code` INT(10) NULL Comment "响应状态码",
`response_json` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "响应体",
`process_time` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "处理时间",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_operation_log_creator_id`(`creator_id` ASC) USING BTREE,
INDEX `ix_system_operation_log_request_method`(`request_method` ASC) USING BTREE,
INDEX `ix_system_operation_log_request_path`(`request_path` ASC) USING BTREE,
INDEX `ix_system_operation_log_type`(`type` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 1 ROW_FORMAT = Dynamic COMMENT = "操作日志表";
-- fastapi_vue_admin.system_position DDL
CREATE TABLE `fastapi_vue_admin`.`system_position` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`name` VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "岗位名称",
`order` INT(10) NOT NULL Comment "显示排序",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_position_creator_id`(`creator_id` ASC) USING BTREE,
UNIQUE INDEX `name`(`name` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 7 ROW_FORMAT = Dynamic COMMENT = "岗位表";
-- fastapi_vue_admin.system_role DDL
CREATE TABLE `fastapi_vue_admin`.`system_role` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`name` VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "角色名称",
`order` INT(10) NOT NULL Comment "显示排序",
`data_scope` INT(10) NOT NULL Comment "数据权限范围",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_role_creator_id`(`creator_id` ASC) USING BTREE,
UNIQUE INDEX `name`(`name` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 2 ROW_FORMAT = Dynamic COMMENT = "角色表";
-- fastapi_vue_admin.system_role_depts DDL
CREATE TABLE `fastapi_vue_admin`.`system_role_depts` (`role_id` INT(10) NOT NULL Comment "角色ID",
`dept_id` INT(10) NOT NULL Comment "部门ID",
INDEX `ix_system_role_depts_dept_id`(`dept_id` ASC) USING BTREE,
INDEX `ix_system_role_depts_role_id`(`role_id` ASC) USING BTREE,
PRIMARY KEY (`role_id`,
`dept_id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic COMMENT = "角色部门关联表";
-- fastapi_vue_admin.system_role_menus DDL
CREATE TABLE `fastapi_vue_admin`.`system_role_menus` (`role_id` INT(10) NOT NULL Comment "角色ID",
`menu_id` INT(10) NOT NULL Comment "菜单ID",
INDEX `ix_system_role_menus_menu_id`(`menu_id` ASC) USING BTREE,
INDEX `ix_system_role_menus_role_id`(`role_id` ASC) USING BTREE,
PRIMARY KEY (`role_id`,
`menu_id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic COMMENT = "角色菜单关联表";
-- fastapi_vue_admin.system_user_positions DDL
CREATE TABLE `fastapi_vue_admin`.`system_user_positions` (`user_id` INT(10) NOT NULL Comment "用户ID",
`position_id` INT(10) NOT NULL Comment "岗位ID",
INDEX `ix_system_user_positions_position_id`(`position_id` ASC) USING BTREE,
INDEX `ix_system_user_positions_user_id`(`user_id` ASC) USING BTREE,
PRIMARY KEY (`user_id`,
`position_id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic COMMENT = "用户岗位关联表";
-- fastapi_vue_admin.system_user_roles DDL
CREATE TABLE `fastapi_vue_admin`.`system_user_roles` (`user_id` INT(10) NOT NULL Comment "用户ID",
`role_id` INT(10) NOT NULL Comment "角色ID",
INDEX `ix_system_user_roles_role_id`(`role_id` ASC) USING BTREE,
INDEX `ix_system_user_roles_user_id`(`user_id` ASC) USING BTREE,
PRIMARY KEY (`user_id`,
`role_id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic COMMENT = "用户角色关联表";
-- fastapi_vue_admin.system_users DDL
CREATE TABLE `fastapi_vue_admin`.`system_users` (`id` INT(10) NOT NULL AUTO_INCREMENT Comment "主键ID",
`username` VARCHAR(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "用户名/登录账号",
`password` VARCHAR(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "密码",
`name` VARCHAR(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL Comment "姓名",
`mobile` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "手机号",
`email` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "邮箱",
`gender` VARCHAR(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "性别(0:男 1:女 2:未知)",
`avatar` VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "头像地址",
`status` TINYINT(3) NOT NULL Comment "是否启用(True:启用 False:禁用)",
`is_superuser` TINYINT(3) NOT NULL Comment "是否为超级管理员",
`last_login` DATETIME NULL Comment "最后登录时间",
`dept_id` INT(10) NULL Comment "部门ID",
`description` TEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL Comment "备注说明",
`created_at` DATETIME NULL Comment "创建时间",
`updated_at` DATETIME NULL Comment "更新时间",
`creator_id` INT(10) NULL Comment "创建人ID",
INDEX `ix_system_users_creator_id`(`creator_id` ASC) USING BTREE,
INDEX `ix_system_users_dept_id`(`dept_id` ASC) USING BTREE,
UNIQUE INDEX `username`(`username` ASC) USING BTREE,
PRIMARY KEY (`id`)) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci AUTO_INCREMENT = 2 ROW_FORMAT = Dynamic COMMENT = "用户表";
-- fastapi_vue_admin.system_config Indexes
ALTER TABLE `fastapi_vue_admin`.`system_config` 
 ADD CONSTRAINT `system_config_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_dept Indexes
ALTER TABLE `fastapi_vue_admin`.`system_dept` 
 ADD CONSTRAINT `system_dept_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_dict_data Indexes
ALTER TABLE `fastapi_vue_admin`.`system_dict_data` 
 ADD CONSTRAINT `system_dict_data_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_dict_type Indexes
ALTER TABLE `fastapi_vue_admin`.`system_dict_type` 
 ADD CONSTRAINT `system_dict_type_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_job Indexes
ALTER TABLE `fastapi_vue_admin`.`system_job` 
 ADD CONSTRAINT `system_job_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_menu Indexes
ALTER TABLE `fastapi_vue_admin`.`system_menu` 
 ADD CONSTRAINT `system_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_notice Indexes
ALTER TABLE `fastapi_vue_admin`.`system_notice` 
 ADD CONSTRAINT `system_notice_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_operation_log Indexes
ALTER TABLE `fastapi_vue_admin`.`system_operation_log` 
 ADD CONSTRAINT `system_operation_log_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_position Indexes
ALTER TABLE `fastapi_vue_admin`.`system_position` 
 ADD CONSTRAINT `system_position_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_role Indexes
ALTER TABLE `fastapi_vue_admin`.`system_role` 
 ADD CONSTRAINT `system_role_ibfk_1` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_role_depts Indexes
ALTER TABLE `fastapi_vue_admin`.`system_role_depts` 
 ADD CONSTRAINT `system_role_depts_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `system_role_depts_ibfk_2` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_role_menus Indexes
ALTER TABLE `fastapi_vue_admin`.`system_role_menus` 
 ADD CONSTRAINT `system_role_menus_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `system_role_menus_ibfk_2` FOREIGN KEY (`menu_id`) REFERENCES `system_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_user_positions Indexes
ALTER TABLE `fastapi_vue_admin`.`system_user_positions` 
 ADD CONSTRAINT `system_user_positions_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `system_position` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `system_user_positions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_user_roles Indexes
ALTER TABLE `fastapi_vue_admin`.`system_user_roles` 
 ADD CONSTRAINT `system_user_roles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `system_users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
ADD CONSTRAINT `system_user_roles_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `system_role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
-- fastapi_vue_admin.system_users Indexes
ALTER TABLE `fastapi_vue_admin`.`system_users` 
 ADD CONSTRAINT `system_users_ibfk_1` FOREIGN KEY (`dept_id`) REFERENCES `system_dept` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
ADD CONSTRAINT `system_users_ibfk_2` FOREIGN KEY (`creator_id`) REFERENCES `system_users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;
-- fastapi_vue_admin.system_config DML
INSERT INTO `fastapi_vue_admin`.`system_config` (`id`,`config_name`,`config_key`,`config_value`,`config_type`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'网站名称','sys_web_title','FastAPI Vue3 Admin',1,'网站名称','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,'网站描述','sys_web_description','FastAPI Vue3 Admin 是完全开源的权限管理系统',1,'网站描述','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(3,'网页图标','sys_web_favicon','http://service.fastapiadmin.com/api/v1/static/image/favicon.png',1,'网页图标','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(4,'网站Logo','sys_web_logo','http://service.fastapiadmin.com/api/v1/static/image/logo.png',1,'网站Logo','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(5,'登录背景','sys_login_background','http://service.fastapiadmin.com/api/v1/static/image/background.png',1,'登录背景','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(6,'版权信息','sys_web_copyright','Copyright © 2025-2026 service.fastapiadmin.com 版权所有',1,'版权信息','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(7,'备案信息','sys_keep_record','陕ICP备2025069493号-1',1,'备案信息','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(8,'帮助文档','sys_help_doc','http://service.fastapiadmin.com/site/index.html',1,'帮助文档','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(9,'隐私政策','sys_web_privacy','https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE',1,'隐私政策','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(10,'用户协议','sys_web_clause','https://github.com/1014TaoTao/fastapi_vue3_admin/blob/master/LICENSE',1,'用户协议','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(11,'源码代码','sys_git_code','https://github.com/1014TaoTao/fastapi_vue3_admin.git',1,'源码代码','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(12,'项目版本','sys_web_version','2.0.0',1,'项目版本','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_dept DML
INSERT INTO `fastapi_vue_admin`.`system_dept` (`id`,`name`,`order`,`parent_id`,`status`,`description`,`created_at`,`updated_at`) VALUES (1,'集团总公司',1,NULL,1,'集团总公司','2025-07-24 00:22:20','2025-07-24 00:22:20'),(2,'西安分公司',1,1,1,'西安分公司','2025-07-24 00:22:20','2025-07-24 00:22:20'),(3,'深圳分公司',2,1,1,'深圳分公司','2025-07-24 00:22:20','2025-07-24 00:22:20'),(4,'开发组',1,2,1,'开发组','2025-07-24 00:22:20','2025-07-24 00:22:20'),(5,'测试组',2,2,1,'测试组','2025-07-24 00:22:20','2025-07-24 00:22:20'),(6,'演示组',3,2,1,'演示组','2025-07-24 00:22:20','2025-07-24 00:22:20'),(7,'销售部',1,3,1,'销售部','2025-07-24 00:22:20','2025-07-24 00:22:20'),(8,'市场部',2,3,1,'市场部','2025-07-24 00:22:20','2025-07-24 00:22:20'),(9,'财务部',3,3,1,'财务部','2025-07-24 00:22:20','2025-07-24 00:22:20'),(10,'研发部',4,3,1,'研发部','2025-07-24 00:22:20','2025-07-24 00:22:20'),(11,'运维部',5,3,1,'研发部','2025-07-24 00:22:20','2025-07-24 00:22:20');
-- fastapi_vue_admin.system_dict_data DML
INSERT INTO `fastapi_vue_admin`.`system_dict_data` (`id`,`dict_sort`,`dict_label`,`dict_value`,`dict_type`,`css_class`,`list_class`,`is_default`,`status`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,1,'男','0','sys_user_sex','blue',NULL,1,1,'性别男','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,2,'女','1','sys_user_sex','pink',NULL,0,1,'性别女','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(3,3,'未知','2','sys_user_sex','red',NULL,0,1,'性别未知','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(4,4,'显示','0','sys_show_hide','btn btn-success btn-xs','primary',1,1,'显示菜单','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(5,2,'隐藏','1','sys_show_hide','','danger',0,1,'隐藏菜单','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(6,1,'正常','0','sys_normal_disable','','primary',1,1,'正常状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(7,2,'停用','1','sys_normal_disable','','danger',0,1,'停用状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(8,1,'正常','0','sys_job_status','','primary',1,1,'正常状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(9,2,'暂停','1','sys_job_status','','danger',0,1,'停用状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(10,1,'默认(Memory)','default','sys_job_group','',NULL,1,1,'默认分组','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(11,2,'数据库','sqlalchemy','sys_job_group','',NULL,0,1,'数据库分组','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(12,3,'redis','redis','sys_job_group','',NULL,0,1,'reids分组','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(13,1,'默认','default','sys_job_executor','',NULL,0,1,'线程池','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(14,2,'进程池','processpool','sys_job_executor','',NULL,0,1,'进程池','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(15,1,'是','true','sys_yes_no','','primary',1,1,'系统默认是','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(16,2,'否','false','sys_yes_no','','danger',0,1,'系统默认否','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(17,1,'通知','1','sys_notice_type','blue','warning',1,1,'通知','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(18,2,'公告','2','sys_notice_type','orange','success',0,1,'公告','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(19,1,'正常','0','sys_notice_status','','primary',1,1,'正常状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(20,2,'关闭','1','sys_notice_status','','danger',0,1,'关闭状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(21,99,'其他','0','sys_oper_type','','info',0,1,'其他操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(22,1,'新增','1','sys_oper_type','','info',0,1,'新增操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(23,2,'修改','2','sys_oper_type','','info',0,1,'修改操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(24,3,'删除','3','sys_oper_type','','danger',0,1,'删除操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(25,4,'授权','4','sys_oper_type','','primary',0,1,'授权操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(26,5,'导出','5','sys_oper_type','','warning',0,1,'导出操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(27,6,'导入','6','sys_oper_type','','warning',0,1,'导入操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(28,7,'强退','7','sys_oper_type','','danger',0,1,'强退操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(29,8,'生成代码','8','sys_oper_type','','warning',0,1,'生成操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(30,9,'清空数据','9','sys_oper_type','','danger',0,1,'清空操作','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(31,1,'成功','0','sys_common_status','','primary',0,1,'正常状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(32,2,'失败','1','sys_common_status','','danger',0,1,'停用状态','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(33,1,'初始化演示函数','scheduler_test.job','sys_job_function','',NULL,1,1,'演示函数','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(34,1,'指定日期(date)','date','sys_job_trigger','',NULL,1,1,'指定日期任务触发器','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(35,2,'间隔触发器(interval)','interval','sys_job_trigger','',NULL,0,1,'间隔触发器任务触发器','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(36,3,'cron表达式','cron','sys_job_trigger','',NULL,0,1,'间隔触发器任务触发器','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(37,1,'默认(default)','default','sys_dictdata_list_class','',NULL,1,1,'默认表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(38,2,'主要(primary)','primary','sys_dictdata_list_class','',NULL,0,1,'主要表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(39,3,'成功(success)','success','sys_dictdata_list_class','',NULL,0,1,'成功表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(40,4,'信息(info)','info','sys_dictdata_list_class','',NULL,0,1,'信息表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(41,5,'警告(warning)','warning','sys_dictdata_list_class','',NULL,0,1,'警告表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(42,6,'危险(danger)','danger','sys_dictdata_list_class','',NULL,0,1,'危险表格回显样式','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_dict_type DML
INSERT INTO `fastapi_vue_admin`.`system_dict_type` (`id`,`dict_name`,`dict_type`,`status`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'用户性别','sys_user_sex',1,'用户性别列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,'菜单状态','sys_show_hide',1,'菜单状态列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(3,'系统开关','sys_normal_disable',1,'系统开关列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(4,'任务状态','sys_job_status',1,'任务状态列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(5,'任务分组','sys_job_group',1,'任务分组列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(6,'任务执行器','sys_job_executor',1,'任务执行器列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(7,'系统是否','sys_yes_no',1,'系统是否列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(8,'通知类型','sys_notice_type',1,'通知类型列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(9,'通知状态','sys_notice_status',1,'通知状态列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(10,'操作类型','sys_oper_type',1,'操作类型列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(11,'系统状态','sys_common_status',1,'登录状态列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(12,'任务函数','sys_job_function',1,'任务函数列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(13,'任务触发器','sys_job_trigger',1,'任务触发器列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(14,'字典配置表格回显样式','sys_dictdata_list_class',1,'字典配置表格回显样式列表','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_job DML
INSERT INTO `fastapi_vue_admin`.`system_job` (`id`,`name`,`jobstore`,`executor`,`trigger`,`trigger_args`,`func`,`args`,`kwargs`,`coalesce`,`max_instances`,`start_date`,`end_date`,`status`,`message`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'系统默认（无参）','default','default','cron','0 0 12 * * ?','scheduler_test.job',NULL,NULL,0,1,NULL,NULL,1,NULL,NULL,'2025-07-24 00:22:20','2025-07-26 16:59:09',1),(2,'系统默认（有参）','default','default','cron','0 0 12 * * ?','scheduler_test.job','test',NULL,0,1,NULL,NULL,1,NULL,NULL,'2025-07-24 00:22:20','2025-07-26 16:59:09',1),(3,'系统默认（多参）','default','default','cron','0 0 12 * * ?','scheduler_test.job','new','{"test": 111}',0,1,NULL,NULL,1,NULL,NULL,'2025-07-24 00:22:20','2025-07-26 16:59:09',1);
-- fastapi_vue_admin.system_menu DML
INSERT INTO `fastapi_vue_admin`.`system_menu` (`id`,`name`,`type`,`order`,`permission`,`status`,`icon`,`route_name`,`route_path`,`component_path`,`redirect`,`hidden`,`keep_alive`,`always_show`,`title`,`params`,`affix`,`parent_id`,`description`,`created_at`,`updated_at`) VALUES (1,'仪表盘',1,1,'',1,'client','Dashboard','/dashboard',NULL,'/dashboard/workplace',0,1,1,'仪表盘',NULL,0,NULL,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(2,'工作台',2,1,'dashboard:workplace:query',1,'homepage','Workplace','/dashboard/workplace','dashboard/workplace',NULL,0,1,0,'工作台',NULL,1,1,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(3,'分析页',2,2,'dashboard:analysis:query',1,'el-icon-PieChart','Analysis','/dashboard/analysis','dashboard/analysis',NULL,0,1,0,'分析页',NULL,0,1,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(4,'系统管理',1,2,NULL,1,'system','System','/system',NULL,'/system/menu',0,1,0,'系统管理',NULL,0,NULL,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(5,'菜单管理',2,1,'system:menu:query',1,'menu','Menu','/system/menu','system/menu/index',NULL,0,1,0,'菜单管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(6,'部门管理',2,2,'system:dept:query',1,'tree','Dept','/system/dept','system/dept/index',NULL,0,1,0,'部门管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(7,'岗位管理',2,3,'system:position:query',1,'el-icon-Coordinate','Position','/system/position','system/position/index',NULL,0,1,0,'岗位管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(8,'角色管理',2,4,'system:role:query',1,'role','Role','/system/role','system/role/index',NULL,0,1,0,'角色管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(9,'用户管理',2,5,'system:user:query',1,'el-icon-User','User','/system/user','system/user/index',NULL,0,1,0,'用户管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(10,'日志管理',2,6,'system:log:query',1,'el-icon-Aim','Log','/system/log','system/log/index',NULL,0,1,0,'日志管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(11,'公告管理',2,7,'system:notice:query',1,'bell','Notice','/system/notice','system/notice/index',NULL,0,1,0,'公告管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(12,'配置管理',2,8,'system:config:query',1,'setting','Config','/system/config','system/config/index',NULL,0,1,0,'配置管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(13,'字典管理',2,9,'system:dict_type:query',1,'dict','Dict','/system/dict','system/dict/index',NULL,0,1,0,'字典管理',NULL,0,4,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(14,'创建菜单',3,1,'system:menu:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建菜单',NULL,0,5,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(15,'修改菜单',3,2,'system:menu:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改菜单',NULL,0,5,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(16,'删除菜单',3,3,'system:menu:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除菜单',NULL,0,5,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(17,'批量修改菜单状态',3,4,'system:menu:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改菜单状态',NULL,0,5,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(18,'创建部门',3,1,'system:dept:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建部门',NULL,0,6,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(19,'修改部门',3,2,'system:dept:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改部门',NULL,0,6,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(20,'删除部门',3,3,'system:dept:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除部门',NULL,0,6,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(21,'批量修改部门状态',3,4,'system:dept:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改部门状态',NULL,0,6,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(22,'创建岗位',3,1,'system:position:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建岗位',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(23,'修改岗位',3,2,'system:position:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(24,'删除岗位',3,3,'system:position:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改岗位',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(25,'批量修改岗位状态',3,4,'system:position:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改岗位状态',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(26,'岗位导出',3,5,'system:position:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'岗位导出',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(27,'创建角色',3,1,'system:role:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建角色',NULL,0,8,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(28,'修改角色',3,2,'system:role:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改角色',NULL,0,8,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(29,'删除角色',3,3,'system:role:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除角色',NULL,0,8,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(30,'批量修改角色状态',3,4,'system:role:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改角色状态',NULL,0,8,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(31,'设置角色权限',3,8,'system:role:permission',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'设置角色权限',NULL,0,7,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(32,'角色导出',3,6,'system:role:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'角色导出',NULL,0,8,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(33,'创建用户',3,1,'system:user:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建用户',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(34,'修改用户',3,2,'system:user:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(35,'删除用户',3,3,'system:user:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除用户',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(36,'批量修改用户状态',3,4,'system:user:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改用户状态',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(37,'导出用户',3,5,'system:user:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出用户',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(38,'导入用户',3,6,'system:user:import',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导入用户',NULL,0,9,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(39,'日志删除',3,1,'system:operation_log:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'日志删除',NULL,0,10,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(40,'日志导出',3,2,'system:operation_log:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'日志导出',NULL,0,10,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(41,'公告创建',3,1,'system:notice:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'公告创建',NULL,0,11,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(42,'公告修改',3,2,'system:notice:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改用户',NULL,0,11,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(43,'公告删除',3,3,'system:notice:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'公告删除',NULL,0,11,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(44,'公告导出',3,4,'system:notice:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'公告导出',NULL,0,11,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(45,'公告批量修改状态',3,5,'system:notice:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'公告批量修改状态',NULL,0,11,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(46,'创建配置',3,1,'system:config:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建配置',NULL,0,12,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(47,'修改配置',3,2,'system:config:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改配置',NULL,0,12,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(48,'删除配置',3,3,'system:config:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除配置',NULL,0,12,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(49,'导出配置',3,4,'system:config:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出配置',NULL,0,12,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(50,'配置上传',3,5,'system:config:upload',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'配置上传',NULL,0,12,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(51,'创建字典类型',3,1,'system:dict_type:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典类型',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(52,'修改字典类型',3,2,'system:dict_type:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典类型',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(53,'删除字典类型',3,3,'system:dict_type:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典类型',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(54,'导出字典类型',3,4,'system:dict_type:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(55,'批量修改字典状态',3,5,'system:dict_type:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典类型',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(56,'字典数据查询',3,6,'system:dict_data:query',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'字典数据查询',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(57,'创建字典数据',3,7,'system:dict_data:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建字典数据',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(58,'修改字典数据',3,8,'system:dict_data:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改字典数据',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(59,'删除字典数据',3,9,'system:dict_data:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除字典数据',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(60,'导出字典数据',3,10,'system:dict_data:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出字典数据',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(61,'批量修改字典数据状态',3,11,'system:dict_data:patch',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'批量修改字典数据状态',NULL,0,13,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(62,'监控管理',1,3,NULL,1,'monitor','Monitor','/monitor',NULL,'/monitor/online',0,0,0,'监控管理',NULL,0,NULL,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(63,'任务管理',2,1,'monitor:job:query',1,'el-icon-DataLine','Job','/monitor/job','monitor/job/index',NULL,0,1,0,'任务管理',NULL,0,62,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(64,'创建任务',3,1,'monitor:job:create',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'创建任务',NULL,0,63,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(65,'修改和操作任务',3,2,'monitor:job:update',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'修改和操作任务',NULL,0,63,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(66,'删除和清除任务',3,3,'monitor:job:delete',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'删除和清除任务',NULL,0,63,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(67,'导出定时任务',3,4,'monitor:job:export',1,NULL,NULL,NULL,NULL,NULL,0,1,0,'导出定时任务',NULL,0,63,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(68,'在线用户',2,2,'monitor:online:query',1,'el-icon-Headset','MonitorOnline','/monitor/online','monitor/online/index',NULL,0,0,0,'在线用户',NULL,0,62,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(69,'在线用户强制下线',3,1,'monitor:online:delete',1,NULL,NULL,NULL,NULL,NULL,0,0,0,'在线用户强制下线',NULL,0,68,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(70,'服务器监控',2,3,'monitor:server:query',1,'el-icon-Odometer','MonitorServer','/monitor/server','monitor/server/index',NULL,0,0,0,'服务器监控',NULL,0,62,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(71,'缓存监控',2,4,'monitor:cache:query',1,'el-icon-Stopwatch','MonitorCache','/monitor/cache','monitor/cache/index',NULL,0,0,0,'缓存监控',NULL,0,62,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(72,'清除缓存',3,1,'monitor:cache:delete',1,NULL,NULL,NULL,NULL,NULL,0,0,0,'清除缓存',NULL,0,71,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(73,'公共模块',1,4,NULL,1,'document','Common','/common',NULL,'/common/docs',0,0,0,'公共模块',NULL,0,NULL,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(74,'接口管理',4,1,'common:docs:query',1,'api','Docs','/common/docs','common/docs/index',NULL,0,0,0,'接口管理',NULL,0,73,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20'),(75,'文档管理',4,2,'common:redoc:query',1,'el-icon-Document','Redoc','/common/redoc','common/redoc/index',NULL,0,0,0,'文档管理',NULL,0,73,'初始化数据','2025-07-24 00:22:20','2025-07-24 00:22:20');
-- fastapi_vue_admin.system_notice DML
INSERT INTO `fastapi_vue_admin`.`system_notice` (`id`,`notice_title`,`notice_type`,`notice_content`,`status`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'系统更新','1','2099年9月9日，晚上12:00，系统更新',1,'系统更新','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,'系统维护','2','2099年9月9日，晚上12:00，系统维护',1,'系统维护','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(3,'系统更新完成','1','2099年9月9日，晚上12:00，系统更新完成',0,'系统更新完成','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(4,'系统维护完成','2','2099年9月9日，晚上12:00，系统维护完成',0,'系统维护完成','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_position DML
INSERT INTO `fastapi_vue_admin`.`system_position` (`id`,`name`,`order`,`status`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'董事长岗',1,1,'董事长岗位','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,'运营岗',2,1,'运营岗位','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(3,'销售岗',3,1,'销售岗','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(4,'人事行政岗',4,1,'人事行政岗','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(5,'开发岗',5,1,'开发岗','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(6,'测试岗',6,1,'测试岗','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(7,'演示岗',7,1,'演示岗','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_role DML
INSERT INTO `fastapi_vue_admin`.`system_role` (`id`,`name`,`order`,`data_scope`,`status`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'管理员角色',1,4,1,'管理员','2025-07-24 00:22:20','2025-07-24 00:22:20',1),(2,'普通角色',2,1,1,'普通角色','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
-- fastapi_vue_admin.system_role_depts DML
INSERT INTO `fastapi_vue_admin`.`system_role_depts` (`role_id`,`dept_id`) VALUES (1,1),(2,1),(2,6);
-- fastapi_vue_admin.system_role_menus DML
INSERT INTO `fastapi_vue_admin`.`system_role_menus` (`role_id`,`menu_id`) VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),(1,13),(1,14),(1,15),(1,16),(1,17),(1,18),(1,19),(1,20),(1,21),(1,22),(1,23),(1,24),(1,25),(1,26),(1,27),(1,28),(1,29),(1,30),(1,31),(1,32),(1,33),(1,34),(1,35),(1,36),(1,37),(1,38),(1,39),(1,40),(1,41),(1,42),(1,43),(1,44),(1,45),(1,46),(1,47),(1,48),(1,49),(1,50),(1,51),(1,52),(1,53),(1,54),(1,55),(1,56),(1,57),(1,58),(1,59),(1,60),(1,61),(1,62),(1,63),(1,64),(1,65),(1,66),(1,67),(1,68),(1,69),(1,70),(1,71),(1,72),(1,73),(1,74),(1,75),(2,1),(2,2);
-- fastapi_vue_admin.system_user_positions DML
INSERT INTO `fastapi_vue_admin`.`system_user_positions` (`user_id`,`position_id`) VALUES (1,5),(2,7);
-- fastapi_vue_admin.system_user_roles DML
INSERT INTO `fastapi_vue_admin`.`system_user_roles` (`user_id`,`role_id`) VALUES (1,1),(2,2);
-- fastapi_vue_admin.system_users DML
INSERT INTO `fastapi_vue_admin`.`system_users` (`id`,`username`,`password`,`name`,`mobile`,`email`,`gender`,`avatar`,`status`,`is_superuser`,`last_login`,`dept_id`,`description`,`created_at`,`updated_at`,`creator_id`) VALUES (1,'admin','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','管理员','15382112222','admin@qq.com','0','http://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,1,NULL,1,'超级管理员','2025-07-24 00:22:20','2025-07-24 00:22:20',NULL),(2,'demo','$2b$12$e2IJgS/cvHgJ0H3G7Xa08OXoXnk6N/NX3IZRtubBDElA0VLZhkNOa','演示用户','15382112121','demo@qq.com','1','http://service.fastapiadmin.com/api/v1/static/image/avatar.png',1,0,NULL,6,'演示用户','2025-07-24 00:22:20','2025-07-24 00:22:20',1);
SET FOREIGN_KEY_CHECKS = 1;
