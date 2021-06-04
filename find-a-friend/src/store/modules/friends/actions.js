export default {
  async registerFriend(context, payload) {
    const friendData = {
      friendId: context.rootGetters.friendId,
      firstName: payload.first,
      lastName: payload.last,
      description: payload.desc,
      hobbies: payload.hobbies,
      image: payload.image,
    };

    let request = await fetch("http://127.0.0.1:5000/friends", {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify(friendData),
    });

    let response = await request.json();

    if (response.ok === "false") {
      const error = new Error(response.message || "Mislykket med å registrere");
      throw error;
    }
  },

  async loadFriends(context) {
    let request = await fetch(`http://127.0.0.1:5000/friends`);

    let response = await request.json();

    let friends = [];

    for (let friend in response) {
      let hobbies = [];
      for (let index in response[friend].hobbies) {
        hobbies.push({
          hobby: response[friend].hobbies[index].hobby,
          backgroundColor: response[friend].hobbies[index].backgroundColor,
        });
      }

      const friendData = {
        friendId: response[friend].friendId,
        firstName: response[friend].firstName,
        lastName: response[friend].lastName,
        description: response[friend].description,
        image: response[friend].image,
        hobbies: hobbies,
      };

      friends.push(friendData);
    }

    context.commit("setFriends", friends);
  },

  async loadMyFriends(context) {
    let request = await fetch("http://127.0.0.1:5000/myfriends/" + sessionStorage.friendId);

    let response = await request.json();

    context.commit("setMyFriends", response);
  },

  async editFriend(_, payload) {
    const editFriendData = {
      description: payload.description,
      hobbies: payload.hobbies,
      image: payload.image,
    };
    await fetch(
      "http://127.0.0.1:5000/friends/" + sessionStorage.friendId,
      {
        method: "PUT",
        body: JSON.stringify(editFriendData),
      }
    );

  },
};
