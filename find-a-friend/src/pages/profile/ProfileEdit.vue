<template>
  <base-item class="edit">
    <h2>Edit Profile</h2>
    <form @submit.prevent="submitEdit">
      <div class="description" :class="{ error: !myDescription.valid }">
        <label for="description">Description</label>
        <textarea
          id="description"
          rows="5"
          v-model.trim="myDescription.input"
          @input="changeValidation('myDescription')"
        ></textarea>
        <p v-if="!myDescription.valid">Description must be filled.</p>
      </div>

      <h3>Hobbies</h3>
      <div :class="{ error: !myHobbies.valid }">
        <div class="flex-container">
          <div v-for="hobby in getHobbies" :key="hobby">
            <input
              type="checkbox"
              :id="hobby"
              :value="hobby"
              v-model="myHobbies.input"
              @blur="changeValidation('myHobbies')"
            />
            <label :for="hobby">{{ hobby }}</label>
          </div>
        </div>
        <p v-if="!myHobbies.valid">Select atleast one hobby.</p>
      </div>
      <h3>Profile Image</h3>
      <p>Selected Image: {{profileImage.id}}</p>
      <friend-gallery :images="images" @select="selectProfile" class="images"></friend-gallery>
      
      <div class="buttons">
        <base-button>Edit</base-button>
        <base-button type="button" mode="outline" @click="cancel">Cancel</base-button>
      </div>
    </form>
  </base-item>
</template>

<script>
import FriendGallery from '../friends/FriendGallery.vue';
export default {
  components: { FriendGallery },
  data() {
    return {
      myDescription: {
        input: "",
        valid: true,
      },
      myHobbies: {
        input: [],
        valid: true,
      },
      validForm: true,
      profileImage: {
        id: null,
        data: null,
      },
    };
  },
  methods: {
    selectProfile(imageId,imageData) {
      this.profileImage.id = imageId;
      this.profileImage.data = imageData;
    },

    mySelf() {
      this.myDescription.input = this.$store.getters["friends/mySelf"][0].description;
      let hobbies = this.$store.getters["friends/mySelf"][0].hobbies;
      hobbies.forEach((element) => {
        this.myHobbies.input.push(element.hobby);
      });
    },
    formValidation() {
      this.validForm = true;
      if (this.myDescription.input === "") {
        this.myDescription.valid = false;
        this.validForm = false;
      }
      if (this.myHobbies.input.length === 0) {
        this.myHobbies.valid = false;
        this.validForm = false;
      }
    },
    changeValidation(input) {
      this[input].valid = true;
    },
    async submitEdit() {
      this.formValidation();
      if (!this.validForm) {
        return;
      }
      let editFriendData = {
        description: this.myDescription.input,
        hobbies: this.myHobbies.input,
        image: this.profileImage.data
      }
      await this.$store.dispatch("friends/editFriend", editFriendData)
      this.$router.replace("/friends");
    },
    cancel() {
      this.$router.replace("/profile");
    },
  },
  computed: {
    getHobbies() {
      return this.$store.getters["hobbies/hobbies"];
    },
    images() {
      return this.$store.getters["images/getImages"];
    },
  },
  created() {
    this.mySelf();
  },
};
</script>

<style scoped>

.error label {
  color: red;
}

.error input,
.error textarea {
  border: 1px solid red;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

.buttons {
  display: flex;
  justify-content: center;
}

textarea {
  width: 100%;

  display: block;
  width: 100%;
  border: 1px solid #ccc;
  font: inherit;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}
.flex-container div {
  margin: 10px;
  padding: 0;
}
input[type="checkbox"] + label {
  font-weight: normal;
  display: inline;
  margin: 0 0 0 0.5rem;
}

h3 {
  margin: 0.5rem 0;
  font-size: 1rem;
}

textarea:focus {
  background-color: #f0e6fd;
  outline: none;
  border-color: #3d008d;
}
</style>
