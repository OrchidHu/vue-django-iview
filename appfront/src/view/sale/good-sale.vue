<template>
  <div>
    <Row :gutter="10" >
      <Col :sm="24" :md="10">
        <Input v-if="searchType === 'scan'" ref="scanInput" element-id="scanInput" icon="ios-clock-outline"
               v-model="scanBarId" placeholder="扫码" @keydown.enter.native="scanSubmit"
               @on-click="searchType='search'"
        />
        <div v-if="searchType === 'search'">
          <Row :gutter="4">
            <Col span="21">
              <AutoComplete ref="searchInput" element-id="searchInput" transfer
                            v-model="searchData" placeholder="搜索" @keydown.enter.native="searchSubmit"
                            @on-search="onSearch" @on-select="onSelect" @on-change="onChange">
                <Option v-for="item in searchList" :value="item.bar_id" :key="item.bar_id">
                  <Row type="flex" justify="center" align="middle">
                    <i-col span="18"><Row>{{item.bar_id}}</Row><Row>{{item.name}}</Row></i-col>
                    <i-col span="3"><Row><Icon style="padding-bottom: 2px" type="logo-yen" /><span style="font-size: 12px"> {{item.price}}</span></Row>
                      <Row>/ {{item.quantify}}</Row></i-col>
                  </Row>
                  <Divider style="height: 2px; margin: 1px;" dashed/>
                </Option>
              </AutoComplete>
            </Col>
            <Col span="3">
              <Button long @click="searchType='scan'">扫码</Button>
            </Col>
          </Row>
        </div>
        <div style="height: 10px"> </div>
        <Row>
          <i-col :sm="0" :md="24">
            <Card style="height: 100%; background: #f8f8f9">
              <Row :gutter="16">
                <i-col span="6">
                  <Card shadow title="访问量">
                  </Card>
                </i-col>
                <i-col span="6">
                </i-col>
                <i-col span="6">
                </i-col>
                <i-col span="6">
                </i-col>
              </Row>
            </Card>
          </i-col>
        </Row>
      </Col>
      <i-col :sm="24" :md="14">
        <Table ref="goodTable" height="380" highlight-row @on-current-change="currentChange"
               @on-keydown="upMove" @on-row-click="onRowClick" disabled-hover
               :data="list" :columns="columns"></Table>
        <br>
        <Row type="flex" justify="start" align="middle" :gutter="36" :offset="1">
          <Col span="4">
            <div>数量: {{totalNumber}}</div>
          </Col>
          <Col span="13">
            <div><Icon type="logo-yen" size="12" slot="prefix" />合计:  <span style="font-weight:bold;font-size: 24px; color: red;">{{totalPrice}}</span></div>
          </Col>
          <Col span="3">
            <Button :disabled="this.list.length !== 0 ? false : true" @click="deleteRow">删除</Button>
          </Col>
          <Col span="3">
            <Poptip
              confirm
              title="确定删除所有吗？"
              @on-ok="clearTableData">
              <Button :disabled="this.list.length !== 0 ? false : true">清空</Button>
            </Poptip>
          </Col>
        </Row>
        <br>
        <Button type="success" long :disabled="this.list.length !== 0 ? false : true"
                :loading="loading" @click="handleSubmit">结算</Button>
      </i-col>
    </Row>
    <Modal width="23" v-model="openCreateModal" @on-ok="createGood">商品不存在，是否新建？
    </Modal>
    <change-good :good-form="goodForm" :set-data="setData"
                 @on-good-data="onGoodData" @delete-current-good="deleteRow"></change-good>
    <balance :balance="balance"></balance>
  </div>
</template>
<script>
import {ajaxGet} from '../../api/user'
import config from '../../config'
import Bus from '../bus'
import ChangeGood from './change-good'
import Balance from './balance'

