-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 24, 2021 at 08:11 PM
-- Server version: 5.7.26
-- PHP Version: 7.3.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pocstrike`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_permissions`
--

CREATE TABLE `account_permissions` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `desc` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_permissions`
--

INSERT INTO `account_permissions` (`id`, `name`, `desc`) VALUES
(100, 'home_view', 'Dashboard'),
(101, 'account_user_view', '获取用户列表'),
(102, 'account_user_add', '添加用户'),
(103, 'account_user_edit', '编辑用户'),
(104, 'account_user_del', '删除用户'),
(105, 'account_user_disable', '禁用用户'),
(201, 'account_role_view', '获取角色列表'),
(202, 'account_role_add', '添加角色'),
(203, 'account_role_edit', '编辑角色'),
(204, 'account_role_del', '删除角色'),
(205, 'account_role_permission_view', '查看角色权限'),
(206, 'account_role_permission_edit', '修改角色权限'),
(301, 'assets_host_view', '获取主机列表'),
(302, 'assets_host_add', '添加主机'),
(303, 'assets_host_edit', '编辑主机'),
(304, 'assets_host_del', '删除主机'),
(305, 'assets_host_valid', '验证主机'),
(306, 'assets_host_exec_view', '批量执行视图'),
(307, 'assets_host_exec', '批量执行权限'),
(308, 'assets_host_exec_tpl_view', '批量执行模板列表'),
(309, 'assets_host_exec_tpl_add', '添加模板'),
(310, 'assets_host_exec_tpl_edit', '编辑模板'),
(311, 'assets_host_exec_tpl_del', '删除模板'),
(401, 'publish_app_view', '获取应用列表'),
(402, 'publish_app_add', '添加应用'),
(403, 'publish_app_edit', '编辑应用'),
(404, 'publish_app_del', '删除应用'),
(405, 'publish_app_publish_view', '应用发布'),
(406, 'publish_app_ctr_view', '容器设置 - 查看'),
(407, 'publish_app_ctr_edit', '容器设置 - 编辑'),
(408, 'publish_app_var_view', '应用设置 - 查看'),
(409, 'publish_app_var_add', '应用设置 - 添加'),
(410, 'publish_app_var_edit', '应用设置 - 编辑'),
(411, 'publish_app_var_del', '应用设置 - 删除'),
(412, 'publish_app_menu_view', '菜单管理 - 查看'),
(413, 'publish_app_menu_edit', '菜单管理 - 编辑'),
(501, 'publish_app_publish_host_select', '选择发布主机'),
(502, 'publish_app_publish_ctr_control', '启动|停止容器'),
(503, 'publish_app_publish_ctr_del', '删除容器'),
(504, 'publish_app_publish_deploy', '执行发布'),
(505, 'publish_app_publish_menu_exec', '执行自定义菜单'),
(601, 'publish_image_view', '获取镜像列表'),
(602, 'publish_image_sync', '执行镜像同步'),
(603, 'publish_image_edit', '镜像编辑'),
(604, 'publish_image_del', '镜像删除'),
(605, 'publish_image_var_view', '镜像设置 - 查看'),
(606, 'publish_image_var_add', '镜像设置 - 添加'),
(607, 'publish_image_var_edit', '镜像设置 - 编辑'),
(608, 'publish_image_var_del', '镜像设置 - 删除'),
(701, 'config_environment_view', '获取环境列表'),
(702, 'config_environment_add', '添加环境'),
(703, 'config_environment_edit', '编辑环境'),
(704, 'config_environment_del', '删除环境'),
(801, 'config_service_view', '获取服务列表'),
(802, 'config_service_add', '添加服务'),
(803, 'config_service_edit', '编辑服务'),
(804, 'config_service_del', '删除服务'),
(805, 'config_service_cfg_view', '服务配置 - 查看'),
(806, 'config_service_cfg_add', '服务配置 - 添加'),
(807, 'config_service_cfg_edit', '服务配置 - 编辑'),
(808, 'config_service_cfg_del', '服务配置 - 删除'),
(901, 'config_app_view', '获取应用列表'),
(902, 'config_app_cfg_view', '应用配置 - 查看'),
(903, 'config_app_cfg_add', '应用配置 - 添加'),
(904, 'config_app_cfg_edit', '应用配置 - 编辑'),
(905, 'config_app_cfg_del', '应用配置 - 删除'),
(906, 'config_app_rel_view', '应用关系 - 查看'),
(907, 'config_app_rel_edit', '应用关系 - 编辑'),
(1001, 'job_task_view', '获取任务列表'),
(1002, 'job_task_add', '添加任务'),
(1003, 'job_task_edit', '编辑任务'),
(1004, 'job_task_del', '删除任务'),
(1005, 'job_task_log', '任务日志'),
(1101, 'publish_menu_view', '自定义菜单 - 查看'),
(1102, 'publish_menu_add', '自定义菜单 - 添加'),
(1103, 'publish_menu_edit', '自定义菜单 - 编辑'),
(1104, 'publish_menu_del', '自定义菜单 - 删除'),
(1105, 'publish_menu_rel_view', '关联配置 - 查看'),
(1106, 'publish_menu_rel_edit', '关联配置 - 编辑'),
(1201, 'publish_field_view', '自定义字段 - 查看'),
(1202, 'publish_field_add', '自定义字段 - 添加'),
(1203, 'publish_field_edit', '自定义字段 - 编辑'),
(1204, 'publish_field_del', '自定义字段 - 删除'),
(1205, 'publish_field_rel_view', '关联配置 - 查看'),
(1206, 'publish_field_rel_edit', '关联配置 - 编辑'),
(1301, 'system_notify_view', '系统通知列表'),
(1302, 'system_notify_add', '添加通知设置'),
(1303, 'system_notify_edit', '编辑通知设置'),
(1304, 'system_notify_del', '删除通知设置');

-- --------------------------------------------------------

--
-- Table structure for table `account_roles`
--

CREATE TABLE `account_roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `desc` varchar(255) DEFAULT NULL,
  `env_ids` text,
  `app_ids` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_roles`
--

INSERT INTO `account_roles` (`id`, `name`, `desc`, `env_ids`, `app_ids`) VALUES
(1, '系统默认角色', '系统默认角色', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `account_role_permission_rel`
--

CREATE TABLE `account_role_permission_rel` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `account_users`
--

CREATE TABLE `account_users` (
  `id` int(11) NOT NULL,
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
  `token_expired` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `account_users`
--

INSERT INTO `account_users` (`id`, `role_id`, `username`, `nickname`, `password_hash`, `email`, `mobile`, `is_supper`, `type`, `is_active`, `access_token`, `token_expired`) VALUES
(1, NULL, 'admin', '管理员', 'pbkdf2:sha256:150000$U9aMCcxU$0824abbbb72ac9e502179c2de11f6974dc3344e83b8a69168abc9708bb53851f', NULL, NULL, 1, '系统用户', 1, 'e72a2cc6a7844336a8ae5c57ba24f78d', 1637784409);

-- --------------------------------------------------------

--
-- Table structure for table `application`
--

CREATE TABLE `application` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `application`
--

INSERT INTO `application` (`id`, `name`) VALUES
(1, 'wordpress'),
(2, 'weblogioc'),
(3, 'joomla'),
(4, 'tomcat'),
(5, 'drupal');

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `name`) VALUES
(1, 'web服务器'),
(2, '中间件'),
(3, 'Web应用');

-- --------------------------------------------------------

--
-- Table structure for table `effect`
--

CREATE TABLE `effect` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `effect`
--

INSERT INTO `effect` (`id`, `name`) VALUES
(1, '执行命令'),
(2, '获取webshell');

-- --------------------------------------------------------

--
-- Table structure for table `exec_model`
--

CREATE TABLE `exec_model` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `exec_model`
--

INSERT INTO `exec_model` (`id`, `name`) VALUES
(1, '验证模式'),
(2, '攻击模式');

-- --------------------------------------------------------

--
-- Table structure for table `exploit`
--

CREATE TABLE `exploit` (
  `id` int(11) NOT NULL,
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
  `virtual_machine_remarks` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `exploit`
--

INSERT INTO `exploit` (`id`, `name`, `cve`, `affect_version`, `os`, `desc`, `enter_time`, `update_time`, `category_id`, `vul_type_id`, `application_id`, `vullevel_id`, `language_id`, `effect_id`, `user_id`, `plugin_file_path`, `standalone_tool_file_path`, `docker_file_path`, `virtual_machine_remarks`) VALUES
(4, 'Tomcat任意写入文件漏洞（CVE-2017-12615）', 'CVE-2017-12615', '7.0.0-7.0.81', 'windows、linux', '首先声明的是CVE-2017-12615漏洞的利用条件是Windows+Tomcat 7.0.x+配置文件readonly=false，配置文件内容如：\n\n<init-param>\n<param-name>readonly</param-name>\n<param-value>false</param-value>\n</init-param>\nTomcat将readonly设置为false的同时也开启了对PUT请求方式的支持。这时候意味着我们可以上传文件，那么是可以上传任意文件吗？并不是，我们首先要了解下Tomcat的下面两员大将：\n\norg.apache.jasper.servlet.JspServlet：默认处理jsp，jspx文件请求，不存在PUT上传逻辑，无法处理PUT请求\norg.apache.catalina.servlets.DefaultServlet：默认处理静态文件（除jsp，jspx之外的文件），存在PUT上传处理逻辑，可以处理PUT请求。\n所以我们即使可以PUT一个文件到服务器但也无法直接PUT以jsp,jspx结尾文件，因为这些这些后缀的文件都是交由JspServlet处理的，它没法处理PUT请求。\n但是当我们利用Windows特性以下面两种方式上传文件时，tomcat并不认为其是jsp文件从而交由DefaultServlet处理，从而成功创建jsp文件，这也就是所谓的CVE-2017-12615漏洞。\n\nevil.jsp%20\nevil.jsp::$DATA\n上面这些属于CVE-2017-12615漏洞的内容，初次之外当我们上传evil.jsp/ 类型的文件时（即以反斜杠结尾）时同样会成功创建jsp文件，并且这种方式把PUT漏洞的利用扩展到了Linux平台及Tomcat的5.x-9.x的所有版本，不过这不属于CVE-2017-12615的内容。', '2021-11-24 15:14:45.218500', '2021-11-24 20:04:39', 2, 4, 4, 3, 1, 2, 1, './upload/1/plugins/1637737614__1_tomcat_upload.py', './upload/1/standalone-tools/1637737659_CVE-2017-12615.zip', './upload/1/dockers/1637737678_CVE-2017-12615.zip', '无'),
(5, 'CVE-2018-7600 Drupal漏洞', 'CVE-2018-7600', 'Drupal 6.x，7.x，8.x', 'windows、linux', '3月底，Drupal核心安全团队发布了安全咨询SA-CORE-2018-002，该安全咨询讨论了一个非常严重的漏洞CVE-2018-7600，该漏洞存在于众多Drupal版本中，本文将对该漏洞进行详细分析。\n\n这个漏洞影响着超过一百万个Drupal用户和网站，它可以启用远程代码执行，并且可以在Drupal 7 Form API上进行不完整的输入验证。\n\n攻击者可以使用此漏洞强制运行Drupal的服务器，并执行可能危害Drupal安装的恶意代码。根据具体配置的不同，这也很可能会危及到主机。\n\n由于没有任何措施可以缓解对该漏洞的访问，所以这个漏洞显得尤为严重，这代表着匿名用户使用此漏洞远程执行代码而无需身份验证。', '2021-11-24 15:36:12.878000', '2021-11-24 20:04:33', 3, 2, 5, 3, 2, 1, 1, './upload/1/plugins/1637739279__2_drupal_rce.py', './upload/1/standalone-tools/1637739351_jspspy.rar', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `language`
--

CREATE TABLE `language` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `language`
--

INSERT INTO `language` (`id`, `name`) VALUES
(1, 'java'),
(2, 'php');

-- --------------------------------------------------------

--
-- Table structure for table `level`
--

CREATE TABLE `level` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `level`
--

INSERT INTO `level` (`id`, `name`) VALUES
(1, '低危'),
(2, '中危'),
(3, '高危');

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
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
  `status` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`id`, `name`, `url_list`, `plugins`, `desc`, `url_file_path`, `start_time`, `create_time`, `update_time`, `user_id`, `finish_time`, `exec_model_id`, `status`) VALUES
(1, 'zxdsd', '127.0.0.1', '5', 'sdsad', '', '', '2021-11-24 16:12:19.483500', '2021-11-24 17:26:04', 1, '', 1, 0);

-- --------------------------------------------------------

--
-- Table structure for table `vul_type`
--

CREATE TABLE `vul_type` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `desc` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Dumping data for table `vul_type`
--

INSERT INTO `vul_type` (`id`, `name`, `desc`) VALUES
(1, 'xss', NULL),
(2, 'rce', NULL),
(3, 'ssrf', NULL),
(4, '文件上传', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_permissions`
--
ALTER TABLE `account_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `account_roles`
--
ALTER TABLE `account_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `account_role_permission_rel`
--
ALTER TABLE `account_role_permission_rel`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `permission_id` (`permission_id`);

