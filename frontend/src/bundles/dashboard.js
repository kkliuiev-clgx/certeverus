import Vue from "vue";
import store from "../store";
import Dashboard from "../components/pages/Dashboard.vue";
import vuetify from "../plugins/vuetify";
import "../lib/global";

new Vue({
  vuetify,
  store,
  components: { Dashboard },
  render: (h) => h(Dashboard),
}).$mount("#dashboard");
