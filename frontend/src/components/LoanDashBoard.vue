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
          <span>{{ currentAmount.toLocaleString() }}원</span>
          <span>/ {{ totalAmount.toLocaleString() }}원</span>
        </div>
      </div>
      <section class="summary">
        <div class="summary-item">
          <span>목표 상환 원금</span>
          <span>{{ targetAmount.toLocaleString() }}원</span>
        </div>
        <div class="summary-item">
          <span>이자 납입액</span>
          <span>{{ interestAmount.toLocaleString() }}원</span>
        </div>
        <div class="summary-total">
          <span>총 납부액</span>
          <span>{{ totalPayment.toLocaleString() }}원</span>
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
          <h2 class="plan-title">{{ selectedPlanName }}</h2>
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
            <span>{{ formatAmount(item.spent) }}원</span>&#47;
            <span>{{ formatAmount(item.budget) }}원</span>
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

// ref 변수들 선언
const userId = 1;
const currentAmount = ref(0);
const totalAmount = ref(0);
const targetAmount = ref(0);
const interestAmount = ref(0);
const totalPayment = ref(0);
const progressPercentage = ref(0);
const expenditure = ref(0);
const income = ref(0);
const budgetItems = ref([]);
const events = ref([]);
const selectedPlanName = ref("");

// 금액 포맷팅 함수
const formatAmount = (amount) => {
  return new Intl.NumberFormat("ko-KR").format(amount);
};

// Progress width 계산 함수
const calculateProgressWidth = (spent, budget) => {
  const percentage = (spent / budget) * 100;
  return Math.min(percentage, 100) + "%";
};

// 데이터 가져오기
const fetchData = async () => {
  try {
    // 상환 상태 데이터 가져오기
    await apiStore.fetchRepaymentStatus(userId);

    // 현재 날짜로 현재 월 구하기
    const today = new Date();
    const currentMonth = `${today.getFullYear()}-${String(
      today.getMonth() + 1
    ).padStart(2, "0")}`;

    // 상환 현황 데이터 설정
    currentAmount.value = Number(apiStore.paidAmount);
    totalAmount.value = Number(apiStore.totalAmount);
    progressPercentage.value = Number(apiStore.completedPercentage.toFixed(1));

    // 소비 데이터 가져오기
    const data = await apiStore.fetchRepaymentSummary(userId);
    expenditure.value = apiStore.totalSpent;
    income.value = apiStore.income;

    // 유저가 선택했던 플랜 데이터 가져오기
    const selectedPlanData = await apiStore.fetchCurrentPlan(userId);
    if (selectedPlanData) {
      const selectedPlanId = selectedPlanData.selected_plan_group_id;

      // 플랜 데이터 가져오기
      const plansData = await apiStore.fetchRepaymentPlans(userId);
      const selectedPlan = plansData.plans.find(
        (plan) => plan.plan_id === selectedPlanId
      );

      // console.log(
      //   selectedPlan.details.map(
      //     (detail) => detail.original_amount - detail.reduced_amount
      //   )
      // );

      selectedPlanName.value = selectedPlan.plan_name;
    }

    // 소비 분석 데이터 가져오기
    const consumptionData = await apiStore.fetchConsumptionAnalysis(userId);

    // 상태 계산 헬퍼 함수
    const calculateStatus = (percent) => {
      if (percent <= 50) return "safe";
      if (percent < 80) return "warning";
      return "danger";
    };

    // budgetItems 업데이트
    if (consumptionData && consumptionData.categories) {
      budgetItems.value = consumptionData.categories.map((category) => ({
        name: apiStore.categories[category.category_id],
        spent: category.amount,
        budget: category.suggestedReducedAmount,
        status: calculateStatus(category.usingPercentage),
      }));
    }
    // console.log(budgetItems.value);

    // 달력 이벤트 데이터 처리
    if (data.summary && data.summary.length > 0) {
      // VueCal에 표시할 이벤트 배열
      let allEvents = [];

      // 각 월별 데이터를 순회하면서 이벤트 생성
      data.summary.forEach((monthData) => {
        if (monthData.transactions) {
          const monthEvents = monthData.transactions.map((transaction) => ({
            start: transaction.date, // "2024-11-01" 형식
            end: transaction.date,
            title:
              transaction.category === "소득"
                ? `+${formatAmount(transaction.amount)}`
                : `-${formatAmount(transaction.amount)}`,
            class:
              transaction.category === "소득"
                ? "income-event"
                : "expense-event",
          }));
          allEvents = [...allEvents, ...monthEvents];
        }
      });

      // 모든 월의 이벤트를 events에 설정
      events.value = allEvents;
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
