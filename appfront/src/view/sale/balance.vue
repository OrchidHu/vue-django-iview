<template>

  <Modal title="结算" v-model="balance.openModal">
    <Row>
      <i-col span="11">
        <Form ref="balanceForm" :model="balance" :label-width="60" :rules="rules">
          <FormItem label="折扣优惠" label-for="discount" prop="discount" >
            <InputNumber :min="0" number style="width: 55px" ref="discount" element-id="discount" v-model="balance.discount" /> %
          </FormItem>
          <FormItem label="折后金额"  label-for="sum-money" prop="sumMoney" >
            <Input readonly ref="sumMoney" element-id="sum-money" :value="discountMoney" />
          </FormItem>
          <FormItem label="实收金额">
            <Input v-model="arrange"/>
          </FormItem>
          <FormItem label="找零">
            <Input readonly v-model="oddChange"/>
          </FormItem>
        </Form>
      </i-col>
      <i-col span="1">
        <Divider type="vertical" style="height: 240px"/>
      </i-col>
      <i-col span="12">
        <!--<number-key-board @on-click="clickOnNumber"></number-key-board>-->
        <Icon size="240" type="md-cart" />
      </i-col>
    </Row>
    <div slot="footer">
      <Row type="flex" justify="start" align="middle">
        <i-col span="3">
          <a style="color: #67647D;" @click="deleteGood"><Icon size="32" type="ios-trash-outline" />删除</a>
        </i-col>
        <i-col span="21">
          <Button type="text" size="large" @click="cancle">取消</Button>
          <Button  type="primary" size="large" @click="handleSubmit">修改</Button>
        </i-col>
      </Row>
    </div>
  </Modal>
</template>
<script>
import NumberKeyBoard from '@/components/number-key-board'
export default {
  name: 'Balance',
  props: {
    balance: {
      type: Object,
      required: true
    }
  },
  components: {
    NumberKeyBoard
  },
  data () {
    return {
      currentInputId: 'number',
      arrange: parseFloat((this.balance.discount * this.balance.sumMoney / 100).toFixed(2)),
      rules: {
        number: [ {required: true, message: '请输入数量'},
          {type: 'number', message: '输入正确的数字'},
          {validator (rule, value, callback) {
            let errors = []
            if (value < 1 || String(value).indexOf('.') !== -1 || value > 99999999) { callback('数量输入有误') }
            callback(errors)
          }}
        ],
        price: [{required: true, message: '请输入价格'},
          {validator (rule, value, callback) {
            let errors = []
            if ((parseInt(value) < 0 || isNaN(parseInt(value))) || isNaN(value) === true || parseInt(value) > 9999999999) { callback('价格输入有误') }
            callback(errors)
          }}
        ]
      }
    }
  },
  computed: {
    discountMoney () {
      return parseFloat((this.balance.discount * this.balance.sumMoney / 100).toFixed(2))
    },
    // arrange () {
    //   return this.discountMoney
    // },
    oddChange () {
      let arrangeMoney = this.arrange
      let discMoney = this.discountMoney
      if (arrangeMoney < discMoney) return 0
      return (arrangeMoney - discMoney).toFixed(1)
    }
  },
  methods: {
    handleSubmit () {
      this.$refs.goodSaleForm.validate((valid) => {
        if (valid) {
          this.$emit('on-good-data', this.goodForm)
          this.setData.openModal = false
        }
      })
    },
    cancle () {
      this.setData.openModal = false
    },
    onBlurNumber () {
      setTimeout(() => { // 如何失焦不是因为点击了价格输入框, 那就继续聚焦自身
        if (this.currentInputId !== 'price' && this.setData.openModal === true) {
          this.$refs.number.focus()
        }
      })
    },
    onBlurBuyPrice () {
      setTimeout(() => { // 如果失焦不是因为点击了数量输入框, 那就继续聚焦到自身
        if (this.currentInputId !== 'number' && this.setData.openModal === true) {
          this.$refs.price.focus()
        }
      })
    },
    deleteGood () {
      this.setData.openModal = false
      this.$emit('delete-current-good')
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
        elInput = document.getElementById('price')
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
        this.goodForm.number = parseInt(result)
      } else {
        if (!result) {
          result = ''
        }
        this.goodForm.price = result
      }
      // elInput.value = parseInt(result) // 普通input可以使用这行，InputNumber要双向绑定才行
      // 此处需要等待赋值给input完成后，再执行光标定位，不然不成功
      this.$nextTick(() => { // 此处用setTimeOut也可以
        elInput.selectionStart = setPos
        elInput.selectionEnd = setPos
        elInput.focus()
      })
    }
  }
}
</script>
