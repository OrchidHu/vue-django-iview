<template>
  <Modal :title="modalData.changeType==='create'?'新增商品': '编辑商品'"
         v-model="modalData.openModal">
    <Form ref="goodForm" :model="modalData.form" :rules="rules" :label-width="50"
          @keydown.enter.native="handleSubmitToSave">
      <FormItem label="条码"  label-for="bar-id" prop="bar_id" >
        <Input element-id="bar-id" v-model="modalData.form.bar_id"/>
      </FormItem>
      <FormItem label="名称" label-for="name" prop="name" >
        <Input element-id="name" v-model="modalData.form.name"/>
      </FormItem>
      <FormItem label="类别" prop="genre">
        <Input v-model="modalData.form.genre"/>
      </FormItem>
      <FormItem label="进价" prop="buy_price">
        <Input v-model="modalData.form.buy_price" number/>
      </FormItem>
      <FormItem label="售价" prop="sale_price">
        <Input v-model="modalData.form.sale_price" number/>
      </FormItem>
      <FormItem label="供应商" prop="supplier">
        <Input v-model="modalData.form.supplier"/>
      </FormItem>
    </Form>
    <div slot="close" @click="closeTheModal"><Icon type="ios-close" /></div>
    <div slot="footer">
      <Button type="text" size="large" @click="closeTheModal">取消</Button>
      <Button v-if="modalData.changeType==='create'" type="primary" size="large" @click="handleSubmitToCreate">确定</Button>
      <Button v-if="modalData.changeType==='edit'" type="primary" size="large" @click="handleSubmitToSave">保存</Button>
    </div>
  </Modal>
</template>
<script>

import config from '@/config'
import {ajaxGet} from '@/api/user'
export default {
  name: 'GoodModal',
  props: {
    modalData: {
      type: Object,
      required: true,
      default: () => {
        return {
        }
      }
    },
    barIdRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '条码不能为空'},
          {validator (rule, value, callback) {
            var errors = []
            if (!/^[0-9]+$/.test(value)) {
              callback('条码必须为数字值')
            }
            callback(errors)
          }}
        ]
      }
    },
    nameRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '名称不能为空', trigger: 'change'}
        ]
      }
    },
    genreRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '类型不能为空', trigger: 'change'}
        ]
      }
    },
    buyPriceRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '进价不能为空'},
          {type: 'number', message: '输入正确的数字', trigger: 'change'}
        ]
      }
    },
    salePriceRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '售价不能为空'},
          {type: 'number', message: '请输入正确的数字', trigger: 'change'}
        ]
      }
    },
    supplierRules: {
      type: Array,
      default: () => {
        return [
          {required: true, message: '供应商不能为空', trigger: 'change'}
        ]
      }
    }
  },
  data () {
    return {

    }
  },
  computed: {
    rules () {
      return {
        bar_id: this.barIdRules,
        name: this.nameRules,
        genre: this.genreRules,
        buy_price: this.buyPriceRules,
        sale_price: this.salePriceRules,
        supplier: this.supplierRules
      }
    }
  },
  methods: {
    closeTheModal () { // 为了避免新建和更新共用Modal在校验上存在缓存问题 如:(如关闭更新Modal后打开新建Modal出现"校验红字")
      this.$refs.goodForm.resetFields()
      this.modalData.openModal = false
    },
    handleSubmitToCreate () {
      this.$refs.goodForm.validate((valid) => {
        if (valid) {
          if (this.myValidate()) {
            ajaxGet(config.createGoodUrl, this.modalData.form).then(res => {
              if (res.data.stat === 'success') {
                this.$Message.info('新建成功')
                this.modalData.form.id = res.data.id // 把新建的商品的id传到前端
                const copyData = Object.assign({}, this.modalData.form)
                this.$emit('modal-success-valid', copyData)
                this.modalData.openModal = false
                this.$refs.goodForm.resetFields()
              } else {
                console.log(res.data)
                this.$Message.error(res.data.msg)
              }
            })
          }
        }
      })
    },
    myValidate () {
      let buySprice = this.modalData.form.buy_price
      let salePrice = this.modalData.form.sale_price
      if (buySprice > salePrice) {
        this.$Message.error('售价不能小于进价')
        return false
      } else {
        return true
      }
    },
    handleSubmitToSave () {
      this.$refs.goodForm.validate((valid) => {
        if (valid) {
          if (this.myValidate()) {
            ajaxGet(config.updateGoodUrl, this.modalData.form).then(res => {
              if (res.data.stat === 'success') {
                this.$Message.info('保存成功')
                this.$emit('modal-success-valid', this.modalData.form)
                this.$refs.goodForm.resetFields()
                this.modalData.openModal = false
              } else {
                console.log(res.data)
                this.$Message.error(res.data.msg)
              }
            })
          }
        }
      })
    }
  },
  mounted () {
  }
}
</script>
