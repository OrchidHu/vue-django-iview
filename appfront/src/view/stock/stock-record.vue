<template>
  <Modal width="960" title="入库详情" placement="left" footer-hide closable v-model="openDrawer.open">
    <Table :data="tableData" :height="currentHeight" size="small" :columns="columns"></Table>
  </Modal>
</template>
<script>
import {ajaxPost} from '../../api/user'
import config from '../../config'
export default {
  name: 'StockRecord',
  props: {
    openDrawer: {
      type: Object
    }
  },
  data () {
    return {
      tableData: [],
      columns: [
        {type: 'index', width: 60},
        {title: '名称', key: 'good_name'},
        {title: '条码', key: 'bar_id'},
        {title: '门店', key: 'shop_name'},
        {title: '单位', key: 'quantify'},
        {title: '单价', key: 'buy_price'},
        {title: '数量', key: 'number'},
        {title: '包装绑定', key: 'package_number'},
        {title: '小计',
          render: (h, {row}) => {
            return h('span', [this.compute(row)])
          }},
        {title: '操作人', key: 'operator'},
        {title: '操作时间', key: 'create_time', width: 100}
      ]
    }
  },
  computed: {
    currentHeight () {
      let clientHeight = `${document.documentElement.clientHeight}`
      if (clientHeight >= 768) {
        return clientHeight - 280
      }
      if (clientHeight >= 1024) {
        return clientHeight - 300
      }
      return clientHeight - 270
    }
  },
  methods: {
    compute (row) {
      return row.buy_price * row.number
    },
    getStockData (row) {
      console.log(row)
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          this.tableData = res.data.data
        } else {
          this.$Message.error(res.data.msg)
        }
      })
      console.log(row)
    }
  }
}
</script>
