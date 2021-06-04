export default {
  async uploadImage(_, payload) {
    let imageData = {
      friendId: sessionStorage.friendId,
      filename: payload.filename,
      image: payload.data
    }
    let request = await fetch('http://127.0.0.1:5000/images', {
        method: "POST",
        body: JSON.stringify(imageData),
    });
    let response = await request.json();

    if (response.ok === "false") {
      const error = new Error(response.message || "Feil bilde format");
      throw error;
    }
  },

  async deleteImage(_,payload) {
    let request = await fetch('http://127.0.0.1:5000/images/' + payload, {
        method: "DELETE",
    });
    await request.json();

  },
  async loadImages(context, payload) {
    let request = await fetch('http://127.0.0.1:5000/images/' + payload);

    let result = await request.json();
    
    context.commit("setImages",result);

    return Promise.resolve(result);
    
  },

};
