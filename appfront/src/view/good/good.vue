<template>
<div style="height: 100%">
  <div style=" font-size: 12px; height: 40px">
    <Row type="flex" justify="center" align="middle" :gutter="4">
      <Col :sm="6" :md="4">
        <Cascader :data="genreList" filterable v-model="genreSelected" @on-change="onChangeGenre" placeholder="选择类别"></Cascader>
      </Col>
      <Col :sm="6" :md="5">
        <Input v-model="searchValue"  @keydown.enter.native="searchSubmit" search placeholder="条码 / 名称"/>
      </Col>
      <Col :sm="3" :md="2">
        <Button @click="searchSubmit" style="background: #2d8cf0; color: white">搜 索</Button>
      </Col>
      <Col :sm="4" :md="3" justify="end" align="middle">
        多选框 <i-switch v-model="showCheckbox"></i-switch>
      </Col>
      <Col :sm="3" :md="7">
        <a @click="reSetData"> 重置</a>

        <a v-if="selected" style="margin-left: 20px; color: chartreuse;">已选择 {{selectCount}} 项</a>
      </Col>
      <Col :sm="2" :md="3">
      <Button @click="createGood" style="margin-right: 50px; color: white; background: #2d8cf0">新建</Button>
    </Col></Row>
  </div>
    <Table @on-row-dblclick="editGood"
           @on-sort-change="handleSortChange"
           @on-filter-change="handleFilterChange"
           @on-selection-change="handleSelect"
           border stripe show-header
           :height="currentHeight"
           :loading="tableLoading"
           :size="tableSize"
           :data="dataWithPage"
           :columns="tableColumns"></Table>
    <div style="margin: 10px;">
      <Row type="flex" justify="center" align="middle">
        <i-col span="4" push="1">
          <Button @click="deleteGood"
                  :loading="deleteLoading"
                  :disabled="this.selected ? false : true"
                  style=" background: tomato; color: white; letter-spacing: 2px; ">删除</Button>
        </i-col>
        <i-col span="20" pull="2">
        <span style="text-align:center">
            <Page :total="limitData.length"
                  :current.sync="current"
                  show-sizer
                  :page-size="pageSize"
                  @on-page-size-change="handleChangePageSize"
            ></Page>
        </span>
        </i-col>
      </Row>
    </div>
  <good-modal ref="child" :modal-data="modalData" @modal-success-valid="handleSubmit"></good-modal>
</div>
</template>
<script>
import config from '@/config'
import {ajaxGet, ajaxExamGet} from '../../api/user'
import GoodModal from '@/components/good-modal'
import Bus from '../bus'

