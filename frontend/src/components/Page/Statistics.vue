<template>
  <div>
    <nav-header></nav-header>
    <el-divider></el-divider>
    <el-row>
      <el-col :span="12">
        <h4>分数分布</h4>
        <v-chart ref="chart1" :options="orgOptions1" :auto-resize="true"></v-chart>
      </el-col>
      <el-col :span="12">
        <h4>提交日期分布</h4>
        <v-chart ref="chart2" :options="orgOptions2" :auto-resize="true"></v-chart>
      </el-col>
    </el-row>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'
  export default{
    name:'statistics',
    components:{
      NavHeader
    },
    props:{
      hid:{
        type:String,
        required:true
      }
    },
    data(){
      return {
        homework:null,
        students:[],
        orgOptions1: {},
        orgOptions2: {}
      }
    },
    computed:{
      isAdmin(){
        return this.$store.state.isAdmin
      },
      orgOptions1data(){
        var lessThen2 = 0
        var from2to5 = 0
        var from5to7 = 0
        var from7to9 = 0
        var moreThen9 = 0
        for (const student of this.students){
          // console.log('student -> score')
          // console.log(student.score)
          if(student.score < 2){
            lessThen2++
          }else if(student.score >= 2 && student.score < 5){
            from2to5++
          }
          else if(student.score >= 5 && student.score < 7){
            from5to7++
          }
          else if(student.score >= 7 && student.score < 9){
            from7to9++
          }else{
            moreThen9++
          }
        }
        var data = [
          {value: lessThen2, name: '< 2分'},
          {value: from2to5, name: '2分 ～ 5分'},
          {value: from5to7, name: '5分 ～ 7分'},
          {value: from7to9, name: '7分 ～ 9分'},
          {value: moreThen9, name: '> 9分'}
        ]
        return data
      },
      orgOptions2data(){
        //折线图
        var dic = new Array(); //定义一个字典
        for (const student of this.students){
          let timestamp = student.submit_time
          let date = this.timeFormatter(timestamp)
          console.log('day -> ')
          console.log(date)
          console.log((date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-')
          console.log(date.getDate())
          let month = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '-'
          let day = date.getDate()
          let time = month + day
          console.log(time)
          if(dic[time]){
            dic[time]++
          }else{
            dic[time] = 1
          }
        }
        var res = Object.keys(dic).sort();
        console.log('time dict')
        console.log(dic)
        return dic
      }
    },
    created(){
      this.$store.dispatch('getHomework',this.hid)
      .then(response => {
        this.homework = response.data.data.homework
        console.log('cur homework is ')
        console.log(this.homework)
      }).catch(error =>{
        console.log(error)
      });
      //获得所有学生的完成情况
      if(this.isAdmin == 1){//如果是老师，就自动获取所有学生的成绩
        this.$store.dispatch('getStudents',this.hid)
        .then(response => {
          this.students = response.data.data.users
          console.log('students is ')
          console.log(this.students)
          // console.log(data)
          //设置数据信息
          this.orgOptions1 = {
              title: {
                  text: '某站点用户访问来源',
                  subtext: '纯属虚构',
                  left: 'center'
              },
              tooltip: {
                  trigger: 'item',
                  formatter: '{a} <br/>{b} : {c} ({d}%)'
              },
              legend: {
                  orient: 'vertical',
                  left: 'left',
                  data: ['< 2分', '2分 ～ 5分', '5分 ～ 7分', '7分 ～ 9分', '> 9分']
              },
              series: [
                  {
                      name: '访问来源',
                      type: 'pie',
                      radius: '55%',
                      center: ['50%', '60%'],
                      data: this.orgOptions1data,
                      emphasis: {
                          itemStyle: {
                              shadowBlur: 10,
                              shadowOffsetX: 0,
                              shadowColor: 'rgba(0, 0, 0, 0.5)'
                          }
                      }
                  }
              ]
          };
          let list = []
          let values = []
          let dic = this.orgOptions2data
          for(var key in dic ){
              console.log("key: " + key + " ,value: " + dic[key]);
              list.push(key)
              values.push(dic[key])
          }
          this.orgOptions2 = {
            xAxis: {
                type: 'category',
                data: list
            },
            yAxis: {
                type: 'value'
            },
            series: [{
                data: values,
                type: 'line'
            }]
          }
        }).catch(error =>{
          console.log(error)
        })
      }
    },
    methods:{
      timeFormatter(timestemp){
        return new Date(parseInt(timestemp) * 1000)
      },
    }
  }
</script>

<style>
</style>
