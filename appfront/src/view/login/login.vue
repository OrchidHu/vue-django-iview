<style lang="less">
  @import './login.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card icon="log-in" title="欢迎登录" :bordered="false">
        <div class="form-con">
          <login-form @on-success-valid="handleSubmit" @on-error-valid="handleErrorValid"></login-form>
          <Row style="height: 30px" type="flex" justify="start" align="middle">
            <Col span="9" style="font-size: 12px">使用第三方登录：</Col>
            <Col span="2"><img height="15" width="18" :src="QQ" key="logo" /></Col>
            <Col span="2"><img height="15" width="16" :src="WeiXin" key="logo" /></Col>
            <Col span="2"><img height="15" width="16" :src="Github" key="logo" /></Col>
          </Row>
          <span style="font-size: 12px"></span>
        </div>
      </Card>
    </div>
  </div>
</template>

<script>
import LoginForm from '../../components/login-form'
import config from '@/config'
import QQ from '@/assets/images/qq.jpg'
import Github from '@/assets/images/github.jpg'
import WeiXin from '@/assets/images/weixin.jpg'
import { mapActions } from 'vuex'
import $ from 'jquery'
export default {
  components: {
    LoginForm
  },
  data () {
    return {
      QQ,
      WeiXin,
      Github,
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
      vid: config.vaptchaVid,
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
