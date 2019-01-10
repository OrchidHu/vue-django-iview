<template>

  <Modal title="结算" v-model="balance.openModal" @on-ok="handleSubmit">
    <Row>
      <i-col span="11">
        <Form ref="balanceForm" :model="balance" :label-width="60">
          <FormItem label="折后金额" label-for="sum-money">
            <Poptip trigger="focus" content="结算以折后金额为准">
              <div slot="title" style="font-weight: bold; font-size: 12px">
                <Icon size="20" color="chocolate" type="ios-information-circle-outline" /> 注意</div>
              <InputNumber :min="0" :max="99999999" @on-change="discMoneyChange" element-id="sum-money"
                           v-model="balance.discMoney" style="color: red; font-weight:bold; min-width: 80px"/>
            </Poptip>
          </FormItem>
          <FormItem label="折扣优惠" label-for="discount">
            <InputNumber :min="0" :max="1000" style="min-width: 80px" element-id="discount"
                         @on-change="discountChange" v-model="balance.discount" :formatter="value => `${value}%`"
                         :parser="value => value.replace('%', '')"
            />
          </FormItem>
          <FormItem label="实收金额" label-for="arrange">
            <InputNumber ref="arrange" element-id="arrange" :min="0" :max="99999999" v-model="balance.arrangeMoney"/>
          </FormItem>
          <FormItem label="找零">
            <Input readonly v-model="oddChange" style="color: red"/>
          </FormItem>
        </Form>
      </i-col>
      <i-col span="1">
        <Divider type="vertical" style="height: 264px"/>
      </i-col>
      <i-col span="12">
        <!--<number-key-board @on-click="clickOnNumber"></number-key-board>-->
        <!--<Icon size="240" type="md-cart" />-->
        <img width="240" height="260" :src="AddMe" alt="">
      </i-col>
    </Row>
  </Modal>
</template>
<script>
import NumberKeyBoard from '@/components/number-key-board'
import AddMe from '@/assets/images/S90106-15113025.jpg'
if (AddMe) {
  var addMe = AddMe
} else { addMe = '' }

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
      AddMe: addMe,
      currentInputId: 'number'
    }
  },
  computed: {
    oddChange () {
      let arrangeMoney = this.balance.arrangeMoney
      let discMoney = this.balance.discMoney
      if (arrangeMoney < discMoney) return 0
      return (arrangeMoney - discMoney).toFixed(1)
    }
  },
  methods: {
    handleSubmit () {
      console.log('ok')
    },
    discMoneyChange () {
      this.balance.discount = (this.balance.discMoney / this.balance.sumMoney * 100).toFixed(2)
      this.balance.arrangeMoney = this.balance.discMoney
    },
    discountChange () {
      this.balance.discMoney = (this.balance.discount * this.balance.sumMoney / 100).toFixed(2)
      this.balance.arrangeMoney = this.balance.discMoney
    },
    cancle () {
      this.setData.openModal = false
    }
  }
}
</script>
