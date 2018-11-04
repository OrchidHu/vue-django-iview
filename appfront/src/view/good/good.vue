<template>
<div style="height:100px">
  <div style="margin: 10px; font-size: 12px">
        边框 <i-switch  v-model="showBorder" style="margin-right: 5px"></i-switch>
        斑马线 <i-switch v-model="showStripe" style="margin-right: 5px"></i-switch>
        索引 <i-switch v-model="showIndex" style="margin-right: 5px"></i-switch>
        多选框 <i-switch v-model="showCheckbox" style="margin-right: 5px"></i-switch>
        表头 <i-switch v-model="showHeader" style="margin-right: 5px"></i-switch>
        表格滚动 <i-switch v-model="fixedHeader" style="margin-right: 35px"></i-switch>
        表格尺寸
        <Radio-group style="display:inline"  v-model="tableSize" type="button">
            <Radio label="large">大</Radio>
            <Radio label="default">中</Radio>
            <Radio label="small">小</Radio>
        </Radio-group>
    </div>
    <Table @on-row-dblclick="clickRow" :border="showBorder" :stripe="showStripe" :show-header="showHeader" :height="fixedHeader ? 250 : ''" :size="tableSize" :data="tableData3" :columns="tableColumns3"></Table>
    <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
            <Page :total="11" show-elevator :current="1" @on-change="changePage"></Page>
        </div>
    </div>
    <Modal title="修改商品" v-model="openModal" footer-hide>
      <Form :model="form" :label-width="70">
        <FormItem label="条码">
          <Input v-model="form.bar_id"/>
        </FormItem>
        <FormItem label="名称">
          <Input v-model="form.name"/>
        </FormItem>
        <FormItem label="类别">
          <Input v-model="form.genre"/>
        </FormItem>
        <FormItem label="进价">
          <Input v-model="form.buy_price"/>
        </FormItem>
        <FormItem label="售价">
          <Input v-model="form.sale_price"/>
        </FormItem>
        <FormItem label="供应商">
          <Input v-model="form.supplier"/>
        </FormItem>
      </Form>
      <div style="width:480px; height:25px">
        <Button @click="cancel" style="float:right">取消</Button>
        <Button @click="save" style="float:right; margin-right: 15px">保存</Button>
      </div>
    </Modal>
</div>
</template>
<script>
import { setToken, setUserName, getToken, getUserName } from '@/libs/util'
import config from '@/config'
export default {
  name: 'good_page',
  data () {
    return {
      openModal: false,
      total:11,
      form: {
        bar_id: '',
        name: '',
        genre: '',
        buy_price: '',
        sale_price: '',
        supplier: ''
       },
      items: [{ name: 'Foo', value: 2 },{ name: 'Bar', value:1 }],
      waiting:"1",
      tableData3: [
        {
            bar_id: '',
            name: '',
            genre: '',
            buy_price: '',
            sale_price: '',
            supplier: ''
        }
      ],
      showBorder: false,
      showStripe: false,
      showHeader: true,
      showIndex: true,
      showCheckbox: false,
      fixedHeader: false,
      tableSize: 'default'
    }
  },

  computed: {
            tableColumns3 () {
                let columns = [];
                if (this.showCheckbox) {
                    columns.push({
                        type: 'selection',
                        width: 60,
                        align: 'center'
                    })
                }
                if (this.showIndex) {
                    columns.push({
                        type: 'index',
                        width: 60,
                        align: 'center'
                    })
                }
                columns.push({
                    title: '条码',
                    key: 'bar_id',
                });
                columns.push({
                    title: '名称',
                    key: 'name',
                    sortable: true
                });
                columns.push({
                    title: '类别',
                    key: 'genre',
                });
                columns.push({
                    title: '进价',
                    key: 'buy_price',
                    sortable: true
                });
                columns.push({
                    title: '售价',
                    key: 'sale_price',
                    sortable: true
                });
                columns.push({
                    title: '供货商',
                    key: 'supplier'
                });
                return columns;
            }
        },
  methods: {
    changePage () {
    },
    clickRow (raw,index) {
      this.openModal = true
      this.editIndex = index
      this.form = this.tableData3[index]
      console.log(this.tableData3[index].name)
    },
    save () {
      this.tableData3[this.editIndex] = this.form
      this.$Message.info('Clicked ok')
      this.openModal = false
    },
    cancel () {
      this.$Message.info('Clicked cancel');
    },
    handleClearCurrentRow () {
    alert("asdf")
      this.$refs.currentRowTable.clearCurrentRow();
    }
  },
  //在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    const token = getToken()
    const username = getUserName()
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.$http.get(config.goodUrl,{withCredentials: true},{params:{token:token, username:username}}).then(res => {
      let dict_data = res.data
      if(dict_data.stat == 'success') {
         this.tableData3 = dict_data.data
      // 后端的token失效或者前端的token和后端的token不匹配，访问权限页面需要再次验证身份
      } else if(dict_data.relogin == 'true'){
        this.$Notice.error({
          title: dict_data.msg,
          desc: '即将进入权限页面'
        })
        // 清除cookies 使得router路由到login, 以验证其身份是否是本人操作
        this.$store.commit('setToken', '')
        this.$store.commit('setUserName', '')
        this.$router.push({
          name: 'login'
        })
      // 后端发现带有此token的用户，不具备访问此页面的权限
      }else{
        this.$router.replace({
          name: 'error_401'
        })
      }
    })
  },
  mounted () {

  },
  beforeDestroy () {

  }
}
</script>
