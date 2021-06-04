<template>
  <li>
    <h3>{{ Name.toUpperCase() }}</h3>
    <div>
      <base-badge
        v-for="hobby in hobbies"
        :key="hobby.hobby"
        :type="hobby.backgroundColor"
        :title="hobby.hobby"
      >
      </base-badge>
    </div>

    <div>
      <div class="request-mode" v-if="!buttonClicked">
        <i class="fas fa-check" @click="respondRequest('accept')"></i>
        <i class="fas fa-times" @click="respondRequest('decline')"></i>
      </div>

      <div :class="clicked" v-else>
        <p>{{ clicked }}</p>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  props: ["friendId", "firstName", "lastName", "hobbies"],

  computed: {
    Name() {
      return this.firstName + " " + this.lastName;
    },
  },
  methods: {
    async respondRequest(event) {
      if (event === "accept") {
        await this.$store.dispatch(
          "friendRequests/acceptRequest",
          this.friendId
        );
      } else {
        await this.$store.dispatch(
          "friendRequests/declineRequest",
          this.friendId
        );
      }
      await this.$store.dispatch("friendRequests/loadRequests");
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

h3 {
  font-size: 1.5rem;
  margin: 0.5rem 0;
}

div {
  margin: 0.5rem 0;
}

.fa-check {
  color: green;
  opacity: 0.4;
}

.fa-check:hover {
  opacity: 1;
}

.fa-times {
  color: red;
  opacity: 0.4;
}

.fa-times:hover {
  opacity: 1;
}

.request-mode {
  font-size: 2em;
  display: flex;
  justify-content: flex-end;
  flex-grow: 1;
}

.request-mode i {
  padding: 0.5em;
}

.Accepted {
  color: green;
}

.Declined {
  color: red;
}
</style>
