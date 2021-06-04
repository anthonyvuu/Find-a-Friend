export default {
  setFriends(state, payload) {
    state.friends = payload;
  },
  setMyFriends(state, payload) {
    state.myFriends = payload;
  },
  setRequests(state, payload) {
    state.requests = payload;
  },
};
