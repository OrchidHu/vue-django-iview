const djangoUrl = 'http://127.0.0.1:8000/'

export default {
  /**
   * @description token在Cookie中存储的天数，默认1天
   */
  cookieExpires: 1,
  /**
   * @description 是否使用国际化，默认为false
   *              如果不使用，则需要在路由中给需要在菜单中展示的路由设置meta: {title: 'xxx'}
   *              用来在菜单中显示文字
   */
  useI18n: false,
  /**
   * @description api请求基础路径
   */
  baseUrl: {
    dev: 'https://www.easy-mock.com/mock/5add9213ce4d0e69998a6f51/iview-admin/',
    pro: 'https://produce.com'
  },
  /**
   * @description 配置路由到django后台的url
   */
  loginUrl: djangoUrl + 'account/login/',
  logoutUrl: djangoUrl + 'account/logout',
  goodUrl: djangoUrl + 'shop/good/',
  createGoodUrl: djangoUrl + 'shop/create_good',
  updateGoodUrl: djangoUrl + 'shop/update_good',
  deleteGoodUrl: djangoUrl + 'shop/delete_good',
  getQuantifyUrl: djangoUrl + 'common/quantify_list',
  getSupplierUrl: djangoUrl + 'common/supplier_list',
  getGenreUrl: djangoUrl + 'common/genre_list',
  addQuantifyUrl: djangoUrl + 'common/add_quantify'
}
