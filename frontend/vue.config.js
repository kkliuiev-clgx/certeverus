const BundleTracker = require("webpack-bundle-tracker");

const is_prod = process.env.NODE_ENV === 'production'
console.log("build for production: " + is_prod)
const publicPath = is_prod ? "/" : "http://127.0.0.1:8080/"

module.exports = {
  transpileDependencies: ["vuetify"],
  publicPath: publicPath,
  outputDir: "./dist/",
  assetsDir: "./static",

  chainWebpack: (config) => {
    config.optimization.splitChunks(false);

    config
      .plugin("BundleTracker")
      .use(BundleTracker, [{ filename: "../frontend/webpack-stats.json" }]);

    config.resolve.alias.set("__STATIC__", "static");

    config.devServer
      .public("http://127.0.0.1:8080")
      .host("127.0.0.1")
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ "Access-Control-Allow-Origin": ["*"] });

    config.entryPoints.delete("app");
    config
      .entry("dashboard")
      .add("./src/bundles/dashboard.js")
      .end();

    config
      .entry("login")
      .add("./src/bundles/login.js")
      .end();

    config
      .entry("signup")
      .add("./src/bundles/signup.js")
      .end();

    config
      .entry("confirm")
      .add("./src/bundles/confirm.js")
      .end();

    config
      .entry("reset-password")
      .add("./src/bundles/reset-password.js")
      .end();
  },
};
