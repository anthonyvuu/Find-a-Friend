<template>
  <div>
    <base-dialog :show="!!error" title="Error" @click="confirmError">
      <p>{{ error }}</p>
    </base-dialog>
    <base-item class="chatWith">
      <img class="profilePicutre" :src="selectedFriend.image" alt="" />
      <h2>{{ name }}</h2>
    </base-item>

    <base-item class="chatbox">
      <chat-messages :messages="messages"></chat-messages>
      <chat-input @send_message="send_message" @send_attachment="send_attachment"></chat-input>
    </base-item>
    
    <p></p>
  </div>
</template>

<script>
import ChatInput from "../../components/chat/ChatInput.vue";
import ChatMessages from "../../components/chat/ChatMessages.vue";
import Pusher from "pusher-js";

export default {
  components: {
    ChatInput,
    ChatMessages,
  },
  props: ["friendId"],

  data() {
    return {
      selectedFriend: null,
      channel: "",
      messages: null,
      error: null,
    };
  },
  computed: {
    username() {
      return this.mySelf[0].firstName;
    },
    mySelf() {
      return this.$store.getters["friends/mySelf"];
    },
    name() {
      return (
        this.selectedFriend.firstName +
        " " +
        this.selectedFriend.lastName
      ).toUpperCase();
    },
  },
  methods: {
    async send_attachment(name, data) {
      let payload = {
        firstName: this.username,
        isAttachment: true,
        message: {
          fileName: name,
          fileData: data
        },
        channel: this.channel,
      };
      try {
        await this.$store.dispatch("chat/sendMessage", payload);
      } catch (err) {
        this.error = err.message || "feilet med å registrere";
      }
    },
    async send_message(message) {
      let payload = {
        firstName: this.username,
        isAttachment: false,
        message: message,
        channel: this.channel,
      };
      try {
        await this.$store.dispatch("chat/sendMessage", payload);
      } catch (err) {
        this.error = err.message || "feilet med å registrere";
      }
    },
    async loadChatmessages() {
      let messages = await this.$store.dispatch(
        "chat/loadChatmessages",
        this.channel
      );

      this.messages = messages;
    },
    confirmError() {
      this.error = null;
    },
  },
  created() {
    this.selectedFriend = this.$store.getters["friends/friends"].find(
      (friend) => friend.friendId === this.friendId
    );

    if (sessionStorage.friendId > this.friendId) {
      this.channel = this.friendId + sessionStorage.friendId;
    } else {
      this.channel = sessionStorage.friendId + this.friendId;
    }
    this.loadChatmessages();

    var pusher = new Pusher("d03450301bfcf65bbaeb", {
      cluster: "eu",
    });

    const channel = pusher.subscribe(this.channel);
    channel.bind("new-message", (data) => {
      console.log(data);
      this.loadChatmessages();
    });
  },
  beforeUnmount() {
    this.$store.commit('chat/removeNotification', String(this.friendId));
  }
};
</script>

<style scoped>
.chatbox {
  height: 600px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}

.chatWith {
  text-align: center;
}

.chatWith img {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}
</style>
