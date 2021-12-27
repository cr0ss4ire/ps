# Host: localhost  (Version: 5.7.26)
# Date: 2021-12-27 14:58:03
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "account_permissions"
#

DROP TABLE IF EXISTS `account_permissions`;
CREATE TABLE `account_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=1305 DEFAULT CHARSET=utf8;

#
# Data for table "account_permissions"
#

/*!40000 ALTER TABLE `account_permissions` DISABLE KEYS */;
INSERT INTO `account_permissions` VALUES (100,'home_view','Dashboard'),(101,'account_user_view','获取用户列表'),(102,'account_user_add','添加用户'),(103,'account_user_edit','编辑用户'),(104,'account_user_del','删除用户'),(105,'account_user_disable','禁用用户'),(201,'account_role_view','获取角色列表'),(202,'account_role_add','添加角色'),(203,'account_role_edit','编辑角色'),(204,'account_role_del','删除角色'),(205,'account_role_permission_view','查看角色权限'),(206,'account_role_permission_edit','修改角色权限'),(301,'assets_host_view','获取主机列表'),(302,'assets_host_add','添加主机'),(303,'assets_host_edit','编辑主机'),(304,'assets_host_del','删除主机'),(305,'assets_host_valid','验证主机'),(306,'assets_host_exec_view','批量执行视图'),(307,'assets_host_exec','批量执行权限'),(308,'assets_host_exec_tpl_view','批量执行模板列表'),(309,'assets_host_exec_tpl_add','添加模板'),(310,'assets_host_exec_tpl_edit','编辑模板'),(311,'assets_host_exec_tpl_del','删除模板'),(401,'publish_app_view','获取应用列表'),(402,'publish_app_add','添加应用'),(403,'publish_app_edit','编辑应用'),(404,'publish_app_del','删除应用'),(405,'publish_app_publish_view','应用发布'),(406,'publish_app_ctr_view','容器设置 - 查看'),(407,'publish_app_ctr_edit','容器设置 - 编辑'),(408,'publish_app_var_view','应用设置 - 查看'),(409,'publish_app_var_add','应用设置 - 添加'),(410,'publish_app_var_edit','应用设置 - 编辑'),(411,'publish_app_var_del','应用设置 - 删除'),(412,'publish_app_menu_view','菜单管理 - 查看'),(413,'publish_app_menu_edit','菜单管理 - 编辑'),(501,'publish_app_publish_host_select','选择发布主机'),(502,'publish_app_publish_ctr_control','启动|停止容器'),(503,'publish_app_publish_ctr_del','删除容器'),(504,'publish_app_publish_deploy','执行发布'),(505,'publish_app_publish_menu_exec','执行自定义菜单'),(601,'publish_image_view','获取镜像列表'),(602,'publish_image_sync','执行镜像同步'),(603,'publish_image_edit','镜像编辑'),(604,'publish_image_del','镜像删除'),(605,'publish_image_var_view','镜像设置 - 查看'),(606,'publish_image_var_add','镜像设置 - 添加'),(607,'publish_image_var_edit','镜像设置 - 编辑'),(608,'publish_image_var_del','镜像设置 - 删除'),(701,'config_environment_view','获取环境列表'),(702,'config_environment_add','添加环境'),(703,'config_environment_edit','编辑环境'),(704,'config_environment_del','删除环境'),(801,'config_service_view','获取服务列表'),(802,'config_service_add','添加服务'),(803,'config_service_edit','编辑服务'),(804,'config_service_del','删除服务'),(805,'config_service_cfg_view','服务配置 - 查看'),(806,'config_service_cfg_add','服务配置 - 添加'),(807,'config_service_cfg_edit','服务配置 - 编辑'),(808,'config_service_cfg_del','服务配置 - 删除'),(901,'config_app_view','获取应用列表'),(902,'config_app_cfg_view','应用配置 - 查看'),(903,'config_app_cfg_add','应用配置 - 添加'),(904,'config_app_cfg_edit','应用配置 - 编辑'),(905,'config_app_cfg_del','应用配置 - 删除'),(906,'config_app_rel_view','应用关系 - 查看'),(907,'config_app_rel_edit','应用关系 - 编辑'),(1001,'job_task_view','获取任务列表'),(1002,'job_task_add','添加任务'),(1003,'job_task_edit','编辑任务'),(1004,'job_task_del','删除任务'),(1005,'job_task_log','任务日志'),(1101,'publish_menu_view','自定义菜单 - 查看'),(1102,'publish_menu_add','自定义菜单 - 添加'),(1103,'publish_menu_edit','自定义菜单 - 编辑'),(1104,'publish_menu_del','自定义菜单 - 删除'),(1105,'publish_menu_rel_view','关联配置 - 查看'),(1106,'publish_menu_rel_edit','关联配置 - 编辑'),(1201,'publish_field_view','自定义字段 - 查看'),(1202,'publish_field_add','自定义字段 - 添加'),(1203,'publish_field_edit','自定义字段 - 编辑'),(1204,'publish_field_del','自定义字段 - 删除'),(1205,'publish_field_rel_view','关联配置 - 查看'),(1206,'publish_field_rel_edit','关联配置 - 编辑'),(1301,'system_notify_view','系统通知列表'),(1302,'system_notify_add','添加通知设置'),(1303,'system_notify_edit','编辑通知设置'),(1304,'system_notify_del','删除通知设置');
/*!40000 ALTER TABLE `account_permissions` ENABLE KEYS */;

#
# Structure for table "account_role_permission_rel"
#

DROP TABLE IF EXISTS `account_role_permission_rel`;
CREATE TABLE `account_role_permission_rel` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`role_id`,`permission_id`),
  KEY `permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

