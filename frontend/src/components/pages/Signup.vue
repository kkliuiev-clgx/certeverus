<template>
  <v-app>
    <NavigationDrawer> </NavigationDrawer>
    <AppBar> </AppBar>

    <v-main>
      <v-container fluid>
        <v-container>
          <h2>Signup</h2>
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
                v-model="model.email"
                label="Email"
                :error-messages="errors.email"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.first_name"
                label="First name"
                :error-messages="errors.first_name"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.last_name"
                label="Last name"
                :error-messages="errors.last_name"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.password1"
                label="Password"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show ? 'text' : 'password'"
                name="input-10-1"
                hint="At least 8 characters"
                :error-messages="errors.password1"
                @click:append="show = !show"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-col cols="12" sm="6" md="3">
              <v-text-field
                v-model="model.password2"
                label="Confirm password"
                :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
                :type="show ? 'text' : 'password'"
                name="input-10-1"
                hint="At least 8 characters"
                :error-messages="errors.password2"
                @click:append="show = !show"
              ></v-text-field>
            </v-col>
          </v-row>
          <v-row>
            <v-btn class="cvbutton" @click="submit">Signup</v-btn>
          </v-row>
        </v-container>
        <notifications
          group="topRightNotification"
          position="top right"
          animation-type="velocity"
        />
      </v-container>
    </v-main>

    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import URLS from "../../constants/urls/routes";
import AppBar from "../common/AppBar";
import NavigationDrawer from "../common/NavigationDrawer";

require("@/assets/style.css")

export default {
  name: "Signup",
  components: {
    AppBar,
    NavigationDrawer,
  },
  data: () => ({
    model: {
      username: "",
      email: "",
      first_name: "",
      last_name: "",
      password1: "",
      password2: "",
    },
    show: false,
    errors: {},
  }),
  methods: {
    clearErrorMessages() {
      this.errors = {
        username: "",
        email: "",
        first_name: "",
        last_name: "",
        password1: "",
        password2: "",
      };
    },
    submit() {
      this.clearErrorMessages();
      this.post(URLS.get("signup"), this);
    },
  },
};
</script>
