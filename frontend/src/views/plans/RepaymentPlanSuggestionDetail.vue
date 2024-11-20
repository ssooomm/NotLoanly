<template>
  <v-card flat class="pa-2 text-start" v-if="currentPlan">
    <v-card-title class="font-weight-bold">
      {{ currentPlan.plan_name }}
    </v-card-title>
    <v-card-subtitle class="text-start" style="white-space: normal">
      {{ currentPlan.description }}
    </v-card-subtitle>
    <v-card-text>
      <div class="chart-container">
        <StackedBarCharts
          v-if="stackedBarChartData"
          :data="stackedBarChartData"
        />
      </div>

      <v-col class="px-0">
        <v-col class="pa-0">
          <div class="text-start category-details">
            <h4 class="mb-1">소비 목표</h4>
            <div
              v-for="(amount, index) in categoryAmounts"
              :key="index"
              class="category-item"
            >
              <span
                class="font-weight-bold"
                :style="{
                  color: stackedBarChartData.datasets[0].backgroundColor[index],
                }"
              >
                {{ stackedBarChartData.labels[index] }}:
              </span>
              <span>
                {{ amount.toLocaleString() }}원 &#8658;
                {{ modifiedCategoryAmounts[index].toLocaleString() }}원
              </span>
            </div>
          </div>
        </v-col>
      </v-col>
      <v-col class="px-0 pt-6 text-end">
        <div>상환 목표 기간: {{ currentPlan.duration }}개월</div>
        <div>월 상환금: {{ currentPlan.monthlyPayment }}만원</div>
      </v-col>
      <v-col class="pa-0 text-end">
        <h3>총 절약액: {{ currentPlan.totalSavingAmount }}원</h3>
      </v-col>
    </v-card-text>
    <v-card-actions>
      <v-btn
        block
        color="yellow-darken-2"
        text="플랜 선택하기"
        variant="flat"
      ></v-btn>
    </v-card-actions>
  </v-card>
  <v-card v-else class="pa-5" flat>
    <v-card-title class="text-h5 font-weight-bold text-start">
      플랜을 찾을 수 없습니다
    </v-card-title>
  </v-card>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import StackedBarCharts from "../../components/StackedBarCharts.vue";
import { useApiStore } from "../../stores/apiStore";

const route = useRoute();
const apiStore = useApiStore();

const userId = 1;
const planId = ref(null);
const currentPlan = ref(null);

const categoryAmounts = ref([]);
const modifiedCategoryAmounts = ref([]);
const stackedBarChartData = ref({
  labels: [],
  datasets: [
    {
      label: "목표 소비액",
      data: [],
      backgroundColor: [
        "#66BB6A", // 금융
        "#FF6384", // 주거 및 통신
        "#36A2EB", // 식비
        "#FFCE56", // 교통
        "#4BC0C0", // 쇼핑
        "#9966FF", // 여가
        "#FF9F40", // 건강
        "#C9CBCF", // 기타
      ],
      hoverOffset: 4,
    },
    {
      label: "절약 금액",
      data: [],
      backgroundColor: [
        "rgba(102, 187, 106, 0.3)", // 금융 (연한 녹색)
        "rgba(255, 99, 132, 0.3)", // 주거 및 통신 (연한 핑크색)
        "rgba(54, 162, 235, 0.3)", // 식비 (연한 파란색)
        "rgba(255, 206, 86, 0.3)", // 교통 (연한 노란색)
        "rgba(75, 192, 192, 0.3)", // 쇼핑 (연한 청록색)
        "rgba(153, 102, 255, 0.3)", // 여가 (연한 보라색)
        "rgba(255, 159, 64, 0.3)", // 건강 (연한 주황색)
        "rgba(201, 203, 207, 0.3)", // 기타 (연한 회색)
      ],
      hoverOffset: 4,
    },
  ],
});

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  planId.value = Number(route.params.id);
  fetchPlanData(planId.value);
});

const fetchPlanData = async () => {
  try {
    const data = await apiStore.fetchRepaymentPlans(userId);
    currentPlan.value = data.plans.find(
      (plan) => plan.plan_id === planId.value
    );
    console.log(currentPlan.value);
    // if (plan) {
    //   currentPlan.value = plan;
    //   // 차트 데이터 및 카테고리 정보 설정
    //   stackedBarChartData.value.labels = plan.categories.map(
    //     (category) => category.categoryName
    //   );
    //   stackedBarChartData.value.datasets[0].data = plan.categories.map(
    //     (category) => category.modifiedSpending
    //   );
    //   stackedBarChartData.value.datasets[1].data = plan.categories.map(
    //     (category) => category.suggestedSaving
    //   );

    //   categoryAmounts.value = plan.categories.map(
    //     (category) => category.currentSpending
    //   );
    //   modifiedCategoryAmounts.value = plan.categories.map(
    //     (category) => category.modifiedSpending
    //   );
    // } else {
    //   console.error("플랜을 찾을 수 없습니다");
    // }
  } catch (error) {
    console.error("데이터 가져오기 실패:", error);
  }
};

