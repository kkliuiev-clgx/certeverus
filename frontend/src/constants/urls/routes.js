export default {
  get: function(name, param) {
    switch (name) {
      case "home":
        return "/";
      case "login":
        return "/login/";
      case "logout":
        return "/logout/";
      case "signup":
        return "/signup/";
      case "reset_password_step_1":
        return "/reset-password/";

      // The urls below include params

      case "reset_password_step_2":
        return `/reset-password/${param.uid}/${param.token}/`;
    }
  },
};
