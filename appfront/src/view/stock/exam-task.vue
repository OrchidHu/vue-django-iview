<template>
  <Table
          show-header
         :loading="loading"
         size="small"
         :data="tableData"
         :columns="columns"></Table>
</template>
<script>
import {ajaxPost} from '../../api/user'
import config from '../../config'
export default {
  data () {
    return {
      loading: false,
      tableData: [],
      columns: [
        {type: 'index', width: 60},
        {title: '批次', key: 'batch_number'},
        {title: '门店', key: 'shop'},
        {title: '审批', key: 'examine_status'},
        {
          title: '操作',
          key: 'action',
          render: (h, {row, index}) => {
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
      ]
    }
  },
  computed: {},
  methods: {
    allow (row, index) {
      row.examine_status = 1
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          this.remove(index)
        } else {
          this.$Message.error(res.data.msg)
        }
      })
    },
    refuse (row, index) {
      row.examine_status = 0
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          this.remove(index)
        } else {
          this.$Message.error(res.data.msg)
        }
      })
    },
    review (row, index) {
      ajaxPost(config.commitExamTask, row).then(res => {
        if (res.data.stat === 'success') {
          console.log(res.data)
        } else {
          this.$Message.error(res.data.msg)
        }
      })
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
