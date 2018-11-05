<template>
<div style="height:100px">
  <div style="margin: 10px; font-size: 12px">
    多选框 <i-switch v-model="showCheckbox" style="margin-right: 5px"></i-switch>
    表格滚动 <i-switch v-model="fixedHeader" style="margin-right: 35px"></i-switch>

    <Button @click="createGood" style="float:right">新建</Button>
    </div>
    <Table @on-row-dblclick="editGood"
           @on-sort-change="handleSortChange"
           @on-filter-change="handleFilterChange"
           border stripe show-header
           :height="fixedHeader ? 250 : ''"
           size="small"
           :data="dataWithPage"
           :columns="tableColumns"></Table>
    <div style="margin: 10px;overflow: hidden">
        <div style="text-align:center; margin: 16px 0">
            <Page :total="limitData.length"
                  :current.sync="current"
                  show-sizer
                  @on-page-size-change="handleChangePageSize"
            ></Page>
        </div>
    </div>
    <Modal :title="changeType==='create'? '新增商品': '编辑商品'" v-model="openModal" footer-hide>
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
        <Button @click="editSave" v-if="changeType==='edit'" style="float:right">保存</Button>
        <Button @click="createSave" v-if="changeType==='create'" style="float:right; margin-right: 15px">新建</Button>
      </div>
    </Modal>
</div>
</template>
<script>
import config from '@/config'
const formData = {
  bar_id: '',
  name: '',
  genre: '',
  buy_price: '',
  sale_price: '',
  supplier: ''
}
export default {
  name: 'good_page',
  data () {
    return {
      total: 0,
      current: 1,
      loading: false,
      openModal: false,
      changeType: 'create',
      pageSize: 10,
      sortType: 'asc', // normal || asc || desc
      filterType: 'undefined', // undefined || 1 || 2 || 或者其他
      form: {
        bar_id: '',
        name: '',
        genre: '',
        buy_price: '',
        sale_price: '',
        supplier: ''
      },
      tableData: [],
      showCheckbox: false,
      fixedHeader: true,
      columns: []
    }
  },

  computed: {
    tableColumns () {
      let columns = []
      if (this.showCheckbox) {
        columns.push({type: 'selection', width: 60, align: 'center'})
      }
      columns.push({
        type: 'index',
        width: 60,
        align: 'center',
        indexMethod: (row) => {
          return (row._index + 1) + this.pageSize * (this.current - 1)
        }
      })
      columns.push({ title: '条码', key: 'bar_id' })
      columns.push({ title: '名称', key: 'name' })
      columns.push({ title: '类别', key: 'genre' })
      columns.push({ title: '进价', key: 'buy_price', sortable: 'custom' })
      columns.push({ title: '售价', key: 'sale_price' })
      columns.push({ title: '供货商', key: 'supplier' })
      return columns
    },
    limitData () {
      let data = [...this.tableData]
      if (this.sortType === 'asc') {
        data = data.sort((a, b) => {
          return a.buy_price > b.buy_price ? 1 : -1
        })
      }
      if (this.sortType === 'desc') {
        data = data.sort((a, b) => {
          return a.buy_price < b.buy_price ? 1 : -1
        })
      }
      return data
    },
    dataWithPage () {
      const data = this.limitData
      const start = this.current * this.pageSize - this.pageSize
      const end = start + this.pageSize
      return [...data].splice(start, end)
    }
  },
  methods: {
    handleFilterChange () {
      this.current = 1
    },
    handleSortChange ({columns, key, order}) {
      this.sortType = order
      this.current = 1
    },
    handleChangePageSize (val) {
      this.pageSize = val
    },
    editGood (raw, index) {
      this.openModal = true
      this.editIndex = index
      this.form = this.tableData[index]
      this.changeType = 'edit'
    },
    createGood () {
      this.form = formData
      this.openModal = true
      this.changeType = 'create'
    },
    editSave () {
      this.tableData[this.editIndex] = this.form
      this.$Message.info('保存成功')
      this.openModal = false
    },
    createSave () {
      this.$Message.info('新建成功')
      this.tableData.push(this.form)
      this.openModal = false
    },
    handleClearCurrentRow () {
      this.$refs.currentRowTable.clearCurrentRow()
    }
  },
  // 在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.$http.get(config.goodUrl, {withCredentials: true}).then(res => {
      let dictData = res.data
      if (dictData.stat === 'success') {
        this.tableData = dictData.data
      // 后端的token失效或者前端的token和后端的token不匹配，访问权限页面需要再次验证身份
      } else if (dictData.relogin === 'true') {
        this.$Notice.error({
          title: dictData.msg,
          desc: '即将进入权限页面'
        })
        // 清除cookies 使得router路由到login, 以验证其身份是否是本人操作
        this.$store.commit('setToken', '')
        this.$store.commit('setUserName', '')
        this.$router.push({
          name: 'login'
        })
      // 后端发现带有此token的用户，不具备访问此页面的权限
      } else {
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
