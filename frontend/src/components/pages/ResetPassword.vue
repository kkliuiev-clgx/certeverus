<template>
  <v-app>
    <NavigationDrawer> </NavigationDrawer>
    <AppBar> </AppBar>

    <v-main>
      <v-container fluid>
        <v-container v-if="model.step === 1">
          <h2>Reset Password - Step 1</h2>
          <p>
            You will need to confirm your email before you can change your
            password. Enter your email and we will send you a confirmation
            email.
          </p>
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
            <v-btn class="cvbutton" @click="submit"
              >Send confirmation email</v-btn
            >
          </v-row>
        </v-container>
        <v-container v-if="model.step === 2">
          <h2>Reset Password - Step 2</h2>
          <p>
            You can now enter your new password.
          </p>
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
            <v-btn class="cvbutton" @click="submit">Change password</v-btn>
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

require("@/assets/style.css");

export default {
  name: "ResetPassword",
  components: {
    AppBar,
    NavigationDrawer,
  },
  data: () => ({
    uid: "",
    token: "",
    model: {
      step: 1,
      email: "",
      password1: "",
      password2: "",
    },
    show: false,
    errors: {},
  }),
  created() {
    try {
      this.django = JSON.parse(localStorage.getItem("djangoData"));
      this.uid = this.django.uid;
      this.token = this.django.token;
      // eslint-disable-next-line
    } catch (err) {}

    if (this.uid && this.token) {
      this.model.step = 2;
    } else {
      this.model.step = 1;
    }

    // TODO - same code is in ResetPassword - make DRY
    let messageType = "error";
    if (this.django.message) {
      if (this.django.success) {
        messageType = "success";
      }
    }

    if (this.django.redirect) {
      this.setNotificationOnNextRefresh(messageType, this.django.message);
      window.location.href = this.django.redirect;
    } else {
      this.showNotification(messageType, this.django.message);
    }
  },
  methods: {
    clearErrorMessages() {
      this.errors = {
        step: 1,
        email: "",
        password1: "",
        password2: "",
      };
    },
    submit() {
      this.clearErrorMessages();
      let url = URLS.get("reset_password_step_1");
      if (this.model.step == 2) {
        url = URLS.get("reset_password_step_2", {
          uid: this.uid,
          token: this.token,
        });
      }
      this.post(url, this);
    },
  },
};
</script>
