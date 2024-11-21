<template>
  <v-card flat class="pa-2 text-start" v-if="currentPlan">
    <!-- 플랜명 -->
    <v-card-title class="font-weight-bold">
      {{ currentPlan.plan_name }}
    </v-card-title>
    <!-- 플랜 간단 설명 -->
    <v-card-subtitle class="text-start" style="white-space: normal">
      <div
        v-for="(description, index) in currentPlan.descriptions"
        :key="index"
        v-html="description"
      ></div>
    </v-card-subtitle>
    <v-card-text>
      <div class="chart-container">
        <StackedBarCharts
          v-if="stackedBarChartData"
          :data="stackedBarChartData"
        />
      </div>
      <div class="desc-container">
        <v-col class="pa-0">
          <v-col class="pa-0">
            <div class="text-start category-details">
              <h3 class="mb-1">소비 목표</h3>
              <div
                v-for="(amount, index) in categoryAmounts"
                :key="index"
                class="category-item"
              >
                <span class="font-weight-bold">
                  <v-badge dot inline :color="categoryColors[index]"></v-badge>

                  {{ stackedBarChartData.labels[index] }}
                </span>
                <span
                  >&#58; {{ amount.toLocaleString() }}원 &#8658;
                  {{ modifiedCategoryAmounts[index].toLocaleString() }}원
                </span>
              </div>
            </div>
          </v-col>
        </v-col>
        <v-divider></v-divider>
        <v-col class="px-0 text-end">
          <div>상환 목표 기간: {{ currentPlan.duration }}개월</div>
          <div>
            월 상환금: {{ currentPlan.total_amount.toLocaleString() }}원
          </div>
        </v-col>
        <v-col class="pa-0 text-end">
          <h3>총 절약액: {{ currentPlan.totalSavingAmount }}원</h3>
        </v-col>
      </div>
    </v-card-text>
    <v-card-actions class="px-4">
      <v-btn
        block
        color="yellow-darken-2"
        text="플랜 선택하기"
        variant="flat"
        @click="handleConfirm"
      ></v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { inject, ref, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import StackedBarCharts from "../../components/StackedBarCharts.vue";
import { useApiStore } from "../../stores/apiStore";

const route = useRoute();
const router = useRouter();
const apiStore = useApiStore();

const categoryColors = inject("categoryColors");
const lightCategoryColors = categoryColors.map((color) => {
  // RGB 색상을 RGBA로 변환하고 투명도를 추가
  const rgbaColor = color
    .replace("#", "rgba(")
    .replace(/([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})/i, (match, r, g, b) => {
      return `${parseInt(r, 16)}, ${parseInt(g, 16)}, ${parseInt(b, 16)}, 0.3)`;
    });
  return rgbaColor;
});

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
      backgroundColor: categoryColors,
      hoverOffset: 4,
    },
    {
      label: "절약 금액",
      data: [],
      backgroundColor: lightCategoryColors,
      hoverOffset: 4,
    },
  ],
});

// 카테고리 목록
const categories = apiStore.categories;

// 플랜 설명
const plansDesc = {
  의류: 7,
  식비: 5,
  문화생활: 8,
  "술/유흥": 8,
  교통비: 6,
  "저축/투자": 3,
};

const fetchPlanData = async (planId) => {
  try {
    const data = await apiStore.fetchRepaymentPlans(userId);
    currentPlan.value = data.plans.find((plan) => plan.plan_id === planId);

    if (currentPlan.value) {
      // Description 객체 생성
      currentPlan.value.descriptions = currentPlan.value.details.map(
        (detail) => {
          const matchedCategoryId =
            plansDesc[currentPlan.value.plan_name.split(" ")[0]];
          if (matchedCategoryId === detail.category_id) {
            return `${
              categories[detail.category_id]
            } 카테고리를 중심으로 절약하는 플랜으로,<br/>해당 카테고리에서 ${detail.saving_percentage.toFixed(
              2
            )}%의 절약률을 목표로 합니다.`;
          }
        }
      );

      // 카테고리 소비 금액 및 수정된 금액 설정
      categoryAmounts.value = currentPlan.value.details.map(
        (detail) => detail.original_amount
      );
      modifiedCategoryAmounts.value = currentPlan.value.details.map(
        (detail) => detail.original_amount - detail.reduced_amount
      );

      // 차트 데이터 설정
      stackedBarChartData.value.labels = currentPlan.value.details.map(
        (detail) => categories[detail.category_id]
      );

      // 목표 소비액 설정
      stackedBarChartData.value.datasets[0].data = categoryAmounts.value.map(
        (_, index) => modifiedCategoryAmounts.value[index]
      );

      // 절약 금액 설정
      stackedBarChartData.value.datasets[1].data =
        currentPlan.value.details.map((detail) => detail.reduced_amount);

      const totalSavings = currentPlan.value.details.reduce(
        (sum, detail) => sum + detail.reduced_amount,
        0
      );

      currentPlan.value.totalSavingAmount = totalSavings.toLocaleString();
    }
  } catch (error) {
    console.error("데이터 가져오기 실패:", error);
  }
};

// 확인 버튼 클릭 시 이벤트
const handleConfirm = async () => {
  try {
    console.log(planId.value);
    const response = await apiStore.selectRepaymentPlan(userId, planId.value);

    if (response.status === "success") {
      console.log("플랜 선택이 완료되었습니다.");
      router.push({ name: "Main" });
    }
  } catch (error) {
    console.error("플랜 선택 중 오류 발생:", error);
    alert("플랜 선택에 실패했습니다. 다시 시도해 주세요.");
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  planId.value = Number(route.params.id);
  fetchPlanData(planId.value);
});
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

.desc-container {
  flex-direction: column;
  padding: 16px;
  margin: 20px 0 0 0;
  border-radius: 10px;
  background: white;
}

.category-details {
  margin-bottom: 10px;
  text-align: center;
}

.category-item {
  margin: 5px 0;
}
</style>
