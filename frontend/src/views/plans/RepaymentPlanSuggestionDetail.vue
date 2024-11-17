<template>
    <v-row class="fill-height">
        <v-col cols="12">
            <v-card class="pa-5" flat v-if="currentPlan">
                <v-card-title class="text-h5 font-weight-bold">
                    {{ currentPlan.planName }}
                </v-card-title>
                <v-card-text>
                    <ul class="text-start">
                        <li>상환 목표: {{ currentPlan.duration }}개월</li>
                        <li>총 월 상환금: {{ currentPlan.monthlyPayment }}만원</li>
                        <li>총 절약액: {{ currentPlan.totalSavingAmount }}원</li>
                    </ul>
                    <div class="doughnutChart">
                        <DoughnutChart v-if="doughnutChartData" :data="doughnutChartData" />
                    </div>
                    <div class="category-details">
                        <div v-for="(amount, index) in categoryAmounts" :key="index" class="category-item">
                            <span :style="{ color: doughnutChartData.datasets[0].backgroundColor[index] }">
                                {{ doughnutChartData.labels[index] }}:
                            </span>
                            <span>{{ amount.toLocaleString() }} 원</span>
                        </div>
                    </div>
                </v-card-text>
            </v-card>
            <v-card v-else class="pa-5" flat>
                <v-card-title class="text-h5 font-weight-bold text-start">
                    플랜을 찾을 수 없습니다
                </v-card-title>
            </v-card>
        </v-col>
    </v-row>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import DoughnutChart from '@/components/DoughnutChart.vue';

const route = useRoute()

// 플랜 데이터 나중에 db에서 받아올 거
const plan = {
    "planId": "001",
    "planName": "금융 중심 절약 플랜",
    "duration": 12,
    "monthlyPayment": 103,
    "totalSavingAmount": 515000,
    "description": "금융 투자를 중심으로 하는 절약 플랜으로, 금융 부문에서 40%의 높은 절약률을 목표로 합니다.",
    "categories": [
        {
            "categoryId": 1,
            "categoryName": "금융",
            "currentSpending": 1000000,
            "savingPercentage": 40.0,
            "suggestedSaving": 400000,
            "modifiedSpending": 600000
        },
        {
            "categoryId": 2,
            "categoryName": "주거 및 통신",
            "currentSpending": 530000,
            "savingPercentage": 10.0,
            "suggestedSaving": 53000,
            "modifiedSpending": 477000
        },
        {
            "categoryId": 3,
            "categoryName": "식비",
            "currentSpending": 270000,
            "savingPercentage": 10.0,
            "suggestedSaving": 27000,
            "modifiedSpending": 243000
        },
        {
            "categoryId": 4,
            "categoryName": "교통",
            "currentSpending": 70000,
            "savingPercentage": 10.0,
            "suggestedSaving": 7000,
            "modifiedSpending": 63000
        }
    ]
}

const currentPlan = ref(null)

// route params가 변경될 때마다 currentPlan 업데이트
const updateCurrentPlan = () => {
    const planId = parseInt(route.params.id);
    currentPlan.value = plan
    // if (planId >= 0 && planId < plans.length) {
    //     currentPlan.value = plan
    // } else {
    //     currentPlan.value = null
    // }
}

const categories = plan.categories;

// 도넛 차트 데이터 생성
const doughnutChartData = ref({
    labels: categories.map(category => category.categoryName),
    datasets: [
        {
            label: '현재 소비액',
            data: categories.map(category => category.currentSpending),
            backgroundColor: [
                '#4bc0c0',  // 금융
                '#36a2eb',  // 주거 및 통신
                '#ff6384',  // 식비
                '#ffcd56'   // 교통
            ],
            hoverOffset: 4,
        },
    ],
});

const categoryAmounts = doughnutChartData.value.datasets[0].data;


// 컴포넌트 마운트 시 초기화
onMounted(() => {
    updateCurrentPlan()
})

// route params 변경 감지
watch(
    () => route.params.id,
    () => {
        updateCurrentPlan()
    }
)
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

.doughnutChart {
    width: 90%;
    margin-top: 20px;
}

.category-details {
    margin-top: 20px;
    text-align: center;
}
</style>