<template>
  <span class="user-avator-dropdown">
    <Dropdown @on-click="handleClick">
      <Avatar :src="userAvator"/>
        <Icon :size="25" type="ios-arrow-down"></Icon>
          <DropdownMenu slot="list">
        <DropdownItem name="logout">退出登录</DropdownItem>
      </DropdownMenu>
    </Dropdown>
  </span>
</template>

<script>
import './login-out.less'
import { mapActions } from 'vuex'
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
    ...mapActions([
      'handleLogOut'
    ]),
    handleClick (name) {
      this.handleLogOut().then(() => {
        this.$router.push({
          name: 'login'
        })
      })
    }
  }
}
</script>
