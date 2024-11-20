<template>
  <div class="main-container">
    <div class="tabs">
      <button class="tab">전체</button>
      <button class="tab">입출금</button>
      <button @click="activeTab = 'notLoanly'" class="tab" :class="{ active: activeTab === 'notLoanly' }">NotLoanly</button>
    </div>
    <div class="content">
      <div v-for="(notification, index) in notifications" :key="index" class="notification">
        <div class="notification-header">
          <img src="@/assets/logo.png" alt="Logo" class="notification-logo">
          <span class="notification-date">{{ formatDate(notification.sent_at) }}</span>
        </div>
        <div class="notification-text">
          <p class="bold-text">I'm Not LOANly</p>
          <p>{{ notification.message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useApiStore } from '@/stores/apiStore'; // Import the API store

const activeTab = ref('notLoanly'); // Set "NotLoanly" as the default active tab

const apiStore = useApiStore(); // Access the API store

// Use computed property to get notifications from the store
const notifications = computed(() => apiStore.notifications);

// Function to format the date
function formatDate(dateString) {
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  };
  return new Date(dateString).toLocaleString('ko-KR', options);
}

// Fetch notifications when the component is mounted
onMounted(async () => {
  const userId = 1; // Replace with actual user ID
  try {
    await apiStore.fetchNotifications(userId);
  } catch (error) {
    console.error('Error fetching notifications:', error);
  }
});
</script>

<style scoped>
.main-container {
  max-width: 430px; /* 모바일 화면 기준 최대 너비 */
  width: 100%; /* 가로 길이를 화면 너비에 맞춤 */
  height: 100vh; /* 뷰포트 높이에 맞춤 */
  overflow-y: auto; /* 화면이 넘칠 경우 세로 스크롤 활성화 */
  margin: 0 auto;
  text-align: center;
  background-color: #ffffff; /* 배경색 추가 */
}

.tabs {
  display: flex;
  justify-content: space-around;
  padding: 10px 0;
}

.tab {
  flex: 1;
  padding: 10px;
  text-align: center;
  border: none;
  background: none;
  cursor: default; /* 비활성 탭에 클릭 방지 */
}

.tab.active {
  border-bottom: 2px solid #fbc02d; /* 활성 탭 강조 */
}

.content {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px; /* 알림 간격 설정 */
}

.notification {
  padding: 10px;
  margin-bottom: 15px;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.notification-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%; /* 이미지 둥글게 */
}

.notification-date {
  font-size: 14px;
  color: #888;
}

.notification-text {
  background-color: #f7f7f7;
  border-radius: 8px;
  text-align: left;
  margin-top: 5px;
  padding: 15px; /* 내부 여백 줄임 */
}

.notification-text p {
  margin: 0;
  color: #555;
}

.notification-text p + p {
  margin-top: 7px;
}

.bold-text {
  font-weight: bold;
}

/* 모바일 화면에 맞게 최대 높이 설정 */
@media (max-height: 812px) {
  .main-container {
    height: 100%;
  }
}
</style>
