<template>
  <div>
    <nav-header></nav-header>
    <el-container style="border: 1px solid #eee">

      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <!-- <el-dropdown v-if="isAdmin==1">
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item @click='handleAddHomework()'>新增</el-dropdown-item>
              <el-dropdown-item @click='handleDeleteHomework()'>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown> -->

          <el-row type="flex" class="row-bg" justify="end">
            <el-col :span="6">
              <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAllChange">全选</el-checkbox>
            </el-col>
            <el-col v-if="isAdmin==1"  :span="2"><el-button type="text"
            @click='handleAddHomework'>新建课程</el-button></el-col>
            <el-col v-if="isAdmin==1 && selected.length > 0"  :span="2"><el-button type="text"
            @click='handleDeleteHomework'>删除课程</el-button></el-col>
          </el-row>
        </el-header>

        <!-- <el-main style="display: flex; justify-content: flex-start;">
            <homework-item
            v-for='homework in homeworks'
            :label='homework' :key='homework.hid'
            :homework="homework"
            ></homework-item>
        </el-main> -->
        <el-main>
            <el-checkbox-group v-model="selected"
            @change="handleSelectedChange">
              <el-checkbox v-for="homework in homeworks" :label="homework" :key="homework.hid">
                <homework-item :homework='homework'></homework-item>
              </el-checkbox>
            </el-checkbox-group>
        </el-main>
      </el-container>
    </el-container>
    <el-dialog title="新建课程" :visible.sync="dialogFormVisible">
      <el-form :model="homeworkForm">
        <el-form-item label="课程名" :label-width="formLabelWidth">
          <el-input v-model="homeworkForm.homeworkname" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="课程介绍" :label-width="formLabelWidth">
          <el-input type="textarea" v-model="homeworkForm.homework_desc" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="截止时间" :label-width="formLabelWidth">
          <el-input v-model="homeworkForm.end_time" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="是否公开排名" :label-width="formLabelWidth">
          <!-- <el-input v-model="shareForm.token_required" autocomplete="off"></el-input> -->
          <el-radio v-model="homeworkForm.publish_rank" label=0>否</el-radio>
          <el-radio v-model="homeworkForm.publish_rank" label=1>是</el-radio>
        </el-form-item>
        <el-form-item label="课程类型" :label-width="formLabelWidth">
          <!-- <el-input v-model="shareForm.token_required" autocomplete="off"></el-input> -->
          <el-radio v-model="homeworkForm.htype" label=0>可视化作业</el-radio>
          <el-radio v-model="homeworkForm.htype" label=1>模型作业</el-radio>
        </el-form-item>
        <el-form-item v-if="homeworkForm.htype==1" label="模型分类" :label-width="formLabelWidth">
          <!-- <el-input v-model="shareForm.token_required" autocomplete="off"></el-input> -->
          <el-radio v-model="homeworkForm.model_class" label=0>回归</el-radio>
          <el-radio v-model="homeworkForm.model_class" label=1>二元分类</el-radio>
          <el-radio v-model="homeworkForm.model_class" label=2>多元分类</el-radio>
        </el-form-item>
        <!-- <el-form-item label="分数比例" :label-width="formLabelWidth">
          <el-radio v-for="weight in weights" v-model="homeworkForm.weightid" :label='weight.weightid'>

          </el-radio>
        </el-form-item> -->
        <el-button type="primary" @click="innerVisible = true">新建一个权重比值</el-button>
        <el-table
            :data="weights | weightFilter(homeworkForm.model_class)"
            highlight-current-row
            @current-change="handleCurrentChange"
            style="width: 100%">
            <el-table-column property="weightid" label="id" width="120"> </el-table-column>
            <el-table-column property="micro" label="micro" width="120"> </el-table-column>
            <el-table-column property="macro" label="macro" width="120"> </el-table-column>
            <el-table-column property="f1_score" label="f1_score" width="120"> </el-table-column>
            <el-table-column property="rmse" label="rmse" width="120"> </el-table-column>
            <el-table-column property="r2_score" label="r2_score" width="120"> </el-table-column>
          </el-table>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitAddHomework">确 定</el-button>
      </div>

      <el-dialog
        width="30%"
        title="新建权重比值"
        :visible.sync="innerVisible"
        append-to-body>
        <el-form :model="weightForm">
          <el-form-item v-if="homeworkForm.model_class == 2" label="micro" :label-width="formLabelWidth">
            <el-input v-model="weightForm.micro" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="homeworkForm.model_class == 2" label="macro" :label-width="formLabelWidth">
            <el-input v-model="weightForm.macro" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="homeworkForm.model_class == 0" label="rmse" :label-width="formLabelWidth">
            <el-input v-model="weightForm.rmse" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="homeworkForm.model_class == 0" label="r2_score" :label-width="formLabelWidth">
            <el-input v-model="weightForm.r2_score" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="homeworkForm.model_class == 1" label="f1_score" :label-width="formLabelWidth">
            <el-input v-model="weightForm.f1_score" autocomplete="off"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="innerVisible = false">取 消</el-button>
          <el-button type="primary" @click="submitAddWeight">确 定</el-button>
        </div>
      </el-dialog>
    </el-dialog>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'
  import HomeworkItem from '../common/HomeworkItem.vue'
  export default{
    name:'login',
    components:{
      NavHeader,
      HomeworkItem
    },
    inject:['reload'],
    data() {
      return {
        dialogFormVisible: false,
        innerVisible: false,
        formLabelWidth: '120px',
        homeworkForm:{
          'homeworkname': '',
          'homework_desc': '',
          'htype':0,
          'end_time':0,
          'publish_rank':0,
          'model_class':-1,
          'weightid':0,
        },
        weightForm:{
          'micro':0,
          'macro':0,
          'rmse':0,
          'f1_score':0,
          'r2_score':0
        },
        selected:[],
        checkAll:false,
        isIndeterminate: true,
        weights:[]
      }
    },
    created(){
      this.$store.dispatch('getAllHomeworks')
      if(this.isAdmin == 1){
        this.$store.dispatch('getAllWeights')
        .then(response => {
          this.weights = response.data.data.weights
        })
        .catch(err => {
          console.log(err)
        })
      }

    },
    computed:{
      homeworks(){
        return this.$store.state.homeworks
      },
      isAdmin(){
        return this.$store.state.isAdmin
      },
    },
    methods:{
      handleAddHomework(){
        this.dialogFormVisible=true
      },
      handleDeleteHomework(){
        console.log('handle delete homework')
        this.selected.forEach(homework => this.$store.dispatch('deleteHomework',homework.hid)
        .then(response =>{
          this.$message({
            message: '删除成功',
            type: 'success'
          })
          // 刷新页面
          this.reload()
        })
        .catch(err =>{
          this.$message.error('删除失败，请刷新后重试');
        }))
      },
      submitAddHomework(){
        this.dialogFormVisible = false
        console.log('submit add homework')
        this.$store.dispatch('addHomework',this.homeworkForm)
        .then(res => {
          this.$message({
            message:'新建成功',
            type:'sucess'
          })
          this.reload()
        })
        .catch(err => {
          this.$message.error('新建失败')
        })
      },
      handleCurrentChange(val) {
        console.log('handle current change -> val : ')
        console.log(val.weightid)
        this.homeworkForm.weightid = val.weightid;
      },
      submitAddWeight(){
        console.log('submit add weight')
        this.innerVisible = false
        this.$store.dispatch('addWeight',this.weightForm)
        .then(res => {
          this.$message({
            message:'新建成功',
            type:'sucess'
          })
          this.reload()
        })
        .catch(err => {
          this.$message.error('新建失败')
        })
      },
      handleSelectedChange(value){
        console.log('handle selected change')
        let checkedCount = value.length;
        this.checkAll = checkedCount === this.homeworks.length;
        this.isIndeterminate = checkedCount > 0 && checkedCount < this.homeworks.length;
      },
      handleCheckAllChange(val){
        this.selected = val ? this.homeworks : [];
        this.isIndeterminate = false;
      }
    },
    filters:{
      weightFilter(weights,model_class){
        console.log('in weightFilter')
        console.log(model_class)
        console.log(weights)
        var filterWeights = []
        if (model_class == 0){
          //回归
          filterWeights = weights.filter(weight => weight.micro == 0 && weight.macro == 0 && weight.rmse > 0 && weight.f1_score == 0&& weight.r2_score > 0)

        }else if(model_class == 1){
          //二元
          filterWeights =  weights.filter(weight => weight.micro == 0 && weight.macro == 0 && weight.rmse == 0 && weight.f1_score > 0&& weight.r2_score ==0)

        }else if(model_class == 2){
          //多元
          filterWeights =  weights.filter(weight => weight.micro > 0 && weight.macro > 0 && weight.rmse == 0 && weight.f1_score == 0&& weight.r2_score ==0)

        }
        console.log('weights after filter')
        console.log(filterWeights)
        return filterWeights
      },
    }
  }
</script>

<style>
  .el-header {
    background-color: #f5f6fa;
    color: #333;
    line-height: 60px;
  }
</style>
