<template>
  <strong class="header">
    <router-link to="">
      <Button size="large" type="text"  @click="backHome">
        <Icon :size="16" type="md-home"></Icon>首页</Button>
    </router-link>
    <Button size="large" type="text"  @click="backPrev">返回上一页</Button>
   <router-link to='/good'> <Button size="large" type="text"  @click="toGood">商品</Button></router-link>
  </strong>
</template>
<script>
export default {
  name: 'backBtnGroup',
  data () {
    return {
      second: 500,
      timer: null,
      message: '2323'
    }
  },
  methods: {
    backHome () {
      this.$router.replace({
        name: 'home'
      })
    },
    backPrev () {
      this.$router.go(-1)
    },
    toGood () {
      this.$router.push({
        name: 'good'
      })
    }
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
