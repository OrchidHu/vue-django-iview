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
import LoginForm from '../components/login-form'
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
          this.$http.post('http://localhost:8000/shop/',{username:userName, password:password},{
                            emulateJSON:true
                        }).then(res => {
                let django_data = res.data
                if(django_data.stat == 'success') {
                this.$store.commit('setToken', '234', '1MIN')
                    this.$router.push("/home")
                } else {
                    this.$Notice.error({
                    title: django_data.msg,
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

