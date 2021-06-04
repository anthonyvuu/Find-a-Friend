export default {
  async loadHobbies(context) {
    let request = await fetch("http://127.0.0.1:5000/hobbies");

    let response = await request.json();

    let hobbies = response;

    context.commit("setHobbies", hobbies);

    // checkbox for alle hobby, som brukes i filter, register friend, edit profile.
    let filters = {};
    for (let key in hobbies) {
      filters[hobbies[key]] = true;
    }
    context.commit("setFilters", filters);
  },

  async addHobby(context, payload) {

    const newHobby = {
      hobby: payload,
    };
    let request = await fetch("http://127.0.0.1:5000/hobbies", {
      method: "POST",
      body: JSON.stringify(newHobby),
    });

    let response = await request.json();
    
    if (response.ok === "false") {
      const error = new Error(response.message || "Mislykket med å legge til ny hobby");
      throw error;
    } else {
      context.commit("addHobby", payload)
    }
    
  },
};
