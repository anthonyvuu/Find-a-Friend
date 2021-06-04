export default {
    setHobbies(state, payload) {
        state.hobbies = payload;
    },
    setFilters(state,payload) {
        state.filters = payload;
    },
    addHobby(state,payload) {
        state.hobbies.push(payload);
    }
};