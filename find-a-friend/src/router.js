import { createRouter, createWebHistory } from "vue-router";

import FriendDetail from "./pages/friends/FriendDetail.vue";
import FriendRegistration from "./pages/friends/FriendRegistration.vue";
import FriendsList from "./pages/friends/FriendsList.vue";
import RequestList from "./pages/friendRequests/RequestList.vue";

import NotFound from "./pages/NotFound.vue";
import Authentication from "./pages/auth/Authentication.vue";
import ProfileFriend from "./pages/profile/ProfileFriend.vue";
import ProfileEdit from "./pages/profile/ProfileEdit.vue";
import ChatFriend from "./pages/chat/ChatFriend.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", redirect: "/friends" },
    { path: "/friends", component: FriendsList },
    {
      path: "/friends/:friendId",
      component: FriendDetail,
      props: true,
    },
    { path: "/friends/:friendId/chat", component: ChatFriend, props: true },
    {
      path: "/profile",
      component: ProfileFriend,
    },
    { path: "/edit", component: ProfileEdit },
    { path: "/requests", component: RequestList },
    {
      path: "/register",
      component: FriendRegistration,
      meta: { notFriend: true },
    },
    { path: "/auth", component: Authentication },
    { path: "/:notFound(.*)", component: NotFound },
  ],
});

export default router;
