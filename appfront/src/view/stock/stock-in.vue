<template>
  <div>
    <Row :gutter="8" type="flex" justify="start" align="middle">
      <Col span="1"  type="flex"  justify="center" align="middle">
        <Icon type="md-barcode" size="24"/>
      </Col>
      <Col span="6">
        <Input element-id="scan" v-model="bar_id"  @keydown.enter.native ="scanSubmit" />
      </Col>
      <Col span="1" type="flex" justify="center" align="middle">
        扫码
      </Col>
    </Row>
    <Divider dashed />
    <Table :data="tableData" :columns="columns" height="360"></Table>
    <Modal v-model="openModal" :title="form.name" @on-ok="handleSubmit">
      <Row>
        <Col span="10">
          <Form ref="stockInForm" :model="form" :rules="rules" :label-width="50">
            <FormItem label="数量"  label-for="number" prop="number">
              <Input ref="number" element-id="number"
                     @on-focus="numberOnFocus" @on-blur="onBlurNumber"
                     style="width: 150px; text-align: right;" v-model="form.number" number>
                <Icon type="md-clipboard" size="14" slot="prefix" />
              </Input>
            </FormItem>
            <FormItem label="进价"  label-for="buy_price" prop="buy_price" >
              <Input ref="buy_price" element-id="buy_price"  @on-focus="buyPriceOnFocus"
                     @on-blur="onBlurBuyPrice"
                     style="width: 150px; text-align: center;" v-model="form.buy_price">
                <Icon type="logo-yen" size="12" slot="prefix" />
              </Input>
            </FormItem>
          </Form>
        </Col>
        <Col span="1" style="height: 240px">
          <Divider type="vertical" style="height: 240px"/></Col>
        <Col span="13">
          <Row style="height: 60px" >
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
              <Button style="height: 60px; width: 100%" @click="clickOnNumber('')"><Icon type="md-arrow-back" /></Button>
            </Col>
          </Row>
        </Col>
      </Row>
      <div slot="footer">
        <Button type="text" size="large" @click="closeTheModal">取消</Button>
        <Button type="primary" size="large"
                @click="handleSubmit" :loading="loading">确定</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
import {ajaxGet} from '../../api/user'
import config from '../../config'
import {isNumber} from '../../libs/tools'

export default {
  data () {
    return {
      openModal: false,
      bar_id: null,
      loading: false,
      tableData: [],
      currentInputId: 'number',
      blurOnClickNumber: false,
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
        number: 0,
        buy_price: 0,
        name: '未知商品'
      },
      rules: {
        number: [ {required: true, message: '请输入数量'},
          {type: 'number', message: '输入正确的数字', trigger: 'change'},
          {validator (rule, value, callback) {
            let errors = []
            if (value < 1 || String(value).indexOf('.') !== -1 || value > 99999999) { callback('数量输入有误') }
            callback(errors)
          }}
        ],
        buy_price: [{required: true, message: '请输入价格'},
          {validator (rule, value, callback) {
            let errors = []
            if ((parseInt(value) < 0) || isNaN(value) === true || parseInt(value) > 9999999999) { callback('价格输入有误') }
            callback(errors)
          }}
        ]
      }
    }
  },
  methods: {
    closeTheModal () {
      this.openModal = false
    },
    numberOnFocus () {
      this.currentInputId = 'number'
    },
    buyPriceOnFocus () {
      this.currentInputId = 'buy_price'
    },
    onBlurNumber () {
      setTimeout(() => { // 如何失焦不是因为点击了价格输入框, 那就继续聚焦自身
        if (this.currentInputId !== 'buy_price') {
          this.$refs.number.focus()
        }
      })
    },
    onBlurBuyPrice () {
      setTimeout(() => { // 如果失焦不是因为点击了数量输入框, 那就继续聚焦到自身
        if (this.currentInputId !== 'number') {
          this.$refs.buy_price.focus()
        }
      })
    },
    clickOnNumber (value) {
      if (this.currentInputId === '') return
      // this.blurOnClickNumber = true
      if (this.currentInputId === 'number') { // 数量输入规则
        var elInput = document.getElementById('number')
        if (value === '.') { // 不允许输入'.'
          elInput.focus()
          return
        }
        if (value === '0' && elInput.selectionStart === 0) {
          elInput.focus()
          return
        }
      } else { // 价格输入规则
        elInput = document.getElementById('buy_price')
        if (value === '.') {
          if (elInput.value.indexOf('.') !== -1 || elInput.selectionStart === 0) {
            elInput.focus()
            return
          }
        }
        // 当value的第一个值为'0'，在第二位输入，且输入的不是'.'  则退出
        if (elInput.value.substring(0, 1) === '0' && elInput.selectionStart === 1) {
          if (value !== '.' && value !== '') { // 当第二位按下退格的情况
            elInput.focus()
            return
          }
        }
      }
      let startPos = elInput.selectionStart
      let endPos = elInput.selectionEnd
      let txt = elInput.value
      let setPos = startPos + txt.length
      let result = ''
      if (value === '') { // 当输入退格键
        if (startPos !== endPos) {
          result = txt.substring(0, startPos) + txt.substring(endPos)
          setPos = startPos
        } else {
          result = txt.substring(0, startPos - 1) + txt.substring(endPos)
          setPos = startPos + value.length - 1
        }
      } else {
        result = txt.substring(0, startPos) + value + txt.substring(endPos)
        setPos = startPos + value.length
      }
      if (this.currentInputId === 'number') {
        if (!result) {
          setPos = 1
          result = 1
        }
        this.form.number = parseInt(result)
      } else {
        if (!result) {
          result = ''
        }
        this.form.buy_price = result
      }
      // elInput.value = parseInt(result) // 普通input可以使用这行，InputNumber要双向绑定才行
      // 此处需要等待赋值给input完成后，再执行光标定位，不然不成功
      this.$nextTick(() => { // 此处用setTimeOut也可以
        elInput.selectionStart = setPos
        elInput.selectionEnd = setPos
        elInput.focus()
      })
    },
    scanSubmit () {
      ajaxGet(config.scanSearch, this.bar_id).then(res => {
        if (res.data.stat === 'success') {
          this.openModal = true
          this.form = Object.assign({}, res.data.data)
          var elInput = document.getElementById('number')
          setTimeout(() => {
            elInput.selectionStart = 0
            elInput.selectionEnd = 1
            elInput.focus()
          })
        } else {
        }
      })
    },
    handleSubmit () {
      this.$refs.stockInForm.validate((valid) => {
        if (valid) {
          this.tableData.push(this.form)
        }
        this.openModal = false
      })
    }
  },
  mounted () {
    this.$nextTick(() => { // 扫码框自动聚焦
      var elInput = document.getElementById('scan')
      elInput.focus()
    })
  }
}
</script>
