<template>
  <v-app>
    <!-- Navbar -->
    <v-app-bar :elevation="0" app class="custom-app-bar">
      <v-btn icon="mdi-chevron-left" v-if="isNotificationsPage" @click="goBack"></v-btn>
      <v-app-bar-title class="custom-title">{{ isNotificationsPage ? '알림함' : 'I’m not LOANly' }}</v-app-bar-title>
      <v-btn v-if="!isNotificationsPage" icon="mdi-bell-outline" @click="goToNotifications"></v-btn>
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
import { useRouter, useRoute } from 'vue-router';
import { ref, watch } from 'vue';

const display = useDisplay();
const router = useRouter();
const route = useRoute();

const isNotificationsPage = ref(false);

// 페이지 변경 감지하여 isNotificationsPage 업데이트
watch(
  () => route.path,
  (newPath) => {
    isNotificationsPage.value = newPath === '/notifications';
  }
);

// 알림 페이지로 이동하는 함수
const goToNotifications = () => {
  router.push('/notifications');
};

// 뒤로 가기 버튼
const goBack = () => {
  router.back();
};
</script>

<style scoped>
@font-face {
  font-family: "SUITE-Regular";
  src: url("https://fastly.jsdelivr.net/gh/projectnoonnu/noonfonts_2304-2@1.0/SUITE-Regular.woff2")
    format("woff2");
  font-weight: 400;
  font-style: normal;
}
#app {
  font-family: SUITE-Regular;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 20px; */
}
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
