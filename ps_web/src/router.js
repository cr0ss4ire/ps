
import Home from './components/Home.vue'
import Deny from './components/Deny.vue'
import Welcome from './components/Welcome.vue'
import Login from './components/Login.vue'
import Layout from './components/Layout.vue'
import account_routes from './components/account/routes'
import vulnerability_routes from './components/vulnerability/routes'
import task_routes from './components/task/routes'
import resource_routes from './components/resource/webshell/routes'

const routes = [
    {
        path: '',
        name: 'home',
        component: Home
    },
    {
        path: '/welcome',
        name: 'welcome',
        component: Welcome
    },
    {
        path: 'account',
        routes: account_routes
    },
    {
        path: 'vulnerability',
        routes: vulnerability_routes
    },
    {
        path: 'task',
        routes: task_routes
    },
    {
        path: 'resource/webshell',
        routes: resource_routes
    },
    {
        path: '*',
        redirect: '/'
    }
];

function load_route(routes) {
    let result = [];
    for (let route of routes) {
        if (route.hasOwnProperty('routes') && Array.isArray(route.routes)) {
            for (let sub_route of load_route(route.routes)) {
                sub_route.path = route.path +  '/' + sub_route.path;
                result.push(sub_route)
            }
        } else {
            result.push(route)
        }
    }
    return result
}

export default [
    {
        path: '/login',
        name: 'login',
        component: Login
    }, {
        path: '/deny',
        component: Deny
    }, {
        path: '/',
        component: Layout,
        children: load_route(routes)
    }
]