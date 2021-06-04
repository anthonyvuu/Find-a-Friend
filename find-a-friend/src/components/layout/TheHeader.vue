<template>
  <header>
    <nav>
      <h1><router-link to="/">Find a Friend</router-link></h1>
      <ul>
        <li>
          <router-link to="/friends">All Friends</router-link>
        </li>
        <li v-if="isLoggedIn && isFriend" class="request-notification">
          <router-link to="/requests">Requests</router-link>
          <span class="request-counter">{{ requestsCounter }}</span>
        </li>
        <li v-if="isLoggedIn && isFriend">
          <router-link to="/profile">Profile</router-link>
        </li>
        <li v-if="isLoggedIn">
          <base-button @click="logout">Logout</base-button>
        </li>
        <li v-else>
          <router-link to="/auth">Login</router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
import Pusher from "pusher-js";
// create pusher instance
var pusher = new Pusher("d03450301bfcf65bbaeb", {
  cluster: "eu",
});

export default {
  computed: {
    isLoggedIn() {
      if (sessionStorage.friendId) {
        // subscribe to a channel event for the pusher to listen to. listens to new-request for incoming request, and notification for chat messages
        const channel = pusher.subscribe(sessionStorage.friendId);
        channel.bind("new-request", (data) => {
          this.loadFriends();
          this.loadRequests();
          console.log(data);
        });
        channel.bind("notification", (data) => {
          this.notificationRecieved(data);
        })
      }
      return this.$store.getters.isLoggedIn;
    },
    requestsCounter() {
      return this.$store.getters["friendRequests/requests"].length;
    },
    isFriend() {
      return this.$store.getters["friends/isFriend"];
    }
  },
  methods: {
    notificationRecieved(from_user) {
      this.$store.commit('chat/addNotification' , String(from_user));
    },
    loadRequests() {
      this.$store.dispatch("friendRequests/loadRequests");
    },
    loadFriends() {
      this.$store.dispatch("friends/loadFriends");
    },
    async logout() {
      await this.$store.dispatch("logout");
      await this.$router.replace("/friends");
      const channel = pusher.unsubscribe(sessionStorage.friendId);
      console.log(channel);
      await location.reload();
    },
  },
};
</script>

<style scoped>
header {
  width: 100%;
  height: 5rem;
  background: #33076c;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-notification {
  background-color: grey;
  position: absolute;
  margin: auto;
  z-index: 999;
  width: 300px;
  height: 100px;
  bottom: 0;
  right: 0;
}

.popup-notification .popup-text {
  color: #fff;
  display: flex;
  margin: auto;
  justify-content: center;
  align-items: center;
}

header a {
  text-decoration: none;
  color: #f391e3;
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border: 1px solid transparent;
}

a:active,
a:hover,
a.router-link-active {
  border: 1px solid #f391e3;
}

h1 {
  margin: 0;
}

h1 a {
  color: white;
  margin: 0;
}

h1 a:hover,
h1 a:active,
h1 a.router-link-active {
  border-color: transparent;
}

header nav {
  width: 90%;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.request-notification {
  position: relative;
}

.request-counter {
  position: absolute;
  top: 1px;
  left: 90px;
  background-color: green;
  border-radius: 50%;
  color: white;
  padding: 2px 5px;
}

header ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

li {
  margin: 0 0.5rem;
}
</style>
