<template>
  <div>
    <Row :gutter="8" type="flex" justify="start" align="middle">
      <Col span="1"  type="flex"  justify="center" align="middle">
        <Icon type="md-barcode" size="24"/>
      </Col>
      <Col span="6">
        <Input ref="scan" element-id="scan" v-model="scanBarId"  @keydown.enter.native ="scanSubmit"/>
      </Col>
      <Col span="1" type="flex" justify="center" align="middle">
        扫码
      </Col>
    </Row>
    <br>
    <!--<Divider dashed />-->
    <Table :data="tableData" :columns="columns" border height="360"></Table>
    <br/>
    <Row :gutter="8" type="flex" justify="start" align="middle">
      <Col span="2" type="flex"  justify="center" align="middle">
        <div>{{goodCount}}</div>
        <div>款数</div>
      </Col>
      <Col span="2" type="flex"  justify="center" align="middle">
        <div>{{totalNumber}}</div>
        <div>数量合计</div>
      </Col>
      <Col span="2" type="flex"  justify="center" align="middle">
        <div><Icon type="logo-yen" size="12" slot="prefix" />  {{totalPrice}}</div>
        <div>价格合计</div>
      </Col>
      <Col span="1" offset="14">
        <Poptip
          confirm
          title="确定删除所有吗？"
          @on-ok="clearTableData"
          @on-cancel="cancel">
          <Button :disabled="this.tableData.length !== 0 ? false : true">清空</Button>
        </Poptip>
      </Col>
      <Col span="1" offset="1">
        <Button type="success" :disabled="this.tableData.length !== 0 ? false : true"
                :loading="loading" @click="handleSubmitToSave">提交</Button>
      </Col>
    </Row>
    <Modal v-model="openModal" :title="form.name" @on-ok="handleSubmit">
      <Row>
        <Col span="10">
          <Form ref="stockInForm" :model="form" :rules="rules" :label-width="50">
            <FormItem label="数量"  label-for="number" prop="number">
              <Input ref="number" element-id="number"
                     @on-focus="currentInputId = 'number'" @on-blur="onBlurNumber"
                     style="width: 150px; text-align: right;" v-model="form.number" number>
                <Icon type="md-clipboard" size="14" slot="prefix" />
              </Input>
            </FormItem>
            <FormItem label="进价"  label-for="buy_price" prop="buy_price" >
              <Input ref="buy_price" element-id="buy_price"
                     @on-focus="currentInputId = 'buy_price'" @on-blur="onBlurBuyPrice"
                     style="width: 150px; text-align: center;" v-model="form.buy_price">
                <Icon type="logo-yen" size="12" slot="prefix" />
              </Input>
            </FormItem>
          </Form>
        </Col>
        <Col span="1" style="height: 240px">
          <Divider type="vertical" style="height: 240px"/></Col>
        <Col span="13">
          <numberKeyBoard @on-click="clickOnNumber"></numberKeyBoard>
        </Col>
      </Row>
      <div slot="close" @click="closeTheModal"><Icon type="ios-close" /></div>
      <div slot="footer">
        <Button type="text" size="large" @click="closeTheModal">取消</Button>
        <Button type="primary" size="large" @keydown.enter.native="handleSubmit"
                @click="handleSubmit" :loading="loading">确定</Button>
      </div>
    </Modal>
  </div>
</template>
<script>
import {ajaxGet, ajaxPost} from '../../api/user'
import config from '../../config'
import NumberKeyBoard from '@/components/number-key-board'

