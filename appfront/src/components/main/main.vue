<style lang="less">
  @import './main.less';
</style>

<template>
  <Layout>
    <Header class="header-con">
      <div>
          <router-view/>
          <slot>
          <loginOut/></slot>
      </div>
    </Header>
  </Layout>
</template>
<script>
import LoginOut from '@/components/login-out'
export default {
  name: 'Main',
  components: {LoginOut},
  data(){
    return{aa:true }
  },
  computed: {
    getImage () {
      return this.$store.state.avatorImgPath
    }
  },
}
</script>
<style>

</style>
