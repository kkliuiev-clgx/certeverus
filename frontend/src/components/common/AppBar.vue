<template>
  <v-app-bar height="75" color="#fff" app>
    <v-app-bar-nav-icon
      v-if="isAuthenticated"
      @click="toggleDrawer()"
    ></v-app-bar-nav-icon>
    <v-toolbar-title v-if="!drawerOpen">
      <v-img max-width="200" src="@/assets/CVAI-logo.jpg"></v-img>
    </v-toolbar-title>

    <v-spacer></v-spacer>

    <a class="dashboard nav-btn" v-if="isAuthenticated">
      <img
        v-if="user.avatar"
        class="dashboard avatar"
        width="40"
        height="36"
        :src="user.avatar"
      />
      <v-icon size="33" v-if="!user.avatar" color="grey">mdi-account</v-icon>
      <small>{{ user.first_name }} {{ user.last_name }}</small>
    </a>

    <div id="navbar-links" v-if="!isAuthenticated">
      <a
        :href="URLS.get('login')"
        :class="this.currentRoute === URLS.get('login') ? 'active' : ''"
        class="nav-li"
        >Login</a
      >

      <a
        :href="URLS.get('signup')"
        :class="this.currentRoute === URLS.get('signup') ? 'active' : ''"
        class="nav-li"
        >Signup</a
      >

      <a
        :href="URLS.get('reset_password_step_1')"
        :class="
          this.currentRoute === URLS.get('reset_password_step_1')
            ? 'active'
            : ''
        "
        class="nav-li"
        >Reset Password</a
      >
    </div>
  </v-app-bar>
</template>

<script>
import URLS from "../../constants/urls/routes";

export default {
  name: "AppBar",
  data() {
    return {
      URLS: URLS,
    };
  },
  computed: {
    currentRoute() {
      return window.location.pathname;
    },
  },
};
</script>

<style scoped src="@/assets/style.css">
.ml-5 {
  margin-left: 5px;
}
</style>
