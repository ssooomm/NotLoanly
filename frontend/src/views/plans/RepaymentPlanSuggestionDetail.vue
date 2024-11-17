<template>
    <v-row>
        <v-col cols="12">
            <v-card class="pa-5" variant="text" v-if="currentPlan">
                <v-card-title class="text-h5 font-weight-bold text-start">
                    {{ currentPlan.title }}
                </v-card-title>
                <v-card-text>
                    <ul>
                        <li>상환 목표: {{ currentPlan.repaymentPeriod }}</li>
                        <li>총 월 상환금: {{ currentPlan.monthlyPayment }}</li>
                    </ul>
                </v-card-text>
            </v-card>
            <v-card v-else class="pa-5" variant="text">
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

const route = useRoute()

// 플랜 데이터 배열
const plans = [
    {
        title: '쇼핑 절약 플랜',
        repaymentPeriod: '3개월 동안 상환 완료',
        monthlyPayment: '약 103만 원 (원금 + 이자 포함)',
    },
    {
        title: '식비 절약 플랜',
        repaymentPeriod: '3개월 동안 상환 완료',
        monthlyPayment: '약 103만 원 (원금 + 이자 포함)',
    },

    {
        title: '문화생활 절약 플랜',
        repaymentPeriod: '12개월 동안 상환 완료',
        monthlyPayment: '약 30만 원 (원금 + 이자 포함)',
    },
    {
        title: '술/유흥 절약 플랜',
        repaymentPeriod: '6개월 동안 상환 완료',
        monthlyPayment: '약 55만 원 (원금 + 이자 포함)',
    },
    {
        title: '교통비 절약 플랜',
        repaymentPeriod: '6개월 동안 상환 완료',
        monthlyPayment: '약 55만 원 (원금 + 이자 포함)',
    },
    // 필요한 만큼 플랜 추가
]

const currentPlan = ref(null)

// route params가 변경될 때마다 currentPlan 업데이트
const updateCurrentPlan = () => {
    const planId = parseInt(route.params.id)
    if (planId >= 0 && planId < plans.length) {
        currentPlan.value = plans[planId]
    } else {
        currentPlan.value = null
    }
}

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
    height: 100vh;
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
</style>