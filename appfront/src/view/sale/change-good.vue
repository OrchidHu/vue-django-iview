<template>

  <Modal :title="goodForm.name" v-model="setData.openModal" @on-ok="handleSubmit">
    <Row>
      <i-col span="11">
        <Form :model="goodForm" :label-width="50" :rules="rules">
          <FormItem label="数量"  label-for="bar-id" prop="number" >
            <Input ref="number" element-id="number" v-model="goodForm.number"
                   @on-focus="currentInputId = 'number'" @on-blur="onBlurNumber"/>
          </FormItem>
          <FormItem label="单价" label-for="name" prop="price" >
            <Input ref="price" element-id="price" v-model="goodForm.price"
                   @on-focus="currentInputId = 'price'" @on-blur="onBlurBuyPrice"/>
          </FormItem>
          <FormItem label="小计" label-for="name" prop="price" >
            <Input element-id="name" disabled v-model="subtotal"/>
          </FormItem>
        </Form>
      </i-col>
      <i-col span="1">
        <Divider type="vertical" style="height: 240px"/>
      </i-col>
      <i-col span="12">
        <number-key-board @on-click="clickOnNumber"></number-key-board>
      </i-col>
    </Row>
    <div slot="footer">
      <Row type="flex" justify="start" align="middle">
        <i-col span="3">
          <a style="color: #67647D;" @click="deleteGood"><Icon size="32" type="ios-trash-outline" />删除</a>
        </i-col>
        <i-col span="21">
          <Button type="text" size="large">取消</Button>
          <Button  type="primary" size="large">确定</Button>
        </i-col>
      </Row>
    </div>
  </Modal>
</template>
<script>
import NumberKeyBoard from '@/components/number-key-board'
export default {
  name: 'ChangeGood',
  props: {
    goodForm: {
      type: Object,
      required: true
    },
    setData: {
      openModal: {
        type: Boolean
      }
    }
  },
  components: {
    NumberKeyBoard
  },
  data () {
    return {
      currentInputId: 'number',
      rules: {
        number: [{required: true, message: '请输入数量'}]
      }
    }
  },
  computed: {
    subtotal () {
      return this.goodForm.number * this.goodForm.price
    }
  },
  methods: {
    handleSubmit () {
      this.$emit('on-good-data', this.goodForm)
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
