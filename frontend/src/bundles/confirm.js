import Vue from "vue";
import store from "../store";
import Confirm from "../components/pages/Confirm.vue";
import vuetify from "../plugins/vuetify";
import "../lib/global";

new Vue({
  vuetify,
  store,
  components: { Confirm },
  render: (h) => h(Confirm),
}).$mount("#confirm");
