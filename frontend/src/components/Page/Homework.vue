<template>
  <div>
    <nav-header></nav-header>
    <div class="contaniner"
     style="padding: 2%;"
     v-if="homework !=null">
      <el-card class="box-card">
        <div slot="header" class="clearfix">
          <span>{{homework.homeworkname}}</span>
          <el-button v-if="isAdmin==1" style="float: right; padding: 3px 0"
          @click='handleScoreStatistics'
          type="text">查看分数统计</el-button>
          <span v-else style="float: right; padding: 3px 0">目前分数: {{curScore}}</span>
        </div>
        <div class="text item">
          {{homework.homework_desc }}
        </div>
      </el-card>
      <el-divider></el-divider>
      <div class="downloadButtons" v-if="isAdmin == 1">
        <h4>数据集下载(老师端)</h4>
        <el-row>
          <el-button v-if="trainingset!=null" type="primary" plain @click='downloadTrainingSet'>训练集下载{{trainingset.filename}}</el-button>
          <el-button v-else type="primary" plain>无可用训练集</el-button>
          <el-button v-if="testset!=null" type="primary" plain @click='downloadTestSet'>测试集下载（数据部分）{{testset.filename}}</el-button>
          <el-button v-else type="primary" plain>无可用测试</el-button>
          <el-button  v-if="answerset!=null" type="primary" plain @click='downloadAnswerSet'>测试集下载（答案部分）{{answerset.filename}}</el-button>
          <el-button v-else type="primary" plain>无可用答案集</el-button>
        </el-row>
      </div>
      <div class="downloadButtons" v-if="isAdmin == 0">
        <h4>数据集下载</h4>
        <el-button v-if="trainingset!=null" type="primary" plain @click='downloadTrainingSet'>训练集下载{{trainingset.filename}}</el-button>
        <el-button v-else type="primary" plain>无可用训练集</el-button>
        <el-button v-if="testset!=null" type="primary" plain @click='downloadTestSet'>测试集下载（数据部分）{{testset.filename}}</el-button>
        <el-button v-else type="primary" plain>无可用测试集</el-button>
      </div>
      <el-divider></el-divider>
      <div class="handleUploadResult" v-if="isAdmin==0">
        <div v-if="homework.htype==0">
          <!-- jupyter 作业 -->
          <el-row>
              <b-form-file
              style="width: 30%;"
              v-model="file_html"
              :state="Boolean(file_html)"
              placeholder="Choose 答案 or drop it here..."
              drop-placeholder="Drop file here..."
            ></b-form-file>
            <el-button type="primary" @click='handleUploadHTML'>上传你的代码（html文件）<i style="margin: 5px;" class="el-icon-upload el-icon--right"></i></el-button>
          </el-row>
        </div>
        <div v-else>
          <!-- python 作业 -->
          <!-- 上传答案 -->
          <h4>上传答案</h4>
          <el-row>
              <b-form-file
              style="width: 30%;"
              v-model="file_python"
              :state="Boolean(file_python)"
              placeholder="Choose 答案 or drop it here..."
              drop-placeholder="Drop file here..."
            ></b-form-file>
            <el-button type="primary" @click='handleUploadPython'>上传你的代码（python文件）<i  class="el-icon-upload el-icon--right"></i></el-button>
          </el-row>
          <el-row>
              <b-form-file
              style="width: 30%;"
              v-model="file_res"
              :state="Boolean(file_res)"
              placeholder="Choose 答案 or drop it here..."
              drop-placeholder="Drop file here..."
            ></b-form-file>
            <el-button type="primary" @click='handleUploadResult'>上传答案（csv文件）<i  class="el-icon-upload el-icon--right"></i></el-button>
          </el-row>
        </div>
      </div>
      <div class="handleUploadDataSet" v-if="isAdmin==1">
        <!-- 上传训练集 -->
        <!-- 上传测试集（数据部分） -->
        <!-- 上传测试集（答案部分） -->
        <h4>上传数据集(老师端)</h4>
        <el-row>
          <b-form-file
            style="width: 25%; margin: 10px;"
            v-model="file_train"
            :state="Boolean(file_train)"
            placeholder="上传训练集"
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <b-form-file
            style="width: 25%; margin: 10px"
            v-model="file_test"
            :state="Boolean(file_test)"
            placeholder="上传测试集(数据部分)"
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <b-form-file
            style="width: 25%; margin: 10px"
            v-model="file_ans"
            :state="Boolean(file_ans)"
            placeholder="上传测试集(答案部分)"
            drop-placeholder="Drop file here..."
          >
          </b-form-file>
          <el-button type="primary" @click='handleUploadAllDataset'>上传所有数据集<i style="margin: 5px;" class="el-icon-upload el-icon--right"></i></el-button>
        </el-row>
      </div>

      <div class="score" v-if="isAdmin==1">
        <el-divider></el-divider>
        <h4>学生分数（老师端）</h4>
        <el-table
          :data="students"
          style="width: 100%"
          max-height="1000"
          :default-sort = "{prop: 'submit_time', order: 'descending'}">
          <el-table-column
            sortable
            fixed
            prop="uid"
            label="学号">
          </el-table-column>
          <el-table-column
            sortable
            fixed
            prop="submit_time"
            label="提交时间"
            :formatter="timeFormatter">
          </el-table-column>
          <el-table-column
            sortable
            fixed
            prop="score"
            label="分数">
          </el-table-column>
          <el-table-column
            fixed="right"
            label="操作"
            width="120">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="rateRow(scope.row.uid)"
                type="text"
                size="small">
                去评分
              </el-button>
            </template>
          </el-table-column>

        </el-table>
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
	  inject:['reload'],
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
      //获得所有学生的完成情况
      if(this.isAdmin == 1){//如果是老师，就自动获取所有学生的成绩
        this.$store.dispatch('getStudents',this.hid)
        .then(response => {
          this.students = response.data.data.users
          console.log('students is ')
          console.log(this.students)
        }).catch(error =>{
          console.log(error)
        })
      }else{//如果是学生，则就获取他自己的成绩
        this.$store.dispatch('getMyScore',this.hid)
        .then(response => {
          this.curScore = response.data.data.score
          console.log('curScore is ')
          console.log(this.curScore)
        }).catch(error =>{
          console.log(error)
        })
      }
    },
    data(){
      return {
        homework:null,
        datasets:[],
        students:[],
        file_train:null,
        file_test:null,
        file_ans:null,
        file_res:null,
        file_html:null,
        file_python:null,
        curScore:0
      }
    },
    computed:{
      isAdmin(){
        return this.$store.state.isAdmin
      },
      trainingset(){
        return this.datasets.filter(dataset => dataset.ftype == 0)[0]
      },
      testset(){
        return this.datasets.filter(dataset => dataset.ftype == 1)[0]
      },
      answerset(){
        return this.datasets.filter(dataset => dataset.ftype == -1)[0]
      }
    },
    methods:{
      handleUploadAllDataset(){
        console.log('handle upload - >dataset is ')
        console.log(this.file_train)
        console.log(this.file_test)
        console.log(this.file_ans)
        if(!this.file_train || !this.file_test ||!this.file_ans){
          return
        }
        //上传数据集
        this.$store.dispatch('uploadDataset',{
          hid:this.hid,
          file:this.file_train,
          ftype:0
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
        //上传测试集
        this.$store.dispatch('uploadTestset',{
          hid:this.hid,
          file:this.file_test,
          ftype:1
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
        //上传答案集
        this.$store.dispatch('uploadAnswerset',{
          hid:this.hid,
          file:this.file_ans,
          ftype:-1
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
      },
      downloadTrainingSet(){
        console.log('downloadTrainingSet')
        this.$store.dispatch('downloadTrainingSet',this.trainingset.fid)
        .then(res => {
          if (res.data.type === "application/json") {
            this.$message({
              type: "error",
              message: "下载失败，文件不存在或权限不足"
            });
          } else {
            if (window.navigator.msSaveOrOpenBlob) {
              navigator.msSaveBlob(blob, 'trainingset.csv');
            } else {
              let url = window.URL.createObjectURL(new Blob([res.data]))
              let link = document.createElement('a')
              link.style.display = 'none'
              link.href = url
              link.setAttribute('download', 'trainingset.csv')

              document.body.appendChild(link)
              link.click()
            }
          }
          this.$message({
            message: '下载成功',
            type: 'success'
          })
        })
        .catch(err => {
          console.log(err)
          this.$message.error('下载失败，请刷新后重试');
        })
      },
      downloadTestSet(){
        console.log('downloadTestSet')
        this.$store.dispatch('downloadTestSet',this.testset.fid)
        .then(res => {
          if (res.data.type === "application/json") {
            this.$message({
              type: "error",
              message: "下载失败，文件不存在或权限不足"
            });
          } else {
            if (window.navigator.msSaveOrOpenBlob) {
              navigator.msSaveBlob(blob, 'testset.csv');
            } else {
              let url = window.URL.createObjectURL(new Blob([res.data]))
              let link = document.createElement('a')
              link.style.display = 'none'
              link.href = url
              link.setAttribute('download', 'testset.csv')

              document.body.appendChild(link)
              link.click()
            }
          }
          this.$message({
            message: '下载成功',
            type: 'success'
          })
        })
        .catch(err => {
          console.log(err)
          this.$message.error('下载失败，请刷新后重试');
        })
      },
      downloadAnswerSet(){
        console.log('downloadAnswerSet')
        this.$store.dispatch('downloadAnswerSet',this.answerset.fid)
        .then(res => {
          if (res.data.type === "application/json") {
            this.$message({
              type: "error",
              message: "下载失败，文件不存在或权限不足"
            });
          } else {
            if (window.navigator.msSaveOrOpenBlob) {
              navigator.msSaveBlob(blob, 'testset_ans.csv');
            } else {
              let url = window.URL.createObjectURL(new Blob([res.data]))
              let link = document.createElement('a')
              link.style.display = 'none'
              link.href = url
              link.setAttribute('download', 'testset_ans.csv')

              document.body.appendChild(link)
              link.click()
            }
          }
          this.$message({
            message: '下载成功',
            type: 'success'
          })
        })
        .catch(err => {
          console.log(err)
          this.$message.error('下载失败，请刷新后重试');
        })
      },
      handleUploadHTML(){
        console.log('handle upload html')
        if(!this.file_html){
          this.$message.error('先选择文件')
          return
        }
        this.$store.dispatch('uploadHTML',{
          hid:this.hid,
          file:this.file_html,
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
      },
      handleUploadPython(){
        console.log('handle upload python')
        if(!this.file_python){
          this.$message.error('先选择文件')
          return
        }
        this.$store.dispatch('uploadPython',{
          hid:this.hid,
          file:this.file_python,
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
      },
      handleUploadResult(){
        console.log('handle upload res')
        if(!this.file_res){
          this.$message.error('先选择文件')
          return
        }
        this.$store.dispatch('uploadResult',{
          hid:this.hid,
          file:this.file_res,
        }).then(response => {
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
      },
      rateRow(uid){
        //去评分
        console.log('rate row ->' + uid)
        this.$router.push('/rate/'+this.homework.hid + '/' + uid)
      },
      handleScoreStatistics(){
        console.log('handle socre')
        this.$router.push('/statistics/'+this.homework.hid)
      },
      //时间戳转string
      timeFormatter(row,col){
        return new Date(parseInt(row.submit_time) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
      },
    },
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
