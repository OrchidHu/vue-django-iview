<template>
  <div>
  <Table
          show-header
         :loading="loading"
         size="small"
          :height="480"
         :data="tableData"
         :columns="columns"></Table>
  <StockRecord ref="stockRecordView" :openDrawer="openDrawer"></StockRecord>
  </div>
</template>
<script>
import {ajaxPost} from '../../api/user'
import config from '../../config'
import StockRecord from './stock-record'
export default {
  components: {StockRecord},
  data () {
    return {
      loading: false,
      tableData: [],
      openDrawer: {
        open: false,
        row: null
      },
      columns: [
        {type: 'index', width: 60},
        {title: '批次', key: 'batch_number'},
        {title: '类型', key: 'stock_genre'},
        {title: '门店', key: 'shop'},
        {title: '审批', key: 'examine_display'},
        {
          title: '操作',
          key: 'action',
          width: 216,
          render: (h, {row, index}) => {
            if (row.examine_status !== -1) {
              return [h('span', {
                style: {textAlign: 'center', paddingLeft: '60px'}
              }, '审核完成')]
            } else {
              return [h('Button', {
                style: {background: 'green', color: 'white'},
                on: {
                  click: () => {
                    this.allow(row, index)
                  }
                }
              }, '通过'),
              h('Button', {
                style: {
                  marginLeft: '6px',
                  background: 'tomato',
                  color: 'white'
                },
                on: {
                  click: () => {
                    this.refuse(row, index)
                  }
                }
              }, '拒绝'),
              h('Button', {
                style: {
                  marginLeft: '6px',
                  background: '#2d8cf0',
                  color: 'white'
                },
                on: {
                  click: () => {
                    this.review(row, index)
                  }
                }
              }, '查看')
              ]
            }
          }
        }
      ]
    }
  },
  computed: {
  },
  methods: {
    allow (row, index) {
      row.examine_status = 1
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          setTimeout(() => {
            this.remove(index)
          }, 500)
          this.examIng = false
        } else {
          this.$Message.error(res.data.msg)
        }
      })
    },
    refuse (row, index) {
      row.examine_status = 0
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          setTimeout(() => {
            this.remove(index)
          }, 500)
          this.examIng = false
        } else {
          this.$Message.error(res.data.msg)
        }
      })
    },
    review (row, index) {
      this.openDrawer.open = true
      this.$refs.stockRecordView.getStockData(row)
    },
    remove (index) {
      this.tableData.splice(index, 1)
    }
  },
  created () {
    this.$http.get(config.getExamTask, {withCredentials: true}).then(res => {
      if (res.data.stat === 'success') {
        this.tableData = res.data.data
      } else {
        this.$Message.error(res.data.msg)
      }
      this.loading = false
    })
  }
}
</script>