/*
category id
1: 소득
2: 대출 상환
3: 금융
4: 주거 및 통신
5: 식비
6: 교통
7: 쇼핑
8: 여가
9: 건강
10: 기타

plan 6개
plan_name: 의류 절약 플랜
category_id: 7 메인으로 절약

plan_name: 식비 절약 플랜 
category_id: 5 메인으로 절약

plan_name: 여가 및 문화생활 절약 플랜
category_id: 8 메인으로 절약

plan_name: 술/유흥 절약 플랜
category_id: 8 메인으로 절약

plan_name: 교통비 절약 플랜
category_id: 6 메인으로 절약

plan_name: 저축/투자 조정 플랜
category_id: 3 메인으로 절약

description 형식
{planName.parse(절약앞부분)} 카테고리를 중심으로 절약하는 플랜으로, {category_id} 부문에서 {saving_percentage}%의 절약률을 목표로 합니다.

*/

// const fetchConsumptionData = async () => {
//   try {
//     const response = await axios.get(
//       "/api/dashboard/consumption-analysis?user_id=1"
//     );
//     const data = response.data;
//     console.log(data.plan_name);

//     // currentPlan 설정
//     currentPlan.value = {
//       planName: data.plan_name,
//       description:
//         "금융 투자를 중심으로 절약하는 플랜으로, 금융 부문에서 40%의 높은 절약률을 목표로 합니다.",
//       duration: 12,
//       monthlyPayment: 103,
//       totalSavingAmount: data.totalAmount,
//     };

//     // 차트 데이터 및 카테고리 정보 설정
//     stackedBarChartData.value.labels = data.categories.map(
//       (category) => category.category
//     );
//     stackedBarChartData.value.datasets[0].data = data.categories.map(
//       (category) => category.suggestedReducedAmount
//     );
//     stackedBarChartData.value.datasets[1].data = data.categories.map(
//       (category) => category.amount - category.suggestedReducedAmount
//     );

//     categoryAmounts.value = data.categories.map((category) => category.amount);
//     modifiedCategoryAmounts.value = data.categories.map(
//       (category) => category.amount - category.suggestedReducedAmount
//     );
//   } catch (error) {
//     console.error("데이터 가져오기 실패:", error);
//   }
// };

// route params 변경 감지하여 데이터 업데이트
// watch(
//   () => route.params.id,
//   () => {
//     fetchConsumptionData();
//   }
// );

// 플랜 데이터 나중에 db에서 받아올 거
// const plan = {
//   planId: "001",
//   planName: "금융 중심 절약 플랜",
//   duration: 12,
//   monthlyPayment: 103,
//   totalSavingAmount: 515000,
//   description:
//     "금융 투자를 중심으로 절약하는 플랜으로, 금융 부문에서 40%의 높은 절약률을 목표로 합니다.",
//   categories: [
//     {
//       categoryId: 1,
//       categoryName: "금융",
//       currentSpending: 1000000,
//       savingPercentage: 40.0,
//       suggestedSaving: 400000,
//       modifiedSpending: 600000,
//     },
//     {
//       categoryId: 2,
//       categoryName: "주거 및 통신",
//       currentSpending: 530000,
//       savingPercentage: 10.0,
//       suggestedSaving: 53000,
//       modifiedSpending: 477000,
//     },
//     {
//       categoryId: 3,
//       categoryName: "식비",
//       currentSpending: 270000,
//       savingPercentage: 10.0,
//       suggestedSaving: 27000,
//       modifiedSpending: 243000,
//     },
//     {
//       categoryId: 4,
//       categoryName: "교통",
//       currentSpending: 70000,
//       savingPercentage: 10.0,
//       suggestedSaving: 7000,
//       modifiedSpending: 63000,
//     },
//   ],
// };

// const currentPlan = ref(null);

// // route params가 변경될 때마다 currentPlan 업데이트
// const updateCurrentPlan = () => {
//   const planId = parseInt(route.params.id);
//   currentPlan.value = plan;
//   // if (planId >= 0 && planId < plans.length) {
//   //     currentPlan.value = plan
//   // } else {
//   //     currentPlan.value = null
//   // }
// };

// const categories = plan.categories;

// // 누적 바 차트 데이터 생성
// const stackedBarChartData = ref({
//   labels: categories.map((category) => category.categoryName),
//   datasets: [
//     {
//       label: "목표 소비액",
//       data: categories.map((category) => category.modifiedSpending),
//       backgroundColor: [
//         "#4bc0c0", // 금융
//         "#36a2eb", // 주거 및 통신
//         "#ff6384", // 식비
//         "#ffcd56", // 교통
//       ],
//       hoverOffset: 4,
//     },
//     {
//       label: "절약 금액",
//       data: categories.map((category) => category.suggestedSaving),
//       backgroundColor: [
//         "#a3e3e3", // 금융 (연한 민트색)
//         "#aed8f4", // 주거 및 통신 (연한 하늘색)
//         "#ffb3ba", // 식비 (연한 분홍색)
//         "#ffe3a1", // 교통 (연한 노란색)
//       ],
//       hoverOffset: 4,
//     },
//   ],
// });

// const categoryAmounts = categories.map((category) => category.currentSpending);
// const modifiedCategoryAmounts = categories.map(
//   (category) => category.modifiedSpending
// );

// // 컴포넌트 마운트 시 초기화
// onMounted(() => {
//   updateCurrentPlan();
// });

// // route params 변경 감지
// watch(
//   () => route.params.id,
//   () => {
//     updateCurrentPlan();
//   }
// );
</script>

<style scoped>
.fill-height {
  height: 100vh !important;
}

.v-card {
  background-color: #f7f7f7;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
}

.flex-grow-1 {
  flex-grow: 1;
  /* 남은 공간을 채움 */
}

.chart-container {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  background: white;
}

.category-details {
  /* margin-top: 20px; */
  text-align: center;
}
</style>
