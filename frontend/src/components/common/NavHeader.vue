<template>
  <div>
    <b-navbar toggleable="lg" type="dark" class="nav-background">
      <b-navbar-brand href="#">机器学习评分系统</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item href="#">Link</b-nav-item>
          <b-nav-item href="#" disabled>Disabled</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">

          <b-navbar-nav>
            <b-nav-item href="/#/coursewares">
              课件
            </b-nav-item>
          </b-navbar-nav>



          <b-nav-form>
            <b-form-input size="sm" class="mr-sm-2" placeholder="Search"></b-form-input>
            <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
          </b-nav-form>



          <b-nav-item-dropdown right v-if="loggedIn">
            <!-- Using 'button-content' slot -->
            <template v-slot:button-content>
              <em>{{username}}</em>
            </template>
            <b-dropdown-item><router-link :to="{name: ''}">Profile</router-link> </b-dropdown-item>
            <b-dropdown-item><router-link :to="{name: 'Logout'}">Sign Out</router-link></b-dropdown-item>
          </b-nav-item-dropdown>
          <b-navbar-nav v-if="!loggedIn">
            <b-nav-item><router-link :to="{name:'Login'}">Login</router-link> </b-nav-item>
          </b-navbar-nav>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>
  export default{
    name:'nav-header',
    computed:{
      loggedIn(){
        return this.$store.getters.loggedIn
      },
      username(){
        return this.$store.state.username
      }
    }
  }
</script>

<style>
  .nav-background{
    background: #FF5900;
  }
</style>
