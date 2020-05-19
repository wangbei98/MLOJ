// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'


// 引入 element ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
Vue.use(ElementUI);

//引入 echarts
import ECharts from 'vue-echarts' // refers to components/ECharts.vue in webpack
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/scatter'
import 'echarts/lib/chart/pie'

Vue.component('v-chart', ECharts)



// highlight.js代码高亮插件
import Highlight from './utils/highlight'; // from 路径是highlight.js的路径，纯属自定义
Vue.use(Highlight);


import {store} from './store/store.js'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.use(router)

Vue.config.productionTip = false

router.beforeEach((to,from,next) => {
  if(to.matched.some(record => record.meta.requiresAuth)){
    if(! store.getters.loggedIn){//如果当前没登录，则需要跳转到登录页
      console.log('requiresAuth -> not login')
      next({
        path:'/login',
        query:{redirect:to.fullPath}
      })
    }else{//如果登录过
      console.log('requiresAuth -> logined')
      next()
    }
  }else if(to.matched.some(record => record.meta.requiresVisitor)){
    if(store.getters.loggedIn){//如果当前登录了
      console.log('requiresVisiter -> logined')
      next({
        path:'/home',
        query:{redirect:to.fullPath}
      })
    }else{//如果没登录
      console.log('requiresVisiter ->  not logined')
      next()
    }
  }else{
    next()
  }
})


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
