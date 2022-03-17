import Vue from "vue";
import Vuex from "vuex";

// Global modules
import site from "./modules/site";

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    site,
  },
});
