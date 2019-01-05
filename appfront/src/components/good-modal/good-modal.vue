<template>
  <Modal :title="modalData.changeType==='create'?'新增商品': '编辑商品'"
         v-model="modalData.openModal" @on-visible-change="onVisibleChange" :mask-closable="false">
    <Form ref="goodForm" :model="modalData.form" :rules="rules" :label-width="50">
      <FormItem label="条码"  label-for="bar-id" prop="bar_id" >
        <Input element-id="bar_id" v-model="modalData.form.bar_id"/>
      </FormItem>
      <FormItem label="名称" label-for="name" prop="name" >
        <Input element-id="name" v-model="modalData.form.name"/>
      </FormItem>
      <FormItem label="类别" prop="genre_id">
        <Cascader v-model="modalData.form.genre_id" :data="genreList" filterable @on-change="onChangeGenre"></Cascader>
      </FormItem>
      <FormItem label="单位" prop="quantify_id">
        <Select v-model="modalData.form.quantify_id" filterable label-in-value
                @on-change="onChangeQuantify" clearable style="width:200px">
          <Option v-for="item in quantifyList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
        <Poptip title="添加单位" v-model="openQuantifyPoptip" placement="top-start" width=200 height=400>
          <Icon style="margin-left: 20px; color: chartreuse;" size="18" type="md-add" /> 添加单位
          <div slot="content" style="height: 80px">
            <Input v-model="addQuantifyValue" />
            <div>
              <Button style="float: right; margin-top: 10px" @click="addQuantifySubmit">确定</Button>
            </div>
          </div>
        </Poptip>
        <Poptip title="商品多包装" v-model="childData.openPackagePoptip" placement="top" @on-popper-show="onPopperShow">
          <Icon style="margin-left: 20px; color: chartreuse;" size="18" type="md-add" /> 添加多包装
          <OtherPackage ref="child" slot="content" :quantifyList="quantifyList" :childData="childData"
                        :changeType="modalData.changeType" @other-package-created="otherPackageCreated"></OtherPackage>
        </Poptip>
      </FormItem>
      <Row>
      <Col span="12">
      <FormItem style="width: 200px" label="进价" prop="buy_price">
        <InputNumber style="width: auto" v-model="modalData.form.buy_price" number/>
      </FormItem>
      </Col>
      <Col span="12">
      <FormItem style="width: 200px; " label="售价" prop="sale_price">
        <InputNumber style="width: auto" v-model="modalData.form.sale_price" number/>
      </FormItem>
      </Col></Row>
      <FormItem label="供应商" prop="supplier_id">
        <Select v-model="modalData.form.supplier_id" filterable label-in-value
                @on-change="onChageSupplier" clearable style="width:200px">
          <Option v-for="item in supplierList" :value="item.value" :key="item.value">{{ item.label }}</Option>
        </Select>
      </FormItem>
    </Form>
    <div slot="close" @click="closeTheModal"><Icon type="ios-close" /></div>
    <div slot="footer">
      <Button type="text" size="large" @click="closeTheModal">取消</Button>
      <Button v-if="modalData.changeType==='create'" type="primary" size="large"
              @click="handleSubmitToCreate" :loading="createLoading">确定</Button>
      <Button v-if="modalData.changeType==='edit'" type="primary" size="large"
              @click="handleSubmitToSave" :loading="saveLoading">保存</Button>
    </div>
  </Modal>
</template>
<script>