#
# Data for table "account_role_permission_rel"
#

/*!40000 ALTER TABLE `account_role_permission_rel` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_role_permission_rel` ENABLE KEYS */;

#
# Structure for table "account_roles"
#

DROP TABLE IF EXISTS `account_roles`;
CREATE TABLE `account_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `env_ids` text,
  `app_ids` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "account_roles"
#

/*!40000 ALTER TABLE `account_roles` DISABLE KEYS */;
INSERT INTO `account_roles` VALUES (1,'普通用户','普通用户',NULL,NULL);
/*!40000 ALTER TABLE `account_roles` ENABLE KEYS */;

#
# Structure for table "account_users"
#

DROP TABLE IF EXISTS `account_users`;
CREATE TABLE `account_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_id` int(11) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `nickname` varchar(50) DEFAULT NULL,
  `password_hash` varchar(100) NOT NULL,
  `email` varchar(120) DEFAULT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `is_supper` tinyint(1) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `access_token` varchar(32) DEFAULT NULL,
  `token_expired` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `role_id` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "account_users"
#

/*!40000 ALTER TABLE `account_users` DISABLE KEYS */;
INSERT INTO `account_users` VALUES (1,NULL,'admin','管理员','pbkdf2:sha256:150000$U9aMCcxU$0824abbbb72ac9e502179c2de11f6974dc3344e83b8a69168abc9708bb53851f',NULL,NULL,1,'系统用户',1,'3bf90b3a5cb34e89a6e8b8907bab125d',1640363377),(2,1,'test','test','pbkdf2:sha256:150000$vwGHd4qf$e7d255a26255eb5ff00c2c9489fc87e9146420e270a09ad0714038581b4130cc','test@test.com','18515443421',1,'系统用户',1,'85940bc69f444c47b57a1967782899b7',1639739071);
/*!40000 ALTER TABLE `account_users` ENABLE KEYS */;

#
# Structure for table "application"
#

DROP TABLE IF EXISTS `application`;
CREATE TABLE `application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "application"
#

/*!40000 ALTER TABLE `application` DISABLE KEYS */;
INSERT INTO `application` VALUES (1,'wordpress'),(2,'weblogioc'),(3,'joomla'),(4,'tomcat'),(5,'drupal');
/*!40000 ALTER TABLE `application` ENABLE KEYS */;

#
# Structure for table "category"
#

