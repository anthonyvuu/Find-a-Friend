<template>
  <section>
    <base-dialog :show="!!error" title="Error" @click="confirmError">
      <p>{{ error }}</p>
    </base-dialog>
    <base-item>
      <h2>Register as a friend</h2>
      <friend-form @save-values="saveValues" @new-hobby="newHobby"></friend-form>
    </base-item>
  </section>
</template>

<script>
import BaseDialog from '../../components/base/BaseDialog.vue';
import FriendForm from "../../components/friends/FriendForm.vue";

export default {
  components: {
    FriendForm,
    BaseDialog,
  },

  data() {
    return {
      error: null
    }
  },

  methods: {
    async saveValues(values) {
      try {
        await this.$store.dispatch("friends/registerFriend", values);
        this.$router.replace("/friends");
      } catch (err) {
        this.error = err.message || "feilet med å registrere";
      }
    },
    async newHobby(value) {
      try {
        await this.$store.dispatch("hobbies/addHobby", value);
        
      } catch (err) {
        this.error = err.message || "feilet med å registrere";
      }
      
    },
    confirmError() {
      this.error = null;
    },
  },
};
</script>