import config from '@/config'
import {ajaxGet} from '@/api/user'
import OtherPackage from './other-package'
import Bus from '../../view/bus'
export default {
  name: 'GoodModal',
  components: {
    OtherPackage
  },
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
          {required: true, message: '请输入条码', trigger: 'change'},
          {validator (rule, value, callback) {
            let errors = []
            if (value && !/^[0-9]+$/.test(value)) { callback('条码必须为数字值') }
            callback(errors)
          }}
        ]
      }
    },
    nameRules: {type: Array,
      default: () => {
        return [{required: true, message: '请输入名称', trigger: 'change'}]
      }
    },
    genreRules: {type: Array,
      default: () => {
        return [{required: true, message: '请输入类别', trigger: 'change'}]
      }
    },
    buyPriceRules: {type: Array,
      default: () => {
        return [{required: true, message: '请输入进价'},
          {type: 'number', message: '输入正确的数字', trigger: 'change'},
          { validator (rule, value, callback) {
            let errors = []
            if (value < 0) { callback('进价不能小于零') }
            callback(errors)
          }}
        ]
      }
    },
    salePriceRules: {type: Array,
      default: () => {
        return [{required: true, message: '请输入售价'},
          {type: 'number', message: '请输入正确的数字', trigger: 'change'},
          {validator (rule, value, callback) {
            let errors = []
            if (value < 0) { callback('售价不能小于零') }
            callback(errors)
          }}
        ]
      }
    },
    supplierIdRules: {type: Array,
      default: () => { // 此处value为id是数字，所以type为number，不然被视为没选
        return [{ type: 'number', message: '请输入类别', trigger: 'change'}]
      }
    }
  },
  data () {
    return {
      saveLoading: false,
      createLoading: false,
      quantifyList: [],
      supplierList: [],
      packageDataList: [],
      genreList: [],
      addQuantifyValue: null,
      openQuantifyPoptip: false,
      childData: {openPackagePoptip: false}
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
        supplier_id: this.supplierIdRules
      }
    }
  },
  methods: {
    onChangeQuantify (data) {
      if (data) {
        this.modalData.form.quantify = data.label
      } else {
        this.modalData.form.quantify = '-'
      }
    },
    addQuantifySubmit () {
      if (!this.addQuantifyValue.trim()) {
        this.$Message.error('不能为空')
        return
      }
      ajaxGet(config.addQuantifyUrl, this.addQuantifyValue).then(res => {
        if (res.data.stat === 'success') {
          this.modalData.form.quantify_id = res.data.data.current_id
          this.quantifyList = res.data.data.quantify_list
          this.modalData.form.quantify = this.addQuantifyValue
          this.addQuantifyValue = null
          this.$Message.success(res.data.msg)
          this.openQuantifyPoptip = false
        } else {
          this.$Message.error(res.data.msg)
        }
      })
    },
    // 调用子组件获取其他包装数据
    onPopperShow () {
      this.$refs.child.getPackageData(this.modalData.form.id)
    },
    onChageSupplier (data) {
      if (data) {
        this.modalData.form.supplier = data.label
      }
    },
    onChangeGenre (value, selectedData) {
      console.log(selectedData)
      if (selectedData.length > 0) {
        this.modalData.form.genre = selectedData[selectedData.length - 1].label
        this.modalData.form.genre_id = value
      }
    },
    closeTheModal () { // 为了避免新建和更新共用Modal在校验上存在缓存问题 如:(如关闭更新Modal后打开新建Modal出现"校验红字")
      setTimeout(() => {
        this.$refs.goodForm.resetFields()
        this.modalData.openModal = false
      })
    },
    onVisibleChange (value) {
      if (value) {
        this.$nextTick(() => {
          var elInput = document.getElementById('bar_id')
          elInput.focus()
        })
      }
    },
    handleSubmitToCreate () {
      if (this.createLoading) return
      this.createLoading = true
      this.$refs.goodForm.validate((valid) => {
        if (valid) {
          if (this.myValidate()) {
            let commitData = {form: this.modalData.form, package_data: this.packageDataList}
            ajaxGet(config.createGoodUrl, commitData).then(res => {
              if (res.data.stat === 'success') {
                this.$refs.goodForm.resetFields()
                this.$Message.success('新建成功')
                this.modalData.form.id = res.data.id // 把新建的商品的id传到前端
                this.modalData.supplier = this.supplierList
                if (this.modalData.form.genre_id.length === 0) {
                  this.modalData.form.genre = null
                }
                const copyData = Object.assign({}, this.modalData.form)
                this.$emit('modal-success-valid', copyData)
                this.modalData.openModal = false
              } else {
                this.$refs.child.modalChangeNotice()
                this.$Message.error(res.data.msg)
              }
            })
          }
        }
      })
      this.createLoading = false
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
      if (this.saveLoading) return
      this.saveLoading = true
      this.$refs.goodForm.validate((valid) => {
        if (valid) {
          if (this.myValidate()) {
            ajaxGet(config.updateGoodUrl, this.modalData.form).then(res => {
              if (res.data.stat === 'success') {
                this.$Message.success('保存成功')
                if (this.modalData.form.genre_id.length === 0) {
                  this.modalData.form.genre = '-'
                }
                this.$emit('modal-success-valid', this.modalData.form)
                this.$refs.goodForm.resetFields()
                this.modalData.openModal = false
              } else {
                this.$Message.error(res.data.msg)
              }
              this.saveLoading = false
            })
          }
        }
      })
    },
    // 后面是子组件相关方法
    modalChangeNotice () {
      this.$refs.child.modalChangeNotice()
    },
    otherPackageCreated (data) {
      this.packageDataList = data
    }
  },
  mounted () {
    ajaxGet(config.getQuantifyUrl).then(res => {
      this.quantifyList = res.data.data
    })
    ajaxGet(config.getSupplierUrl).then(res => {
      this.supplierList = res.data.data
    })
    ajaxGet(config.getGenreUrl).then(res => {
      this.genreList = res.data.data
    })
    Bus.$on('focusName', () => {
      setTimeout(() => {
        var elInput = document.getElementById('name')
        elInput.focus()
      })
    })
  }
}
</script>
