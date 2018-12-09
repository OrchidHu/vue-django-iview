<template>
  <div class="header">{{sock}}
  </div>
</template>
<script>
var message = '12'
export default {
  data () {
    var sock
    if ('WebSocket' in window) { // 判断当前浏览器是否支持webSocket
      sock = new WebSocket('ws://127.0.0.1:8000/chart/push') // 建立连接
    }
    sock.onopen = (e) => { // 成功建立连接
      sock.send('hello world')
    }
    sock.onmessage = (evt) => {
      var msg = evt.data
      message = evt.data
      console.log(message)
    }
    setTimeout(() => {
      this.$Message.success(message)
    }, 2000)
    return {
      sock: sock
    }
  },
  methods: {
  }
}
</script>
