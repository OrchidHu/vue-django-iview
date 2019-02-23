<template>
  <div>
    <Row :gutter="10">
      <i-col span="16">
        <Form ref="registerForm" :model="form" :rules="rules" @keydown.enter.native="handleSubmit">
        <FormItem prop="userName">
          <Input v-model="form.userName" placeholder="请输入用户名">
        <span slot="prepend">
          <Icon :size="16" type="ios-person"></Icon>
        </span>
          </Input>
        </FormItem>
        <FormItem prop="password">
          <Input type="password" @on-change="onChangePassword" v-model="form.password" placeholder="请输入密码">
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
      </Form>
        <div id="vaptchaContainer" class="vaptcha-container" style="width:100%;height:100%;">
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
      </i-col>
      <i-col span="8">
        <div v-if="form.password" style="margin-top: 50px">
          <div style="font-size: 12px;"><Icon size="16" color="orange" type="md-alert" /> 请输入6-16位数字、字母或常用符号，字母区分大小写</div>
          <br>
          <span style="font-size: 12px">密码安全等级：</span>
          <Progress :percent="percent" :status="status" :stroke-width="5">
            <Icon type="checkmark-circled"></Icon>
            <span style="font-size: 12px">{{statusWord}}</span>
          </Progress>
        </div>
      </i-col>
    </Row>
    <br>
    <Button @click="handleSubmit" type="primary" long>注册</Button>
  </div>
</template>
<script>

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
          { required: true, message: '密码不能为空', trigger: 'change' },
          { type: 'string', pattern: /^[A-Za-z0-9_,.*&^%$#@!`?]{5,17}$/,
            message: '请输入6-16位数字、字母或常用符号', trigger: 'blur'}
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
      percent: '',
      status: '',
      statusWord: '',
      form: {
        userName: '',
        password: '',
        rePassword: ''
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
          this.$emit('on-success-valid', {
            userName: this.form.userName,
            password: this.form.password
          })
        }
      })
    },
    onChangePassword () {
      if (this.form.password) {
        this.status = 'wrong'
        this.percent = 15
        this.statusWord = '低'
      }
      if (this.form.password.match(RegExp(/(?=.*[a-z]+)(?=.*\d+).{6,16}|(?=.*[A-Z]+)(?=.*\d+).{6,16}/))) {
        this.status = 'wrong'
        this.percent = 40
        this.statusWord = '弱'
      }
      if (this.form.password.match(
        RegExp(/(?=.*[a-z]+)(?=.*\d+)(?=.*[A-Z]+).{8,16}|(?=.*[A-Za-z]+)(?=.*[_,.*&^%$#@!`?]+).{8,16}/))) {
        this.status = 'active'
        this.percent = 75
        this.statusWord = '中'
      }
      if (this.form.password.match(RegExp(/(?=.*[a-z]+)(?=.*\d+)(?=.*[A-Z]+)(?=.*[_,.*&^%$#@!`?]+).{10,16}/))) {
        this.status = 'success'
        this.percent = 100
        this.statusWord = '强'
      }
    }
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
