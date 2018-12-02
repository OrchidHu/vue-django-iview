// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import store from './store'
import router from './router'
import iView from 'iview'
import axios from 'axios'
import VueAxios from 'vue-axios'
import 'iview/dist/styles/iview.css'
Vue.config.productionTip = false

Vue.use(VueAxios, axios)

Vue.use(iView)

/* eslint-disable no-new */

new Vue({
  el: '#app',
  store,
  router,
  components: { App },
  template: '<App/>'
})
iView.Message.config({
  top: 50,
  duration: 1.5
})
// notice 配置
iView.Notice.config({
  top: 50,
  duration: 3
})
// LoadingBar 配置
iView.LoadingBar.config({
  // color: '#5cb85c',
  // failedColor: '#f0ad4e',
  height: 3
})
