<template>
  <div>
    <!-- 로딩 화면 -->
    <div v-if="isLoading" class="loading-container">
      <v-col
        ><v-progress-circular
          indeterminate
          color="yellow-darken-3"
          size="70"
          width="6"
        ></v-progress-circular>
        <v-col>GPT가 맞춤 상환 플랜을 생성중입니다.</v-col>
      </v-col>
    </div>

    <!-- 메인 콘텐츠 -->
    <div v-else>
      <!-- 상환 플랜 제목 -->
      <h1 class="title text-center">상환 플랜 선택</h1>
      <!-- 플랜 카드 리스트 -->
      <v-row dense>
        <v-col
          cols="12"
          class="justify-center"
          v-for="plan in plans"
          :key="plan.id"
        >
          <v-card class="plan-card" outlined>
            <div class="card-body" @click="goToDetail(plan.plan_id)" v-ripple>
              <!-- 왼쪽: 해시태그, 오른쪽: 이미지 -->
              <div class="left-content">
                <v-card-title class="plan-title">{{
                  plan.plan_name
                }}</v-card-title>
                <v-card-subtitle class="plan-hashtags">
                  <p
                    v-for="(hashtag, idx) in plan.hashtags.split(',')"
                    :key="idx"
                    class="hashtag"
                  >
                    {{ hashtag.trim() }}
                  </p>
                </v-card-subtitle>
              </div>
              <div class="right-content">
                <img
                  :src="images[plan.plan_id]"
                  class="plan-image"
                  alt="Plan Image"
                />
              </div>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useApiStore } from "../../stores/apiStore";

// 이미지 경로
import shoppingImage from "@/assets/img/shopping.png";
import foodImage from "@/assets/img/food.png";
import leisureImage from "@/assets/img/leisure.png";
import alcoholImage from "@/assets/img/alcohol.png";
import trafficImage from "@/assets/img/traffic.png";
import financeImage from "@/assets/img/finance.png";

const router = useRouter();
const apiStore = useApiStore();

const userId = 1;
const plans = ref([]);
const isLoading = ref(true); // 로딩 상태

// 이미지 매핑
const images = {
  1: shoppingImage,
  2: foodImage,
  3: leisureImage,
  4: alcoholImage,
  5: trafficImage,
  6: financeImage,
};

const fetchConsumptionData = async () => {
  try {
    // 사용자 선택 카테고리 기반 상환 플랜 가져오기
    const data = await apiStore.fetchRepaymentPlans(userId);
    plans.value = data.plans;
  } catch (error) {
    console.error("데이터 가져오기 실패:", error);
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  setTimeout(async () => {
    await fetchConsumptionData();
    isLoading.value = false; // 로딩 상태 해제
  }, 2000); // 2초 후 로딩 해제
});

// 세부 페이지로 이동하는 함수
const goToDetail = async (planId) => {
  try {
    const selectedPlan = plans.value.find((plan) => plan.plan_id === planId);
    console.log("selectedPlan:", selectedPlan);
    // console.log("planId:", planId);
    // console.log("plan.id:", plans.value[0].plan_id);
    if (selectedPlan) {
      await router.push({
        name: "RepaymentPlanSuggestionDetail",
        params: { id: selectedPlan.plan_id },
      });
    } else {
      console.error("해당 ID의 플랜을 찾을 수 없습니다:", planId);
    }
  } catch (error) {
    console.error("Navigation failed:", error);
  }
};
</script>

<style scoped>
/* 로딩 화면 스타일 */
.loading-container {
  position: fixed; /* 화면 전체 기준으로 고정 */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9); /* 배경에 살짝 투명도 추가 */
  z-index: 1000; /* 다른 콘텐츠보다 위에 표시 */
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-bottom: 1rem;
}

.plan-card {
  display: flex;
  flex-direction: column;
  padding: 1rem;
  border-radius: 12px;
  background-color: #f7f7f7;
  height: auto;
  margin: 0 auto 1rem;

  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  top: 0;
}

.plan-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2) !important;
  top: -4px;
}

.plan-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: left;
  padding: 0;
}

.card-body {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
}

.left-content {
  flex: 1;
}

.plan-hashtags {
  margin: 0;
  padding: 0.5rem 0;
  text-align: left;
}

.hashtag {
  font-size: 0.75rem;
  color: #666;
}

.right-content {
  flex-shrink: 0;
  /* margin-left: 16px; */
}

.plan-image {
  width: 100%;
  height: auto;
}

/* .details-button {
  color: #3f51b5;
  text-decoration: none;
} */
</style>
