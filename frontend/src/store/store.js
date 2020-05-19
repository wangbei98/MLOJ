import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);
axios.defaults.baseURL = '/api'

export const store = new Vuex.Store({
  state:{
    uid:localStorage.getItem('uid') || null,
    username:localStorage.getItem('username') || null,
    isAdmin: localStorage.getItem('isAdmin') || 0,
    homeworks:[],
    // weights:[],
    coursewares:[],
    scores:[],
  },
  getters:{
    loggedIn(state){
      return state.uid != null
    },
    targetHost(state){
      return 'http://116.62.177.146'
    }
  },
  mutations:{
    refreshUid(state,uid){
      state.uid = uid
    },
    refreshUsername(state,username){
      state.username = username
    },
    refreshIsAdmin(state,isAdmin){
      state.isAdmin = isAdmin
    },
    deleteUid(state){
      state.uid = null
    },
    deleteUsername(state){
      state.username = null
    },
    deleteIsAdmin(state){
      state.isAdmin = 0
    },
    refreshHomeworks(state,homeworks){
      state.homeworks = homeworks
    },
    // refreshWeights(state,weights){
    //   state.weights = weights
    // }
  },
  actions:{
    login(context,credentials){
      // 将axios封装为Promise请求
      return new Promise((resolve,reject) => {
        axios.post('/login',{
          uid:credentials.uid,
          password:credentials.password
        }).then(response => {
          console.log('actioin -> login :')
          console.log(response)
          const uid = response.data.data.user.uid
          const username = response.data.data.user.username
          const isAdmin = response.data.data.user.is_admin
          context.commit('refreshUid',uid)
          context.commit('refreshUsername',username)
          context.commit('refreshIsAdmin',isAdmin)
          localStorage.setItem('uid',uid)
          localStorage.setItem('username',username)
          localStorage.setItem('isAdmin',isAdmin)
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    logout(context){
      if(context.getters.loggedIn){
        return new Promise((resolve,reject) => {
          axios.get('/logout')
          .then(response => {
            localStorage.removeItem('uid')
            localStorage.removeItem('username')
            localStorage.removeItem('isAdmin')
            context.commit('deleteUid')
            context.commit('deleteUsername')
            context.commit('deleteIsAdmin')
            resolve(response)
          }).catch(err => {
            localStorage.removeItem('uid')
            localStorage.removeItem('username')
            localStorage.removeItem('isAdmin')
            context.commit('deleteUid')
            context.commit('deleteUsername')
            context.commit('deleteIsAdmin')
            reject(err)
          })
        })
      }
    },
    register(context,data){
      // 将axios封装为Promise请求
      return new Promise((resolve,reject) => {
        axios.post('/register',{
          uid:data.uid,
          username:data.username,
          password:data.password
        }).then(response => {
          alert('success')
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    getAllHomeworks(context){
      return new Promise((resolve,reject) => {
        axios.get('/homeworks')
        .then(response=>{
          const homeworks = response.data.data.homeworks
          context.commit('refreshHomeworks',homeworks)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    getAllWeights(context){
      return new Promise((resolve,reject) => {
        axios.get('/weight')
        .then(response=>{
          // const weights = response.data.data.weights
          // context.commit('refreshWeights',weights)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    addWeight(context,params){
      return new Promise((resolve,reject) => {
        axios.post('/weight',{
          micro:params.micro,
          macro:params.macro,
          rmse:params.rmse,
          f1_score:params.f1_score,
          r2_score:params.r2_score
        }).then( response => {
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    addHomework(context,params){
      return new Promise((resolve,reject) => {
        axios.post('/homeworks',{
          homeworkname:params.homeworkname,
          desc:params.homework_desc,
          type:params.htype,
          end_time:params.end_time,
          publish_rank:params.publish_rank,
          weightid:params.weightid
        }).then(respons =>{
          resolve(respons)
        }).catch(err => {
          reject(err)
        })
      })
    },
    deleteHomework(context,hid){
      return new Promise((resolve,reject) => {
        axios.delete('/homework?hid='+hid)
        .then(response =>{
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    getHomework(context,hid){
      return new Promise((resolve,reject) => {
        axios.get('/homework?hid='+hid)
        .then(response => {
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    getCoursewares(context){
      return new Promise((resolve,reject) => {
        axios.get('/coursewares')
        .then(response => {
          resolve(response)
        }).catch(err => {
          reject(err)
        })
      })
    },
    uploadCourseware(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload courseware')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/coursewares',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    downloadCourseware(context,cwid){
      console.log('action downloadCourseware')
      return new Promise((resolve,reject) => {
        axios.get('/courseware?cwid='+cwid,{
          responseType: 'blob'
        })
        .then(response =>{
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    deleteCourseware(context,cwid){
      return new Promise((resolve,reject) => {
        axios.delete('/courseware?cwid='+cwid)
        .then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    uploadDataset(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload dataset')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      formData.append('ftype',data.ftype)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/datasets',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    uploadTestset(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload testset')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      formData.append('ftype',data.ftype)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/datasets',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    uploadAnswerset(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload answerset')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      formData.append('ftype',data.ftype)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/datasets',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    downloadTrainingSet(context,fid){
      console.log('action downloadTrainingSet')
      return new Promise((resolve,reject) => {
        axios.get('/dataset?fid='+fid,{
          responseType: 'blob'
        })
        .then(response =>{
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    downloadTestSet(context,fid){
      console.log('action downloadTestSet')
      return new Promise((resolve,reject) => {
        axios.get('/dataset?fid='+fid,{
          responseType: 'blob'
        })
        .then(response =>{
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    downloadAnswerSet(context,fid){
      console.log('action downloadAnswerSet')
      return new Promise((resolve,reject) => {
        axios.get('/dataset?fid='+fid,{
          responseType: 'blob'
        })
        .then(response =>{
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    getStudents(context,hid){
      console.log('action getStudents')
      return new Promise((resolve,reject) => {
        axios.get('/homework/students?hid='+hid)
        .then(response=>{
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    uploadHTML(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload html')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/homework/submit',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    uploadPython(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload python')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/homework/submit',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    uploadResult(context,data){
      let config = {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
      console.log('action : upload html')
      console.log(data.file)
      let formData = new FormData();
      formData.append('file',data.file)
      formData.append('hid',data.hid)
      console.log('action: submit upload')
      console.log(formData)
      return new Promise((resolve,reject) => {
        axios.post('/homework/uploadcsv',formData,config)
        .then(response=>{
          // context.commit('reNameFile',data)
          console.log(response)
          resolve(response)
        }).catch(err => {
          console.log(err)
          reject(err)
        })
      })
    },
    getSubmitedData(context,data){
      return new Promise((resolve,reject) => {
        axios.get('/homework/submit?hid='+data.hid + '&uid='+ data.uid)
        .then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    submitScore(context,data){
      return new Promise((resolve,reject) => {
        axios.post('/homework/score',{
          hid:data.hid,
          uid:data.uid,
          score:data.score
        })
        .then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    },
    getMyScore(context,hid){
      return new Promise((resolve,reject) => {
        axios.get('/homework/score?hid='+hid)
        .then(response => {
          resolve(response)
        })
        .catch(err => {
          reject(err)
        })
      })
    }
  }
})
