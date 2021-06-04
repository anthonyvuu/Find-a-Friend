import { createApp } from "vue";

import App from "./App.vue";
import router from "./router.js";
import store from "./store/index.js";
import BaseItem from "./components/base/BaseItem.vue";
import BaseButton from "./components/base/BaseButton.vue";
import BaseBadge from "./components/base/BaseBadge.vue";
import BaseDialog from "./components/base/BaseDialog.vue";
 
const app = createApp(App)

app.use(router);
app.use(store);

app.component('base-item', BaseItem);
app.component('base-button', BaseButton);
app.component('base-badge', BaseBadge);
app.component('base-dialog', BaseDialog);

app.mount("#app");


