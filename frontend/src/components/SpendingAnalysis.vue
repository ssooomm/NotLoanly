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
          {{ doughnutChartData.labels[index] }}
        </span>
        <span>{{ amount.toLocaleString() }} 원</span>
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
  labels: ['식비', '주거/통신', '교통', '쇼핑', '여가', '건강', '기타'],
  datasets: [
    {
      label: '나의 소비',
      data: [], // 이 부분은 API에서 받아온 데이터로 채워질 것입니다
      backgroundColor: '#ffcc00',
    },
    {
      label: '20대 평균',
      data: [304000, 500000, 45000, 200000, 70000, 60000, 100000],
      backgroundColor: '#4caf50',
    },
  ],
});

const fetchConsumptionData = async () => {
  const data = await apiStore.fetchRepaymentSummary(1); 
  const summaryData = apiStore.summary;

  if (summaryData && summaryData.length > 0) {
    // 현재 날짜 기준으로 이전 달 계산
    const today = new Date();
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1);
    const lastMonthString = `${lastMonth.getFullYear()}-${String(lastMonth.getMonth() + 1).padStart(2, '0')}`;
    
    // 이전 달 데이터 찾기
    const lastMonthData = summaryData.find(month => month.month === lastMonthString);
    
    if (lastMonthData) {
      // 소득, 금융, 대출 상환을 제외한 실제 소비 카테고리만 필터링
      const spendingCategories = lastMonthData.categories.filter(cat => 
        !["소득","대출 상환"].includes(cat.category)
      );

      totalSpending.value = spendingCategories.reduce((sum, cat) => sum + cat.totalAmount, 0);
      
      // 도넛 차트 데이터 설정
      doughnutChartData.value = {
        labels: spendingCategories.map(cat => cat.category),
        datasets: [{
          label: '소비 비율',
          data: spendingCategories.map(cat => cat.totalAmount),
          backgroundColor: [
            "#66BB6A", // 금융
            '#FF6384', // 주거 및 통신
            '#36A2EB', // 식비
            '#FFCE56', // 교통
            '#4BC0C0', // 쇼핑
            '#9966FF', // 여가
            '#FF9F40', // 건강
            '#C9CBCF'  // 기타
          ],
          hoverOffset: 4
        }]
      };

      // 카테고리별 금액 설정
      categoryAmounts.value = spendingCategories.map(cat => cat.totalAmount);

      // 바 차트 데이터 업데이트
      const mySpending = barChartData.value.labels.map(label => {
        const category = spendingCategories.find(cat => 
          label === '주거/통신' ? cat.category === '주거 및 통신' : cat.category === label
        );
        return category ? category.totalAmount : 0;
      });

      barChartData.value = {
        labels: ['식비', '주거/통신', '교통', '쇼핑', '여가', '건강', '기타'],
        datasets: [
          {
            label: '나의 소비',
            data: mySpending,
            backgroundColor: '#ffcc00',
          },
          {
            label: '20대 평균',
            data: [304000, 500000, 45000, 200000, 70000, 60000, 100000],
            backgroundColor: '#4caf50',
          },
        ],
      };
    }
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
  margin-top : 25px;
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

.category-details {
  margin-top: 20px; 
}

.category-item {
  font-size: 16px; 
  margin: 5px 0; 
}
</style>