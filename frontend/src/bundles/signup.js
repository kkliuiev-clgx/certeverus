import Vue from "vue";
import store from "../store";
import Signup from "../components/pages/Signup.vue";
import vuetify from "../plugins/vuetify";
import "../lib/global";

new Vue({
  vuetify,
  store,
  components: { Signup },
  render: (h) => h(Signup),
}).$mount("#signup");
