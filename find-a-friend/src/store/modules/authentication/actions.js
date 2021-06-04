export default {
  //automatisk logger brukeren inn visst siden refreshes, grunnet hvordan vuex store fungerer med at, ved reload så vil alle store states også forsvinne.
  autoLogin(context) {
    const friendId = sessionStorage.getItem("friendId");
    if (friendId) {
      context.commit("setFriend", {
        friendId: friendId,
      });
    }
  },
  logout(context) {
    sessionStorage.removeItem("friendId");
    context.commit("setFriend", {
      friendId: null,
    });
  },

  async authorize(context, payload) {
    const userData = {
      type: payload.type,
      email: payload.email,
      password: payload.password,
    };

    let request = await fetch("http://127.0.0.1:5000/auth", {
      method: "POST",
      body: JSON.stringify(userData),
    });

    let response = await request.json();

    if (response.ok === "false") {
      const error = new Error(response.message || "failed to signup");
      throw error;
    }
   

    sessionStorage.setItem("friendId", response.id);

    context.commit("setFriend", {
      friendId: response.id,
    });
  },
};
