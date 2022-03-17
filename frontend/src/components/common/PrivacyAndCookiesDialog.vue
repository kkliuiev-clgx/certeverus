<template>
  <div class="privacy-cookies">
    <p class="cookies title">
      This website uses cookies to ensure you get the best experience on our
      website.
    </p>
    <div id="privacy">
      <v-btn @click="accept()" id="accept-btn" class="cvbutton br-50"
        >Accept & Close</v-btn
      >
      <a class="text-white link" href="https://certeverus.ai/privacy-policy/"
        >Privacy Policy</a
      >
    </div>
  </div>
</template>

<script>
export default {
  name: "PrivacyAndCookiesDialog",
  mounted() {
    this.checkCookie("certeverus");
  },
  methods: {
    createCookie(name, value, expiry) {
      let d = new Date();
      d.setTime(d.getTime() + expiry * 24 * 60 * 60 * 1000);
      let expires = "expires=" + d.toUTCString();
      document.cookie = name + "=" + value + ";" + expires + ";path=/";
    },

    getCookie(name) {
      let cookie = decodeURIComponent(document.cookie);
      let cookieSegments = cookie.split(";");
      for (let i = 0; i < cookieSegments.length; i++) {
        let segments = cookieSegments[i];

        let keyValuePair = segments.split("=");
        let key = keyValuePair[0].trim();
        let value = keyValuePair[1];

        if (key === name) return value;
      }
      return "";
    },
    checkCookie(name) {
      let value = this.getCookie(name);
      if (value != "") {
        this.dismiss();
      }
    },
    deleteCookie(name) {
      document.cookie =
        name + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    },
    dismiss() {
      let banner = document.getElementsByClassName("privacy-cookies")[0];
      banner.style.display = "none";
    },
    accept() {
      this.createCookie("certeverus", "true", 30);
      this.dismiss();
    },
  },
};
</script>

<style scoped>
.privacy-cookies .title {
  color: #fff;
  font-size: 1em !important;
  margin-top: 7px;
  margin-bottom: 7px;
  padding: 10px;
}
.privacy-cookies {
  position: absolute;
  z-index: 5;
  bottom: 0;
  left: 0;
  width: 100vw;
  background: #000;
  display: flex;
  justify-content: space-around;
  align-items: center;
}
.v-btn.br-50 {
  border-radius: 50px !important;
  padding-left: 25px !important;
  padding-right: 25px !important;
}
#accept-btn {
  background: #b89a4d !important;
  transition: 0.3s;
}
#accept-btn:hover {
  background: #000 !important;
  transition: 0.3s;
}
.text-white {
  color: #fff;
}
#privacy {
  display: flex;
  align-items: baseline;
}
.link {
  text-decoration: none;
  padding: 10px;
}
</style>
