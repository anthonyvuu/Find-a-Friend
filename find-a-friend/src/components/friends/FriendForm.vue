<template>
  <form @submit.prevent="submitForm">
    <div class="form-control" :class="{ error: !firstName.valid }">
      <label for="firstname">Firstname</label>
      <input
        type="text"
        id="firstname"
        v-model.trim="firstName.input"
        @input="changeValidation('firstName')"
      />
      <p v-if="!firstName.valid">Firstname cannot be empty.</p>
    </div>
    <div class="form-control" :class="{ error: !lastName.valid }">
      <label for="lastname">Lastname</label>
      <input
        type="text"
        id="lastname"
        v-model.trim="lastName.input"
        @input="changeValidation('lastName')"
      />
      <p v-if="!lastName.valid">Lastname cannot be empty.</p>
    </div>
    <div class="form-control" :class="{ error: !description.valid }">
      <label for="description">Description</label>
      <textarea
        id="description"
        rows="5"
        v-model.trim="description.input"
        @input="changeValidation('description')"
      ></textarea>
      <p v-if="!description.valid">Description must be filled.</p>
    </div>

    <h3>Hobbies</h3>
    <div :class="{ error: !hobbies.valid }">
      <div class="flex-container">
        <div v-for="hobby in getHobbies" :key="hobby">
          <input
            type="checkbox"
            :id="hobby"
            :value="hobby"
            v-model="hobbies.input"
            @blur="changeValidation('hobbies')"
          />
          <label :for="hobby">{{ hobby }}</label>
        </div>
      </div>
      
      <div class="addHobby">
        <div v-if="addHobby" class="newHobby">
          <form @submit.prevent="">
            <div class="hobbyForm">
              <input @input="changeValidation('newHobby')" type="text" name="hobby" v-model.trim="newHobby.input" placeholder="Enter name for new hobby">
              <button type="submit" @click="hobbyAdded">Add</button>
              <p v-if="!newHobby.valid">Check name of hobby, cant be empty</p>
            </div>
            
          </form>
        </div>
        <base-button mode="outline" type="button" @click="showHobbyForm">{{
        type
      }}</base-button>
        
      </div>
      <p v-if="!hobbies.valid">Select atleast one hobby.</p>
    </div>

    <h3>Profile Image</h3>

    <div class="upload">
      <input type="file" @change="onSelectedImage" />
      
      <div v-if="selectedImage" class="previewImage">
        <img :src="selectedImage" alt="" width="200" height="200" />
      </div>
    </div>

    <p v-if="!validForm">
      Check the form is filled out correctly and try submit again.
    </p>
    <base-button>Register</base-button>
  </form>
</template>

<script>
export default {
  emits: ["save-values"],
  data() {
    return {
      firstName: {
        input: "",
        valid: true,
      },
      lastName: {
        input: "",
        valid: true,
      },
      description: {
        input: "",
        valid: true,
      },
      hobbies: {
        input: [],
        valid: true,
      },
      newHobby: {
        input: "",
        valid: true,
      },
      selectedImage: null,
      type: "Add hobby",
      addHobby: false,
      validForm: true,
    };
  },
  computed: {
    getHobbies() {
      return this.$store.getters["hobbies/hobbies"];
    },
  },

  methods: {
    // reads select image to DataURL to show user a preview of image
    async onSelectedImage(event) {
      this.selectedImage = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = function(e) {
          resolve(e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
      });
    },
    changeValidation(input) {
      this[input].valid = true;
    },
    hobbyAdded() {
      if(this.newHobby.input === "") {
        this.newHobby.valid = false;
      } else {
        this.$emit("new-hobby", this.newHobby.input);
        this.newHobby.input = "";
        this.addHobby = false;
        this.type = "Add hobby";
      }
      
    },

    showHobbyForm() {
      if (this.addHobby) {
        this.addHobby = false;
        this.type = "Add hobby";
      } else {
        this.addHobby = true;
        this.type = "Close";
      }
      
    },

    formValidation() {
      this.validForm = true;
      if (this.firstName.input === "") {
        this.firstName.valid = false;
        this.validForm = false;
      }
      if (this.lastName.input === "") {
        this.lastName.valid = false;
        this.validForm = false;
      }
      if (this.description.input === "") {
        this.description.valid = false;
        this.validForm = false;
      }
      if (this.hobbies.input.length === 0) {
        this.hobbies.valid = false;
        this.validForm = false;
      }
    },
    submitForm() {
      this.formValidation();
      if (!this.validForm) {
        return;
      }
      const formValues = {
        first: this.firstName.input,
        last: this.lastName.input,
        desc: this.description.input,
        hobbies: this.hobbies.input,
        image: this.selectedImage,
      };
      
      this.$emit("save-values", formValues);
    },
  },
};
</script>

<style scoped>
.form-control {
  margin: 0.5rem 0;
}

label {
  font-weight: bold;
  display: block;
  margin-bottom: 0.5rem;
}

input[type="checkbox"] + label {
  font-weight: normal;
  display: inline;
  margin: 0 0 0 0.5rem;
}

.flex-container {
  display: flex;
  flex-wrap: wrap;
}
.flex-container div {
  margin: 10px;
  padding: 0;
}

input,
textarea {
  display: block;
  width: 100%;
  border: 1px solid #ccc;
  font: inherit;
}

input:focus,
textarea:focus {
  background-color: #f0e6fd;
  outline: none;
  border-color: #3d008d;
}
.hobbyForm {
  width: 100%;
  display: inline; 
}

.hobbyForm input {
  width: 90%;
  position: relative;
  display: inline;
}

.hobbyForm button {
  display: inline;
}

input[type="checkbox"] {
  display: inline;
  width: auto;
  border: none;
}

input[type="checkbox"]:focus {
  outline: #3d008d solid 1px;
}

h3 {
  margin: 0.5rem 0;
  font-size: 1rem;
}

.error label {
  color: red;
}

.error input,
.error textarea {
  border: 1px solid red;
}

.previewImage img {
  border-radius: 50%;
}
</style>
