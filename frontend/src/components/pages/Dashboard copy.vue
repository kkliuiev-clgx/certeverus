<template>
  <v-app>
    <NavigationDrawer> </NavigationDrawer>
    <AppBar> </AppBar>
    <v-main>
      <v-container fluid>
        <v-container>
          <v-container class="grey- lighten-5">
            <v-row>
              <v-col md="4" class="auto">
                <v-select
                  v-if="showParentOptions"
                  menu-props="auto"
                  label="Parent"
                  v-model="model.parent"
                  :items="parentFilterItems"
                  :error-messages="errors.parent"
                >
                </v-select>
              </v-col>
              <v-col md="4" class="refresh-data">
                <div v-if="isAuthenticated" @click="getChartData()">
                  <v-icon size="30">mdi-sync</v-icon><br />
                  <strong>Refresh Chart</strong>
                </div>
              </v-col>

              <v-col md="4" class="ml-auto- auto">
                <v-select
                  v-if="currentChart == 'isoquant' || currentChart== 'single_factor' && showDriverOptions"
                  menu-props="auto"
                  label="Drivers"
                  v-model="model.driver"
                  :items="driverFilterItems"
                  :error-messages="errors.driver"
                  @change="getChartData()"
                ></v-select>

                <v-select
                  v-if="(currentChart =='waterfall' || currentChart == 'sparkline') && showResampleOptions"
                  menu-props="auto"
                  label="Resample period"
                  v-model="model.resample_period"
                  :items="resampleItems"
                  :error-messages="errors.resample_period"
                ></v-select>
              </v-col>
            </v-row>
            <v-row name = "attributes-row">  
                    <v-select
                    v-if="currentChart == 'isoquant' && showAttribSelection"
                     menu-props="auto"
                     label="Select a Single Attribute"
                     v-model="model.attribs"
                     :items="attribFilterItems"
                     chips
                     deletable-chips
                     
                     clearable
                    
                     hide-selected
                     solo
                     @change="getChartData()"
                    > 
                    <!-- <option v-for="(attrib, driver) in attribFilterItems"
                       :value="attrib"
                       :key="driver">
                        {{attrib}}
                    </option> -->
                    <template 
                      v-slot:selection="{attribs, item, select, selected }">
                      <v-chip
                       v-bind="attribs"                      
                       :input-value="selected"
                       
                       @click="select"
                       @click:close="remove(item)"
                      >
                        <strong>{{ item.text }}</strong>&nbsp;
                      </v-chip>
                     </template>
                    </v-select>
            </v-row>
            <v-row name = "filters-row">  
                    <v-select
                     menu-props="auto"
                     label="Select a Single Filter"
                     v-model="model.filtered_by"
                     :items="filtered_by"
                     item-text= "filtered_by"
                     chips
                     deletable-chips
                     
                     clearable
                    
                     hide-selected
                     solo
                     @change="getChartData()"
                    > 

                    <template 
                      v-slot:selection="{attrs, item, select, selected }">
                      <v-chip
                       v-bind="attrs"                      
                       :input-value="selected"
                       
                       @click="select"
                       @click:close="remove(item)"
                      >
                        <strong>{{ item.filtered_by }}</strong>&nbsp;
                      </v-chip>
                     </template>
                    </v-select>
            </v-row>
            <v-row class="chart-row">
              <v-col md="12" class="ml-md-auto">
                <div class="text-center">
                  <div
                    v-if="currentChart == 'waterfall' && showChartHeading"
                    class="text-center"
                  >
                    <h2 class="text-center">Waterfall</h2>
                  </div>

                  <div
                    v-if="currentChart == 'nodemap' "
                    class="text-center"
                  >
                    <h2 class="text-center"></h2>
                  </div>

                  <div
                    v-if="currentChart == 'isoquant' && showChartHeading"
                    class="text-center"
                  >
                    <h2 class="text-center">Isoquant</h2>
                  </div>

                  <div
                    v-if="currentChart == 'single_factor' && showChartHeading"
                    class="text-center"
                  >
                    <h2 class="text-center">Single Factor</h2>
                  </div>

                  <div
                    v-if="currentChart == 'sparkline' && showChartHeading"
                    class="text-center"
                  >
                    <h2 class="text-center">Sparkline</h2>
                  </div>

                  <div v-if="isProcessing" class="text-center mt-10">
                    <v-progress-circular
                      :size="100"
                      class="cvgold"
                      indeterminate
                    ></v-progress-circular>
                  </div>

                  <div id="chart" style="display:none"></div>
                  <div id="chartHelp" class="mt-10"></div>
                  <div
                    id="chartScrollerHelp"
                    class="mt-10"
                    style="display:none"
                  >

                  </div>
                </div>
              </v-col>
            </v-row>
            <v-row name = "bottom-row">
              <v-col cols="auto" class="mr-auto">
                <v-menu
                  v-if="showDateOptions"
                  v-model="startDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="model.start_date"
                      label="Start Date"
                      hint="YYYY-MM-DD - select first day of month"
                      persistent-hint
                      readonly
                      v-on="on"
                      :error-messages="errors.start_date"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="model.start_date"
                    
                    @input="startDateMenu = false"
                  ></v-date-picker>

                </v-menu>
              </v-col>

              <v-col
                v-if="currentChart == 'single_factor' || currentChart == 'waterfall'||currentChart =='isoquant'"
                class="col-auto mr-auto"
              >
                <!-- <v-subheader
                  v-if ="currentChart== 'waterfall'"
                >
                 <template>
                 Select Plan v. Actual or Date Comparison
                 </template>


                </v-subheader> -->

                 <v-switch
                  color="grey"
                  v-if="currentChart == 'waterfall'"
                  v-model="model.pva"
                  :label="model.pva? 'Date to Date Comparison' : 'Plan vs Actuals'"
                  persistent-hint
                  hint="Select Plan v. Actual or Date Comparison" 
                  @change="getChartData()"
                 ></v-switch>

                 
                <!-- TODO #266 The user can use the YTD and the Date switches on the isoquant, sparkline and singlefactor charts -->
                <v-switch name="YTD Switch Water Fall"
                  color="grey"
                  v-if="currentChart == 'waterfall'"
                  v-model="model.ytd"
                  :label="model.ytd? 'YTD':'Single Month'"
                  :disabled="model.pva"
                  persistent-hint
                  hint="Select Single Month Comparison or YTD" 
                  @change="getChartData()"
                  
                 ></v-switch>

                <v-switch name="YTD Switch isoquant"
                  color="blue"
                  v-if="currentChart == 'isoquant'"
                  v-model="model.ytd"
                  :label="model.ytd? 'YTD':'By Month'"
                  persistent-hint
                  hint="Select By Month or YTD" 
                  @change="getChartData()"
                  
                 ></v-switch>
                

                <!-- TODO #265 Need to determine how to set a default value based on PVA value (i.e set the YTD to FALSE AND DISABLED when selecting Singel Month)  -->
                <v-switch
                  color="grey"
                  v-if="currentChart == 'waterfall'"
                  v-model="model.ordered"
                  :label="model.ordered ? 'Value' : 'Sequence'"
                  persistent-hint
                  hint="Select sorted by sequence or value"                   
                   @change="getChartData()"

                ></v-switch>
                <!-- <v-select -->
                  <!-- v-if="showResampleOptions && currentChart == 'single_factor' | currentChart == 'isoquant'" -->
                  <!-- menu-props="auto" -->
                  <!-- label="Resample period" -->
                  <!-- v-model="model.resample_period" -->
                  <!-- :items="resampleItems" -->
                  <!-- :error-messages="errors.resample_period" -->
                <!-- ></v-select> -->
              </v-col>
              <v-col cols="auto">
                <v-menu
                  v-if="showDateOptions"
                  v-model="endDateMenu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  max-width="290px"
                  min-width="290px"
                >
                  <template v-slot:activator="{ on }">
                    <v-text-field
                      v-model="model.end_date"
                      label="End Date"
                      hint="YYYY-MM-DD"
                      persistent-hint
                      readonly
                      v-on="on"
                      :error-messages="errors.end_date"
                    ></v-text-field>
                  </template>
                  <v-date-picker
                    v-model="model.end_date"
                    no-title
                    @input="endDateMenu = false"
                  ></v-date-picker>
                </v-menu>
              </v-col>
            </v-row>
          </v-container>

          <notifications
            group="topRightNotification"
            position="top right"
            animation-type="velocity"
          />
        </v-container>
      </v-container>
    </v-main>

    <PrivacyAndCookiesDialog />

    <v-footer app></v-footer>
  </v-app>
