export default {
  get: function(name, param) {
    switch (name) {
      case "get_client_data":
        return "/api/clients/";

      // The urls below include params
      case "get_chart_data":
        return `/api/clients/${param.client_id}/chart/`;
    }
  },
};
