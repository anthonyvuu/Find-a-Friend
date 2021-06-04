export default {
  async sendMessage(_, payload) {
    console.log(payload);
    let msgData = {
      firstName: payload.firstName,
      date: new Date().toLocaleDateString(),
      isAttachment: payload.isAttachment,
      message: payload.message,
      channel: payload.channel,
    };

    let request = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      body: JSON.stringify(msgData),
    });

    let response = await request.json();
    
    if (response.ok === "false") {
      const error = new Error(response.message || "Feil fil format");
      throw error;
    }

  },

  async loadChatmessages(_, payload) {
    let request = await fetch("http://127.0.0.1:5000/chat/" + payload);

    let response = await request.json();

    return Promise.resolve(response);
  },
};
