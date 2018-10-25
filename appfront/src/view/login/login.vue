<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit"></login-form>
          <p class="login-tip">输入任意用户名和密码即可</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '../../components/login-form'
import config from '@/config'
import { mapActions, mapMutations} from 'vuex'
export default {
  components: {
    LoginForm
  },
  methods: {
    ...mapActions([
      'handleLogin',
      'getUserInfo'
    ]),
    ...mapMutations([
      'setUser'
    ]),
    handleSubmit ({ userName, password }) {
          let that = this.$router;
          this.$http.post(config.loginUrl, {username:userName, password:password},{
                            emulateJSON:true
                        }).then(res => {
                let dict_data = res.data
                if(dict_data.stat == 'success') {
                this.$store.commit('setToken', dict_data.token)
                this.$store.commit('setUserName', dict_data.username)
                this.$store.commit('setSessionId', dict_data.session_id)
                    this.$router.push("/home")
                } else {
                    this.$Notice.error({
                    title: dict_data.msg,
                    desc: '注意大小写'
                })
                }
            })
    }
  }
}
</script>

<style>

</style>

