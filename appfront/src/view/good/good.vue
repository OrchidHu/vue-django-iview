<template>
<div style="height:100px">
  <div style="margin: 10px">
        Display border <i-switch v-model="showBorder" style="margin-right: 5px"></i-switch>
        Display stripe <i-switch v-model="showStripe" style="margin-right: 5px"></i-switch>
        Display index <i-switch v-model="showIndex" style="margin-right: 5px"></i-switch>
        Display multi choice <i-switch v-model="showCheckbox" style="margin-right: 5px"></i-switch>
        Display header <i-switch v-model="showHeader" style="margin-right: 5px"></i-switch>
        Table scrolling <i-switch v-model="fixedHeader" style="margin-right: 5px"></i-switch>
        Table size
        <Radio-group style="display:inline"  v-model="tableSize" type="button">
            <Radio label="large">大</Radio>
            <Radio label="default">中</Radio>
            <Radio label="small">小</Radio>
        </Radio-group>
    </div>
    <Table @on-row-dblclick="clickRow" :border="showBorder" :stripe="showStripe" :show-header="showHeader" :height="fixedHeader ? 250 : ''" :size="tableSize" :data="tableData3" :columns="tableColumns3"></Table>
    <div style="margin: 10px;overflow: hidden">
        <div style="float: right;">
            <Page :total="1" show-elevator :current="1" @on-change="changePage"></Page>
        </div>
    </div>
    <createGood v-show='true'/>
</div>
</template>
<script>
import { setToken, setUserName, getToken, getUserName } from '@/libs/util'
import config from '@/config'
import CreateGood from './create-good.vue'
export default {
  name: 'good_page',
  components: {CreateGood},
  data () {
    return {
      value: '',
      aaa:"23222222222222222",
      items: [{ name: 'Foo', value: 2 },{ name: 'Bar', value:1 }],
      waiting:"1",
      tableData3: [
                    {
                        name: 'John Brown',
                        age: 18,
                        address: 'New York No. 1 Lake Park',
                        date: '2016-10-03'
                    }
                ],
                showBorder: false,
                showStripe: false,
                showHeader: true,
                showIndex: true,
                showCheckbox: false,
                fixedHeader: false,
                tableSize: 'default'
    }
  },

  computed: {
            tableColumns3 () {
                let columns = [];
                if (this.showCheckbox) {
                    columns.push({
                        type: 'selection',
                        width: 60,
                        align: 'center'
                    })
                }
                if (this.showIndex) {
                    columns.push({
                        type: 'index',
                        width: 60,
                        align: 'center'
                    })
                }
                columns.push({
                    title: 'Date',
                    key: 'date',
                    sortable: true
                });
                columns.push({
                    title: 'Name',
                    key: 'name'
                });
                columns.push({
                    title: 'Age',
                    key: 'age',
                    sortable: true,
                    filters: [
                        {
                            label: 'Greater than 25',
                            value: 1
                        },
                        {
                            label: 'Less than 25',
                            value: 2
                        }
                    ],
                    filterMultiple: false,
                    filterMethod (value, row) {
                        if (value === 1) {
                            return row.age > 25;
                        } else if (value === 2) {
                            return row.age < 25;
                        }
                    }
                });
                columns.push({
                    title: 'Address',
                    key: 'address',
                    filters: [
                        {
                            label: 'New York',
                            value: 'New York'
                        },
                        {
                            label: 'London',
                            value: 'London'
                        },
                        {
                            label: 'Sydney',
                            value: 'Sydney'
                        }
                    ],
                    filterMethod (value, row) {
                        return row.address.indexOf(value) > -1;
                    }
                });
                return columns;
            }
        },
  methods: {
    changePage (curpage) {
      alert("当前页面页码是：" + curpage);
      this.pagerData.data.splice(0,this.pagerData.data.length);
      //alert("当前页面应该显示的数据index是：");  //  10(n-1) ~ 10n
      for(var i = 10*(curpage - 1) + 1;
        i<= ((this.pagerData.page.totalCount>10*curpage)?(10*curpage):(this.pagerData.page.totalCount));
        i++){
        console.log(" i = " + i + "，item：" + JSON.stringify(this.listdata[i]));
        this.pagerData.data.push(this.listdata[i-1]);
      }
    },
    clickRow (raw,index) {
      console.log(this.tableData3[index].name="哈哈")
    },
    handleClearCurrentRow () {
    alert("asdf")
      this.$refs.currentRowTable.clearCurrentRow();
    }
  },
  //在渲染商品之前，检查该用户是否有权限，否则返回401页面
  created () {
    const token = getToken()
    const username = getUserName()
    // 利用{withCredentials: true} 闯入COOKIES包含（sessionid）到django后台， 自动识别请求用户 此时params无效
    this.$http.get(config.goodUrl,{withCredentials: true},{params:{token:token, username:username}}).then(res => {
      let dict_data = res.data
      if(dict_data.stat == 'success') {
         this.value = 'isok'
         this.tableData3 = dict_data.data
      // 后端的token失效或者前端的token和后端的token不匹配，访问权限页面需要再次验证身份
      } else if(dict_data.relogin == 'true'){
        this.$Notice.error({
          title: dict_data.msg,
          desc: '即将进入权限页面'
        })
        // 清除cookies 使得router路由到login, 以验证其身份是否是本人操作
        this.$store.commit('setToken', '')
        this.$store.commit('setUserName', '')
        this.$router.push({
          name: 'login'
        })
      // 后端发现带有此token的用户，不具备访问此页面的权限
      }else{
        this.$router.replace({
          name: 'error_401'
        })
      }
    })
  },
  mounted () {

  },
  beforeDestroy () {

  }
}
</script>
