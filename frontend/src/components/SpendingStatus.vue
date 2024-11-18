<template>
  <div>
    <h2>오수민님의 상환현황</h2>
    <div class="chart-container">
      <div class="donut-chart-wrapper">
        <DoughnutChart :data="donutChartData" />
        <p class="percentage-text">{{ completedPercentage.toFixed(1) }}%</p>
      </div>
      <p class="amount-text">상환 금액 530,000</p>
    </div>
    <div class="status-circles">
      <div class="circle-row">
        <div class="circle active">
          <img src="@/assets/stamp.png" alt="1개월" class="icon" /> 
          1개월
        </div>
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
import DoughnutChart from './DoughnutChart.vue'; 
import BarChart from './BarChart.vue'; 

const completedPercentage = 17.3;

const donutChartData = ref({
  labels: ['상환 비율'],
  datasets: [{
    data: [completedPercentage, 100 - completedPercentage],
    backgroundColor: ['#ecbf28', '#e0e0e0'],
    borderWidth: 0,
  }]
});

const monthlyData = [30, 50, 80, 40, 60, 90, 20, 70, 100, 50, 80, 60]; 

const barChartData = ref({
  labels: Array.from({ length: 12 }, (_, i) => i + 1), 
  datasets: [{
    label: '월별 상환금액',
    data: monthlyData,
    backgroundColor: 'rgba(255, 206, 86, 0.6)', 
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
  margin: 30px 0;
}

.donut-chart-wrapper {
  position: relative; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  width: 200px; 
  height: 200px; 
  margin-left: 10px;
}

.percentage-text {
  position: absolute; 
  margin-top: 30px;
  font-size: 18px; 
  font-weight: bold; 
  color: #ecbf28; 
}

.amount-text {
  margin-left: 20px; 
  font-size: 16px;
  font-weight: bold;
}

.bar-chart-container {
  margin: 20px 0; 
  max-width: 800px;
}

.status-circles {
  margin-top: 20px;
  margin-bottom: 50px;
}

.circle-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px; /* 간격 조정 */
}

.circle {
  width: 70px; 
  height: 70px; 
  border-radius: 50%; 
  background-color: #e0e0e0; 
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative; 
  font-size: 14px;
  transition: background-color 0.3s; 
}

.circle.active {
  border: 2px solid #ecbf28; 
  background-color: #fff; 
}

.circle:hover {
  background-color: #d0d0d0; 
}

.icon {
  width: 45px; 
  height: 50px; 
  position: absolute;
  top: 10px; 
  left: 10px; 
}
</style>