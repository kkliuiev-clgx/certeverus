<script>
import Vue from "vue";
import URLS from "../constants/urls/routes";

export default {
  data() {
    return {
      django: {},
      user: {},
    };
  },
  beforeMount: function() {
    try {
      this.django = JSON.parse(document.getElementById("data").dataset.django);
      this.user = this.django.user;
      // eslint-disable-next-line
    } catch (err) {}
  },
  mounted() {
    // This message was saved before page was
    // refreshed so show it now then delete it
    const msg = localStorage.getItem("refreshMessage");
    const msgType = localStorage.getItem("refreshMessage");

    if (msg) {
      localStorage.setItem("refreshMessage", "");
      localStorage.setItem("refreshMessageType", "");
      this.showNotification(msgType, msg);
    }
  },
  computed: {
    isAuthenticated() {
      return this.user.username;
    },
    drawerOpen: {
      get() {
        return this.$store.getters["site/getDrawer"];
      },
      set(newValue) {
        this.$store.dispatch("site/setDrawer", newValue);
      },
    },
  },
  methods: {
    copy(json) {
      // Recommended way to copy vue object data is to parse the stringified object
      return JSON.parse(JSON.stringify(json));
    },
    setChart(chartType) {
      this.$store.dispatch("site/setCurrentChart", chartType);
    },
    toggleDrawer() {
      const isOpen = this.drawerOpen;
      this.$store.dispatch("site/setDrawer", !isOpen);
    },
    showNotification(type, msg) {
      Vue.notify({
        group: "topRightNotification",
        type: type,
        text: msg,
      });
    },
    logout() {
      if (confirm("Are you sure you want to logout?")) {
        this.post(URLS.get("logout"), this);
      }
    },
    setNotificationOnNextRefresh(type, msg) {
      localStorage.setItem("refreshMessageType", type);
      localStorage.setItem("refreshMessage", msg);
    },
    post(url, vm) {
      return vm.$http
        .post(url, vm.model)
        .then((response) => {
          if (response.data.success == true) {
            if (response.data.redirect) {
              if (response.data.message) {
                // Save the message so it is shown on refresh
                vm.setNotificationOnNextRefresh(
                  "success",
                  response.data.message
                );
              }
              window.location.href = response.data.redirect;
            } else {
              if (response.data.message) {
                vm.showNotification("success", response.data.message);
              }
            }
          } else {
            if (response.data.errors) {
              vm.errors = Object.assign(
                vm.copy(vm.errors),
                response.data.errors
              );
            }

            if (vm.errors.__all__) {
              vm.showNotification("error", vm.errors.__all__.join(", "));
            } else if (response.data.message) {
              vm.showNotification("error", response.data.message);
            }
          }
        })
        .catch((error) => {
          if (error.response.data.errors) {
            vm.errors = Object.assign(
              vm.copy(vm.errors),
              error.response.data.errors
            );
          }
          if (vm.errors.__all__) {
            vm.showNotification("error", vm.errors.__all__.join(", "));
          } else if (error.response.data.message) {
            vm.showNotification("error", error.response.data.message);
          }
        });
    },
    get(url, vm) {
      let params = {};
      if (vm.model.params) {
        params = vm.model.params;
      }
      return vm.$http.get(url, { params: params });
    },
    goToUrl(name) {
      if (window.location.pathname != URLS.get(name)) {
        window.location.href = URLS.get(name);
      }
    },
  },
};
</script>
