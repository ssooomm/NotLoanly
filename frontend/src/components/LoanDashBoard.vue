<template>
  <div class="dashboard">
    <h2>KB 비상금 대출</h2>
    <div class="body">
      <div class="progress-container">
        <div class="progress-label">
          <span>11월 상환 진행률</span>
          <span>1/6 개월</span>
          <span>{{ progressPercentage }}%</span>
        </div>
        <div class="progress-bar">
          <div
            class="progress"
            :style="{ width: progressPercentage + '%' }"
          ></div>
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
          <p class="expense">
            지출: <span class="red-text">{{ formatAmount(expenditure) }}</span
            >원
          </p>
          <p class="income">
            수입: <span class="blue-text">{{ formatAmount(income) }}</span
            >원
          </p>
        </div>
        <vue-cal
          xsmall
          v-model="events"
          :time="false"
          hide-view-selector
          active-view="month"
          :disable-views="['years', 'year', 'week', 'day']"
          :events="events"
          events-on-month-view="short"
          class="vuecal--yellow-theme"
          style="height: 400px"
        >
        </vue-cal>
      </section>
      <section class="plan">
        <div class="plan-header">
          <h2 class="plan-title">식비 절약 플랜</h2>
          <div class="change" @click="toggleEditMode">플랜 변경 ></div>
        </div>
        <div class="budget-container">
          <div class="budget-bar">
            <div
              v-for="(item, index) in budgetItems"
              :key="index"
              class="budget-segment"
              :style="{
                width: (item.budget / totalBudget) * 100 + '%',
                backgroundColor:
                  item.status === 'danger'
                    ? '#f44336'
                    : item.status === 'warning'
                    ? '#ffcc00'
                    : '#4caf50',
              }"
            >
              {{ item.name }}
            </div>
          </div>
        </div>
        <div class="category" v-for="(item, index) in budgetItems" :key="index">
          <div class="category-header">
            <div class="category-name">{{ item.name }}</div>
            <div :class="['status', getStatusClass(item.status)]">
              {{ getStatusText(item.status) }}
            </div>
          </div>
          <div class="category-bar">
            <div
              class="progress"
              :style="{
                width: calculateProgressWidth(item.spent, item.budget),
              }"
              :class="item.status"
            ></div>
          </div>
          <div class="amounts">
            <span>{{ formatAmount(item.spent) }}원</span>
            <span>/ {{ formatAmount(item.budget) }}원</span>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import VueCal from "vue-cal";
import { useRouter } from "vue-router";
import { useApiStore } from "@/stores/apiStore";
import "../../node_modules/vue-cal/dist/vuecal.css";

const router = useRouter();
const apiStore = useApiStore();

const currentAmount = 530000;
const totalAmount = 3000000;
const targetAmount = 500000;
const interestAmount = 20000;
const totalPayment = currentAmount + interestAmount;
const progressPercentage = ((currentAmount / totalAmount) * 100).toFixed(1);

// 반응형 데이터 설정 - 초기값 설정
const expenditure = ref(0);
const income = ref(0);
const budgetItems = ref([]);
const events = ref([]);

// 금액 포맷팅 함수
const formatAmount = (amount) => {
  return new Intl.NumberFormat("ko-KR").format(amount);
};

// 달력 이벤트 변환 함수
const convertTransactionsToEvents = (transactions) => {
  return transactions.map((transaction) => ({
    start: transaction.date,
    end: transaction.date,
    title:
      transaction.category === "소득"
        ? `+${formatAmount(transaction.amount)}`
        : `-${formatAmount(transaction.amount)}`,
    class: transaction.category === "소득" ? "income-event" : "expense-event",
  }));
};

// Progress width 계산 함수
const calculateProgressWidth = (spent, budget) => {
  const percentage = (spent / budget) * 100;
  // 100%를 초과하지 않도록 제한
  return Math.min(percentage, 100) + "%";
};

// 상태 계산 헬퍼 함수
const calculateStatus = (spent, budget) => {
  const ratio = (spent / budget) * 100;
  if (ratio <= 50) return "safe";
  if (ratio < 80) return "warning";
  return "danger";
};

// 데이터 가져오기
const fetchData = async () => {
  try {
    const data = await apiStore.fetchRepaymentSummary(1);
    expenditure.value = apiStore.totalSpent;
    income.value = apiStore.income;

    // 소비 분석 데이터 가져오기
    const consumptionData = await apiStore.fetchConsumptionAnalysis(1);

    // budgetItems 업데이트
    if (consumptionData && consumptionData.categories) {
      budgetItems.value = consumptionData.categories.map((category) => ({
        name: category.category === "쇼핑" ? "쇼핑비" : category.category,
        spent: category.amount,
        budget: category.suggestedReducedAmount,
        status: calculateStatus(
          category.amount,
          category.suggestedReducedAmount
        ),
      }));
    }

    // 최신 달의 거래 내역을 이벤트로 변환
    const latestMonth = data.summary[data.summary.length - 1];
    if (latestMonth && latestMonth.transactions) {
      events.value = convertTransactionsToEvents(latestMonth.transactions);
    }
  } catch (error) {
    console.error("Failed to fetch data:", error);
  }
};

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(fetchData);

// Function to get status text
const getStatusText = (status) => {
  switch (status) {
    case "safe":
      return "안전";
    case "danger":
      return "위험";
    case "warning":
      return "적정";
    default:
      return "";
  }
};

// Function to get status class
const getStatusClass = (status) => {
  switch (status) {
    case "safe":
      return "status-safe";
    case "danger":
      return "status-danger";
    case "warning":
      return "status-warning";
    default:
      return "";
  }
};

const totalBudget = computed(() =>
  budgetItems.value.reduce((sum, item) => sum + item.budget, 0)
);

const toggleEditMode = () => {
  router.push("/repayment-plan-suggestion");
};
</script>

<style>
@import "./LoanDashBoard.css";
</style>
