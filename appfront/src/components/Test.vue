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
import { mapActions } from 'vuex'
export default {
  components: {
    LoginForm
  },
  methods: {
    handleSubmit ({ userName, password }) {
          let that = this.$router;
          this.$http.post('http://localhost:8000/shop/',{username:userName, password:password},{
                            emulateJSON:true
                        }).then(res => {
                let reStat = res.data.stat
                console.log(res.data)
                if(reStat == 'success') {
                    this.$router.push("/")
                } else {
                    this.$Notice.error({
                    title: '账号密码错误',
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

