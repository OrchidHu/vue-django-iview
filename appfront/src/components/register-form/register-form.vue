<template>
  <Form ref="registerForm" :model="form" :rules="rules" @keydown.enter.native="handleSubmit">
    <FormItem prop="userName">
      <Input v-model="form.userName" placeholder="请输入用户名">
        <span slot="prepend">
          <Icon :size="16" type="ios-person"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="password">
      <Input type="password" v-model="form.password" placeholder="请输入密码">
        <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <FormItem prop="rePassword">
      <Input type="password" v-model="form.rePassword" placeholder="请确认密码">
        <span slot="prepend">
          <Icon :size="14" type="md-lock"></Icon>
        </span>
      </Input>
    </FormItem>
    <div id="vaptchaContainer" class="vaptcha-container" style="width:366px;height:100%;">
      <!--vaptcha-container是用来引入VAPTCHA的容器，下面代码为预加载动画，仅供参考-->
      <div class="vaptcha-init-main">
        <div class="vaptcha-init-loading">
          <a href="https://www.vaptcha.com" target="_blank">
            <img src="https://cdn.vaptcha.com/vaptcha-loading.gif" />
          </a>
          <span class="vaptcha-text">VAPTCHA启动中...</span>
        </div>
      </div>
    </div>
    <br>
    <FormItem>
      <Button @click="handleSubmit" type="primary" long>注册</Button>
    </FormItem>
  </Form>
</template>
<script>
import {register} from '@/api/user'

export default {
  name: 'LoginForm',
  props: {
    userNameRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '账号不能为空', trigger: 'blur' }
        ]
      }
    },
    passwordRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '密码不能为空', trigger: 'blur' }
        ]
      }
    },
    rePasswordRules: {
      type: Array,
      default: () => {
        return [
          { required: true, message: '请输入确认密码' }
        ]
      }
    }
  },
  data () {
    return {
      form: {
        userName: '1',
        password: '1',
        rePassword: '1'
      },
      isValid: false
    }
  },
  computed: {
    rules () {
      return {
        userName: this.userNameRules,
        password: this.passwordRules,
        rePassword: this.rePasswordRules
      }
    }
  },
  methods: {
    handleSubmit () {
      this.$refs.registerForm.validate((valid) => {
        if (valid) {
          let username = this.form.password.trim()
          let password = this.form.rePassword.trim()
          if (username !== password) {
            this.$Message.error('两次输入的密码不相同')
            return
          }
          if (!this.isValid) this.$Message.error('请完成人机验证')
          else {
            console.log(11)
            register({username, password}).then(res => {
              console.log(res)
            })
          }
        }
      })
    }
  },
  mounted () {
    vaptcha({
      vid: '5c6e0bd8fc650e1408d0a2b2', // 验证单元id
      type: 'embed', // 显示类型 点击式
      container: '#vaptchaContainer' // 按钮容器，可为Element 或者 selector
    }).then((vaptchaObj) => {
      vaptchaObj.listen('pass', () => {
        // 验证成功， 进行登录操作
        this.isValid = true
      })
      vaptchaObj.render()// 调用验证实例 vpObj 的 render 方法加载验证按钮
    })
  }
}
</script>
<style>
  .vaptcha-init-main {
    display: table;
    width: 100%;
    height: 100%;
    background-color: #EEEEEE;
  }
  .vaptcha-init-loading {
    display: table-cell;
    vertical-align: middle;
    text-align: center
  }
  .vaptcha-init-loading>a {
    display: inline-block;
    width: 18px;
    height: 18px;
    border: none;
  }
  .vaptcha-init-loading>a img {
    vertical-align: middle
  }
  .vaptcha-init-loading .vaptcha-text {
    font-family: sans-serif;
    font-size: 12px;
    color: #CCCCCC;
    vertical-align: middle
  }
</style>
