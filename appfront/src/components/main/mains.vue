<template>
    <div class="layout">
        <Layout :style="{minHeight: '100vh'}">
          <hearder-bar></hearder-bar>
            <Content :style="{padding: '0 48px'}">
              <Breadcrumb :style="{margin: '12px 0'}">
                <Icon size="16" type="md-home" />
                <BreadcrumbItem v-for="item in breadCrumbList" :to="item.to" :key="`bread-crumb-${item.name}`">
                  <common-icon  style="margin-right: 4px;" :size="12"  :type="item.icon || ''"/>
                  {{ item.meta.title }}
                </BreadcrumbItem>
              </Breadcrumb>
                <Card class="content">
                    <div style="min-height: 640px; ">
                      <router-view></router-view>
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2018-2019 &copy; iView</Footer>
        </Layout>
    </div>
</template>
<script>
import { mapMutations } from 'vuex'
import CommonIcon from '@/components/common-icon'
import HearderBar from './header-bar'
export default {
  name: 'Main',
  data () {
    return {
      theme1: 'light',
      notification: this.$store.state.app.task,
      noticeLabel: (h) => {
        return h('div', [
          h('span', '通知信息'),
          h('Badge', {
            props: {
              count: 3
            }
          })
        ])
      }
    }
  },
  components: {HearderBar, CommonIcon},
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
    },
    count () {
      return this.$store.state.app.task.length
    }
  },
  methods: {
    ...mapMutations([
      'setBreadCrumb'
    ]),
    ok (name) {
      if (name === 'notification') {
        console.log('we')
        this.clearTask()
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
