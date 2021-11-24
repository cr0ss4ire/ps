
let menu = {
    menus: [
        {
            key: '/home', desc: '首页', icon: 'el-icon-s-home', permission: 'home_view',
        },
        {
            key: '1', desc: '用户管理', icon: 'el-icon-user', permission: 'account_user_view|account_role_view', subs: [
                {key: '/account/user', permission: 'account_user_view', desc: '用户列表'},
                {key: '/account/role', permission: 'account_role_view', desc: '角色权限'}
            ]
        },
        {
            key: '9', desc: '漏洞管理', icon: 'el-icon-monitor',  permission: 'exploit_view',  subs: [
                {key: '/exploit/plugins', permission: 'exploit_view', desc: '漏洞列表'},
            ]
        },
        {
            key: '10', desc: '任务管理', icon: 'el-icon-date',  permission: 'exploit_view',  subs: [
                {key: '/task/index', permission: 'exploit_view', desc: '任务列表'},
            ]
        },
        {
            key: '11', desc: '资源管理', icon: 'el-icon-receiving',  permission: 'exploit_view',  subs: [
                {key: '/resource/webshell/index', permission: 'exploit_view', desc: 'Webshell列表'},
                {key: '/resource/shell/index', permission: 'exploit_view', desc: '反弹Shell列表'}
            ]
        },
        {
            key: '12', desc: '系统配置', icon: 'el-icon-setting',  permission: 'exploit_view',  subs: [
                {key: '/webshell/index', permission: 'exploit_view', desc: 'Webshell列表'},
                {key: '/shell/index', permission: 'exploit_view', desc: '反弹Shell列表'}
            ]
        }
    ]
};

export default menu;
