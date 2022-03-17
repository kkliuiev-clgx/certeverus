<template>
  <v-app>
    <NavigationDrawer> </NavigationDrawer>
    <AppBar> </AppBar>
    <v-main>
      <v-container fluid> </v-container>
    </v-main>

    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import URLS from "../../constants/urls/routes";
import AppBar from "../common/AppBar";
import NavigationDrawer from "../common/NavigationDrawer";

export default {
  name: "Confirm",
  components: {
    AppBar,
    NavigationDrawer,
  },
  created() {
    // TODO - similar code is in ResetPassword - make DRY
    let redirect = URLS.get("login");
    try {
      const djangoData = JSON.parse(localStorage.getItem("djangoData"));
      if (djangoData.message) {
        if (djangoData.success) {
          if (djangoData.redirect) {
            redirect = djangoData.redirect;
          }
          this.setNotificationOnNextRefresh("success", djangoData.message);
        } else {
          this.setNotificationOnNextRefresh("error", djangoData.message);
        }
      }
      // eslint-disable-next-line
    } catch (err) {}

    window.location.href = redirect;
  },
};
</script>
