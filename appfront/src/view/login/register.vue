<style lang="less">
  @import './register.less';
</style>

<template>
  <div class="login">
    <div class="login-con">
      <Card class="login-card" icon="log-in" title="注册" :bordered="false">
        <Row>
          <i-col span="18">
            <div class="form-con">
              <register-form @on-success-valid="handleSubmit"></register-form>
            </div>
          </i-col>
          <i-col span="1">
            <Divider style="height: 450px" type="vertical" />
          </i-col>
          <i-col span="5">
            <div style="text-align: end;padding-top: 15px;">已有账号. <a href="login">直接登录 >></a></div>
            <span style="font-size: 12px"></span>
          </i-col>
        </Row>
      </Card>
    </div>
  </div>
</template>

<script>
import RegisterForm from '@/components/register-form'
import config from '@/config'
import { mapActions } from 'vuex'
import {register} from '@/api/user'
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
      if (!this.isValid) this.$Message.error('请完成人机验证')
      else {
        register({userName, password}).then(res => {
          if (res.data.stat === 'success') {

          } else {
            this.$Message.error(res.data.msg)
          }
        })
      }
    },
    handleErrorValid () {
      this.isValid = false
    }
  },
  mounted: function () {
    vaptcha({
      vid: config.vaptchaVid, // 验证单元id
      type: 'embed', // 显示类型 点击式
      container: '#vaptchaContainer' // 按钮容器，可为Element 或者 selector
    }).then((vaptchaObj) => {
      vaptchaObj.listen('pass', () => {
        // 验证成功， 进行登录操作
        this.isValid = true
      })
      vaptchaObj.render()// 调用验证实例 vpObj 的 render 方法加载验证按钮
    })
    var storage = window.localStorage
    storage.clear()
  }
}
</script>
