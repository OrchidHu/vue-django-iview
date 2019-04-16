<template>
  <div>
    <Row :gutter="16">
      <i-col span="6">
        <Card title="销售额">
          <Tooltip content="这里是指标说明" slot="extra" placement="top" transfer>
            <Icon type="ios-alert-outline" size="18"/>
          </Tooltip>
          <div class="count"> ¥ {{salesVolume}}</div>
          <Divider></Divider>
          周同比 12% <Icon type="md-arrow-dropup" size="22" color="#ed4014"></Icon>
          日环比 10% <Icon type="md-arrow-dropdown" size="22" color="#19be6b"></Icon>
        </Card>
      </i-col>
      <i-col span="6">
        <Card title="毛利润">
          <Tooltip content="这里是指标说明" slot="extra" placement="top" transfer>
            <Icon type="ios-alert-outline" size="18"/>
          </Tooltip>
          <div class="count"> ¥ {{salesProfit}}</div>
          <Divider></Divider>
          周同比 12% <Icon type="md-arrow-dropup" size="22" color="#ed4014"></Icon>
          日环比 10% <Icon type="md-arrow-dropdown" size="22" color="#19be6b"></Icon>
        </Card>
      </i-col>
      <i-col span="6">
        <Card title="营销分析">
          <Tooltip content="这里是指标说明" slot="extra" placement="top" transfer>
            <Icon type="ios-alert-outline" size="18"/>
          </Tooltip>
          <div class="count">{{salesDiscount}} %</div>
          <Divider></Divider>
          <Progress :percent="salesDiscount" status="success" hide-info />
        </Card>
      </i-col>
      <i-col span="6">
        <Card title="优惠额">
          <Tag color="green" slot="extra">日</Tag>
          <div class="count">¥ {{salesFavour}}</div>
          <Divider></Divider>
          日访问量1,230
        </Card>
      </i-col>
    </Row>
    <Card style="margin-top: 16px">
      <Tabs @on-click="clickTabs">
        <template v-if="displayDateButton" slot="extra">
          <RadioGroup v-model="dateType" @on-change="handleSetDate">
            <Radio label="day">今天</Radio>
            <Radio label="week">本周</Radio>
            <Radio label="month">本月</Radio>
            <Radio label="year">今年</Radio>
          </RadioGroup>
          <DatePicker type="daterange" v-model="countDate" style="width: 250px" transfer></DatePicker>
        </template>
        <TabPane label="销售额" name="sell">
          <Row>
            <i-col span="18">
              <div style="width: 100%; height: 400px;" ref="chart"></div>
            </i-col>
            <i-col span="6"></i-col>
          </Row>
        </TabPane>
        <TabPane label="访问量" name="visit">
          <Row>
            <i-col span="18">
              <div style="width: 100%; height: 400px;" ref="todayChart"></div>
            </i-col>
            <i-col span="6"></i-col>
          </Row>
        </TabPane>
      </Tabs>
    </Card>
  </div>
</template>
<script>
import { mapMutations } from 'vuex'
import {ajaxExamGet, ajaxGet} from '../../api/user'
import echarts from 'echarts'
import config from '@/config'

export default {
  data () {
    this.initSocket()
    return {
      salesVolume: 0.00,
      salesProfit: 0.00,
      salesDiscount: 0.00,
      salesFavour: 0.00,
      displayDateButton: true,
      dateType: 'day', // 'week', 'month', 'year'
      countDate: [new Date(), new Date()]
    }
  },
  computed: {
  },
  methods: {
    ...mapMutations([
      'setTask'
    ]),
    handleSetDate (type) {
      const today = (new Date()).getTime()
      let date
      switch (type) {
        case 'day': date = today; break
        case 'week': date = today - 86400000 * 7; break
        case 'month': date = today - 86400000 * 30; break
        case 'year': date = today - 86400000 * 365; break
      }
      this.countDate = [new Date(date), new Date()]
    },
    getData () {
      ajaxExamGet(config.getCommonData, {fast_report: true}).then(res => {
        let data = res.data.data
        this.salesVolume = data.total_sale.toFixed(2)
        this.salesProfit = data.total_profit.toFixed(2)
        this.salesDiscount = parseFloat(data.sales_discount.toFixed(2))
        this.salesFavour = data.sales_favour.toFixed(2)
      })
    },
    clickTabs (value) {
      if (value === 'sell') this.displayDateButton = true
      if (value === 'visit') {
        this.displayDateButton = false
        const todayChart = echarts.init(this.$refs.todayChart)
        const option = {
          xAxis: {
            type: 'category',
            data: ['0', '2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22']
          },
          yAxis: {
            type: 'value'
          },
          series: [{
            data: [820, 932, 901, 934, 1290, 1330, 1320, 820, 932, 901, 934, 1290, 1330, 1320, 820, 932, 901, 934, 1290, 1330, 1320, 820, 932, 901, 934, 1290, 1330, 1320],
            type: 'line'
          }]
        }
        todayChart.setOption(option)
      }
    },
    initChart () {
      ajaxGet(config.goodsSalesRank, JSON.stringify(this.countDate)).then(res => {
        if (res.data.stat === 'success') {
          console.log(11)
        }
      })
      const myChart = echarts.init(this.$refs.chart)
      const option = {
        title: {
          text: '销售额'
        },
        tooltip: {},
        legend: {
          data: ['销量']
        },
        xAxis: {
          data: ['红牛', '怡宝', '香飘飘', '乐虎', '苏打水', '绿箭口香糖']
        },
        yAxis: {},
        series: [{
          name: '销量',
          type: 'bar',
          data: [5, 20, 13, 8, 23, 9]
        }]
      }
      myChart.setOption(option)
    },
    initSocket () {
      var sock
      var message
      if ('WebSocket' in window) { // 判断当前浏览器是否支持webSocket
        sock = new WebSocket(config.webSocket) // 建立连接
        console.log(config.webSocket)
      }
      sock.onopen = (e) => { // 成功建立连接
        sock.send('hello world')
      }
      sock.onmessage = (evt) => {
        message = evt.data
        this.setTask(message)
      }
      setTimeout(() => {
        if (message) {
          this.$Message.success(message)
        } else {
          console.log('websock连接错误')
        }
      }, 2000)
      return {
        sock: sock,
        message: this.$store.state.task
      }
    }
  },
  mounted () {
    this.initChart()
    this.getData()
  }
}
</script>
<style>
  .count{
    font-size: 24px;
  }
</style>
