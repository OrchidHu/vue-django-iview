<template>
    <Input v-model="value" v-if="waitingToLoad" placeholder="Enter something..." style="width: 300px" />
</template>
<script>
import { setToken, setUserName, getToken, getUserName } from '@/libs/util'
import config from '@/config'
export default {
  name: 'backBtnGroup',
  data () {
    return {
      value: ''
    }
  },
  methods: {

  },
  //在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    const token = getToken()
    const username = getUserName()
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.$http.get(config.goodUrl,{withCredentials: true},{params:{token:token, username:username}}).then(res => {
      let dict_data = res.data
      if(dict_data.stat == 'success') {
         this.value = 'isok'
      // 后端的token失效或者前端的token和后端的token不匹配，访问权限页面需要再次验证身份
      } else if(dict_data.relogin == 'true'){
        this.$Notice.error({
          title: dict_data.msg,
          desc: '即将进入权限页面'
        })
        // 清除cookies 使得router路由到login, 以验证其身份是否是本人操作
        this.$store.commit('setToken', '')
        this.$store.commit('setUserName', '')
        this.$router.push({
          name: 'login'
        })
      // 后端发现带有此token的用户，不具备访问此页面的权限
      }else{
        this.$router.replace({
          name: 'error_401'
        })
      }
    })
  },
  mounted () {

  },
  beforeDestroy () {

  }
}
</script>
