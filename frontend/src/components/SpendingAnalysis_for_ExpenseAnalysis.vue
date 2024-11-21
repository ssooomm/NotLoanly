<template>
  <div class="spending-analysis">
    <h2>소비 분석</h2>
    <div class="doughnutChart">
      <div class="doughnut-wrapper">
        <DoughnutChart v-if="doughnutChartData" :data="doughnutChartData" />
        <p class="total-spending">{{ totalSpending.toLocaleString() }} 원</p>
      </div>
    </div>

    <div class="category-details">
      <div v-for="(category, index) in categories" :key="index" class="category-item">
        <span :style="{ color: chartColors[index] }">
          {{ category.name }}
        </span>
        <span>{{ category.amount.toLocaleString() }} 원</span>
      </div>
    </div>

    <h3>20대 평균 소비</h3>
    <BarChart v-if="barChartData" :data="barChartData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DoughnutChart from './DoughnutChart.vue';
import BarChart from './BarChart.vue';
import { useApiStore } from '@/stores/apiStore';

const apiStore = useApiStore();

// 카테고리 매핑
const categoryMap = {
  1: '소득',
  2: '대출 소비',
  3: '금융',
  4: '주거 및 통신',
  5: '식비',
  6: '교통',
  7: '쇼핑',
  8: '여가',
  9: '건강',
  10: '기타'
};

// 도넛 차트에 표시할 카테고리 순서 정의 (금융 포함)
const doughnutDisplayOrder = ['금융', '식비', '주거 및 통신', '교통', '쇼핑', '여가', '건강', '기타'];

// 바 차트에 표시할 카테고리 순서 정의 (금융 제외)
const barDisplayOrder = ['식비', '주거 및 통신', '교통', '쇼핑', '여가', '건강', '기타'];

const chartColors = [
              "#66BB6A", // 금융
              "#FF6384", // 주거 및 통신
              "#36A2EB", // 식비
              "#FFCE56", // 교통
              "#4BC0C0", // 쇼핑
              "#9966FF", // 여가
              "#FF9F40", // 건강
              "#C9CBCF", // 기타
];

const totalSpending = ref(0);
const categories = ref([]);
const doughnutChartData = ref(null);
const barChartData = ref(null);

const fetchData = async () => {
  try {
    const expenses = await apiStore.fetchUserExpenses(1, 9);
    
    // 소득, 대출 소비 제외하고 데이터 정리
    const expenseMap = new Map();
    expenses
      .filter(item => ![1, 2].includes(item.category_id))
      .forEach(item => {
        const categoryName = categoryMap[item.category_id];
        expenseMap.set(categoryName, item.total_amount);
      });

    // 총 지출액 계산
    totalSpending.value = Array.from(expenseMap.values()).reduce((sum, amount) => sum + amount, 0);

    // 정해진 순서대로 카테고리 데이터 구성 (금융 포함)
    categories.value = doughnutDisplayOrder.map(categoryName => ({
      name: categoryName,
      amount: expenseMap.get(categoryName) || 0
    }));

    // 도넛 차트 데이터
    doughnutChartData.value = {
      labels: doughnutDisplayOrder,
      datasets: [{
        data: doughnutDisplayOrder.map(category => expenseMap.get(category) || 0),
        backgroundColor: chartColors,
        hoverOffset: 4
      }]
    };

    // 바 차트 데이터 (금융 제외)
    barChartData.value = {
      labels: barDisplayOrder,
      datasets: [
        {
          label: '나의 소비',
          data: barDisplayOrder.map(category => expenseMap.get(category) || 0),
          backgroundColor: "#ffcc00"
        },
        {
          label: '20대 평균',
          data: [304000, 500000, 45000, 200000, 70000, 60000, 100000],
          backgroundColor: '#4caf50'
        }
      ]
    };
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(fetchData);
</script>

<style scoped>
.spending-analysis {
  text-align: center;
  padding: 20px;
}

.doughnutChart {
  width: 90%;
  margin: 20px auto;
  max-width: 500px;
}

.doughnut-wrapper {
  position: relative;
  padding-bottom: 20px;
}

.total-spending {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 18px;
  font-weight: bold;
  margin-top: 25px;
  color: #333;
  text-align: center;
  line-height: 1.2;
}

.category-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 30px;
  padding: 0 50px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  padding: 5px 0;
}

h2 {
  margin-bottom: 10px;
}

h3 {
  margin: 20px 0;
}
</style>