</template>

<script>
import API_URLS from "../../constants/urls/api";
import APP_CONSTANTS from "../../constants/app";

import AppBar from "../common/AppBar";
import NavigationDrawer from "../common/NavigationDrawer";
import PrivacyAndCookiesDialog from "../common/PrivacyAndCookiesDialog";

export default {
  name: "Dashboard",
  components: {
    AppBar,
    NavigationDrawer,
    PrivacyAndCookiesDialog,
  },
  data() {
    return {
      showChartHeading: true,
      valid: false,
      startDateMenu: false,
      endDateMenu: false,
      isProcessing: false,
      model: {
        ytd:false,
        ordered: true,
        pva: true,
        plan: "",
        client_id: "",
        parent: "",
        start_date: "",
        end_date: "",
        driver: "",
        chart_type: "sparkline",
        attribs: [],
        filtered_by:[],
      },
      errors: {},
      parentFilterItems: [],
      resampleItems: APP_CONSTANTS.resampleItems,
      driverFilterItems: [],
      parentDrivers: [],
      attribFilterItems: [],
      filterbyFilterItems:[]


    };
  },

  watch: {
    currentChart: function(newVal, oldVal) {
      if (oldVal != newVal) {
        this.showHideChartHelp(true);
      }
    },
    currentParent: function(newVal, oldVal) {
      if (oldVal != newVal) {
        this.driverFilterItems = [];
        this.driverFilterItems.push({
          text: "Select a driver",
          value: "",
        });

        this.parentDrivers.forEach((element) => {
          if (element.parent == newVal) {
            this.driverFilterItems.push({
              text: element.driver,
              value: element.driver,
            });
          }
        });
      }
    },

// here is where I filter and refresh the filterItems
 
    currentFiltered_by:function(newVal, oldVal) {
      oldVal=''
      if (oldVal != newVal) {        
        this.filterbyFilterItems = [];
              this.filterbyFilterItems.push({
                text: "Select a filter",
                value: "",
              });
        this.filterbyFilterItems.forEach((element) => {
          if (element == newVal) {
            this.filterbyFilterItems.push({
              text: element.filtered_by,
              value: element.filtered_by,
            });
          }
        });
      }
    },      
    
    currentDriver: function(newVal, oldVal) {
      oldVal=''
      if (oldVal != newVal) {
        this.attribFilterItems = [];
        this.attribFilterItems.push({
          text: "",
          value: "",
        });
         
        this.attribs.forEach((element) => {
          if (element.driver == newVal) {
            this.attribFilterItems.push({
              text: element.attribs,
              value: element.attribs,
            });
          }
        });
      }
    },
  },

  computed: {
    showDriverOptions() {
      return (
        /* this.currentChart === "waterfall" ||*/
        this.currentChart === "isoquant" ||
        this.currentChart === "single_factor"
      );
    },
    showAttribSelection() {
      return (
        /* this.currentChart === "waterfall" ||*/
        this.currentChart === "isoquant" 
      );
    },
    showParentOptions() {
      return (
        this.currentChart === "waterfall" ||
        this.currentChart === "single_factor" ||
        this.currentChart === "sparkline" ||
        this.currentChart === "nodemap" ||
        this.currentChart === "isoquant"
      );
    },
    showResampleOptions() {
      return (
        false
      );
    },
    showDateOptions() {
      return (
        this.currentChart === "single_factor" ||
        this.currentChart === "isoquant" ||
        this.currentChart === "waterfall"
      );
    },
    currentParent() {
      return this.model.parent;
    },

    currentDriver() {
      return this.model.driver;
    },
    currentAttribs() {
      return this.model.attribs;
    },
    currentFiltered_by() {
      return this.model.filtered_by;
    },

    currentChart() {
      this.showHideChart(false);
      return this.$store.getters["site/getCurrentChart"];
    },
  },
  mounted() {
    this.showHideChartHelp(true);
  },
  created() {
    this.setChart("nodemap");
    this.getClientAndTeams();
    this.getChartData();
  },
  methods: {
    clearErrorMessages() {
      this.errors = {
        client_id: "",
        resample_period: "",
        parent: "",
        driver: "",
        start_date: "",
        end_date: "",
      };
    },
    getClientAndTeams() {
      this.clearErrorMessages();
      this.get(API_URLS.get("get_client_data"), this)
        .then((response) => {
          if (response.data.success) {
            if (response.data.data.client) {
              this.model.client_id = response.data.data.client.id;
              this.model.client_name = response.data.data.client.name;
            }
            this.parentFilterItems.push({
              text: "Select a parent",
              value: "",
            });

            this.driverFilterItems.push({
              text: "Select a driver",
              value: "",
            });

            this.attribFilterItems.push({
              text: "Select Attributes",
              value: response.data.data.attribs,
            })
            console.log("this is the attribs", this.attribs);

            this.filterbyFilterItems.push({
              text: "Select Filter",
              value: response.data.data.filtered_by,
            })
            console.log("these are the filter inputs",this.filterbyFilterItems);

            response.data.data.parents.forEach((element) => {
              this.parentFilterItems.push({
                text: element,
                value: element,
              });
              
            });


            this.parentDrivers = response.data.data.drivers;
            console.log('The drivers are ',this.parentDrivers)


            this.attribs = response.data.data.attribs;
            console.log('the attributes',this.attribs)

            this.filtered_by = response.data.data.filtered_by;
            console.log('the filters', this.filtered_by)
            console.log(this.filterbyFilterItems)

            // Setup initial data
            if (this.model.client_name=='Accordion_inv'){
             this.model.parent = "Inventory Value";
             this.model.start_date = "2021-06-01";
             console.log("CLIENT is ", this.model.client_name)
              console.log("ACCORDION INVENTORY", this.model.parent);
            }else {this.model.parent = "Sourcing";
                 this.model.start_date = "2021-05-01";
                 console.log("FALLBACK"); 
              }
           //   // this.model.parent = "Sourcing";

            this.model.end_date = "2021-06-30";
            this.model.resample_period = "MS";
            this.getChartData();
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    validate() {
      this.clearErrorMessages();

      this.valid = true;

      if (!this.model.client_id) {
        this.showNotification(
          "error",
          "Your account does not have a Client attached to it."
        );
        this.valid = false;
      }

      if (
        ["waterfall", "sparkline", "single_factor", "isoquant"].indexOf(this.currentChart) >
        -1
      ) {
        if (!this.model.resample_period) {
          this.errors.resample_period = "This field is required";
          this.valid = false;
        }

        if (!this.model.parent) {
          this.errors.parent = "This field is required";
          this.valid = false;
        }

        if (["waterfall", "single_factor","isoquant"].indexOf(this.currentChart) > -1) {
          if (!this.model.start_date) {
            this.errors.start_date = "This field is required";
            this.valid = false;
          }

          if (!this.model.end_date) {
            this.errors.end_date = "This field is required";
            this.valid = false;
          }
        }

        if (["single_factor","isoquant"].indexOf(this.currentChart) > -1) {
          if (!this.model.driver) {
            this.errors.driver = "This field is required";
            this.valid = false;
          }
        }
      }
    },
    showHideChart(show) {
      try {
        if (show) {
          document.getElementById("chart").style.display = "block";
        } else {
          document.getElementById("chartHelp").innerHTML = "";
          document.getElementById("chart").style.display = "none";
        }
        document.getElementById("chartScrollerHelp").style.display = show
          ? "block"
          : "none";

        // eslint-disable-next-line
      } catch (err) {}
    },
    showHideChartHelp(show) {
      let msg = "";
      if (this.currentChart == "waterfall") {
        msg =
          "Please provide a parent, resample period, start and end dates.<br>When you are done click the 'Refresh Data' button.";
      } else if (this.currentChart == "isoquant") {
        msg =
          "Please provide a parent, resample period, driver, start and end dates.<br>When you are done click the 'Refresh Data' button.";
      } else if (this.currentChart == "sparkline") {
        msg =
          "Please provide a parent and resample period.<br>When you are done click the 'Refresh Data' button.";
      } else if (this.currentChart == "single_factor") {
        msg =
          "Please provide a parent, resample period, driver, start and end dates.<br>When you are done click the 'Refresh Data' button.";
      }

      document.getElementById("chartHelp").innerHTML = msg;
      document.getElementById("chartHelp").style.display = show
        ? "block"
        : "none";

      this.showChartHeading = show;
    },
    getChartData() {
      this.validate();
      if (!this.valid) {
        return;
      }

      this.showHideChart(false);
      this.showHideChartHelp(false);

      this.showChartHeading = true;

      this.isProcessing = true;

      // Add get params
      this.model.params = {
        parent: this.model.parent,
        start_date: this.model.start_date,
        end_date: this.model.end_date,
        resample_period: this.model.resample_period,
        chart_type: this.currentChart,
        driver: this.model.driver,
        ordered: this.model.ordered,
        pva: this.model.pva,
        ytd: this.model.ytd,
        attribs: this.model.attribs,
        filtered_by: this.model.filtered_by,
      };

      this.get(
        API_URLS.get("get_chart_data", { client_id: this.model.client_id }),
        this
      )
        .then((response) => {
          this.showHideChartHelp(false);
          this.isProcessing = false;
          this.showChartHeading = false;

          if (response.data.success && response.data.data) {
            this.showHideChart(true);
            // eslint-disable-next-line
            Plotly.newPlot("chart", JSON.parse(response.data.data));
          } else {
            this.showHideChartHelp(true);
            this.showHideChart(false);
            this.showNotification("error", response.data.message);
          }
        })
        .catch((error) => {
          console.error(error);
          this.isProcessing = false;
          this.showChartHeading = true;
          this.showHideChartHelp(true);
          this.showHideChart(false);
          this.showNotification("error", "No data     ");
        });
    },
    remove (item) {
        this.chips.splice(this.chips.indexOf(item), 1)
          this.chips = [...this.chips]
      },
  },
};
</script>
<style scoped>
.chart-row {
  min-height: 300px;
}
.cvgold {
  color: #b78b20;
}
.refresh-data {
  text-align: center;
  cursor: pointer;
}
#chart {
  min-height: 1000px;
  min-width: 1000px;
  max-height: 1000px;
}
</style>
