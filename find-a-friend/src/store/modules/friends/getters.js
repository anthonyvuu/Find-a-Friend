export default {
  friends(state) {
    return state.friends;
  },
  isFriend(state) {
    const friends = state.friends;
    let friendId = sessionStorage.getItem("friendId");
    return friends.some((friend) => friend.friendId === friendId);
  },
  mySelf(state) {
    const friends = state.friends;
    let friendId = sessionStorage.getItem("friendId");
    return friends.filter(friend => friend.friendId === friendId);
  },
  myFriends(state) {
    const friends = state.friends;
    const myfriends = state.myFriends;
    
    return friends.filter((friend) => myfriends.includes(friend.friendId) && friend.friendId != sessionStorage.friendId)
  },
  newFriends(state) {
    const friends = state.friends;
    const myfriends = state.myFriends;
    return friends.filter((friend) => !myfriends.includes(friend.friendId) ) 
  },
};
