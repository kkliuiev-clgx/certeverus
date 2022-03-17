<template>
  <v-navigation-drawer v-if="isAuthenticated" v-model="drawerOpen" app fixed>
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            <v-img src="@/assets/CVAI-logo.jpg"></v-img>
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>

      <!-- <v-list-item @click="goToUrl('home')">
        <v-list-item-icon>
          <v-icon>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>Home</v-list-item-content>
      </v-list-item> -->

      <v-list-item @click="setChart('nodemap')">
        <v-list-item-icon>
          <v-icon>mdi-home</v-icon>
        </v-list-item-icon>
        <v-list-item-content>Home</v-list-item-content>
      </v-list-item>

      <v-list-item @click="setChart('prescriptions')">
        <v-list-item-icon> </v-list-item-icon>
        <v-list-item-content>Prescriptions</v-list-item-content>
      </v-list-item>
      <v-list-item @click="setChart('waterfall')">
        <v-list-item-icon> </v-list-item-icon>
        <v-list-item-content>Waterfall</v-list-item-content>
      </v-list-item>

      <v-list-item @click="setChart('sparkline')">
        <v-list-item-icon> </v-list-item-icon>
        <v-list-item-content>Sparkline</v-list-item-content>
      </v-list-item>

      <v-list-item @click="setChart('isoquant')">
        <v-list-item-icon> </v-list-item-icon>
        <v-list-item-content>Isoquant</v-list-item-content>
      </v-list-item>

      <v-list-item @click="setChart('single_factor')">
        <v-list-item-icon> </v-list-item-icon>
        <v-list-item-content>Single Factor</v-list-item-content>
      </v-list-item>
     
    
      <v-list-item key="Logout" @click="logout()">
        <v-list-item-icon>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-icon>
        <v-list-item-content>Logout</v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  name: "NavigationDrawer",
};
</script>
