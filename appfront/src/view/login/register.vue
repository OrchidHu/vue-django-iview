<style lang="less">
  @import './register.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="注册" :bordered="false">
        <div class="form-con">
          <register-form @on-success-valid="handleSubmit" @on-error-valid="handleErrorValid"></register-form>
          <div style="text-align: end; padding-right: 16px;">已有账号... <a href="login">直接登录 >></a></div>
          <span style="font-size: 12px"></span>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import RegisterForm from '@/components/register-form'
import { mapActions } from 'vuex'
import $ from 'jquery'
export default {
  components: {
    RegisterForm
  },
  data () {
    return {
      vaptchaObj: '', // 定义全局变量, vaptcha实例
      token: '',
      isValid: false, // 这里是表单通过验证，才启动vaptcha验证
      isPass: false // 多次操作错误，vaptcha就会累加之前的监听
    }
  },
  methods: {
    ...mapActions([
      'handleLogin'
    ]),
    handleSubmit ({ userName, password }) {
      this.isValid = true
      this.vaptchaObj.listen('pass', () => {
        // 验证成功进行后续操作
        if (this.isPass) return
        this.isPass = true
        this.token = this.vaptchaObj.getToken()
        this.handleLogin({ userName, password }).then(res => {
          if (res.stat === 'success') {
            this.$router.push({
              name: 'home'
            })
          } else {
            this.vaptchaObj.reset();
            this.$Notice.error({title: res.msg})
          }
        })
      })
      this.isPass = false
    },
    handleErrorValid () {
      this.isValid = false
    }
  },
  mounted: function () {
    // 加载完成后启动vaptcha
    window.vaptcha({
      // 配置参数
      vid: '5c6e0bd8fc650e1408d0a2b2',
      type: 'invisible'
      // 其他配置参数省略
    }).then(vaptchaObj => {
      this.vaptchaObj = vaptchaObj // 将VAPTCHA验证实例保存到局部变量中
      // 验证码加载完成后将事件绑定到按钮
      // 调用validate()方法的伪代码，将该方法的调用绑定在'click'事件上，实际开发中需要更改为合适的调用方式
      this.vaptchaObj.render() // 执行该方法, 生成验证码
      // 点击登录按钮，启动vaptcha验证
      $('#login-button').on('click', () => {
        if (this.isValid) {
          vaptchaObj.validate()
        }
      })
      // $('#reset').on('click', function () {
      //   vaptchaObj.reset()
      // })
    })
    // 登录清除上次的localStorage
    var storage = window.localStorage
    storage.clear()
  }
}
</script>
