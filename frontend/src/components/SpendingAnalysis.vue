<template>
  <div class="spending-analysis">
    <h2>오수민님의 월 평균 소비</h2>
    <div class="doughnutChart">
      <div class="doughnut-wrapper">
        <DoughnutChart v-if="doughnutChartData" :data="doughnutChartData" />
        <p class="total-spending">{{ totalSpending.toLocaleString() }} 원</p>
      </div>
    </div>

    <div class="category-details">
      <div v-for="(amount, index) in categoryAmounts" :key="index" class="category-item">
        <span :style="{ color: doughnutChartData.datasets[0].backgroundColor[index] }">
          {{ doughnutChartData.labels[index] }}:
        </span>
        <span>{{ amount.toLocaleString() }} 원</span>
      </div>
    </div>

    <h3>20대 평균 소비 TOP3</h3>
    <BarChart v-if="barChartData" :data="barChartData" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DoughnutChart from './DoughnutChart.vue';
import BarChart from './BarChart.vue';
import { useApiStore } from '@/stores/apiStore'; 

const apiStore = useApiStore(); 

const totalSpending = ref(0);
const doughnutChartData = ref({
  labels: [],
  datasets: [
    {
      label: '소비 비율',
      data: [],
      backgroundColor: ['#4bc0c0', '#36a2eb', '#ff6384'],
      hoverOffset: 4,
    },
  ],
});

// Calculate category amounts
const categoryAmounts = ref([]);

// Bar 차트 데이터
const barChartData = ref({
  labels: ['나의 소비', '20대 평균'],
  datasets: [
    {
      label: '나의 소비',
      data: [],
      backgroundColor: '#ffcc00',
    },
    {
      label: '20대 평균',
      data: [700000, 200000, 250000], 
      backgroundColor: '#4caf50',
    },
  ],
});

// 소비 분석 데이터 가져오기
const fetchConsumptionData = async () => {
  await apiStore.fetchConsumptionAnalysis(); 
  const summaryData = apiStore.consumptionAnalysis.summary;

  // 도넛 차트 데이터 설정
  if (summaryData.length > 0) {
    const latestMonthData = summaryData[0]; 
    totalSpending.value = latestMonthData.totalSpent;
    categoryAmounts.value = latestMonthData.categories.map(category => category.totalAmount); // 카테고리 금액

    
    doughnutChartData.value.labels = latestMonthData.categories.map(category => category.category);
    doughnutChartData.value.datasets[0].data = categoryAmounts.value;

    
    barChartData.value.datasets[0].data = [latestMonthData.totalSpent]; 
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(fetchConsumptionData);
</script>

<style scoped>
.spending-analysis {
  text-align: center;
}

.doughnutChart {
  width: 85%;
  margin-left: 20px;
  margin-top: 20px;
}

.doughnut-wrapper {
  position: relative; 
}

.total-spending {
  position: absolute; 
  top: 50%; 
  left: 50%; 
  transform: translate(-50%, -50%); 
  font-size: 18px;
  font-weight: bold; 
  margin-top: 2px;
  color: #080600; 
}

h2 {
  margin-bottom: 10px;
}

h3 {
  margin: 20px 0;
}

.category-details {
  margin-top: 20px; 
}

.category-item {
  font-size: 16px; 
  margin: 5px 0; 
}
</style>