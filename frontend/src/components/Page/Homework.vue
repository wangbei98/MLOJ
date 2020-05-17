<template>
  <div>
    <nav-header></nav-header>
    <div class="contaniner"
     style="padding: 2%;"
     v-if="homework !=null">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>{{homework.homeworkname}}</span>
          <el-button style="float: right; padding: 3px 0"
          @click='handleScore'
          type="text">查看分数</el-button>
        </div>
        <div class="text item">
          {{homework.homework_desc }}
        </div>
      </el-card>
      <el-divider></el-divider>
      <div class="downloadButtons" v-if="isAdmin == 1">
        <h4>数据集下载(老师端)</h4>
        <el-row>
          <el-button type="primary" plain @click='downloadTrainingSet'>训练集下载</el-button>
          <el-button type="primary" plain @click='downloadTestSet'>测试集下载（数据部分）</el-button>
          <el-button type="primary" plain @click='downloadAnswerSet'>测试集下载（答案部分）</el-button>
        </el-row>
      </div>
      <div class="downloadButtons" v-if="isAdmin == 0">
        <h4>数据集下载</h4>
        <el-button type="primary" plain @click='downloadTrainingSet'>训练集下载</el-button>
        <el-button type="primary" plain @click='downloadTestSet'>测试集下载（数据部分）</el-button>
      </div>
      <el-divider></el-divider>
      <div class="handleUploadResult" v-if="isAdmin==0">
        <!-- 上传答案 -->
        <h4>上传答案</h4>
        <b-form-file
          style="width: 30%;"
          v-model="file"
          :state="Boolean(file)"
          placeholder="Choose 答案 or drop it here..."
          drop-placeholder="Drop file here..."
        ></b-form-file>
      </div>
      <div class="handleUploadDataSet" v-if="isAdmin==1">
        <!-- 上传训练集 -->
        <!-- 上传测试集（数据部分） -->
        <!-- 上传测试集（答案部分） -->
        <h4>上传数据集(老师端)</h4>
        <el-row>
          <b-form-file
            style="width: 25%; margin: 10px;"
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose 训练集 or drop it here..."
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <b-form-file
            style="width: 25%; margin: 10px"
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose 训练集 or drop it here..."
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <b-form-file
            style="width: 25%; margin: 10px"
            v-model="file"
            :state="Boolean(file)"
            placeholder="Choose 训练集 or drop it here..."
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <el-button type="primary">上传所有数据集<i style="margin: 5px;" class="el-icon-upload el-icon--right"></i></el-button>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'

  export default{
    name:'homework',
    components:{
      NavHeader
    },
    props:{
      hid:{
        type:String,
        required:true
      }
    },
    mounted(){
      this.$store.dispatch('getHomework',this.hid)
      .then(response => {
        this.homework = response.data.data.homework
        console.log('cur homework is ')
        console.log(this.homework)
      }).catch(error =>{
        console.log(error)
      })
    },
    data(){
      return {
        homework:null
      }
    },
    computed:{
      isAdmin(){
        return this.$store.state.isAdmin
      }
    },
    methods:{
      downloadTrainingSet(){
        console.log('downloadTrainingSet')
      },
      downloadTestSet(){
        console.log('downloadTestSet')
      },
      downloadAnswerSet(){
        console.log('downloadAnswerSet')
      }
    }
  }
</script>

<style>
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }
  .clearfix:after {
    clear: both
  }

  .box-card {
    width: 480px;
  }
</style>
