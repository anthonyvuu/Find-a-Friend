<template>
  <div>
    <base-dialog :show="!!error" title="Error" @click="confirmError">
      <p>{{ error }}</p>
    </base-dialog>

    <base-dialog :show="!!imageDelete" title="Delete" @exit="cancelDelete">
      <p>Sure you want to delete image?</p>
      <div class="confirm">
        <i class="fas fa-check" @click="confirmDelete"></i>
      </div>
    </base-dialog>

    <base-item class="container">
      <img class="profilePicture" :src="profilePicture" alt="" />

      <h2>{{ name }}</h2>
      <base-button mode="outline" link to="/edit">Edit profile</base-button>
    </base-item>

    <base-item class="information">
      <p>{{ description }}</p>
      <base-badge
        v-for="hobby in myHobbies"
        :key="hobby.hobby"
        :type="hobby.backgroundColor"
        :title="hobby.hobby"
      ></base-badge>
    </base-item>

    <base-item>
      <h2>Gallery</h2>
      <friend-gallery :images="images" @select="deleteImage"></friend-gallery>
      <div class="upload">
        <input type="file" @change="onSelectedFile" ref="fileInput" />
        <button @click="onUpload">Submit</button>
      </div>
    </base-item>
  </div>
</template>

<script>
import FriendGallery from "../friends/FriendGallery.vue";

export default {
  components: { FriendGallery },
  data() {
    return {
      selectedFile: null,
      selectedFileName: null,
      error: null,
      imageDelete: null,
    };
  },
  computed: {
    description() {
      return this.mySelf.description;
    },
    name() {
      return (this.mySelf.firstName + " " + this.mySelf.lastName).toUpperCase();
    },
    myHobbies() {
      return this.mySelf.hobbies;
    },
    profilePicture() {
      return this.mySelf.image;
    },
    hasImages() {
      return this.images.length > 0;
    },
    images() {
      return this.$store.getters["images/getImages"];
    },
    mySelf() {
      return this.$store.getters["friends/mySelf"][0];
    },
  },
  methods: {
    async onSelectedFile(event) {
      this.selectedFile = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = function(e) {
          resolve(e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
        this.selectedFileName = event.target.files[0].name;
      });
    },
    confirmError() {
      this.error = null;
    },
    deleteImage(imageId) {
      this.imageDelete = imageId;
    },
    cancelDelete() {
      this.imageDelete = null;
    },
    async confirmDelete() {
      await this.$store.dispatch("images/deleteImage", this.imageDelete);
      this.imageDelete = null;
      this.loadImages();
    },
    async onUpload() {
      let payload = {
        filename: this.selectedFileName,
        data: this.selectedFile,
      };
      try {
        await this.$store.dispatch("images/uploadImage", payload);
        
        this.loadImages();
      } catch (err) {
        this.error = err.message;
      }
    },
    loadImages() {
      this.$store.dispatch("images/loadImages", sessionStorage.friendId);
    },
  },
  created() {
    this.loadImages();
  },
};
</script>

<style scoped>
* {
  text-align: center;
}

.profilePicture {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}
i {
  font-size: 30px;
  color: green;
  opacity: 0.4;
}

i:hover {
  opacity: 1;
}

.confirm {
  padding: 5px;
  display: flex;
  justify-content: center;
  align-content: center;
}
</style>
