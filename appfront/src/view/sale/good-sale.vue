<template>
  <div>
    <Row :gutter="10">
      <i-col :sm="24" :md="10">
        <Input ref="scanInput" element-id="scanInput" v-model="scanBarId" search placeholder="扫码 / 搜索"
               @on-search="scanSubmit"
        />
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
      </i-col>
      <i-col :sm="24" :md="14">
        <Table height="380" highlight-row @on-current-change="currentChange"
               @on-keydown="upMove" @on-row-click="onRowClick"
               :data="list" :columns="columns"></Table>
        <br>
        <Row type="flex" justify="start" align="middle" :gutter="36">
          <Col span="4">
            <div>数量: {{totalNumber}}</div>
          </Col>
          <Col span="6">
            <div><Icon type="logo-yen" size="12" slot="prefix" />合计:  <span style="font-weight:bold;font-size: 24px; color: red;">{{totalPrice}}</span></div>
          </Col>
          <Col span="4">
            <Button :disabled="this.list.length !== 0 ? false : true" @click="deleteRow">删除</Button>
          </Col>
          <Col span="4">
            <Poptip
              confirm
              title="确定删除所有吗？"
              @on-ok="clearTableData"
              @on-cancel="cancel">
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
  </div>
</template>
<script>
import {ajaxGet, ajaxPost} from '../../api/user'
import config from '../../config'
import Bus from '../bus'
import ChangeGood from './change-good'
export default {
  name: 'GoodSale',
  components: {
    ChangeGood
  },
  data () {
    let storeGoodList = localStorage.getItem('good-sale-list')
    let goodList
    if (storeGoodList) {
      goodList = JSON.parse(storeGoodList)
    } else {
      goodList = []
    }
    return {
      currentRow: null,
      loading: false,
      editIndex: -1,
      copyScanBarId: null,
      openChangeModal: false,
      openCreateModal: false,
      scanBarId: null,
      list: goodList,
      highLightIndex: null,
      columns: [
        {type: 'index',
          key: 'index',
          width: 40,
          indexMethod: (row) => {
            return (row._index + 1)
          }
        },
        {title: '条码', key: 'bar_id', minWidth: 108},
        {title: '名称', key: 'name', minWidth: 120},
        {title: '数量', key: 'number', minWidth: 60},
        {title: '单价', key: 'price', minWidth: 80},
        {title: '小计', key: 'subtotal', minWidth: 120}
      ],
      goodForm: {
        number: '',
        name: '',
        price: null
      },
      setData: {
        openModal: false
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
      return totalPrice
    }
  },
  methods: {
    currentChange (currentRow) {
      let index = -1
      for (let _index in this.list) {
        index += 1
        if (this.list[_index].bar_id === currentRow.bar_id) {
          index = _index
          break
        }
      }
      this.highLightIndex = index
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
    },
    scanSubmit () {
      let isDav = false // 如果列表中有直接累加，如果没有访问后台
      // let index = 0
      this.list.forEach((value) => {
        if (value.bar_id === this.scanBarId) {
          value.number += 1
          value.subtotal += value.price
          isDav = true
          return
        }
        // index += 1
      })
      // this.list[index]['_highlight'] = true
      this.copyScanBarId = this.scanBarId
      if (isDav === false) {
        ajaxGet(config.scanSaleSearch, this.scanBarId).then(res => {
          if (res.data.stat === 'success') {
            this.list = [res.data.data].concat(this.list)
          } else {
            this.openCreateModal = true
          }
        })
      }
      this.scanBarId = null
      localStorage.setItem('good-sale-list', JSON.stringify(this.list))
      this.$refs.scanInput.focus()
    },
    deleteRow () {
      if (!this.highLightIndex) {
        this.$Message.error('请选择需要删除的数据')
      } else {
        this.list.splice(this.highLightIndex, 1)
        localStorage.setItem('good-sale-list', JSON.stringify(this.list))
        if (this.list[this.highLightIndex]) {
          this.list[this.highLightIndex]['_highlight'] = true
        }
      }
    },
    clearTableData () {},
    cancel () {},
    handleSubmit () {},
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
