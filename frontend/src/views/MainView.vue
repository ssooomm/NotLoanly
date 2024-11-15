<!-- loanlyManager/src/views/MainView.vue -->
<template>
  <div>
    <!-- <div class="main-container"> -->
    <!-- <header class="header">
      <button class="back-button">◀</button>
      <h1 class="title">I’m not LOANly</h1>
      <div class="icons">
        <span class="icon">🔔</span>
        <span class="icon">🏠</span>
        <span class="icon">☰</span>
      </div>
    </header> -->
    <div class="tabs">
      <button
        @click="activeTab = 'dashboard'"
        class="tab"
        :class="{ active: activeTab === 'dashboard' }"
      >
        요약
      </button>
      <button
        @click="activeTab = 'spending'"
        class="tab"
        :class="{ active: activeTab === 'spending' }"
      >
        상환현황
      </button>
      <button
        @click="activeTab = 'analysis'"
        class="tab"
        :class="{ active: activeTab === 'analysis' }"
      >
        소비분석
      </button>
    </div>
    <div class="content">
      <component :is="activeTabComponent" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import LoanDashboard from "../components/LoanDashboard.vue";
import SpendingAnalysis from "../components/SpendingAnalysis.vue";
import SpendingStatus from "../components/SpendingStatus.vue";

const activeTab = ref("dashboard");

const activeTabComponent = computed(() => {
  switch (activeTab.value) {
    case "dashboard":
      return LoanDashboard;
    case "spending":
      return SpendingStatus;
    case "analysis":
      return SpendingAnalysis;
    default:
      return LoanDashboard;
  }
});
</script>

<style scoped>
/* .main-container {
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
} */

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
  cursor: pointer;
}

.tab.active {
  border-bottom: 2px solid #fbc02d; /* Active tab underline */
}

.content {
  padding: 20px;
}
</style>
