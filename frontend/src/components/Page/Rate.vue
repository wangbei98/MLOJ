<template>
  <div>
    <nav-header></nav-header>
    <el-divider></el-divider>
    <h4>学生代码</h4>
    <el-container style="height: 500px; border: 1px solid #eee">
      <el-aside width="60%">
        <div id="codeView" v-highlight>
            <pre><code v-html="submitedData"></code></pre>
        </div>
      </el-aside>

      <el-container>
        <el-form :inline="true" class="demo-form-inline">
          <el-form-item label="分数">
            <el-input v-model="score" placeholder="0"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSubmitScore">提交分数</el-button>
          </el-form-item>
        </el-form>
      </el-container>
    </el-container>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'
  export default{
    name:'rate',
    components:{
      NavHeader
    },
    props:{
      hid:{
        type:String,
        required:true
      },
      uid:{
        type:String,
        required:true
      }
    },
    inject:['reload'],
    data(){
      return {
        homework:null,
        submitedData:'',
        score:0
      }
    },
    mounted(){
      this.$store.dispatch('getHomework',this.hid)
      .then(response => {
        this.homework = response.data.data.homework
        this.datasets = this.homework.files
        console.log('cur homework is ')
        console.log(this.homework)
      }).catch(error =>{
        console.log(error)
      })
      this.$store.dispatch('getSubmitedData',{
        hid:this.hid,
        uid:this.uid
      })
      .then(response => {
        console.log('get submited data -> ')
        console.log(response.data)
        this.submitedData = response.data
      }).catch(error =>{
        console.log(error)
      })
    },
    computed:{
      htype(){
        return this.homework.htype
      }
    },
    methods:{
      handleSubmitScore(){
        this.$store.dispatch('submitScore',{
          hid:this.hid,
          uid:this.uid,
          score:this.score
        })
        .then(resposne => {
          this.$message({
            message: '提交成功',
            type: 'success'
          })
          this.$router.push('/homework/'+this.homework.hid)
        })
        .catch( err => {
          console.log(err)
        })
      }
    }
  }
</script>

<style>

</style>
