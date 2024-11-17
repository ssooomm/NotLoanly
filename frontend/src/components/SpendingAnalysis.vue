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
import { ref } from 'vue';
import DoughnutChart from './DoughnutChart.vue';
import BarChart from './BarChart.vue';


const totalSpending = 1824235;


const doughnutChartData = ref({
  labels: ['쇼핑/의류비', '식비', '여가/취미비'],
  datasets: [
    {
      label: '소비 비율',
      data: [638465, 241881, 170940],
      backgroundColor: ['#4bc0c0', '#36a2eb', '#ff6384'],
      hoverOffset: 4,
    },
  ],
});

// Calculate category amounts
const categoryAmounts = doughnutChartData.value.datasets[0].data;

// Bar 차트 데이터
const barChartData = ref({
  labels: ['쇼핑/의류비', '여가/취미비', '식비'],
  datasets: [
    {
      label: '나의 소비',
      data: [638465, 170940, 241881],
      backgroundColor: '#ffcc00',
    },
    {
      label: '20대 평균',
      data: [700000, 200000, 250000],
      backgroundColor: '#4caf50',
    },
  ],
});
</script>

<style scoped>
.spending-analysis {
  text-align: center;
}

.doughnutChart {
  width: 90%;
  margin-left: 20px;
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
  margin-top: 25px;
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