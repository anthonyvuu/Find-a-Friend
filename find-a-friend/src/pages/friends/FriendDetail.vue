<template>
  <div>
    <section>
      <base-item>
        <img
          v-if="profilePicture !== 'NULL'"
          class="profilePicture"
          :src="profilePicture"
          alt=""
        />
        <h2>{{ name }}</h2>
      </base-item>
    </section>
    <section>
      <base-item>
        <p>{{ description }}</p>
        <base-badge
          v-for="hobby in hobbies"
          :key="hobby.hobby"
          :type="hobby.backgroundColor"
          :title="hobby.hobby"
        ></base-badge>
      </base-item>
      <base-item>
        <h2>Gallery</h2>
        <friend-gallery :images="images"></friend-gallery>
      </base-item>
    </section>
  </div>
</template>

<script>
import FriendGallery from "./FriendGallery.vue";

export default {
  components: { FriendGallery },
  props: ["friendId"],
  data() {
    return {
      selectedFriend: null,
      images: [],
    };
  },
  computed: {
    name() {
      return (
        this.selectedFriend.firstName.toUpperCase() +
        " " +
        this.selectedFriend.lastName.toUpperCase()
      );
    },
    profilePicture() {
      return this.selectedFriend.image;
    },
    contactLink() {
      return this.$route.path + "/contact";
    },
    hobbies() {
      return this.selectedFriend.hobbies;
    },
    description() {
      return this.selectedFriend.description;
    },
  },
  methods: {
    async loadImages() {
      let images = await this.$store.dispatch("images/loadImages",this.selectedFriend.friendId);
      this.images = images;
    },
  },
  created() {
    this.selectedFriend = this.$store.getters["friends/friends"].find(
      (friend) => friend.friendId === this.friendId
    );
    this.loadImages();
  },
};
</script>

<style scoped>
div {
  text-align: center;
}

.profilePicture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}
</style>