DROP TABLE IF EXISTS `category`;
CREATE TABLE `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

#
# Data for table "category"
#

/*!40000 ALTER TABLE `category` DISABLE KEYS */;
INSERT INTO `category` VALUES (1,'web服务器'),(2,'中间件'),(3,'Web应用');
/*!40000 ALTER TABLE `category` ENABLE KEYS */;

#
# Structure for table "effect"
#

DROP TABLE IF EXISTS `effect`;
CREATE TABLE `effect` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "effect"
#

/*!40000 ALTER TABLE `effect` DISABLE KEYS */;
INSERT INTO `effect` VALUES (1,'执行命令'),(2,'获取webshell');
/*!40000 ALTER TABLE `effect` ENABLE KEYS */;

#
# Structure for table "exec_model"
#

DROP TABLE IF EXISTS `exec_model`;
CREATE TABLE `exec_model` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

#
# Data for table "exec_model"
#

/*!40000 ALTER TABLE `exec_model` DISABLE KEYS */;
INSERT INTO `exec_model` VALUES (1,'验证模式'),(2,'攻击模式'),(3,'指纹模式');
/*!40000 ALTER TABLE `exec_model` ENABLE KEYS */;

#
# Structure for table "exploit"
#

DROP TABLE IF EXISTS `exploit`;
CREATE TABLE `exploit` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `cve` varchar(255) DEFAULT NULL,
  `affect_version` varchar(255) DEFAULT NULL,
  `os` varchar(255) DEFAULT NULL,
  `desc` text,
  `enter_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `vul_type_id` int(11) DEFAULT NULL,
  `application_id` int(11) DEFAULT NULL,
  `vullevel_id` int(11) DEFAULT NULL,
  `language_id` int(11) DEFAULT NULL,
  `effect_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `plugin_file_path` varchar(255) DEFAULT NULL,
  `standalone_tool_file_path` varchar(255) DEFAULT NULL,
  `docker_file_path` varchar(255) DEFAULT NULL,
  `virtual_machine_remarks` text,
  PRIMARY KEY (`id`),
  KEY `category_id` (`category_id`),
  KEY `vul_type_id` (`vul_type_id`),
  KEY `application_id` (`application_id`),
  KEY `vullevel_id` (`vullevel_id`),
  KEY `language_id` (`language_id`),
  KEY `effect_id` (`effect_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

#
# Data for table "exploit"
#

/*!40000 ALTER TABLE `exploit` DISABLE KEYS */;
INSERT INTO `exploit` VALUES (4,'Tomcat任意写入文件漏洞（CVE-2017-12615）','CVE-2017-12615','7.0.0-7.0.81','windows、linux','首先声明的是CVE-2017-12615漏洞的利用条件是Windows+Tomcat 7.0.x+配置文件readonly=false，配置文件内容如：\n\n<init-param>\n<param-name>readonly</param-name>\n<param-value>false</param-value>\n</init-param>\nTomcat将readonly设置为false的同时也开启了对PUT请求方式的支持。这时候意味着我们可以上传文件，那么是可以上传任意文件吗？并不是，我们首先要了解下Tomcat的下面两员大将：\n\norg.apache.jasper.servlet.JspServlet：默认处理jsp，jspx文件请求，不存在PUT上传逻辑，无法处理PUT请求\norg.apache.catalina.servlets.DefaultServlet：默认处理静态文件（除jsp，jspx之外的文件），存在PUT上传处理逻辑，可以处理PUT请求。\n所以我们即使可以PUT一个文件到服务器但也无法直接PUT以jsp,jspx结尾文件，因为这些这些后缀的文件都是交由JspServlet处理的，它没法处理PUT请求。\n但是当我们利用Windows特性以下面两种方式上传文件时，tomcat并不认为其是jsp文件从而交由DefaultServlet处理，从而成功创建jsp文件，这也就是所谓的CVE-2017-12615漏洞。\n\nevil.jsp%20\nevil.jsp::$DATA\n上面这些属于CVE-2017-12615漏洞的内容，初次之外当我们上传evil.jsp/ 类型的文件时（即以反斜杠结尾）时同样会成功创建jsp文件，并且这种方式把PUT漏洞的利用扩展到了Linux平台及Tomcat的5.x-9.x的所有版本，不过这不属于CVE-2017-12615的内容。','2021-11-24 15:14:45.218500','2021-12-03 16:38:19',2,4,4,3,1,2,1,'./upload/1/plugins/1637737614__1_tomcat_upload.py','./upload/1/standalone-tools/1637737659_CVE-2017-12615.zip','./upload/1/dockers/1637737678_CVE-2017-12615.zip','无'),(5,'CVE-2018-7600 Drupal漏洞','CVE-2018-7600','Drupal 6.x，7.x，8.x','windows、linux','3月底，Drupal核心安全团队发布了安全咨询SA-CORE-2018-002，该安全咨询讨论了一个非常严重的漏洞CVE-2018-7600，该漏洞存在于众多Drupal版本中，本文将对该漏洞进行详细分析。\n\n这个漏洞影响着超过一百万个Drupal用户和网站，它可以启用远程代码执行，并且可以在Drupal 7 Form API上进行不完整的输入验证。\n\n攻击者可以使用此漏洞强制运行Drupal的服务器，并执行可能危害Drupal安装的恶意代码。根据具体配置的不同，这也很可能会危及到主机。\n\n由于没有任何措施可以缓解对该漏洞的访问，所以这个漏洞显得尤为严重，这代表着匿名用户使用此漏洞远程执行代码而无需身份验证。','2021-11-24 15:36:12.878000','2021-12-03 16:38:13',3,2,5,3,2,1,1,'./upload/1/plugins/1637739279__2_drupal_rce.py','./upload/1/standalone-tools/1637739351_jspspy.rar',NULL,NULL);
/*!40000 ALTER TABLE `exploit` ENABLE KEYS */;

