<template>
  <div>
    <base-item>
      <header>
        <h2>Friend Requests</h2>
      </header>
      <ul v-if="hasRequests">
        <request-item
          v-for="friend in requests"
          :key="friend.friendId"
          :friendId="friend.friendId"
          :first-name="friend.firstName"
          :last-name="friend.lastName"
          :hobbies="friend.hobbies"
        ></request-item>
      </ul>
      <p v-else>No friend Requests</p>
    </base-item>
  </div>
</template>

<script>

import RequestItem from "../../components/friendRequests/RequestItem.vue";
export default {
  components: { RequestItem},
  computed: {
    hasRequests() {
      return this.requests.length > 0;
    },
    requests() {
      const request = this.$store.getters["friendRequests/requests"];
      const friends = this.$store.getters["friends/friends"];
      return friends.filter((friend) => request.includes(friend.friendId))
     
    },
  },
  methods: {
    loadRequests() {
      this.$store.dispatch("friendRequests/loadRequests");
    },
  },
  created() {
    this.loadRequests();
  },
};
</script>

<style scoped>
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

header {
  text-align: center;
}

p {
  text-align: center;
}

</style>
