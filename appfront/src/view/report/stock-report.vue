<template>
  <div>
    <Row style="height: 48px" type="flex" justify="start" align="middle" :gutter="4">
      <Col :sm='6' :md="3">
        <Cascader :data="shopList" :disabled="identity==='manager'? true : false" filterable
                  v-model="shopSelect" @on-change="onChangeShop" placeholder="选择门店"></Cascader>
      </Col>
      <Col :sm="8" :md="4">
        <Cascader :data="genreList" filterable v-model="genreSelect" @on-change="onChangeGenre"
                  placeholder="选择类别"></Cascader>
      </Col>
      <Col :sm="7" :md="5">
        <Input v-model="submitData.searchValue"  @keydown.enter.native="searchSubmit"
               earch placeholder="条码 / 名称"/>
      </Col>
      <Col :sm="1" :md="2">
        <Button @click="searchSubmit" style="background: #2d8cf0; color: white">搜 索</Button>
      </Col>
    </Row>
    <Table
      show-header
      size="small"
      :height="390"
      :data="tableData"
      :columns="columns"></Table>
  </div>
</template>
<script>
import {ajaxExamGet, ajaxPost, ajaxGet} from '@/api/user'
import config from '@/config'

export default {
  name: 'StockReport',
  data () {
    return {
      tableData: [],
      shopList: [],
      shopSelect: [],
      genreList: [],
      identity: '',
      genreSelect: [''],
      searchLoading: false,
      submitData: {
        searchValue: '',
        shopSelected: [],
        genreSelected: []
      },
      columns: [
        {type: 'index', width: 60},
        {title: '门店', key: 'shop_name'},
        {title: '名称', key: 'good_name'},
        {title: '条码', key: 'bar_id'},
        {title: '数量', key: 'number'},
        {title: '单位', key: 'quantify'},
        {title: '进价', key: 'stock_buy_price'},
        {title: '售价', key: 'stock_sale_price', width: 100}
      ]
    }
  },
  methods: {
    onChangeShop (value) {
      this.submitData.shopSelected = value
      this.searchData()
    },
    onChangeGenre (value) {
      this.submitData.genreSelected = value
      this.searchData()
    },
    searchSubmit () {
      this.searchData()
    },
    searchData () {
      if (this.searchLoading) return
      this.searchLoading = true
      ajaxPost(config.searchStockReport, this.submitData).then((res) => {
        if (res.data.stat === 'success') {
          this.tableData = res.data.data
        }
      })
      this.searchLoading = false
    }
  },
  mounted () {
    ajaxExamGet(config.getShopList).then((res) => {
      if (res.data.stat === 'success') {
        this.shopList = res.data.data['shop_data']
        this.shopSelect = res.data.data['user_data']
        this.identity = res.data.data['identity']
      }
    })
    ajaxGet(config.getGenreUrl).then(res => {
      this.genreList = res.data.data
      this.genreList = [{'value': '', 'label': '全部'}].concat(this.genreList)
    })
    setTimeout(() => {
      this.submitData.shopSelected = this.shopSelect
      this.searchData()
    }, 200)
  }
}
</script>