#
# Structure for table "language"
#

DROP TABLE IF EXISTS `language`;
CREATE TABLE `language` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

#
# Data for table "language"
#

/*!40000 ALTER TABLE `language` DISABLE KEYS */;
INSERT INTO `language` VALUES (1,'java'),(2,'php');
/*!40000 ALTER TABLE `language` ENABLE KEYS */;

#
# Structure for table "level"
#

DROP TABLE IF EXISTS `level`;
CREATE TABLE `level` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

#
# Data for table "level"
#

/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (1,'低危'),(2,'中危'),(3,'高危');
/*!40000 ALTER TABLE `level` ENABLE KEYS */;

#
# Structure for table "task"
#

DROP TABLE IF EXISTS `task`;
CREATE TABLE `task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `url_list` text,
  `plugins` text,
  `desc` varchar(255) DEFAULT NULL,
  `url_file_path` varchar(255) DEFAULT NULL,
  `start_time` varchar(255) DEFAULT NULL,
  `create_time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `finish_time` varchar(255) DEFAULT NULL,
  `exec_model_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `exec_model_id` (`exec_model_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "task"
#

/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (1,'zxdsd','http://192.168.2.243,http://192.168.2.243:8080','5,4','sdsad','','2021-12-23 17:50:23','2021-11-24 16:12:19.483500','2021-12-06 18:10:06',1,'',1,2);
/*!40000 ALTER TABLE `task` ENABLE KEYS */;

#
# Structure for table "task_detail"
#

DROP TABLE IF EXISTS `task_detail`;
CREATE TABLE `task_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `target` varchar(255) NOT NULL,
  `vul_id` int(32) NOT NULL,
  `webshell_url` varchar(255) DEFAULT NULL,
  `webshell_pass` varchar(255) DEFAULT NULL,
  `webshell_access_tool` varchar(255) DEFAULT NULL,
  `remark` text,
  `error_info` text,
  `status` int(32) NOT NULL,
  `task_id` int(11) NOT NULL DEFAULT '0',
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `vul_id` (`vul_id`),
  KEY `task_id` (`task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=104 DEFAULT CHARSET=utf8;

#
# Data for table "task_detail"
#

/*!40000 ALTER TABLE `task_detail` DISABLE KEYS */;
INSERT INTO `task_detail` VALUES (100,'http://192.168.2.243',5,'http://192.168.2.243/cu7pfXtI62.php','rebeyond','behinder','','',1,1,1),(101,'http://192.168.2.243:8080',5,'','','','','POC-2: Drupal remote code execute AttributeError occurs, \'NoneType\' object has no attribute \'find\'',0,1,1),(102,'http://192.168.2.243',4,'','','','','{http://192.168.2.243} server not vulnerable',0,1,1),(103,'http://192.168.2.243:8080',4,'http://192.168.2.243:8080/1640253023.jsp?pwd=023&cmd=whoami','','browser','','',1,1,1);
/*!40000 ALTER TABLE `task_detail` ENABLE KEYS */;

#
# Structure for table "vul_type"
#

DROP TABLE IF EXISTS `vul_type`;
CREATE TABLE `vul_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

#
# Data for table "vul_type"
#

/*!40000 ALTER TABLE `vul_type` DISABLE KEYS */;
INSERT INTO `vul_type` VALUES (1,'xss',NULL),(2,'rce',NULL),(3,'ssrf',NULL),(4,'文件上传',NULL);
/*!40000 ALTER TABLE `vul_type` ENABLE KEYS */;
