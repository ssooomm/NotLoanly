<template>
  <v-app>
    <!-- Navbar -->
    <v-app-bar :elevation="0" app class="custom-app-bar">
      <v-btn icon="mdi-chevron-left"></v-btn>
      <v-app-bar-title class="custom-title">I’m not LOANly</v-app-bar-title>
      <v-btn icon="mdi-bell-outline"></v-btn>
      <v-btn icon="mdi-home"></v-btn>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </v-app-bar>
    <!-- Main -->
    <v-main class="custom-main">
      <v-container fluid class="custom-container">
        <router-view />
      </v-container>
    </v-main>
    <!-- Footer -->
    <v-footer app></v-footer>
  </v-app>
</template>

<script setup>
import { useDisplay } from "vuetify";

const display = useDisplay();
</script>

<style scoped>
.custom-app-bar {
  max-width: 400px; /* Apply the same max-width as mobile-wrapper */
  margin: 0 auto;
  left: 0;
  right: 0;
}
.custom-title {
  margin: 0;
}
.custom-main {
  padding-top: 50px;
}
.custom-container {
  padding: 0;
}
</style>
