
<template>
  <div>
    <Button size="warning" type="text"  @click="backHome">返回首页</Button>
    <Button size="warning" type="text" >返回上一页({{ second }}s)</Button>
  </div>
</template>

<script>
export default {
  name: 'backBtnGroup',
  data () {
    return {
      second: 5,
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
