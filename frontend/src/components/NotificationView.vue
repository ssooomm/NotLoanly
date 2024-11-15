<template>
  <div class="main-container">
    <header class="header">
      <button class="back-button">◀</button>
      <h1 class="title">알림함</h1>
      <div class="icons">
        <span class="icon">🏠</span>
        <span class="icon">☰</span>
      </div>
    </header>
    <div class="tabs">
      <button class="tab">전체</button>
      <button class="tab">입출금</button>
      <button @click="activeTab = 'notLoanly'" class="tab" :class="{ active: activeTab === 'notLoanly' }">NotLoanly</button>
    </div>
    <div class="content">
      <div v-for="(notification, index) in notifications" :key="index" class="notification">
        <div class="notification-header">
          <img src="@/assets/logo.png" alt="Logo" class="notification-logo">
          <span class="notification-date">{{ notification.date }}</span>
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
import { ref } from 'vue';

const activeTab = ref('notLoanly'); // Set "NotLoanly" as the default active tab

const notifications = ref([
  { date: '2024.10.30', message: '오*민님, 쇼핑 부분에서 계획보다 10% 더 사용했습니다.' },
  { date: '2024.10.25', message: '오*민님, 쇼핑 부분에서 100% 사용했습니다. 조금만 줄이면 목표가 더 가까워집니다!' },
  { date: '2024.10.18', message: '오*민님, 쇼핑 부분에서 80% 사용했습니다. 한 발짝만 더 절약해볼까요?' },
]);
</script>

<style scoped>
.main-container {
  width: 393px;
  height: 928px;
  margin: 0 auto;
  text-align: center;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #fff;
  border-bottom: 1px solid #e0e0e0;
}

.back-button {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.title {
  flex-grow: 1;
  font-size: 18px;
  font-weight: bold;
  margin-left: 40px;
}

.icons {
  display: flex;
  gap: 10px;
}

.icon {
  cursor: pointer;
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
  cursor: default; /* Make other tabs unclickable */
}

.tab.active {
  border-bottom: 2px solid #fbc02d; /* Active tab underline */
}

.content {
  padding: 20px;
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
  padding: 20px;
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
</style>