const formData = {
  id: null,
  bar_id: '',
  name: '',
  genre: '',
  genre_id: [],
  quantify: '',
  quantify_id: null,
  buy_price: null,
  sale_price: null,
  supplier: '',
  supplier_id: null
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
      tableSize: 'small',
      deleteLoading: false,
      changeType: 'create',
      pageSize: 10,
      sortType: 'normal', // normal || asc || desc
      filterType: 'undefined', // undefined || 1 || 2 || 或者其他
      fullData: [], // 备份的全量数据，在未更改之前全量数据不会被改变
      showCheckbox: false,
      fixedHeader: true,
      copyFullData: [], // 全量数据，用作筛选，搜索，排序的操作
      columns: [],
      selected: null,
      searchValue: null,
      selectCount: 0,
      genreList: [],
      genreSelected: [],
      genreFilterFullData: []
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
      columns.push({ title: '单位', key: 'quantify' })
      columns.push({ title: '进价', key: 'buy_price', sortable: 'custom' })
      columns.push({ title: '售价', key: 'sale_price', sortable: 'custom'})
      columns.push({ title: '供应商', key: 'supplier' })
      return columns
    },
    // 过滤排序筛选数据
    limitData () {
      let data = [...this.copyFullData]
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
    // 由于iview在表格<Table>操作(如:排序,搜索等)后会刷新所选项的样式展示，但是selection不会改变
    // 因此操作表格都对selected重置为空
    dataWithPage () {
      const data = this.limitData
      this.selected = null // 这里是防止已有选中项，并对表格进行删除以外的操作，导致表格没勾，实际却是已选
      const start = this.current * this.pageSize - this.pageSize
      this.cleanData = [...data].splice(start, this.pageSize)
      return this.cleanData
    },
    currentHeight () {
      let clientHeight = `${document.documentElement.clientHeight}`
      if (clientHeight >= 768) {
        this.pageSize = 20
      }
      if (clientHeight >= 1024) {
        this.pageSize = 30
      }
      return clientHeight - 260
    }
  },
  methods: {
    reSetData () {
      this.copyFullData = this.fullData
      this.searchValue = null
      this.genreSelected = []
      this.genreFilterFullData = []
    },
    onChangeGenre (value, selectedData) {
      if (selectedData.length < 1) return
      this.genreFilterFullData = []
      this.searchValue = null
      this.copyFullData = [...this.fullData]
      let label = selectedData[selectedData.length - 1].label
      for (let index in this.copyFullData) {
        if (this.copyFullData[index].genre.indexOf(label) >= 0) {
          this.genreFilterFullData.push(this.copyFullData[index])
        }
      }
      this.copyFullData = this.genreFilterFullData
      this.current = 1
    },
    searchSubmit () {
      if (!this.searchValue && this.genreSelected.length < 1) {
        this.copyFullData = [...this.fullData]
        return
      }
      if (this.genreSelected.length < 1) {
        this.copyFullData = [...this.fullData]
      } else {
        this.copyFullData = this.genreFilterFullData
      }
      if (!this.searchValue) return
      let result = []
      for (let index in this.copyFullData) {
        if (this.copyFullData[index].name.indexOf(this.searchValue) >= 0 ||
          this.copyFullData[index].bar_id.indexOf(this.searchValue) >= 0) {
          result.push(this.copyFullData[index])
        }
      }
      this.copyFullData = result // 如果搜索筛选不是第一页，进行的时候。
      this.current = 1 // 搜索后数据改变了，理当显示第一页。 页面导航Tab自定义组件显示会自动跳转到第一页，但实际数据却可能为空
      // 如果不设置当前页为第一页，默认显示的是搜索之前的页面。从而入坑：显示的是第一页，实际数据却不是
    },
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
      this.$refs.child.modalChangeNotice()
    },
    // 双击修改当前行的值
    editGood (row, index) {
      this.editIndex = index
      this.modalData.openModal = true
      this.modalData.changeType = 'edit'
      this.modalData.form = Object.assign({}, row) // 把当前行的数据赋值给管道变量
      this.$refs.child.modalChangeNotice() // 访问子组件方法，告知编辑点击事件
    },
    deleteGood () {
      if (this.deleteLoading) return
      this.deleteLoading = true
      const list = {'del_list': this.selected}
      ajaxGet(config.deleteGoodUrl, list).then((res) => {
        this.selected = null
        if (res.data.stat === 'success') {
          this.$Message.success(res.data.msg)
        } else {
          this.$Message.error(res.data.msg)
        }
        this.fullData = res.data.data // 如果失败，返回信息，并赋予最新的值
        this.copyFullData = [...this.fullData]
        this.deleteLoading = false
      })
    },
    // 当多选框开启的时候，选择某项触发
    handleSelect (selection) {
      this.selected = selection
      this.selectCount = selection.length
      if (selection.length === 0) {
        this.selected = null
      }
    },
    // 处理Modal成功校验后回调的数据
    handleSubmit (data) {
      if (this.modalData.changeType === 'create') { // 新建就push数据
        // this.copyFullData.push(data)
        this.copyFullData = [data].concat(this.copyFullData) // concat把data插入到fullData最前面
        this.fullData = [data].concat(this.fullData)
      } else { // 更新则把新值赋值给当前行
        for (let key in formData) {
          this.cleanData[this.editIndex][key] = data[key] // 索引更改值，所有包括copyFullData，fullData都会被改变
        }
      }
      this.reSetData()
    }
    // getData () {
    //   this.$http.get(config.goodUrl, {withCredentials: true}).then(res => {
    //     if (res.data.stat === 'success') {
    //       this.fullData = res.data.data
    //     } else {
    //       this.$Message.error(res.data.msg)
    //     }
    //   })
    // }
  },
  // 在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.tableLoading = true
    ajaxExamGet(config.goodUrl).then(res => {
      this.tableLoading = false
      let dictData = res.data
      if (dictData.stat === 'success') {
        this.fullData = dictData.data
        this.copyFullData = [...this.fullData]
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
    ajaxGet(config.getGenreUrl).then(res => {
      this.genreList = res.data.data
    })
    Bus.$on('createGood', (barId) => {
      this.modalData.changeType = 'create'
      this.modalData.openModal = true
      this.modalData.form.bar_id = barId
    })
  }
}
</script>
