import Main from '@/components/main'
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
    path: '/',
    redirect: '/home'
  },
  {
    path: '/login',
    name: 'login',
    meta: {
      title: 'Login - 登录',
      hideInMenu: true
    },
    component: () => import('@/view/login/login.vue')
  },
  {
    path: '/register',
    name: 'register',
    meta: {
      title: 'Register - 注册',
      hideInMenu: true
    },
    component: () => import('@/view/login/register.vue')
  },
  {
    path: '/',
    name: '_home',
    redirect: '/home',
    component: Main,
    meta: {
      hideInMenu: true,
      icon: 'md-home',
      notCache: true
    },
    children: [
      {
        path: '/home',
        name: 'home',
        meta: {
          hideInMenu: true,
          icon: 'md-home',
          title: '首页',
          notCache: true
        },
        component: () => import('@/view/home/home.vue')
      }
    ]
  },
  {
    path: '/good',
    name: 'good',
    meta: {
      hide: true
    },
    component: Main,
    children: [
      {
        path: 'good_page',
        name: 'good_page',
        meta: {
          icon: 'logo-buffer',
          title: '商品管理',
          notCache: true
        },
        component: () => import('@/view/good/good.vue')
      }
    ]
  },
  {
    path: '/sale',
    name: 'sale',
    meta: {
      hide: true
    },
    component: Main,
    children: [
      {
        path: 'good_sale',
        name: 'good_sale',
        meta: {
          icon: 'logo-buffer',
          title: '商品销售',
          notCache: true
        },
        component: () => import('@/view/sale/good-sale.vue')
      }
    ]
  },
  {
    path: '/401',
    name: 'error_401',
    component: () => import('@/view/error-page/401.vue')
  },
  {
    path: '/stock',
    name: 'stock',
    meta: {
      hide: false,
      title: '库存管理'
    },
    component: Main,
    children: [
      {
        path: 'stock_in',
        name: 'stock_in',
        meta: {
          icon: 'ios-calendar',
          title: '快速入库'
        },
        component: () => import('@/view/stock/stock-in.vue')
      },
      {
        path: 'stock_out',
        name: 'stock_out',
        meta: {
          icon: 'ios-calendar',
          title: '快速出库'
        },
        component: () => import('@/view/stock/stock-out.vue')
      },
      {
        path: 'exam_task',
        name: 'exam_task',
        meta: {
          icon: 'ios-calendar',
          title: '审核任务'
        },
        component: () => import('@/view/stock/exam-task.vue')
      }
    ]
  },
  {
    path: '/report',
    name: 'report',
    meta: {
      hide: false,
      title: '报表查询'
    },
    component: Main,
    children: [
      {
        path: 'stock_report',
        name: 'stock_report',
        meta: {
          icon: 'ios-calendar',
          title: '库存查询'
        },
        component: () => import('@/view/report/stock-report.vue')
      },
      {
        path: 'sale_detail',
        name: 'sale_detail',
        meta: {
          icon: 'ios-calendar',
          title: '交易明细'
        },
        component: () => import('@/view/report/sale_detail.vue')
      }
    ]
  }
]
