<template>
  <div class="message-input">
    <input
      id="input"
      type="text"
      placeholder="Enter your message"
      v-model="messageInput"
      v-on:input="checkemoji"
      v-on:keyup.enter="send_message"
    />
    <span @click="$refs.fileInput.click()"
      ><i class="fas fa-file-image"></i
    ></span>
    <input
      type="file"
      style="display : none"
      ref="fileInput"
      @change="sendAttachment"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedFile: {
        name: null,
        data: null,
      },
      messageInput: "",
      emojis: {
        XD: "😁",
        ":')": "😂",
        "8)": "😄",
        ":)": "😊",
        ":angry": "😡",
        ":*": "😘",
        ":scream": "😱",
        ":sleepy": "😪",
      },
    };
  },
  methods: {
    async sendAttachment(event) {
      this.selectedFile.data = await new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = function(e) {
          resolve(e.target.result);
        };
        reader.readAsDataURL(event.target.files[0]);
        this.selectedFile.name = event.target.files[0].name;
      });
      this.$emit("send_attachment", this.selectedFile.name, this.selectedFile.data);
      
    },
    send_message() {
      this.$emit("send_message", this.messageInput);
      this.messageInput = "";
    },
    checkemoji() {
      let input = this.messageInput && this.messageInput.split(" ");
      let newtext = [];

      if (input) {
        input.forEach((word) => {
          let substring = word;
          if (substring in this.emojis) {
            substring = this.emojis[word];
          }
          newtext.push(substring);
        });
      }
      this.messageInput = newtext.join(" ");
    },
  },
};
</script>

<style scoped>
.message-input {
  position: relative;
  width: 100%;
}
span {
  position: absolute;
  right: 2%;
  top: 10px;
}

i {
  font-size: 20px;
}
i:hover {
  opacity: 0.4;
}

.message-input input {
  border-top: 1px solid black;
  font-size: 20px;
  height: 40px;
  width: 95%;
  outline: none;
}
</style>
