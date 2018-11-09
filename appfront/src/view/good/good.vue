<template>
<div >
  <div style="margin-left: 10px; font-size: 12px; height: 35px">
    多选框 <i-switch v-model="showCheckbox" style="margin-right: 5px"></i-switch>
    <Button @click="createGood" style="float: right; margin-right: 50px; color: white; background: #2d8cf0">新建</Button>
    </div>
    <Table @on-row-dblclick="editGood"
           @on-sort-change="handleSortChange"
           @on-filter-change="handleFilterChange"
           border stripe show-header
           :height="fixedHeader ? 390 : ''"
           :loading="tableLoading"
           size="small"
           :data="dataWithPage"
           :columns="tableColumns"></Table>
    <div style="margin: 10px;overflow: hidden">
      <Button @click="deleteGood" style=" background: tomato; color: white; letter-spacing: 2px; margin-left: 50px">删除</Button>
        <span style="text-align:center; ">
            <Page :total="limitData.length"
                  :current.sync="current"
                  show-sizer
                  @on-page-size-change="handleChangePageSize"
            ></Page>
        </span>
    </div>
  <good-modal v-bind:modalData="modalData" @modal-success-valid="handleSubmit"></good-modal>
</div>
</template>
<script>
import config from '@/config'
import {ajaxGet} from '@/api/user'
import GoodModal from '@/components/good-modal'

const formData = {
  id: null,
  bar_id: '',
  name: '',
  genre: '',
  buy_price: null,
  sale_price: null,
  supplier: ''
}

export default {
  name: 'good_page',
  components: {
    GoodModal
  },
  data () {
    return {
      modalData: {
        openModal: false,
        changeType: '',
        form: Object.assign({}, formData)
      },
      total: 0,
      current: 1,
      loading: false,
      changeType: 'create',
      pageSize: 10,
      sortType: 'normal', // normal || asc || desc
      filterType: 'undefined', // undefined || 1 || 2 || 或者其他
      fullData: [],
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
    // 过滤排序筛选数据
    limitData () {
      let data = [...this.fullData]
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
    // 将筛选过滤后的数据进行分页
    dataWithPage () {
      const data = this.limitData
      const start = this.current * this.pageSize - this.pageSize
      this.cleanData = [...data].splice(start, this.pageSize)
      return this.cleanData
    }
  },
  methods: {
    // 自定义过滤
    handleFilterChange () {
      this.current = 1
    },
    // 自定义排序
    handleSortChange ({columns, key, order}) {
      this.sortType = order
      this.current = 1
    },
    // 处理一页显示多少条数据
    handleChangePageSize (val) {
      this.pageSize = val
    },
    createGood () {
      this.modalData.changeType = 'create'
      this.modalData.openModal = true
      this.modalData.form = Object.assign({}, formData)
    },
    // 双击修改当前行的值
    editGood (row, index) {
      this.editIndex = index
      this.modalData.openModal = true
      this.modalData.changeType = 'edit'
      this.modalData.form = row // 把当前行的数据赋值给管道变量
    },
    deleteGood () {

    },
    // 处理Modal成功校验后回调的数据
    handleSubmit (data) {
      if (this.modalData.changeType === 'create') { // 新建就push数据
        // this.fullData.push(data)
        this.fullData = [data].concat(this.fullData)
      } else { // 更新则把新值赋值给当前行
        for (let key in formData) {
          this.cleanData[this.editIndex][key] = data[key]
        }
      }
    },
  },
  // 在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.tableLoading = true
    this.$http.get(config.goodUrl, {withCredentials: true}).then(res => {
      this.tableLoading = false
      let dictData = res.data
      if (dictData.stat === 'success') {
        this.fullData = dictData.data
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

  }
}
</script>
