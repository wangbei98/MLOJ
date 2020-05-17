import Vue from 'vue'
import Router from 'vue-router'

import Login from '../components/Auth/Login.vue'
import Register from '../components/Auth/Register.vue'
import Logout from '../components/Auth/Logout.vue'
import Home from '../components/Page/Home.vue'
import Homework from '../components/Page/Homework.vue'
import Coursewares from '../components/Page/Coursewares.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/register',
      name: 'Register',
      component: Register
    },
    {
      path: '/logout',
      name: 'Logout',
      component: Logout
    },
    {
      path: '/homework/:hid',
      name: 'Homework',
      component: Homework,
      props:true
    },
    {
      path: '/coursewares',
      name: 'Coursewares',
      component:Coursewares
    }
  ]
})
