// const djangoUrl = 'http://127.0.0.1:8000/'

let socket = {
  dev: 'ws://./vue/chart/push',
  pro: 'ws://./vue/chart/push'
}
let vid = {
  dev: '5c6e0bd8fc650e1408d0a2b2',
  pro: '5c6e08f2fc650e1408d0a2ac'
}
const webSocket = process.env.NODE_ENV === 'development' ? socket.dev : socket.pro
const vaptchaVid = process.env.NODE_ENV === 'development' ? vid.dev : vid.pro
console.log(process.env)
let djUrl = '/vue'

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
  webSocket: webSocket,
  vaptchaVid: vaptchaVid,
  baseUrl: {
    dev: djUrl,
    pro: djUrl
  },
  /**
   * @description 配置路由到django后台的url
   */
  registerUrl:  'account/register',
  loginUrl:  'account/login',
  logoutUrl: 'account/logout',
  goodUrl: 'shop/good',
  createGoodUrl: 'shop/create_good',
  updateGoodUrl: 'shop/update_good',
  deleteGoodUrl:  'shop/delete_good',
  getQuantifyUrl: 'common/quantify_list',
  getSupplierUrl: 'common/supplier_list',
  getGenreUrl: 'common/genre_list',
  addQuantifyUrl: 'common/add_quantify',
  getPackageData: 'shop/other_package_list',
  otherPackage: 'shop/other_package',
  scanStockSearch: 'shop/scan_stock_search',
  saveStockGood: 'shop/create_stock_in_record',
  getExamTask: 'shop/get_exam_task',
  commitExamTask: 'shop/commit_exam_task',
  getShopList: 'shop/shop_list',
  searchStockReport: 'shop/search_stock_report',
  scanSaleSearch: 'shop/scan_sale_search',
  searchGoodSale: 'shop/search_good_sale',
  arrangeGoodsSale: 'sale/goods_sale',
  getPersonList: 'common/person_list',
  getOrderList: 'sale/order_list',
  getOrderDetail: 'sale/order_detail',
  getCommonData: 'sale/marketing_analysis',
  goodsSalesRank: 'sale/goods_sales_rank'
}
