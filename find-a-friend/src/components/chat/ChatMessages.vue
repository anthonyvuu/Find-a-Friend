<template>
  <div class="list">
    <div class="chat-container">
      <ul class="chat">
        <chat-item
          v-for="(message, idx) in messages"
          :key="idx"
          :message="message"
        ></chat-item>
      </ul>
    </div>
  </div>
</template>

<script>
import ChatItem from "../chat/ChatItem.vue";
export default {
  components: { ChatItem },
  props: ["messages"],

  methods: {},
};
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column-reverse;
  overflow: scroll;
  max-height: 520px;
  border-top: 1px solid lightgray
}

.chat {
  list-style-type: none;
  margin: 0;
  padding-left: 0;
  display: flex;
  flex-direction: column;
}
</style>
