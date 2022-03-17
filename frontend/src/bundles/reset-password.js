import Vue from "vue";
import store from "../store";
import ResetPassword from "../components/pages/ResetPassword.vue";
import vuetify from "../plugins/vuetify";
import "../lib/global";

new Vue({
  vuetify,
  store,
  components: { ResetPassword },
  render: (h) => h(ResetPassword),
}).$mount("#reset-password");
