<template>
  <li :class="me ? 'me' : 'other'">
    <div class="sender">

      <h2>{{ message.firstName }}</h2>
      <h2 v-if="me">(Me)</h2>
      <h3>{{message.date}}</h3>
    </div>

    <div class="message" v-if="message.isImage">
      <a :href="message.message" :download="message.fileName">
      <img :src="message.message" alt="">
      </a>
    </div>
    
    <div class="message" v-else-if="message.isFile">
       <a :href="message.message" :download="message.fileName"> {{message.fileName}}
      </a>
    </div>

    <div v-else class="message">
      {{ message.message }}
    </div>
    
  </li>
</template>

<script>
export default {
  props: ["message"],
  computed: {
    me() {
      return (
        this.$store.getters["friends/mySelf"][0].firstName ===
        this.message.firstName
      );
    },
  },

};
</script>

<style scoped>


li {
  padding: 10px 30px;
}

h2,h3 {
  margin: 2px;
  display: inline-block;
  font-size: 13px;
  font-weight: normal;
}
h3 {
  color: #bbb;
}

.sender {
  margin-bottom: 5px;
}

.message {
  padding: 20px;
  color: #fff;
  line-height: 25px;
  max-width: 90%;
  display: inline-block;
  text-align: left;
  border-radius: 5px;
}

img {
  max-width: 300px;
  max-height: 400px
}

.me {
  text-align: right;
}

.other .message {
  background-color: #58b666;
}

.me .message{
	background-color:#6fbced;
}

</style>
