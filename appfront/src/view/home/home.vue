<template>
  <div>
    <Button size="warning" type="text"  @click="backHome">返回首页</Button>
    <Button size="warning" type="text"  @click="backPrev">返回上一页</Button>
    <Button size="error" type="text"  @click="toGood">商品</Button>
    <p>{{ second }}s</p>
  </div>
</template>

<script>
export default {
  name: 'backBtnGroup',
  data () {
    return {
      second: 500,
      timer: null
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
  mounted () {
    this.timer = setInterval(() => {
      if (this.second === 0) this.backPrev()
      else this.second--
    }, 1000)
  },
  beforeDestroy () {
    clearInterval(this.timer)
  }
}
</script>
