<template>
  <div class="header">{{sock}}
    {{message}}
  </div>
</template>
<script>
import { mapMutations } from 'vuex'
export default {
  data () {
    var sock
    var message
    if ('WebSocket' in window) { // 判断当前浏览器是否支持webSocket
      sock = new WebSocket('ws://127.0.0.1:8000/chart/push') // 建立连接
    }
    sock.onopen = (e) => { // 成功建立连接
      sock.send('hello world')
    }
    sock.onmessage = (evt) => {
      message = evt.data
      this.setTask(message)
      console.log(message)
    }
    setTimeout(() => {
      this.$Message.success(message)
    }, 2000)
    return {
      sock: sock,
      message: this.$store.state.task
    }
  },
  computed: {
  },
  methods: {
    ...mapMutations([
      'setTask'
    ])
  },
  destroyed () {
    this.sock.close()
  }
}
</script>