--
-- Indexes for table `account_users`
--
ALTER TABLE `account_users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD KEY `role_id` (`role_id`);

--
-- Indexes for table `application`
--
ALTER TABLE `application`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `effect`
--
ALTER TABLE `effect`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exec_model`
--
ALTER TABLE `exec_model`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `exploit`
--
ALTER TABLE `exploit`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`),
  ADD KEY `vul_type_id` (`vul_type_id`),
  ADD KEY `application_id` (`application_id`),
  ADD KEY `vullevel_id` (`vullevel_id`),
  ADD KEY `language_id` (`language_id`),
  ADD KEY `effect_id` (`effect_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `language`
--
ALTER TABLE `language`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `level`
--
ALTER TABLE `level`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `exec_model_id` (`exec_model_id`);

--
-- Indexes for table `vul_type`
--
ALTER TABLE `vul_type`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account_permissions`
--
ALTER TABLE `account_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1305;

--
-- AUTO_INCREMENT for table `account_roles`
--
ALTER TABLE `account_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `account_users`
--
ALTER TABLE `account_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `application`
--
ALTER TABLE `application`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `effect`
--
ALTER TABLE `effect`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `exec_model`
--
ALTER TABLE `exec_model`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `exploit`
--
ALTER TABLE `exploit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `language`
--
ALTER TABLE `language`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `level`
--
ALTER TABLE `level`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `vul_type`
--
ALTER TABLE `vul_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