export default {
  name: 'Stock',
  components: {
    NumberKeyBoard
  },
  props: {
    stockGenre: Number,
    stockName: String
  },
  data () {
    const storeTableData = localStorage.getItem(`${this.stockName}-table-data`)
    let tableData
    if (storeTableData) {
      tableData = JSON.parse(storeTableData)
    } else {
      tableData = []
    }
    return {
      editIndex: -1,
      openModal: false,
      scanBarId: null,
      loading: false,
      tableData: tableData,
      copyData: [],
      currentInputId: 'number',
      blurOnClickNumber: false,
      value: null,
      editBuyPrice: null,
      editNumber: null,
      columns: [
        {type: 'index', width: 60},
        {title: '名称', key: 'name'},
        {title: '条码', key: 'bar_id'},
        {title: '单位', key: 'quantify'},
        {
          title: '类型',
          key: 'stock_genre',
          render: (h) => {
            return h('span', [this.stockGenre === 1 ? '入库' : '出库'])
          }
        },
        {
          title: '进价',
          key: 'buy_price',
          render: (h, {row, index}) => {
            let edit
            if (this.editIndex === index) {
              edit = [h('InputNumber', {
                props: {
                  value: row.buy_price
                },
                on: {
                  input: (val) => {
                    this.editBuyPrice = val
                  }
                }
              })]
            } else {
              edit = row.buy_price
            }
            return h('div', [edit])
          }
        },
        {
          title: '数量',
          key: 'number',
          render: (h, {row, index}) => {
            let edit
            if (this.editIndex === index) {
              edit = [h('InputNumber', {
                props: {
                  value: row.number
                },
                on: {
                  input: (val) => {
                    this.editNumber = val
                  }
                }
              })]
            } else {
              edit = row.number
            }
            return h('div', [edit])
          }
        },
        {
          title: '小计',
          key: 'subtotal',
          render: (h, {row, index}) => {
            let edit
            edit = (row.number * row.buy_price).toFixed(2)
            return h('div', [edit])
          }
        },
        {
          title: '操作',
          render: (h, {row, index}) => {
            if (this.editIndex === index) {
              return [
                h('Button', {
                  props: {
                    type: 'success'
                  },
                  on: {
                    click: () => {
                      if (this.editNumber < 1) {
                        this.$Message.error('数量不能小于1')
                      } else if (this.editBuyPrice < 0) {
                        this.$Message.error('价格不能小于0')
                      } else {
                        this.tableData[index].buy_price = this.editBuyPrice
                        this.tableData[index].number = parseInt(this.editNumber)
                        this.editIndex = -1
                      }
                    }
                  }
                }, '保存'),
                h('Button', {
                  style: {
                    marginLeft: '6px'
                  },
                  on: {
                    click: () => {
                      this.editIndex = -1
                    }
                  }
                }, '取消')
              ]
            } else {
              return [h('Button', {
                on: {
                  click: () => {
                    this.editBuyPrice = row.buy_price
                    this.editNumber = row.number
                    this.editIndex = index
                  }
                }
              }, '修改'),
              h('Button', {
                style: {
                  marginLeft: '6px',
                  background: 'tomato',
                  color: 'white'
                },
                on: {
                  click: () => {
                    this.remove(index)
                  }
                }
              }, '删除')
              ]
            }
          },
          width: 160
        }
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
  computed: {
    goodCount () {
      return this.tableData.length
    },
    totalNumber () {
      let totalNumber = 0
      this.tableData.forEach(function (value, index, array) {
        totalNumber += value.number
      })
      return totalNumber
    },
    totalPrice () {
      let totalPrice = 0
      this.tableData.forEach(function (value, index, array) {
        totalPrice += value.buy_price * value.number
      })
      return totalPrice
    }
  },
  methods: {
    closeTheModal () {
      this.openModal = false
      this.scanBarId = null
      this.$refs.scan.focus()
    },
    clearTableData () {
      this.tableData = []
      localStorage.setItem(`${this.stockName}-table-data`, JSON.stringify(this.tableData))
    },
    cancel () {
      // this.$Message.info('取消删除')
    },
    remove (index) {
      this.tableData.splice(index, 1)
      localStorage.setItem(`${this.stockName}-table-data`, JSON.stringify(this.tableData))
    },
    onBlurNumber () {
      setTimeout(() => { // 如何失焦不是因为点击了价格输入框, 那就继续聚焦自身
        if (this.currentInputId !== 'buy_price' && this.openModal === true) {
          this.$refs.number.focus()
        }
      })
    },
    onBlurBuyPrice () {
      setTimeout(() => { // 如果失焦不是因为点击了数量输入框, 那就继续聚焦到自身
        if (this.currentInputId !== 'number' && this.openModal === true) {
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
      ajaxGet(config.scanStockSearch, this.scanBarId).then(res => {
        if (res.data.stat === 'success') {
          this.openModal = true
          this.form = Object.assign({'stock_genre': this.stockGenre}, res.data.data)
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
          this.tableData.push(Object.assign({}, this.form))
          localStorage.setItem(`${this.stockName}-table-data`, JSON.stringify(this.tableData))
          this.scanBarId = null
          this.$refs.scan.focus()
        }
        this.openModal = false
      })
    },
    handleSubmitToSave () {
      if (this.loading) return
      this.loading = true
      let submitData = {'list': this.tableData, 'total_price': this.totalPrice, 'stock_genre': this.stockGenre}
      ajaxPost(config.saveStockGood, submitData).then(res => {
        if (res.data.stat === 'success') {
          this.$Message.success(res.data.msg)
          this.tableData = []
        } else {
          this.$Message.error(res.data.msg)
        }
        this.loading = false
      })
    }
  },
  mounted () {
    this.$nextTick(() => { // 扫码框自动聚焦
      var elInput = document.getElementById('scan')
      elInput.focus()
    })
  },
  beforeDestroy () {
    localStorage.setItem(`${this.stockName}-table-data`, JSON.stringify(this.tableData))
  }
}
</script>
