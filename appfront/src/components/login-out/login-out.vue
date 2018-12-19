<template>
  <div style="display: inline" class="user-avator-dropdown">
    <Dropdown @on-click="handleClick">
      <Avatar :src="userAvator"/>
        <Icon :size="25" type="ios-arrow-down"></Icon>
          <DropdownMenu slot="list">
        <DropdownItem name="1">
          <Icon size="16" type="md-person" />
          个人中心</DropdownItem>
        <DropdownItem name="2">
          <Icon size="16" type="ios-settings" />
          设置
          <Badge status="error"></Badge></DropdownItem>
        <DropdownItem divided name="logout">
          <Icon size="16" type="md-log-out" />
          退出登录</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  </div>
</template>

<script>
import './login-out.less'
import { mapActions, mapMutations } from 'vuex'
// 临时使用一张图片
import minBoy from '@/assets/images/default-avator.jpg'
export default {
  name: 'LoginOut',
  props: {
    userAvator: {
      type: String,
      default: minBoy
    }
  },
  methods: {
    ...mapMutations([
      'clearTask'
    ]),
    ...mapActions([
      'handleLogOut'
    ]),
    handleClick (name) {
      if (name === 'logout') {
        this.handleLogOut().then(() => {
          this.$router.push({
            name: 'login'
          })
        })
        setTimeout(() => {
          // this.clearTask()
          this.$store.commit('clearTask', [])
        })
      }
      if (name === '1') {}
    }
  }
}
</script>
