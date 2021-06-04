export default {
  async sendRequest(_, payload) {
    const requestData = {
      friendId: sessionStorage.friendId,
      requesttoId: payload.requesttoId,
    };
   

    let request = await fetch("http://127.0.0.1:5000/requests", {
      method: "POST",
      body: JSON.stringify(requestData),
    });

    let response = await request.json();

    if (response.ok === "false") {
      const error = new Error(response.message || "failed to signup");
      throw error;
    } 
  },

  async loadRequests(context) {
    let request = await fetch("http://127.0.0.1:5000/requests/" + sessionStorage.friendId)

    let response = await request.json();

    context.commit("setRequests", response);
  },

  async acceptRequest(_, payload) {
    const respondData = {
      friendId: sessionStorage.friendId,
      friendWith: payload
    };

    await fetch("http://127.0.0.1:5000/myfriends", {
      method: "POST",
      body: JSON.stringify(respondData),
    });

  },

  async declineRequest(_, payload) {
    const respondData = {
      friendId: sessionStorage.friendId,
      friendWith: payload
    };
    await fetch("http://127.0.0.1:5000/myfriends", {
      method: "DELETE",
      body: JSON.stringify(respondData)
    });

   
  }
};
