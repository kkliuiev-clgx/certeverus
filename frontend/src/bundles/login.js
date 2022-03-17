import Vue from "vue";
import store from "../store";
import Login from "../components/pages/Login.vue";
import vuetify from "../plugins/vuetify";
import "../lib/global";

new Vue({
  vuetify,
  store,
  components: { Login },
  render: (h) => h(Login),
}).$mount("#login");
