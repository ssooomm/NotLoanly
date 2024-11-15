<template>
  <div>
    <h2>오수민님의 상환현황</h2>
    <div class="chart-container">
      <DoughnutChart :data="donutChartData" />
      <p class="amount-text">전체 상환 금액 530,000원</p>
    </div>
    <div class="status-circles">
      <div class="circle-row">
        <div class="circle">1개월</div>
        <div class="circle">2개월</div>
        <div class="circle">3개월</div>
      </div>
      <div class="circle-row">
        <div class="circle">4개월</div>
        <div class="circle">5개월</div>
        <div class="circle">6개월</div>
      </div>
    </div>
    <div class="bar-chart-container">
      <BarChart :data="barChartData" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DoughnutChart from './DoughnutChart.vue'; // Adjust the path as necessary
import BarChart from './BarChart.vue'; // Adjust the path as necessary

const completedPercentage = 17.3;

// Chart data for the donut chart
const donutChartData = ref({
  labels: ['상환 비율'],
  datasets: [{
    data: [completedPercentage, 100 - completedPercentage],
    backgroundColor: ['#4caf50', '#e0e0e0'],
    borderWidth: 0,
  }]
});

// Monthly data for the bar chart
const monthlyData = [30, 50, 80, 40, 60, 90, 20, 70, 100, 50, 80, 60]; // Example data for each month

// Chart data for the bar chart
const barChartData = ref({
  labels: Array.from({ length: 12 }, (_, i) => i + 1), // Months 1 to 12
  datasets: [{
    label: '월별 상환금액',
    data: monthlyData,
    backgroundColor: 'rgba(255, 206, 86, 0.6)', // Yellow color
    borderColor: 'rgba(255, 206, 86, 1)',
    borderWidth: 1,
  }]
});
</script>

<style scoped>
.chart-container {
  display: flex; 
  align-items: center; 
  width: 65%;
  margin: 50px 0;
}

.amount-text {
  margin-left: 20px; 
  font-size: 16px; 
}

.bar-chart-container {
  margin: 20px 0; /* Space between charts */
}

.status-circles {
  margin-top: 20px;
  margin-bottom: 50px;
}

.circle-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px; /* Space between rows */
}

.circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>