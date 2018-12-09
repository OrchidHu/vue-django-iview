<template>
    <div class="layout">
        <Layout :style="{minHeight: '100vh'}">
            <Header class="header-con">
                <Menu class="menu-con" mode="horizontal" :theme="theme1" active-name="1">
                  <Row>
                    <Col span="4">
                    <div class="layout-logo">
                      <img  height="30" width="80" :src="Logo" key="logo" />
                    </div>
                    </Col>
                    <Col span="14" offset="6">
                      <div class="layout-nav">
                        <MenuItem name="8" to="/good/good_page">
                            <Icon type="ios-navigate"></Icon>
                            商品管理
                        </MenuItem>
                        <MenuItem name="2">
                            <Icon type="ios-keypad"></Icon>
                            商品销售
                        </MenuItem>
                        <MenuItem name="3">
                          <Dropdown trigger="hover" @on-click="clickStock">
                            <div href="javascript:void(0)">
                              <Icon type="ios-settings-outline"/>
                              库存管理
                            </div>
                            <DropdownMenu slot="list">
                              <DropdownItem name="stockIn">快速入库</DropdownItem>
                              <DropdownItem name="stockOut">快速出库</DropdownItem>
                            </DropdownMenu>
                          </Dropdown>
                        </MenuItem>
                        <MenuItem name="4">
                            <Icon type="ios-settings-outline"/>
                            报表查询
                        </MenuItem>
                        <MenuItem name="5">
                            <Icon type="ios-settings-outline"/>
                            设置
                        </MenuItem>
                        <MenuItem name="6">
                            <fullScreen v-model="isFullscreen"/>
                        </MenuItem>
                        <MenuItem name="7">
                            <loginOut :user-avator="userAvator"/>
                        </MenuItem>
                      </div>
                    </Col>
                  </Row>
                </Menu>
            </Header>
            <Content :style="{padding: '0 48px'}">
              <Breadcrumb :style="{margin: '12px 0'}">
                <Icon size="16" type="md-home" />
                <BreadcrumbItem v-for="item in breadCrumbList" :to="item.to" :key="`bread-crumb-${item.name}`">
                  <common-icon  style="margin-right: 4px;" :size="12"  :type="item.icon || ''"/>
                  {{ item.meta.title }}
                </BreadcrumbItem>
              </Breadcrumb>
                <Card>
                    <div style="min-height: 640px; ">
                      <router-view></router-view>
                    </div>
                </Card>
            </Content>
            <!--<Footer class="layout-footer-center">2018-2019 &copy; iView</Footer>-->
        </Layout>
    </div>
</template>
<script>
import FullScreen from '@/components/fullScreen'
import LoginOut from '@/components/login-out'
import Logo from '@/assets/images/logo.jpg'
import { mapMutations } from 'vuex'
import CommonIcon from '@/components/common-icon'

export default {
  name: 'Main',
  data () {
    return {
      isFullscreen: false,
      Logo,
      theme1: 'light'
    }
  },
  components: {LoginOut, FullScreen, CommonIcon},
  computed: {
    userAvator () {
      // let aa = 'images/2018/11/16/VXR5LLL18U_LNVNKCZECK.png'
      let avator = this.$store.state.avator
      if (!avator) {
        // return '' //如果后台没有传avator参数, 则使用的iview默认图片
        return // 直接return使用的是props默认值
      }
      return require('@/assets/' + avator)
    },
    breadCrumbList () {
      return this.$store.state.app.breadCrumbList
    }
  },
  methods: {
    ...mapMutations([
      'setBreadCrumb'
    ]),
    clickStock (name) {
      if (name === 'stockIn') {
        this.$router.push({
          name: 'stock_in'
        })
      }
    },
    getCustomIconName (iconName) {
      return iconName.slice(1)
    }
  },
  watch: {
    '$route' (newRoute) {
      // const { name, query, params, meta } = newRoute
      // this.addTag({
      //   route: { name, query, params, meta },
      //   type: 'push'
      // })
      this.setBreadCrumb(newRoute)
      // this.setTagNavList(getNewTagList(this.tagNavList, newRoute))
      // this.$refs.sideMenu.updateOpenName(newRoute.name)
    }
  }
}
</script>
<style>
  @import "./mains.less"
</style>
