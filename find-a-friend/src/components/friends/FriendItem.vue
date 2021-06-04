<template>
  <li>
    <base-dialog :show="!!error" title="Error" @click="confirmError">
      <p>{{ error }}</p>
    </base-dialog>
    <h3>
      {{ Name.toUpperCase() }}
    </h3>
    <div>
      <base-badge
        v-for="hobby in hobbies"
        :key="hobby.hobby"
        :type="hobby.backgroundColor"
        :title="hobby.hobby"
      >
      </base-badge>
    </div>
    <div class="actions">
      <span>
        <base-button v-if="!add" mode="outline" link :to="chatFriendref"
          >Chat<span class="notification" v-if="notification"></span
        ></base-button>
      </span>
      <base-button
        v-if="isFriend && isLoggedIn && add"
        @click="addFriend"
        mode="outline"
        >Add friend</base-button
      >
      <base-button link :to="friendDetailref">Details</base-button>
    </div>
  </li>
</template>

<script>
export default {
  props: ["friendId", "firstName", "lastName", "hobbies", "add"],

  data() {
    return {
      error: null,
    };
  },

  computed: {
    Name() {
      return this.firstName + " " + this.lastName;
    },
    chatFriendref() {
      return this.$route.path + "/" + this.friendId + "/chat";
    },
    friendDetailref() {
      return this.$route.path + "/" + this.friendId;
    },
    isFriend() {
      return this.$store.getters["friends/isFriend"];
    },
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    notification() {
      return this.$store.getters["chat/notifications"].includes(this.friendId);
    },
  },
  methods: {
    async addFriend() {
      const requestData = {
        requesttoId: this.friendId,
      };
      try {
        await this.$store.dispatch("friendRequests/sendRequest", requestData);
      } catch (err) {
        this.error = err.message || "failed";
      }
    },
    confirmError() {
      this.error = null;
    },
  },
};
</script>

<style scoped>
li {
  margin: 1rem 0;
  border: 1px solid #424242;
  border-radius: 12px;
  padding: 1rem;
}
.online {
  height: 18px;
  width: 18px;
  border-radius: 50%;
  background-color: rgb(17, 147, 22);
  display: inline-block;
}

h3 {
  font-size: 1.5rem;
  margin: 0.5rem 0;
}

div {
  margin: 0.5rem 0;
}

.actions {
  display: flex;
  justify-content: flex-end;
  flex-shrink: 1;
}

.notification {
  height: 10px;
  width: 10px;
  border-radius: 50%;
  background-color: red;
  display: inline-block;
}
</style>
