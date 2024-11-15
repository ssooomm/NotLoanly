<template>
  <div class="dashboard">
    <h2>KB 비상금 대출</h2>
    <div class="body">
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
    <section class="summary">
      <div class="summary-item">
        <span>목표 상환 원금</span>
        <span>{{ targetAmount }}원</span>
      </div>
      <div class="summary-item">
        <span>이자 납입액</span>
        <span>{{ interestAmount }}원</span>
      </div>
      <div class="summary-total">
        <span>총 납부액</span>
        <span>{{ totalPayment }}원</span>
      </div>
    </section>
    <section class="calendar">
      <div class="financial-info">
        <p class="expense">지출: {{ expenditure }}원</p>
        <p class="income">수입: {{ income }}원</p>
      </div>
      <vue-cal
        small
        v-model="events"
        :hide-view-selector="true"
        :time="false"
        :active-view="'month'"
        :events="events"
        :event-count-on-month-view
        :style="{ border: 'none' }">
        <template #events-count="{ events }">
          <span v-if="events.length">
            {{ events.length }} 이벤트
          </span>
        </template>
      </vue-cal>
    </section>
    <section class="plan">
      <h2>식비 절약 플랜</h2>
      <div class="budget-container">
        <div class="budget-bar">
          <div class="budget-segment" :style="{ width: (budgetItems[0].budget / totalBudget) * 100 + '%', backgroundColor: '#f44336' }">식비</div>
          <div class="budget-segment" :style="{ width: (budgetItems[1].budget / totalBudget) * 100 + '%', backgroundColor: '#ffcc00' }">쇼핑비</div>
          <div class="budget-segment" :style="{ width: (budgetItems[2].budget / totalBudget) * 100 + '%', backgroundColor: '#4caf50' }">여가비</div>
        </div>
        <div class="change" @click="toggleEditMode">
          비율 변경 >
        </div>
      </div>
      <div class="category" v-for="(item, index) in budgetItems" :key="index">
        <div class="category-header">
          <div class="category-name">{{ item.name }}</div>
          <div :class="['status', getStatusClass(item.status)]">{{ getStatusText(item.status) }}</div>
        </div>
        <div class="category-bar">
          <div
            class="progress"
            :style="{ width: (item.spent / item.budget) * 100 + '%' }"
            :class="item.status"
          ></div>
        </div>
        <div class="amounts">
          <span>{{ item.spent }}원</span>
          <span>/ {{ item.budget }}원</span>
        </div>
      </div>
    </section>
  </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import VueCal from 'vue-cal';
import '../../node_modules/vue-cal/dist/vuecal.css'; // Ensure you import the CSS

const currentAmount = 530000; // 현재 금액
const totalAmount = 3000000; // 총 목표 금액
const targetAmount = 500000; // 목표 상환 원금
const interestAmount = 20000; // 이자 납입액
const totalPayment = currentAmount + interestAmount; // 총 납부액
const progressPercentage = ((currentAmount / totalAmount) * 100).toFixed(1); // 진행률
const expenditure = 1488100; // 지출
const income = 2835502; // 수입

const events = ref([
  { start: '2024-11-19', end: '2024-11-19', title: '지출: 50,000원', color: '#f44336' }, // Expenditure
  { start: '2024-11-20', end: '2024-11-20', title: '수입: 100,000원', color: '#4caf50' }, // Income
  // Add more events as needed
]);

const budgetItems = [
  { name: '식비', spent: 70000, budget: 200000, status: 'safe' },
  { name: '쇼핑비', spent: 100000, budget: 150000, status: 'danger' },
  { name: '여가비', spent: 50000, budget: 280000, status: 'warning' },
];

// Function to get status text
const getStatusText = (status) => {
  switch (status) {
    case 'safe':
      return '안전';
    case 'danger':
      return '위험';
    case 'warning':
      return '적정';
    default:
      return '';
  }
};

// Function to get status class
const getStatusClass = (status) => {
  switch (status) {
    case 'safe':
      return 'status-safe'; 
    case 'danger':
      return 'status-danger'; 
    case 'warning':
      return 'status-warning'; 
    default:
      return '';
  }
};

const totalBudget = budgetItems.reduce((sum, item) => sum + item.budget, 0);
</script>

<style scoped>
.dashboard {
  text-align: center;
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

.summary {
  margin: 20px 0;
  text-align: left;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}

.summary-total {
  font-weight: bold;
  border-top: 1px solid #e0e0e0;
  padding-top: 10px;
  display: flex;
  justify-content: space-between;
  margin: 5px 0;
}

.calendar {
  margin: 20px 0;
}

.financial-info {
  display: flex;
  justify-content: flex-end; 
  margin: 20px 0;
  color: #ecb91f;
  font-weight: bold;
}

.expense {
  margin-right: 10px;
}

.plan {
  margin: 20px 0;
}

.budget-container {
  display: flex;
  align-items: center; 
  justify-content: space-between; 
}

.budget-bar {
  display: flex;
  height: 30px; 
  border-radius: 5px;
  margin-bottom: 20px;
  margin-top: 20px;
  width: 70%; 
}

.budget-segment {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white; 
  font-weight: bold;
}

.change {
  margin-left: 10px; 
  color: rgb(48, 110, 243);
  cursor: pointer; 
}

.category {
  margin: 15px 0;
}

.category-header {
  display: flex;
  justify-content: space-between; 
  align-items: center;
}

.category-name {
  font-size: 18px;
  margin-bottom: 5px;
  font-weight: bold;
}

.status {
  font-size: 14px;
  margin-bottom: 5px;
  padding: 5px 10px;
  border-radius: 10px; 
  color: rgb(255, 255, 255); 
}

.status-safe {
  background-color: #4caf50; 
}

.status-danger {
  background-color: #f44336; 
}

.status-warning {
  background-color: #ffcc00; 
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

.amounts {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

</style>