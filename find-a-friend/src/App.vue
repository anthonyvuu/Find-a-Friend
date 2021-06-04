<template>
  <div>
    <the-header></the-header>
    <router-view></router-view>
  </div>
</template>

<script>
import TheHeader from "./components/layout/TheHeader.vue";


export default {
  components: {
    TheHeader,
  },
  created () {
    // autologin visst siden reloades
    this.$store.dispatch('autoLogin');
    this.$router.replace("friends");
  },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

* {
  box-sizing: border-box;
}

html {
  font-family: "Roboto", sans-serif;
}

body {
  margin: 0;
  background-color: lightblue;
  
}
</style>
