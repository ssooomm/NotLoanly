<template>
  <div class="spending-analysis">
    <SpendingAnalysis />

    <div class="category-selection">
      <h4>줄이기 어려운 걸 선택해주세요.</h4>
      <p class="info-text">한 가지 이상 선택 가능합니다.</p>
      <div class="category-buttons">
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('식비') }"
          @click="toggleCategory('식비')"
        >
          식비
        </button>
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('카페/간식') }"
          @click="toggleCategory('카페/간식')"
        >
          카페/간식
        </button>
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('쇼핑') }"
          @click="toggleCategory('쇼핑')"
        >
          쇼핑
        </button>
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('교통') }"
          @click="toggleCategory('교통')"
        >
          교통
        </button>
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('자동차') }"
          @click="toggleCategory('자동차')"
        >
          자동차
        </button>
        <button
          class="category-button"
          :class="{ selected: selectedCategories.includes('주거/통신') }"
          @click="toggleCategory('주거/통신')"
        >
          주거/통신
        </button>
      </div>
    </div>

    <div class="period-selection">
      <h4>상환 기간을 선택해주세요.</h4>
      <div class="period-buttons">
        <button
          class="period-button"
          :class="{ selected: selectedPeriod === '3개월' }"
          @click="selectPeriod('3개월')"
        >
          3개월
        </button>
        <button
          class="period-button"
          :class="{ selected: selectedPeriod === '6개월' }"
          @click="selectPeriod('6개월')"
        >
          6개월
        </button>
        <button
          class="period-button"
          :class="{ selected: selectedPeriod === '12개월' }"
          @click="selectPeriod('12개월')"
        >
          12개월
        </button>
        <button
          class="period-button"
          :class="{ selected: selectedPeriod === '직접 입력' }"
          @click="selectPeriod('직접 입력')"
        >
          직접 입력
        </button>
      </div>

      <div v-if="selectedPeriod === '직접 입력'" class="input-container">
        <input
          type="text"
          v-model="customPeriod"
          placeholder="기간을 입력하세요 (예: 5개월)"
          class="custom-input"
        />
      </div>
    </div>

    <div class="footer">
      <button class="footer-button" @click="navigateToRepaymentPlanSuggestion">
        상환 플랜 제안받기
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import SpendingAnalysis from "../components/SpendingAnalysis.vue";
import { useRouter } from "vue-router";
import { useApiStore } from "../stores/apiStore"; // Import the store

const router = useRouter();
const apiStore = useApiStore(); // Initialize the store

const selectedPeriod = ref(null);
const customPeriod = ref("");

const selectPeriod = (period) => {
  selectedPeriod.value = period;
  if (period !== "직접 입력") {
    customPeriod.value = "";
  }
};

const doughnutChartData = ref({
  labels: ["쇼핑/의류비", "식비", "여가/취미비"],
  datasets: [
    {
      label: "소비 비율",
      data: [638465, 241881, 170940],
      backgroundColor: ["#ffcc00", "#36a2eb", "#4bc0c0"],
      hoverOffset: 4,
    },
  ],
});

const selectedCategories = ref([]);

const toggleCategory = (category) => {
  if (selectedCategories.value.includes(category)) {
    selectedCategories.value = selectedCategories.value.filter(
      (c) => c !== category
    ); // Deselect
  } else {
    selectedCategories.value.push(category);
  }
};

const navigateToRepaymentPlanSuggestion = async () => {
  const period = selectedPeriod.value === "직접 입력" ? customPeriod.value : selectedPeriod.value;
  const categories = selectedCategories.value.map(category => ({
    category,
    isHardToReduce: true
  }));

  try {
    await apiStore.saveRepaymentPlan("1", categories, period); // Replace "3" with actual user ID if needed
    router.push("/repayment-plan-suggestion");
  } catch (error) {
    console.error("Error saving repayment plan:", error);
  }
};
</script>

<style scoped>
.spending-analysis {
  text-align: center;
}

.doughnutChart {
  width: 80%;
  margin-left: 40px;
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
  margin-right: 30px;
  color: #080600;
}

h2 {
  margin-bottom: 10px;
  font-size: 24px;
}

h3 {
  margin: 20px 0;
  font-size: 18px;
}

.category-details {
  margin-top: 20px;
}

.category-item {
  font-size: 16px;
  margin: 5px 0;
}

.category-selection,
.period-selection {
  margin-top: 30px;
}

.category-buttons,
.period-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 10px;
}

.period-buttons {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
}

.period-button {
  background-color: #f0f0f0;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.period-button.selected {
  background-color: #ffcc00;
}

.input-container {
  margin-top: 10px;
}

.custom-input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
}

.category-button,
.period-button {
  background-color: #f0f0f0;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  margin: 5px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.category-button:hover,
.period-button:hover {
  background-color: #e0e0e0;
}

.category-button.selected,
.period-button.selected {
  background-color: #ffcc00;
}

.info-text {
  color: #888;
  font-size: 12px;
  margin-top: 5px;
}

.footer {
  margin-top: 40px;
}

.footer-button {
  background-color: #ffcc00;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  width: 100%;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.footer-button:hover {
  background-color: #e0a800;
}
</style>
