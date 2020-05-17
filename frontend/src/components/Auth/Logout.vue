<template>
</template>

<script>
export default{
  created(){
    this.$store.dispatch('logout')
    .then(response => {
      // 如果登录成功，则跳转到首页
      this.$router.push('/')
    })
  }
}
</script>

<style>
</style>
