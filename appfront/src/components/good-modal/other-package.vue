<template>
  <div style="width: 840px; height: 260px">
    <Form ref="packageForm" style="width: 720px" :model="form" :rules="rules" :label-width="70">
      <Row :gutter="80">
        <Col span="8">
          <FormItem label="包装条码" label-for="bar-id" prop="bar_id">
            <Input element-id="bar-id"  v-model="form.bar_id"/>
          </FormItem>
        </Col>
        <Col span="8">
          <FormItem label="包装名称" prop="name">
            <Input v-model="form.name"></Input>
          </FormItem>
        </Col>
        <Col span="8">
          <FormItem label="包装单位" prop="quantify_id">
            <Select v-model="form.quantify_id" filterable label-in-value
                    @on-change="onChangeQuantify" clearable style="width:200px">
              <Option v-for="item in quantifyList" :value="item.value" :key="item.value">{{ item.label }}</Option>
            </Select>
          </FormItem>
        </Col>
      </Row>
      <br>
      <Row :gutter="80">
        <Col span="8">
          <FormItem label="包装数量" prop="number">
            <InputNumber v-model="form.number"></InputNumber>
          </FormItem>
        </Col>
        <Col span="8">
          <FormItem label="包装售价" prop="package_price">
            <Input v-model="form.package_price"></Input>
          </FormItem>
        </Col>
        <Col span="8" type="flex" justify="center" align="right">
          <Button type="primary" @click="handleSubmit">添加</Button>
        </Col>
        <Button  @click="finished">完成</Button>
      </Row>
    </Form>
    <br>
    <Table :data="packageDataList" :columns="columns"></Table>
  </div>
</template>
<script>
import {ajaxGet} from '../../api/user'
import config from '@/config'

const formData = {
  bar_id: null,
  name: '',
  quantify_id: null,
  quantify: null,
  number: null,
  package_price: null
}
export default {
  name: 'OtherPackage',
  props: {
    quantifyList: {
      type: Array,
      required: true,
      default: () => {
        return {
        }
      }
    },
    changeType: {
      type: String,
      required: true
    },
    childData: {
      type: Object,
      required: true
    }
  },
  data () {
    return {
      rules: {
        bar_id: [{required: true, message: '请输入包装条码', trigger: 'blur'}],
        name: [{required: true, message: '请输入包装名称', trigger: 'blur'}],
        quantify_id: [{type: 'number', required: true, message: '请输入包装单位', trigger: 'blur'}],
        number: [{type: 'number', required: true, message: '请输入包装数量', trigger: 'blur'}],
        package_price: [{required: true, message: '请输入包装售价', trigger: 'blur'}]
      },
      packageDataList: [],
      good_id: null,
      columns: [
        {
          title: '包装条码',
          key: 'bar_id'
        },
        {
          title: '包装名称',
          key: 'name'
        },
        {
          title: '包装单位',
          key: 'quantify'
        },
        {
          title: '包装数量',
          key: 'number'
        },
        {
          title: '包装售价',
          key: 'package_price'
        },
        {
          title: '操作',
          key: 'action',
          render: (h, params) => {
            return h('div', [
              h('Button', {
                props: {
                  type: 'error',
                  size: 'small'
                },
                on: {
                  click: () => {
                    this.remove(params.index)
                  }
                }
              }, 'Delete')
            ])
          }
        }
      ],
      form: Object.assign({}, formData)
    }
  },
  methods: {
    getPackageData (good) {
      if (good) {
        this.good_id = good
        ajaxGet(config.getPackageData, good).then(res => {
          if (res.data.stat === 'success') {
            this.packageDataList = res.data.data
          } else {
            console.log(res.data.msg)
          }
        })
      }
    },
    handleSubmit () {
      this.$refs.packageForm.validate((valid) => {
        if (valid) {
          if (this.changeType === 'create') {
            let packageData = Object.assign({}, this.form)
            this.packageDataList.push(packageData)
            this.form = Object.assign({}, formData)
            this.$emit('other-package-created', this.packageDataList)
            this.$refs.packageForm.resetFields()
          } else {
            this.form['good_id'] = this.good_id
            ajaxGet(config.otherPackage, this.form).then(res => {
              if (res.data.stat === 'success') {
                let packageData = Object.assign({}, this.form)
                packageData['id'] = res.data.data['package_id']
                this.packageDataList.push(packageData)
                this.$Message.success(res.data.msg)
                this.$refs.packageForm.resetFields()
              } else {
                this.$Message.error(res.data.msg)
              }
            })
          }
        }
      })
    },
    finished () {
      this.childData.openPackagePoptip = false
    },
    modalChangeNotice () {
      this.packageDataList = []
      this.$refs.packageForm.resetFields()
      this.form = Object.assign({}, formData)
    },
    remove (index) {
      if (this.changeType === 'edit') {
        const data = {'delete_id': this.packageDataList[index].id}
        ajaxGet(config.otherPackage, data).then(res => {
          if (res.data.stat === 'success') {
            this.packageDataList.splice(index, 1)
            this.$Message.success(res.data.msg)
            this.$refs.packageForm.resetFields()
          } else {
            this.$Message.error(res.data.msg)
          }
        })
      } else {
        this.packageDataList.splice(index, 1)
      }
    },
    onChangeQuantify (data) {
      if (data) {
        this.form.quantify = data.label
      }
    }
  },
  mounted () {
  }
}
</script>
