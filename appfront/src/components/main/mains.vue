<template>
    <div class="layout">
        <Layout>
            <Header class="header-con">
                <Menu class="menu-con" mode="horizontal" theme="dark" active-name="1">
                    <div class="layout-logo">
                      <img  height="30" width="80":src="Logo" key="logo" />
                    </div>
                    <div class="layout-nav">
                        <MenuItem name="1">
                            <Icon type="ios-navigate"></Icon>
                            Item 1
                        </MenuItem>
                        <MenuItem name="2">
                            <Icon type="ios-keypad"></Icon>
                            Item 2
                        </MenuItem>
                        <MenuItem name="3">
                            <Icon type="ios-settings-outline" />
                            设置
                        </MenuItem>
                        <MenuItem name="4">
                            <loginOut/>
                        </MenuItem>
                    </div>
                </Menu>
            </Header>
            <Content :style="{padding: '0 50px'}">
                <Breadcrumb :style="{margin: '20px 0'}">
                    <BreadcrumbItem to="/401">
                        <Icon :size="16" type="md-home">
                        </Icon>首页
                    </BreadcrumbItem>
                    <BreadcrumbItem>Components</BreadcrumbItem>
                    <BreadcrumbItem>Layout</BreadcrumbItem>
                </Breadcrumb>
                <Card>
                    <div style="min-height: 380px;">
                        Content
                    </div>
                </Card>
            </Content>
            <Footer class="layout-footer-center">2018-2019 &copy; iView</Footer>
        </Layout>
    </div>
</template>
<script>
    import LoginOut from '@/components/login-out'
    import Logo from '@/assets/images/logo.jpg'
    export default {
      name: 'Main',
      data () {
        return {
          Logo
        }
      },
      components: {LoginOut},
      computed: {
        getImage () {
          return this.$store.state.avatorImgPath
        }
      },
    }
</script>
<style>
  @import './mains.less'
</style>
