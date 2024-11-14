<template>
    <div class="dashboard">
      <header>
        <h1>KB 비상금 대출</h1>
        <div class="progress-container">
          <div class="progress-label">
            <span>0월 상환 진행률</span>
            <span>1/6 개월</span>
            <span>{{ progressPercentage }}%</span>
          </div>
          <div class="progress-bar">
            <div class="progress" :style="{ width: progressPercentage + '%' }"></div>
          </div>
          <div class="amounts">
            <span>{{ currentAmount }}원</span>
            <span>/ {{ totalAmount }}원</span>
          </div>
        </div>
      </header>
      <section class="calendar">
        <div class="financial-info">
        <p class="expense">지출: {{ expenditure }}원</p>
        <p class="income">수입: {{ income }}원</p>
      </div>
        <vue-cal
          v-model="events"
          :hide-view-selector="true" 
          :time="false" 
          :active-view="'month'" 
          xs-small 
        ></vue-cal>
      </section>
      <section class="plan">
        <h2>식비 절약 플랜</h2>
        <div class="category" v-for="(item, index) in budgetItems" :key="index">
          <div class="category-name">{{ item.name }}</div>
          <div class="category-bar">
            <div
              class="progress"
              :style="{ width: item.spent / item.budget * 100 + '%' }"
              :class="item.status"
            ></div>
          </div>
          <div class="amounts">
            <span>{{ item.spent }}원</span>
            <span>{{ item.budget }}원</span>
          </div>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import VueCal from 'vue-cal';
  
  const currentAmount = 530000; // 현재 금액
  const totalAmount = 3000000; // 총 목표 금액
  const progressPercentage = ((currentAmount / totalAmount) * 100).toFixed(1); // 진행률
  const expenditure = 1488100; // 지출
  const income = 2835502; // 수입
  
  const events = ref([
    { start: '2022-09-12', end: '2022-09-12', title: '지출' },
    { start: '2022-09-20', end: '2022-09-20', title: '수입' },
  ]);
  
  const budgetItems = [
    { name: '식비', spent: 70000, budget: 200000, status: 'safe' },
    { name: '쇼핑비', spent: 100000, budget: 150000, status: 'danger' },
    { name: '여가비', spent: 50000, budget: 280000, status: 'warning' },
  ];
  </script>
  
  <style scoped>
  .dashboard {
    text-align: center;
  }
  
  header {
    margin-bottom: 20px;
  }
  
  .progress-container {
    margin: 20px 0;
  }
  
  .progress-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
  }
  
  .progress-bar {
    background: #e0e0e0;
    border-radius: 5px;
    height: 20px;
    position: relative;
  }
  
  .progress {
    background: #ffc107; /* 노란색 */
    height: 100%;
    border-radius: 5px;
    transition: width 0.3s ease;
  }
  
  .amounts {
    display: flex;
    justify-content: space-between;
    font-size: 18px;
    margin-top: 5px;
  }
  .financial-info {
  display: flex;
  margin-bottom: 10px;
}
.expense {
    margin-right: 10px;
}
  .calendar {
    margin: 20px 0;
  }
  
  .category {
    margin: 15px 0;
  }
  
  .category-name {
    font-size: 18px;
    margin-bottom: 5px;
  }
  
  .category-bar {
    background-color: #e0e0e0;
    border-radius: 5px;
    height: 20px;
    position: relative;
  }
  
  .progress {
    height: 100%;
    border-radius: 5px;
    transition: width 0.3s ease;
  }
  
  .safe {
    background-color: #4caf50; /* 안전 */
  }
  
  .warning {
    background-color: #ffcc00; /* 적정 */
  }
  
  .danger {
    background-color: #f44336; /* 위험 */
  }
  
  .amounts {
    display: flex;
    justify-content: space-between;
    font-size: 14px;
  }
  </style>