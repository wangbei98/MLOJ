<template>
  <div>
    <nav-header></nav-header>
    <b-container>
      <b-row align-h="center" class="mt-5">
        <b-col cols="5">
          <b-card class="p-3">
            <h3 class="mb-4">账号注册</h3>
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
                  placeholder="Enter user id"
                ></b-form-input>
              </b-form-group>

              <b-form-group id="input-group-3" label="姓名" label-for="input-2">
                <b-form-input
                  id="input-3"
                  v-model="form.username"
                  required
                  placeholder="Enter username"
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
              
              <div class="d-flex justify-content-between">
                <div>
                  <b-button type="submit" variant="primary">Submit</b-button>&nbsp;
                  <b-button type="reset" variant="danger">Reset</b-button>
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
          username: ''
        },
        show: true
      }
    },
    methods:{
      onSubmit(evt) {
        evt.preventDefault()
        this.$store.dispatch('register',{
          uid:this.form.uid,
          password:this.form.password,
          username:this.form.username
        }).then(response => {
          // 如果登录成功，则跳转到首页
          this.$router.push('/login')
        })
      },
      onReset(evt) {
        evt.preventDefault()
        // Reset our form values
        this.form.uid = ''
        this.form.password = ''
        this.username = ''
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
