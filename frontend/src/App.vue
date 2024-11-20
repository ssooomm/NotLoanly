<template>
  <v-app>
    <!-- Navbar -->
    <v-app-bar :elevation="0" app class="custom-app-bar">
      <v-btn icon="mdi-chevron-left" @click="goBack"></v-btn>
      <v-app-bar-title class="custom-title">{{
        isNotificationsPage ? "알림함" : "I’m not LOANly"
      }}</v-app-bar-title>
      <v-btn
        v-if="!isNotificationsPage"
        icon="mdi-bell-outline"
        @click="goToNotifications"
      ></v-btn>
      <v-btn icon="mdi-home"></v-btn>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </v-app-bar>
    <!-- Main -->
    <v-main class="custom-main">
      <v-container fluid class="custom-container" :style="containerStyle">
        <router-view />
      </v-container>
    </v-main>
    <!-- Footer -->
    <v-footer v-if="!hideFooter" app></v-footer>
  </v-app>
</template>

<script setup>
import { useDisplay } from "vuetify";
import { useRouter, useRoute } from "vue-router";
import { ref, computed, watch } from "vue";

const display = useDisplay();
const router = useRouter();
const route = useRoute();

const isNotificationsPage = ref(false);

// 페이지 변경 감지하여 isNotificationsPage 업데이트
watch(
  () => route.path,
  (newPath) => {
    isNotificationsPage.value = newPath === "/notifications";
  }
);

// 알림 페이지로 이동하는 함수
const goToNotifications = () => {
  router.push("/notifications");
};

// 뒤로 가기 버튼
const goBack = () => {
  router.back();
};

// LoanInfoNotice.vue 페이지에서만 적용할 스타일
const containerStyle = computed(() => {
  return route.path === "/loan-info-notice" ? { padding: "0 0 24px 0" } : {};
});

// 푸터 숨김 여부
const footerHiddenRoutes = [
  "/loan-input",
  "/loan-complete",
  "/loan-info-notice",
]; // 푸터를 숨길 라우트 경로 추가

const hideFooter = computed(() => {
  // 현재 라우트가 repayment-plan-suggestion에 대한 동적 패턴과 일치하는지 확인
  const isRepaymentPlanRoute = /^\/repayment-plan-suggestion\/\d+$/.test(
    route.path
  );

  return footerHiddenRoutes.includes(route.path) || isRepaymentPlanRoute;
});
</script>

<style scoped>
.custom-app-bar {
  max-width: 430px;
  /* Apply the same max-width as mobile-wrapper */
  margin: 0 auto;
  left: 0;
  right: 0;
}

.custom-title {
  margin: 0;
}

.custom-main {
  padding-top: 64px;
}

.custom-container {
  padding: 24px;
}
</style>
