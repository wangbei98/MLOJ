<template>
  <div>
    <nav-header></nav-header>
    <div style="padding: 2%;">
      <div v-if="isAdmin==1">
        <el-button type="text" @click="dialogVisible = true">上传课件</el-button>

        <el-dialog
          title="上传"
          :visible.sync="dialogVisible"
          width="30%"
          :before-close="handleClose">

          <div>
            <b-form-file
                  v-model="file"
                  :state="Boolean(file)"
                  placeholder="Choose a file or drop it here..."
                  drop-placeholder="Drop file here..."
                ></b-form-file>
            <div class="mt-3">Selected file: {{ file ? file.name : '' }}</div>
          </div>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="handleUpload">确 定</el-button>
          </span>
        </el-dialog>
      </div>
      <el-table
        :data="coursewares"
        style="width: 100%"
        max-height="250">
        <el-table-column
          fixed
          prop="courseware_name"
          label="文件名">
        </el-table-column>
        <el-table-column
          fixed="right"
          label="操作"
          width="120">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="downloadRow(scope.row.cwid,scope.row.courseware_name)"
              type="text"
              size="small">
              下载
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          v-if="isAdmin==1"
          fixed="right"
          label="操作"
          width="120">
          <template slot-scope="scope">
            <el-button
              @click.native.prevent="deleteRow(scope.row.cwid)"
              type="text"
              size="small">
              移除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'

  export default{
    name:'coursewares',
    components:{
      NavHeader
    },
    inject:['reload'],
    data(){
      return{
        coursewares:[],
        file:null,
        dialogVisible: false
      }
    },
    created(){
      this.$store.dispatch('getCoursewares')
      .then(response => {
        console.log(response)
        let coursewares = response.data.data.coursewares
        this.coursewares = coursewares
      }).catch(err => {
        console.log(err)
      })
    },
    computed:{
      isAdmin(){
        return this.$store.state.isAdmin
      }
    },
    methods: {
      deleteRow(cwid) {
        console.log('deleteRow')
        console.log(cwid)
        this.$store.dispatch('deleteCourseware',cwid)
        .then(response => {
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          this.reload()
        })
        .catch(err => {
          this.$message.error('删除失败')
        })
      },
      downloadRow(cwid,courseware_name){
        console.log('download courseware')
        this.$store.dispatch('downloadCourseware',cwid)
        .then(res => {
          if (res.data.type === "application/json") {
            this.$message({
              type: "error",
              message: "下载失败，文件不存在或权限不足"
            });
          } else {
            if (window.navigator.msSaveOrOpenBlob) {
              navigator.msSaveBlob(blob, courseware_name);
            } else {
              let url = window.URL.createObjectURL(new Blob([res.data]))
              let link = document.createElement('a')
              link.style.display = 'none'
              link.href = url
              link.setAttribute('download', courseware_name)

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
      handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
      },
      handleUpload(){
        console.log('handle upload file is ')
        console.log(this.file)
        this.dialogVisible = false
        if(!this.file){
          return
        }
        this.$store.dispatch('uploadCourseware',{
          file:this.file
        }).then(response => {
          //成功后提示
          // this.showuploadSuccessAlert()
          this.$message({
            message: '上传成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        }).toLocaleString(err => {})
      }
    },
  }
</script>

<style>
</style>
