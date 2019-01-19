<template>
  <div>
    <Row :gutter="10">
      <Col :sm="24" :md="8">
        <Input placeholder="订单流水号" search @keydown.enter.native="handleSubmit"/>
      </Col>
      <Col :sm="24" :md="16">
        <Row :gutter="10">
          <Col span="4">
            <Tooltip :disabled="identity==='manager'? true : false" content="选择门店" placement="top" transfer>
              <Cascader :data="shopList" :disabled="identity==='manager'? true : false" filterable
                        v-model="shopSelected" @on-change="onChangeShop" placeholder="选择门店"></Cascader>
            </Tooltip>
          </Col>
          <Col span="3">
            <Tooltip content="选择操作员工" placement="top" transfer>
              <Cascader :data="personList" v-model="personSelected" @on-change="onChangePerson"></Cascader>
            </Tooltip>
          </Col>
          <Col span="17">
            <Tooltip content="选择起始时间" placement="top" transfer>
              <DatePicker v-model="startTime" type="datetime" placeholder="请选择起始时间"
                          style="width: 200px" @on-change="onChange" @on-ok="onOkSelectTime" @on-open-change="onOpenChange"></DatePicker>
            </Tooltip>
            -
            <Tooltip content="选择结束时间" placement="top" transfer>
              <DatePicker v-model="endTime" type="datetime" placeholder="请选择结束时间"
                          style="width: 200px" @on-change="onChange" @on-ok="onOkSelectTime" @on-open-change="onOpenChange"></DatePicker>
            </Tooltip>
          </Col>
        </Row>
      </Col>
    </Row>
    <div style="height: 10px"></div>
    <Card>
      <Collapse simple accordion @on-change="onChangeCollapse">
        <Panel :key="order.serial_number" v-for="order in orderList">
          {{order.create_time}} &#8195 {{order.serial_number}}({{order.text}}) <span style="float: right; padding-right: 40px">¥{{order.discount_price}}</span>
          <Card slot="content">
            <Row type="flex" style="background: darkturquoise; color: white; height: 60px; font-size: 16px" justify="center" align="middle">
              <Col span="24" style="text-align: center"> 实收 </Col>
              <Col span="24" style="text-align: center; font-size: 20px"> ¥{{order.discount_price}} </Col>
            </Row>
            <br>
            <div v-for="detail in orderDetails">
              <Row type="flex" justify="center" align="middle" style="height: 28px">
                <i-col span="10" style="text-align: center; font-size: 14px">{{detail.name}}</i-col>
                <i-col span="4" style="text-align: center; font-size: 14px">x{{detail.number}}</i-col>
                <i-col span="10" style="text-align: center; font-size: 14px">¥{{detail.sale_price.toFixed(2)}}</i-col>
              </Row>
            </div>
            <Divider/>
            <Row>
              <i-col span="18" offset="2">
                <p >订单号：{{order.serial_number}}</p>
                <p >操作日期：{{order.detail_create_time}}</p>
                <p >操作人： {{order.operator}}</p>
              </i-col>
              <i-col span="4">
                <Button>退货</Button>
              </i-col>
            </Row>
          </Card>
        </Panel>
      </Collapse>
    </Card>
    <div style="height: 10px"></div>
  </div>
</template>
<script>
  import {ajaxExamGet, ajaxGet, ajaxPost} from '../../api/user'
import config from '@/config'
export default {
  data () {
    const time1 = new Date()
    console.log(time1)
    return {
      nameString: '1',
      orderList: [],
      orderDetails: [],
      personList: [],
      shopList: [],
      identity: false,
      personSelected: [-1],
      shopSelected: [-1],
      startTime: time1.toLocaleDateString() + '00-00-00',
      endTime: time1.toLocaleDateString() + '23-59-59'
    }
  },
  computed: {
  },
  methods: {

    onChangeShop (value) {
      this.shopSelected = value
      this.searchData()
      console.log('mend')
    },
    handleSubmit () {
      alert()
    },
    onOkSelectTime () {
      if (this.startTime > this.endTime) {
        this.$Message.error('选择有误')
      } else {
        this.searchData()
      }
    },
    onChange () {
      if (this.startTime > this.endTime) {
        this.$Message.error('选择有误')
      }
    },
    onChangePerson (value) {
      this.personSelected = value
      this.searchData()
    },
    onChangeCollapse (key) {
      console.log(key)
      if (key.length) {
        let value = this.orderList[key[0]].serial_number
        ajaxGet(config.getOrderDetail, value).then((res) => {
          if (res.data.stat === 'success') {
            this.orderDetails = res.data.data
          }
        })
      }
    },
    onOpenChange () {
      if (this.startTime > this.endTime) {
        let time = new Date()
        this.startTime = time.toLocaleDateString() + '00-00-00'
        this.endTime = time.toLocaleDateString() + '23-59-59'
      }
    },
    searchData () {
      console.log(this.startTime)
      let searchParams = {
        person_id: this.personSelected,
        shop_id: this.shopSelected,
        start_time: this.startTime,
        end_time: this.endTime
      }
      ajaxPost(config.getOrderList, searchParams).then((res) => {
        if (res.data.stat === 'success') {
          this.orderList = res.data.data
          console.log(this.orderList)
        }
      })
    }
  },
  mounted () {
    ajaxExamGet(config.getPersonList).then((res) => {
      if (res.data.stat === 'success') {
        this.personList = res.data.data
        console.log(this.personList)
      }
    })
    ajaxExamGet(config.getShopList).then((res) => {
      if (res.data.stat === 'success') {
        this.shopList = res.data.data['shop_data']
        this.shopSelected = res.data.data['user_data']
        this.identity = res.data.data['identity']
        console.log(this.shopSelected, '11111111')
      }
    })
    setTimeout(() => {
      this.searchData()
    }, 250)
  }
}
</script>
<style>

</style>
