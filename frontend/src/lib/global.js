import Vue from "vue";
import SiteMixin from "../mixins/SiteMixin";
import "@mdi/font/css/materialdesignicons.css"; // Ensure you are using css-loader
import axios from "axios";
import Notifications from "vue-notification";
import velocity from "velocity-animate";

Vue.config.productionTip = false;
Vue.prototype.$http = axios;

// These two lines are required to setup axios to work with django csrf_token
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

Vue.mixin(SiteMixin);
Vue.use(Notifications, { velocity });
