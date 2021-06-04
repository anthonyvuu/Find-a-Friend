export default {
  addMessage(state, payload) {
    state.messages.push(payload);
  },
  setChatmessages(state, payload) {
    state.messages = payload;
  },
  addNotification(state, payload) {
    if (!state.notification.includes(payload)) {
      state.notification.push(payload);
    } else {
      return;
    }
  },
  removeNotification(state, payload) {
    var index = state.notification.indexOf(payload);
    state.notification.splice(index, 1);
  },
};
