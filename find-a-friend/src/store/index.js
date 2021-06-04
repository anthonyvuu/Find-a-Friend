import { createStore } from "vuex";

import friendModules from "./modules/friends/index.js";
import authenticationModules from "./modules/authentication/index.js";
import hobbiesModules from "./modules/hobbies/index.js";
import friendRequestsModules from "./modules/friendRequests/index.js";
import imageModules from "./modules/images/index.js";
import chatModules from "./modules/chat/index.js";

const store = createStore({
  modules: {
    friends: friendModules,
    authentication: authenticationModules,
    hobbies: hobbiesModules,
    friendRequests: friendRequestsModules,
    images: imageModules,
    chat: chatModules,
  },
});

export default store;
