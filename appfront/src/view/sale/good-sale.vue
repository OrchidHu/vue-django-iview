<template>
  <div>
    <Row :gutter="10">
      <i-col :sm="24" :md="10">
        <Input ref="scanInput" element-id="scanInput" v-model="scanBarId" search placeholder="扫码 / 搜索" @keydown.enter.native ="scanSubmit"/>
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
        <Table height="380" highlight-row :data="list" :columns="columns"></Table>
        <br>
        <Row type="flex" justify="center" align="middle" :gutter="36">
          <Col span="4">
            <div>{{totalNumber}}</div>
            <div>数量</div>
          </Col>
          <Col span="4" >
            <div><Icon type="logo-yen" size="12" slot="prefix" />  {{totalPrice}}</div>
            <div>合计</div>
          </Col>
          <Col span="3">
            <Button :disabled="this.list.length !== 0 ? false : true">删除</Button>
          </Col>
          <Col span="2">
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
  </div>
</template>
<script>
import {ajaxGet, ajaxPost} from '../../api/user'
import config from '../../config'
import NumberKeyBoard from '@/components/number-key-board'
// var elInput = document.getElementById('scanInput')
export default {
  data () {
    return {
      loading: false,
      scanBarId: null,
      list: [],
      columns: [
        {type: 'index', width: 40},
        {title: '条码', key: 'bar_id', minWidth: 108},
        {title: '名称', key: 'name', minWidth: 120},
        {title: '数量', key: 'number', minWidth: 60},
        {title: '单价', key: 'price', minWidth: 80},
        {title: '小计', key: 'subtotal', minWidth: 120}
      ]
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
    scanSubmit () {
      let isDav = false // 如果列表中有直接累加，如果没有访问后台
      this.list.forEach((value) => {
        if (value.bar_id === this.scanBarId) {
          value.number += 1
          value.subtotal += value.price
          isDav = true
        }
      })
      if (isDav === false) {
        ajaxGet(config.scanSaleSearch, this.scanBarId).then(res => {
          if (res.data.stat === 'success') {
            this.list = [res.data.data].concat(this.list)
          } else {
            alert("meiy")
          }
        })
      }
      this.scanBarId = null
      this.$refs.scanInput.focus()
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
  .demo-split{
    height: 500px;
    border: 1px solid #ff4d;
  }
  .demo-split-pane{
    padding: 10px;
  }
</style>
