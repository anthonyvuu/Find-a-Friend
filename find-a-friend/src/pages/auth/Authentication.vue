<template>
  <div>
    <base-dialog :show="!!error" title="Error" @click="confirmError">
      <p>{{ error }}</p>
    </base-dialog>
    <base-item>
      <form @submit.prevent="submitForm">
        <div class="form-inputs">
          <label for="email">E-Mail</label>
          <input type="email" id="email" v-model="email" />
        </div>
        <div class="form-inputs">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" />
        </div>

        <p v-if="!valid">
          Enter a valid email and password (minimum length of 4 characters)
        </p>
        <base-button>{{ submitbuttonText }}</base-button>
        <base-button type="button" mode="flat" @click="typeSwitch">{{
          typebutton
        }}</base-button>
      </form>
    </base-item>
  </div>
</template>

<script>
import BaseDialog from "../../components/base/BaseDialog.vue";

export default {
  components: { BaseDialog },
  data() {
    return {
      email: "",
      password: "",
      valid: true,
      type: "login",
      error: null,
    };
  },
  computed: {
    submitbuttonText() {
      if (this.type === "login") {
        return "Login";
      } else {
        return "Sign Up";
      }
    },
    typebutton() {
      if (this.type === "login") {
        return "Signup instead";
      } else {
        return "Login instead";
      }
    },
  },
  methods: {
    async submitForm() {
      this.valid = true;
      if (this.email === "" || this.password.length < 4) {
        this.valid = false;
        return;
      }

      try {
        if (this.type === "login") {
          await this.$store.dispatch("authorize", {
            type: this.type,
            email: this.email,
            password: this.password,
          });
        } else {
          await this.$store.dispatch("authorize", {
            type: this.type,
            email: this.email,
            password: this.password,
          });
        }
        this.$router.replace("/friends");

      } catch (err) {
        this.error = err.message || "failed";
        console.log(this.error);
      }
    },
    typeSwitch() {
      if (this.type === "login") {
        this.type = "signup";
      } else {
        this.type = "login";
      }
    },
    confirmError() {
      this.error = null;
    },
  },
  
};
</script>

<style scoped>
form {
  margin: 1rem;
  padding: 1rem;
}

.form-inputs {
  margin: 0.5rem 0;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  display: block;
}

input,
textarea {
  display: block;
  width: 100%;
  font: inherit;
  border: 1px solid #ccc;
  padding: 0.15rem;
}

input:focus,
textarea:focus {
  border-color: #3d008d;
  background-color: #faf6ff;
  outline: none;
}
</style>
