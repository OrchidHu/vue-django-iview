<template>
  <div>
    <Row :gutter="8" type="flex" justify="start" align="middle">
      <Col span="1"  type="flex"  justify="center" align="middle">
        <Icon type="md-barcode" size="24"/>
      </Col>
      <Col span="6">
        <Input v-model="bar_id"  @keydown.native.enter.prevent ="scanSubmit" />
      </Col>
      <Col span="1" type="flex" justify="center" align="middle">
         扫码
      </Col>
    </Row>
    <Divider dashed />
    <Table :data="table_data" :columns="columns" height="360"></Table>
    <Modal v-model="openModal" :title="form.name">
      <Row>
        <Col span="10">
          <Form ref="stockInForm" :modal="form" :label-width="50">
            <FormItem label="数量"  label-for="number" prop="number">
              <Input ref="gain" element-id="number" v-model="form.number" />
            </FormItem>
            <FormItem label="进价"  label-for="buy_price" prop="buy_price" >
              <Input element-id="buy_price" v-model="form.buy_price" />
            </FormItem>
          </Form>
        </Col>
        <Col span="1" style="height: 240px">
          <Divider type="vertical" style="height: 240px"/></Col>
        <Col span="13">
          <Row style="height: 60px;" >
            <Col span="8"  type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('1')">1</Button>
            </Col>
            <Col span="8" type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('2')">2</Button>
            </Col>
            <Col span="8"type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('3')">3</Button>
            </Col>
          </Row>
          <Row style="height: 60px;" >
            <Col span="8"  type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('4')">4</Button>
            </Col>
            <Col span="8" type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('5')">5</Button>
            </Col>
            <Col span="8"type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('6')">6</Button>
            </Col>
          </Row>
          <Row style="height: 60px;" >
            <Col span="8"  type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('7')">7</Button>
            </Col>
            <Col span="8" type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('8')">8</Button>
            </Col>
            <Col span="8"type="flex" justify="center"  align="middle" >
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('9')">9</Button>
            </Col>
          </Row>
            <Row style="height: 60px;" >
              <Col span="8"  type="flex" justify="center"  align="middle" >
                <Button style="height: 60px; width: 100%" @click="clickOnNumber('.')">.</Button>
              </Col>
              <Col span="8" type="flex" justify="center"  align="middle" >
                <Button style="height: 60px; width: 100%" @click="clickOnNumber('0')">0</Button>
              </Col>
              <Col span="8"type="flex" justify="center"  align="middle" >
                <Button style="height: 60px; width: 100%" @click="clickOnNumber('space')">退格</Button>
              </Col>
            </Row>
        </Col>
      </Row>
    </Modal>
  </div>
</template>
<script>
import {ajaxGet} from '../../api/user'
import config from '../../config'

export default {
  data () {
    return {
      openModal: true,
      bar_id: null,
      table_data: [],
      value: null,
      columns: [
        {title: '名称', key: 'name'},
        {title: '条码', key: 'bar_id'},
        {title: '单位', key: 'quantify'},
        {title: '进价', key: 'buy_price'},
        {title: '数量', key: 'number'},
        {title: '小计', key: 'subtotal'}
      ],
      form: {
        number: '',
        buy_price: null,
        name: '323'
      }
    }
  },
  computed: {
  },
  methods: {
    clickOnNumber (value) {
      this.$refs.gain.focus()
      if (value === '.') {
        if (this.form.number.indexOf(value) !== -1) {
          return
        }
      }
      this.form.number += value
    },
    scanSubmit () {
      ajaxGet(config.scanSearch, this.bar_id).then(res => {
        if (res.data.stat === 'success') {
          this.openModal = true
        } else {
          alert('商品不存在，是否新建')
        }
      })
    }
  },
  mounted () {
    this.$refs.gain.focus()
  }
}
</script>
