<template>
  <div>
    <section class="filter">
      <friend-filter
        @change-search="setSearch"
        @change-filter="setFilters"
        :hobbies="hobbies"
      ></friend-filter>
    </section>

    <section>
      <base-item>
        <div class="controls">
          <base-button @click="refresh">Refresh</base-button>
          <base-button
            mode="outline"
            v-if="isLoggedIn && isFriend"
            @click="typeSwitch"
            >{{ type }}</base-button
          >
          
          <base-button mode="outline" link to="/register" v-if="isLoggedIn && !isFriend"
            >Register as Friend</base-button
          >
        </div>
        <ul v-if="hasFriends">
          <friend-item
            v-for="friend in filtered"
            :key="friend.friendId"
            :friendId="friend.friendId"
            :first-name="friend.firstName"
            :last-name="friend.lastName"
            :hobbies="friend.hobbies"
            :add="mode"
          ></friend-item>
        </ul>
        <h3 v-else>No friends to show.</h3>
      </base-item>
    </section>
  </div>
</template>

<script>
import BaseButton from "../../components/base/BaseButton.vue";
import FriendFilter from "../../components/friends/FriendFilter.vue";
import FriendItem from "../../components/friends/FriendItem.vue";
export default {
  components: {
    FriendItem,
    FriendFilter,
    BaseButton,
  },

  data() {
    return {
      search: "",
      type: "My Friends",
      mode: true,
    };
  },

  computed: {
    isLoggedIn() {
      return this.$store.getters.isLoggedIn;
    },
    isFriend() {
      return this.$store.getters["friends/isFriend"];
    },
    hobbies() {
      return this.$store.getters["hobbies/hobbies"];
    },
    newFriends() {
      return this.$store.getters["friends/newFriends"];
    },
    myFriends() {
      return this.$store.getters["friends/myFriends"];
    },
    //filter based on checkboxes.
    filteredFriends() {
      const friends = this.friends;
      return friends.filter((friend) => {
        for (let key in this.filters) {
          for (let j = 0; j < friend.hobbies.length; j++) {
            if (this.filters[key] && friend.hobbies[j].hobby === key) {
              return true;
            }
          }
        }
        return false;
      });
    },
    // refilter based search input included
    filtered() {
      const filteredfriends = this.filteredFriends;
      return filteredfriends.filter((friend) => {
        return friend.firstName
          .toLowerCase()
          .includes(this.search.toLowerCase());
      });
    },
    hasFriends() {
      if (this.type === "My Friends") {
        return this.newFriends.length > 0;
      } else {
        return this.myFriends.length > 0;
      }
    },
    filters() {
      return this.$store.getters["hobbies/filters"];
    },
    friends() {
      if (this.type === "My Friends") {
        return this.newFriends;
      } else {
        return this.myFriends;
      }
    },
  },
  methods: {
    refresh() {
      this.loadFriends();
      this.loadHobbies();
      if (this.isLoggedIn) {
        this.loadMyFriends();
      }
    },
    setFilters(updatedFilters) {
      this.$store.commit("hobbies/setFilters", updatedFilters);
    },
    loadFriends() {
      this.$store.dispatch("friends/loadFriends");
    },
    loadMyFriends() {
      this.$store.dispatch("friends/loadMyFriends");
    },
    loadHobbies() {
      this.$store.dispatch("hobbies/loadHobbies");
    },
    loadRequests() {
      this.$store.dispatch("friendRequests/loadRequests");
    },
    setSearch(search) {
      this.search = search;
      sessionStorage.setItem("search", search);
    },
    typeSwitch() {
      if (this.type === "My Friends") {
        this.type = "New Friends";
        this.mode = false;
      } else {
        this.type = "My Friends";
        this.mode = true;
      }
    },
  },
  created() {
    this.loadFriends();
    this.loadHobbies();

    if (sessionStorage.search) {
      this.search = sessionStorage.search;
    }
    this.activeFilters = this.$store.getters["hobbies/filters"];

    if (this.isLoggedIn) {
      this.loadMyFriends();
      this.loadRequests();
    }
  },
};
</script>

<style scoped>
h3 {
  text-align: center;
}

ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.controls {
  display: flex;
  justify-content: space-between;
  
}
</style>
