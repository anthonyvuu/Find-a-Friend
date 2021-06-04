export default {
  friendId(state) {
    return state.friendId;
  },
  isLoggedIn(state) {
    return !!state.friendId;
  }
};
