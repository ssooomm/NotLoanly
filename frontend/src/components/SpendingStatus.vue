<template>
  <div>
    <h2>오수민님의 상환현황</h2>
    <div class="chart-container">
      <div class="donut-chart-wrapper">
        <DoughnutChart :data="donutChartData" />
        <p class="percentage-text">{{ completedPercentage.toFixed(1) }}%</p>
      </div>
      <p class="amount-text">상환 금액 {{ paidAmount.toLocaleString() }} 원</p>
    </div>
    <div class="bar-chart-container">
      <BarChart :data="barChartData" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import DoughnutChart from './DoughnutChart.vue'; 
import BarChart from './BarChart.vue'; 
import { useApiStore } from '@/stores/apiStore'; // Pinia 스토어 가져오기

const apiStore = useApiStore(); // Pinia 스토어 인스턴스 생성

const paidAmount = ref(0);
const totalAmount = 5000000; // 총 대출 금액
const completedPercentage = ref(0);

const donutChartData = ref({
  labels: ['상환 비율'],
  datasets: [{
    data: [completedPercentage.value, 100 - completedPercentage.value],
    backgroundColor: ['#ecbf28', '#e0e0e0'],
    borderWidth: 0,
  }]
});

const monthlyData = ref([]); // 월별 상환 데이터

const barChartData = ref({
  labels: Array.from({ length: 12 }, (_, i) => `${i + 1}월`), 
  datasets: [{
    label: '월별 상환금액',
    data: monthlyData.value,
    backgroundColor: 'rgba(255, 206, 86, 0.6)', 
    borderColor: 'rgba(255, 206, 86, 1)',
    borderWidth: 1,
  }]
});

// 상환 현황 데이터 가져오기
const fetchRepaymentStatus = async () => {
  await apiStore.fetchRepaymentStatus(); 

  
  paidAmount.value = apiStore.paidAmount; 
  completedPercentage.value = (paidAmount.value / totalAmount) * 100; 

  
  donutChartData.value.datasets[0].data = [completedPercentage.value, 100 - completedPercentage.value];

  // 월별 상환 데이터 업데이트
  monthlyData.value = apiStore.repaymentChart.map(item => item.paid);
  barChartData.value.datasets[0].data = monthlyData.value;
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(fetchRepaymentStatus);
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
</style>