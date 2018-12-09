<template>
<div>
  <Row style="height: 60px" >
    <Col span="8"  type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('1')">1</Button>
    </Col>
    <Col span="8" type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('2')">2</Button>
    </Col>
    <Col span="8"type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('3')">3</Button>
    </Col>
  </Row>
  <Row style="height: 60px;" >
    <Col span="8"  type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('4')">4</Button>
    </Col>
    <Col span="8" type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('5')">5</Button>
    </Col>
    <Col span="8"type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('6')">6</Button>
    </Col>
  </Row>
  <Row style="height: 60px;" >
    <Col span="8"  type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('7')">7</Button>
    </Col>
    <Col span="8" type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('8')">8</Button>
    </Col>
    <Col span="8"type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('9')">9</Button>
    </Col>
  </Row>
  <Row style="height: 60px;" >
    <Col span="8"  type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('.')">.</Button>
    </Col>
    <Col span="8" type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('0')">0</Button>
    </Col>
    <Col span="8"type="flex" justify="center"  align="middle" >
      <Button style="height: 60px; width: 100%" @click="clickOnNumber('')"><Icon type="md-arrow-back" /></Button>
    </Col>
  </Row>
</div>
</template>

<script>
export default {
  name: 'NumberKeyBoard',
  methods: {
    clickOnNumber (val) {
      this.$emit('on-click', val)
    }
  }
}
</script>
