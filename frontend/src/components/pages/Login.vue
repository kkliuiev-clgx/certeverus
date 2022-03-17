<template>
  <v-app>
    <NavigationDrawer> </NavigationDrawer>
    <AppBar> </AppBar>

    <v-main>
      <v-container fluid>
        <v-container>
          <h2>Login</h2>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.username"
                label="Username"
                :error-messages="errors.username"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.password"
                label="Password"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show ? 'text' : 'password'"
                name="input-10-1"
                hint="At least 8 characters"
                :error-messages="errors.password"
                @click:append="show = !show"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
           <v-form @submit="submit">
            <v-btn class="cvbutton" @click="submit">Login</v-btn>
           </v-form> 
          </v-row>
        </v-container>
        <notifications
          group="topRightNotification"
          position="top right"
          animation-type="velocity"
        />
      </v-container>
    </v-main>

     <!-- Privacy and cookies -->
      <PrivacyAndCookiesDialog />
      
    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import URLS from "../../constants/urls/routes";
import AppBar from "../common/AppBar";
import NavigationDrawer from "../common/NavigationDrawer";
import PrivacyAndCookiesDialog from '../common/PrivacyAndCookiesDialog';

require('@/assets/style.css')

export default {
  name: "Login",
  components: {
    AppBar,
    NavigationDrawer,
    PrivacyAndCookiesDialog,
  },
  data: () => ({
    model: {
      username: "",
      password: "",
    },
    show: false,
    errors: {},
  }),
  methods: {
    clearErrorMessages() {
      this.errors = {
        username: "",
        password: "",
      };
    },
    submit() {
      this.clearErrorMessages();
      this.post(URLS.get("login"), this);
    },
  },
};
</script>
