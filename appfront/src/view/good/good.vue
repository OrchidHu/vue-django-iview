

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

  },
  //在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    this.$router.replace({
      name: 'error_401'
    })
  },
  mounted () {

  },
  beforeDestroy () {

  }
}
</script>