export default {
  name: 'GoodSale',
  components: {
    ChangeGood, Balance
  },
  data () {
    let storeGoodList = localStorage.getItem('good-sale-list')
    let storeHighLight = localStorage.getItem('high-light-index')
    let goodList
    if (storeGoodList) {
      goodList = JSON.parse(storeGoodList)
    } else {
      goodList = []
    }
    if (!storeHighLight) {
      storeHighLight = -1
    }
    console.log(this.scanBarId)
    return {
      searchType: 'scan',
      currentRow: null,
      test: '',
      searchData: '',
      searchList: [],
      loading: false,
      editIndex: -1,
      copyScanBarId: null,
      openChangeModal: false,
      openCreateModal: false,
      scanBarId: null,
      list: goodList,
      highLightIndex: storeHighLight,
      oldLightIndex: -1,
      columns: [
        {type: 'index',
          key: 'index',
          width: 40,
          indexMethod: (row) => {
            return (row._index + 1)
          }
        },
        {title: '条码', key: 'bar_id', minWidth: 108},
        {title: '名称', key: 'name', minWidth: 160},
        {title: '数量', key: 'number', minWidth: 60},
        {title: '单价', key: 'price', minWidth: 80},
        {title: '小计',
          key: 'subtotal',
          minWidth: 80,
          render: (h, {row, index}) => {
            let edit = (row.subtotal).toFixed(2)
            return [h('div', {style: {color: 'tomato', fontWeight: 'bold'}}, edit)]
          }
        }
      ],
      goodForm: {
        number: '',
        name: '',
        price: null
      },
      setData: {
        openModal: false
      },
      balance: {
        openModal: false,
        sumMoney: 0,
        discount: 100
      }
    }
  },
  computed: {
    totalNumber () {
      let totalNumber = 0
      this.list.forEach((value) => {
        totalNumber += value.number
      })
      return totalNumber
    },
    totalPrice () {
      let totalPrice = 0
      this.list.forEach((value) => {
        totalPrice += value.subtotal
      })
      this.balance.sumMoney = totalPrice
      return totalPrice
    }
  },
  methods: {
    onSelect (value) {
      console.log(value, 'select')
    },
    onChange (value) {
      console.log(value, 'change')
      // if (value) {
      //   // this.searchType = 'scan'
      //   // setTimeout(() => {
      //     this.scanBarId = value
      //     this.searchGood()
      //   // }, 50)
      // }
      // setTimeout(() => {
      //   this.searchType = 'search'
      // }, 150)
      // setTimeout(() => {
      //   setTimeout(() => {
      //     // var searchInput = document.getElementById('searchInput')
      //     // this.searchData = ''
      //     // searchInput.focus()
      //   }, 150)
      // })
    },
    },
    onSearch (query) {
      console.log(query, 'search')
      console.log(typeof(query))
      if (query === ' ') return  // 选择后
      if (query !== this.searchData) {
        console.log("已选择")
        this.searchSubmit()
      }
      ajaxGet(config.searchGoodSale, query).then((res) => {
        if (res.data.stat === 'success') {
          // this.searchList = [{'bar_id': 12, 'name': '3', 'price': 23}, {'bar_id': 123, 'name': '3', 'price': 23}]
          this.searchList = res.data.data
          console.log(res.data.data)
        } else {
          this.searchList = []
        }
      })
    },
    currentChange (currentRow) {
      let index = -1
      for (let _index in this.list) {
        index += 1
        if (this.list[_index].bar_id === currentRow.bar_id) {
          index = _index
          break
        }
      }
      this.oldLightIndex = this.highLightIndex
      this.highLightIndex = index
      if (this.list[this.oldLightIndex]) {
        this.list[this.highLightIndex]['_highlight'] = true
        this.list[this.oldLightIndex]['_highlight'] = false
      }
    },
    createGood () {
      this.$router.push({
        name: 'good_page'
      })
      setTimeout(() => {
        Bus.$emit('createGood', this.copyScanBarId)
        Bus.$emit('focusName')
      })
    },
    upMove () {
      if (this.highLightIndex) {
        this.highLightIndex += 1
        this.list[this.highLightIndex]['_highlight'] = true
      }
    },
    onRowClick (row, index) {
      this.editIndex = index
      this.setData.openModal = true
      this.goodForm = Object.assign({}, row)
      var elInput = document.getElementById('number')
      setTimeout(() => {
        elInput.selectionStart = 0
        elInput.selectionEnd = String(this.goodForm.number).length
        elInput.focus()
      })
    },
    onGoodData (value) {
      const data = [...this.list]
      value['subtotal'] = value.number * value.price
      data[this.editIndex] = Object.assign({}, value)
      this.list = data
      this.handleHighLight()
    },
    scanSubmit () {
      this.searchGood()
      this.$refs.scanInput.focus()
    },
    searchSubmit () {
      setTimeout(() => {
        this.scanBarId = this.searchData
        this.searchGood()
      })
      setTimeout(() => {
        this.searchList = []
        this.searchData = ''
        var elInput = document.getElementById('searchInput')
        elInput.focus()
      }, 400)
    },
    searchGood () {
      if (!this.scanBarId) return
      console.log(this.scanBarId, '12bar')
      let isDav = false // 如果列表中有直接累加，如果没有访问后台
      let index = -1
      for (let _index in this.list) {
        index += 1
        if (this.list[_index].bar_id === this.scanBarId) {
          this.list[_index].number += 1
          this.list[_index].subtotal += this.list[_index].price
          isDav = true
          break
        }
      }
      if (isDav === true) {
        this.oldLightIndex = this.highLightIndex
        this.highLightIndex = index
      }
      this.highLightIndex = parseInt(this.highLightIndex) // localStore取出的为str
      this.oldLightIndex = parseInt(this.oldLightIndex)
      this.copyScanBarId = this.scanBarId
      if (isDav === false) {
        ajaxGet(config.scanSaleSearch, this.scanBarId).then(res => {
          if (res.data.stat === 'success') {
            this.list = [res.data.data].concat(this.list)
            this.oldLightIndex = this.highLightIndex
            this.highLightIndex = 0
            if (this.oldLightIndex !== -1 && this.highLightIndex !== -1) {
              this.oldLightIndex += 1
            }
            this.handleHighLight()
          } else {
            this.openCreateModal = true
          }
        })
      } else {
        this.handleHighLight()
      }
    },
    handleHighLight () {
      if (this.highLightIndex !== -1) {
        this.list[this.highLightIndex]['_highlight'] = true
        if (this.highLightIndex !== -1 && this.oldLightIndex !== this.highLightIndex) {
          if (this.list[this.oldLightIndex]) {
            this.list[this.oldLightIndex]['_highlight'] = false
          }
        }
      }
      this.scanBarId = null
      localStorage.setItem('good-sale-list', JSON.stringify(this.list))
      localStorage.setItem('high-light-index', this.highLightIndex)
    },
    deleteRow () {
      if (this.highLightIndex === -1) {
        this.$Message.error('请选择需要删除的数据')
      } else {
        this.list.splice(this.highLightIndex, 1)
        localStorage.setItem('good-sale-list', JSON.stringify(this.list))
        if (this.highLightIndex > this.list.length - 1) {
          this.highLightIndex = this.list.length - 1
        }
        if (this.list[this.highLightIndex]) {
          this.list[this.highLightIndex]['_highlight'] = true
        }
      }
      if (this.list.length === 0) {
        this.highLightIndex = -1
        this.oldLightIndex = -1
      }
      this.$refs.scanInput.focus()
    },
    clearTableData () {
      this.list = []
      localStorage.setItem('good-sale-list', JSON.stringify(this.list))
      this.searchType = 'scan'
      setTimeout(() => {
        this.$refs.scanInput.focus()
      }, 5)
    },
    cancel () {},
    handleSubmit () {
      this.balance.openModal = true
      this.balance.discount = 100
    },
    subtotal (row) {
      return row.number * row.price
    }
  },
  mounted () {
    this.$nextTick(() => { // 扫码框自动聚焦
      var elInput = document.getElementById('scanInput')
      elInput.focus()
    })
  }
}
</script>
<style>
</style>
