import Vue from "vue";

export default {
  namespaced: true,
  state: {
    data: {
      drawerOpen: false,
      currentChart: "waterfall",
    },
  },
  getters: {
    getDrawer: (state) => state.data.drawerOpen,
    getCurrentChart: (state) => state.data.currentChart,
  },
  actions: {
    setDrawer(context, value) {
      context.commit("setDrawer", value);
    },
    setCurrentChart(context, value) {
      context.commit("setCurrentChart", value);
    },
  },
  mutations: {
    setDrawer(state, value) {
      Vue.set(state.data, "drawerOpen", value);
    },
    setCurrentChart(state, value) {
      Vue.set(state.data, "currentChart", value);
    },
  },
};
