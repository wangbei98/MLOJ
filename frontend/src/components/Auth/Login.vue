<template>
  <div>
    <nav-header></nav-header>
    <b-container>
      <b-row align-h="center" class="mt-5">
        <b-col cols="5">
          <b-card class="p-3">
            <h3 class="mb-4">账号登录</h3>
            <b-form @submit="onSubmit" @reset="onReset" v-if="show">
              <b-form-group
                id="input-group-1"
                label="学号:"
                label-for="input-1"
              >
                <b-form-input
                  id="input-1"
                  v-model="form.uid"
                  required
                  placeholder="Enter your id"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-2" label="密码" label-for="input-2">
                <b-form-input
                  id="input-2"
                  type="password"
                  v-model="form.password"
                  required
                  placeholder="Enter Password"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-4">
                <b-form-checkbox-group v-model="form.checked" id="checkboxes-4">
                  <b-form-checkbox value="remember">Remenber me</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
              <div class="d-flex justify-content-between">
                <div>
                  <b-button type="submit" variant="primary">Submit</b-button>&nbsp;
                  <b-button type="reset" variant="danger">Reset</b-button>
                </div>
                <div>
                  <router-link :to="{name: 'Register'}">Register</router-link>
                </div>
              </div>
            </b-form>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
  import NavHeader from '../common/NavHeader.vue'

  export default{
    name:'login',
    components:{
      NavHeader
    },
    data() {
      return {
        form: {
          uid: '',
          password: '',
          checked: []
        },
        show: true
      }
    },
    methods:{
      onSubmit(evt) {
        evt.preventDefault()
        this.$store.dispatch('login',{
          uid:this.form.uid,
          password:this.form.password
        }).then(response => {
          // 如果登录成功，则跳转到主页
          this.$router.push('/')

          // TODO：拉取所有课程信息
          //this.$store.dispatch('getAllCourses')
        })
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.uid = ''
        this.form.password = ''
        this.form.checked = []
        // Trick to reset/clear native browser form validation state
        this.show = false
        this.$nextTick(() => {
          this.show = true
        })
      }
    }
  }
</script>

<style>
  body {
    background: #eef1f4;
  }
</style>
