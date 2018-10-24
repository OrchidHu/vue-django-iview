//import Main from '@/components/main'
//import parentView from '@/components/parent-view'

/**
 * iview-admin中meta除了原生参数外可配置的参数:
 * meta: {
 *  hideInMenu: (false) 设为true后在左侧菜单不会显示该页面选项
 *  notCache: (false) 设为true后页面不会缓存
 *  access: (null) 可访问该页面的权限数组，当前路由设置的权限会影响子路由
 *  icon: (-) 该页面在左侧菜单、面包屑和标签导航处显示的图标，如果是自定义图标，需要在图标名称前加下划线'_'
 *  beforeCloseName: (-) 设置该字段，则在关闭当前tab页时会去'@/router/before-close.js'里寻找该字段名对应的方法，作为关闭前的钩子函数
 * }
 */

export default [

  {
    path:'/',
    redirect:'/home'
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path:'/home',
    name:'home',
    component: () => import('@/view/home/home.vue')
  },
  {
    path:'/good',
    name:'good',
    component: () => import('@/view/good/good.vue')
  },
  {
    path:'/401',
    name:'error_401',
    component:() => import('@/view/error-page/401.vue')
  }
]
