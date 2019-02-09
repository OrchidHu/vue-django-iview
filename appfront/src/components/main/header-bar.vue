<template>
  <Header class="header-con">
    <Row>
      <Col :sm="0" :md="4">
        <div class="layout-logo">
          <img  height="30" width="80" :src="Logo" key="logo" />
        </div>
      </Col>
      <Col :sm="18" :md="15">
        <Menu class="menu-con" mode="horizontal" :theme="theme1" :active-name="activeName">
          <Row type="flex" justify="end" class="code-row-bg">
            <i-col>
              <MenuItem name="good_page" to="/good/good_page">
                <Icon color="orange" type="logo-github" />
                商品管理
              </MenuItem>
            </i-col>
            <MenuItem name="good_sale" to="/sale/good_sale">
              <Icon color="orange" type="md-cart" />
              商品销售
            </MenuItem>
            <MenuItem name="stock">
              <Dropdown trigger="hover" @on-click="clickStock">
                <div href="javascript:void(0)">
                  <Icon color="orange" type="ios-browsers" />
                  库存管理
                </div>
                <DropdownMenu id="abc" slot="list">
                  <DropdownItem name="stockIn">
                    <Icon size="16" color="#5cadff" type="md-exit" />
                     快速入库</DropdownItem>
                  <DropdownItem name="stockOut">
                    <Icon size="16" color="#5cadff" type="md-open" />
                     快速出库</DropdownItem>
                  <DropdownItem name="examTask">
                    <Icon size="16" color="#5cadff" type="md-checkbox-outline" />
                     审核任务
                    <Badge v-if="count" status="error"></Badge>
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </MenuItem>
            <MenuItem name="report">
              <Dropdown trigger="hover" @on-click="clickReport">
                <Icon color="orange" type="md-list-box" />
                报表查询
                <DropdownMenu slot="list">
                  <DropdownItem name="stockReport">
                    <Icon size="16" color="#5cadff" type="ios-browsers" />
                    库存查询
                  </DropdownItem>
                  <DropdownItem name="saleDetail">
                    <Icon size="16" color="#5cadff" type="ios-browsers" />
                    交易明细
                  </DropdownItem>
                </DropdownMenu>
              </Dropdown>
            </MenuItem>
          </Row>
        </Menu>
      </Col>
      <Col :sm="6" :md="5" >
        <Row type="flex" justify="end" class="code-row-bg">
          <i-col :sm="5" :md="5">
            <fullScreen v-model="isFullscreen"/>
          </i-col>
          <i-col :sm="5" :md="5">
            <Dropdown>
              <Badge :count="count" :offset="[20,4]">
                <Icon type="md-notifications-outline" size="24" />
              </Badge>
              <DropdownMenu slot="list">
                <Tabs  value="notification" @on-click="ok">
                  <TabPane :label="noticeLabel" name="notification" >
                    <div class="notifications">
                      {{notification}}
                    </div>
                  </TabPane>
                  <TabPane label="系统消息" icon="logo-apple" name="system">
                    <div class="notifications">
                      <CellGroup>
                      </CellGroup>
                    </div>
                  </TabPane>
                </Tabs>
              </DropdownMenu>
            </Dropdown>
          </i-col>
          <i-col :sm="14" :md="10" >
            <loginOut :user-avator="userAvator" />
          </i-col>
        </Row>
      </Col>
    </Row>
  </Header>
</template>
<script>
import FullScreen from '@/components/fullScreen'
import LoginOut from '@/components/login-out'
import Logo from '@/assets/images/logo.jpg'
import { mapMutations } from 'vuex'
import CommonIcon from '@/components/common-icon'
export default {
  name: 'HearderBar',
  data () {
    return {
      isFullscreen: false,
      activeName: '8',
      Logo,
      theme1: 'light',
      notification: this.$store.state.task,
      noticeLabel: (h) => {
        return h('div', [
          h('span', '通知信息'),
          h('Badge', {
            props: {
              count: this.$store.state.task.length
            }
          })
        ])
      }
    }
  },
  components: {LoginOut, FullScreen, CommonIcon},
  computed: {
    userAvator () {
      // let aa = 'images/2018/11/16/VXR5LLL18U_LNVNKCZECK.png'
      console.log(this.$store.state.avator)
      let storeAvator = this.$store.state.avator
      let avator = storeAvator || localStorage.getItem('userAvator')
      if (!avator) {
        // return '' //如果后台没有传avator参数, 则使用的iview默认图片
        return // 直接return使用的是props默认值
      }
      return require('@/assets/' + avator)
    },
    count () {
      return this.$store.state.task.length
    }
  },
  methods: {
    ...mapMutations([
      'clearTask'
    ]),
    ok (name) {
      if (name === 'notification') {
        this.$store.commit('clearTask', [])
      }
    },
    clickStock (name) {
      if (name === 'stockIn') {
        this.$router.push({
          name: 'stock_in'
        })
      } else if (name === 'stockOut') {
        this.$router.push({
          name: 'stock_out'
        })
      } else if (name === 'examTask') {
        this.$router.push({
          name: 'exam_task'
        })
      }
    },
    clickReport (name) {
      if (name === 'stockReport') {
        this.$router.push({
          name: 'stock_report'
        })
      }
      if (name === 'saleDetail') {
        this.$router.push({
          name: 'sale_detail'
        })
      }
    }
  },
  watch: {
    '$route' (newRoute) {
      this.activeName = newRoute.name
    }
  }
}
</script>
<style>
  /*#abc{*/
    /*background: red;*/
    /*position: relative;*/
    /*z-index: 200000000000000*/
  /*}*/
</style>
