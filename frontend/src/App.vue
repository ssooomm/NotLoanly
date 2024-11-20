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

    <!-- Real-time Notification Alert -->
    <v-alert
      v-if="apiStore.showAlert && !isNotificationsPage"
      :value="true"
      class="notification-alert"
      color="warning"
      icon="priority_high"
      variant="outlined"
    >
      <!-- 이미지 추가 -->
      <template #prepend>
        <img
          src="@/assets/logo.png"
          alt="Notification Icon"
          class="notification-image"
        />
      </template>
      {{ apiStore.alertMessage }}
    </v-alert>

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
import { ref, computed, watch, onMounted  } from "vue";
import { useApiStore } from '@/stores/apiStore';

const display = useDisplay();
const router = useRouter();
const route = useRoute();
const apiStore = useApiStore();

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

// SSE 연결
onMounted(() => {
  const userId = 1; 
  apiStore.connectSSE(userId); // SSE 연결 시작
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

.notification-alert {
  position: fixed;
  top: 10%; /* 화면 상단에서 10% 아래 */
  left: 50%; /* 화면 가로 중앙 */
  transform: translateX(-50%); /* 가로 중앙 정렬 */
  z-index: 1000; /* 다른 요소 위로 표시 */
  width: 88%; /* 알림 너비를 더 길게 설정 (뷰포트의 90%) */
  max-width: 500px; /* 최대 너비를 500px로 제한 */
  display: flex;
  align-items: center; /* 이미지와 텍스트를 수직 가운데 정렬 */
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2); /* 약간의 그림자 추가 */
  border-radius: 8px; /* 알림 모서리를 둥글게 */
}

.notification-image {
  width: 48px; /* 이미지 크기 증가 */
  height: 48px; /* 이미지 크기 증가 */
  
  border-radius: 50%; /* 이미지 둥글게 */
  object-fit: cover; /* 이미지가 컨테이너 크기에 맞게 조정 */
}
.notification-alert .v-alert__content {
  font-size: 0.875rem; /* 글자 크기를 줄임 (14px) */
  line-height: 1.4; /* 줄 간격 설정 */
}
</style>
