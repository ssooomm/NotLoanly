<template>
  <div>
    <h2>최민호님의 상환현황</h2>
    <div class="chart-container">
      <div class="donut-chart-wrapper">
        <DoughnutChart :data="donutChartData" />
        <p class="percentage-text">{{ completedPercentage.toFixed(1) }}%</p>
      </div>
    </div>
    <div class="amount-bg">
      <div class="amount-text mb-3">
        <span class="me-2">상환 금액</span> {{ paidAmount.toLocaleString() }}원
      </div>
      <div class="amount-text"><span class="me-2">남은 금액</span> {{ remainingAmount.toLocaleString() }}원</div>
    </div>
    <div class="status-circles">
      <!-- 각 행에 3개씩 circle을 묶어서 렌더링 -->
      <div v-for="(row, rowIndex) in chunkedRepaymentPeriods" :key="rowIndex" class="circle-row">
        <div v-for="(month, index) in row" :key="index"
          :class="['circle', { active: repaymentPeriod.indexOf(month) < paidPeriod }]">
          <img v-if="repaymentPeriod.indexOf(month) < paidPeriod" src="@/assets/stamp.png" alt="상환 완료" class="icon" />
          {{ month }}개월
        </div>
      </div>
    </div>
    <!-- <div class="bar-chart-container">
      <BarChart :data="barChartData" />
    </div> -->
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import DoughnutChart from './DoughnutChart.vue';
import BarChart from './BarChart.vue';
import { useApiStore } from '@/stores/apiStore';

const apiStore = useApiStore();
const userId = 1;

const completedPercentage = ref(0);
const paidAmount = ref(0);
const remainingAmount = ref(0);
const repaymentPeriod = ref([]);
const paidPeriod = ref(0);

const donutChartData = ref({
  labels: ['상환 비율'],
  datasets: [{
    data: [0, 100],
    backgroundColor: ['#ecbf28', '#e0e0e0'],
    borderWidth: 0,
  }]
});

const barChartData = ref({
  labels: [],
  datasets: [{
    label: '월별 상환금액',
    data: [],
    backgroundColor: 'rgba(255, 206, 86, 0.6)',
    borderColor: 'rgba(255, 206, 86, 1)',
    borderWidth: 1,
  }]
});

// repaymentPeriod 배열을 3개씩 나누어 2차원 배열로 반환하는 computed 속성
const chunkedRepaymentPeriods = computed(() => {
  const chunkSize = 3;
  let chunks = [];
  for (let i = 0; i < repaymentPeriod.value.length; i += chunkSize) {
    chunks.push(repaymentPeriod.value.slice(i, i + chunkSize));
  }
  return chunks;
});

// 상환 현황 및 차트 데이터 가져오기
const fetchRepaymentData = async () => {
  try {
    const data = await apiStore.fetchRepaymentStatus(userId);

    completedPercentage.value = Number(apiStore.completedPercentage.toFixed(1));
    paidAmount.value = Number(apiStore.paidAmount);
    remainingAmount.value = Number(apiStore.remainingAmount);
    repaymentPeriod.value = Array.from({ length: Number(apiStore.totalPeriod) }, (_, i) => i + 1);
    paidPeriod.value = Number(apiStore.paidPeriod);

    // 도넛 차트 데이터 업데이트
    donutChartData.value = {
      labels: ['상환 비율'],
      datasets: [{
        data: [completedPercentage.value, 100 - completedPercentage.value],
        backgroundColor: ['#ecbf28', '#e0e0e0'],
        borderWidth: 0,
      }]
    };

    // 월별 상환 데이터 업데이트
    // const monthlyData = data.repaymentChart.map(item => parseInt(item.paid));
    // const monthlyLabels = data.repaymentChart.map(item => {
    //   const month = item.month.split('-')[1].replace(/^0+/, '');
    //   return `${month}월`;
    // });

    // barChartData.value = {
    //   labels: monthlyLabels,
    //   datasets: [{
    //     label: '월별 상환금액',
    //     data: monthlyData,
    //     backgroundColor: 'rgba(255, 206, 86, 0.6)',
    //     borderColor: 'rgba(255, 206, 86, 1)',
    //     borderWidth: 1,
    //   }]
    // };

  } catch (error) {
    console.error('Failed to fetch repayment data:', error);
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(fetchRepaymentData);
</script>


<style scoped>
.chart-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  margin: 2rem 0;
}

.donut-chart-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 65%;
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

.amount-bg {
  margin-left: 3rem;
  margin-right: 3rem;
  padding: 1rem;
  /* background-color: #e0e0e0; */
  border-radius: 15px;
  border: 2px solid #e0e0e0;
}

.amount-text {
  /* margin-left: 20px; */
  font-size: 16px;
  font-weight: bold;
}

.bar-chart-container {
  margin: 20px 0;
  max-width: 800px;
}

.status-circles {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

.circle-row {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
  /* 간격 조정 */
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