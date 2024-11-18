// frontend/src/stores/apiStore.js

import { defineStore } from 'pinia';

export const useApiStore = defineStore('api', {
    state: () => ({
        categories: [],
        repaymentPlans: [],
        repaymentStatus: {},
        consumptionAnalysis: {},
        notifications: [],
        message: '',
        totalAmount: 5000000, // 총 대출 금액
        paidAmount: 0, // 상환한 총 금액
        remainingAmount: 0, // 남은 상환 금액
        completedPercentage: 0, // 상환 비율
        repaymentChart: [],
    }),
    actions: {
        // 대출 신청
        async applyForLoan(userId, loanAmount, interestRate) {
            const response = await fetch('/api/loan/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, loan_amount: loanAmount, interest_rate: interestRate }),
            });
            const data = await response.json();
            this.message = data.message; // "상환 계획이 저장되었습니다."
            return data; // 응답 반환
        },

        // 상환 플랜 제안
        async suggestRepaymentPlan() {
            const response = await fetch('/api/loan/apply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            });
            return await response.json();
        },

        // 카테고리 조회
        async fetchCategories() {
            const response = await fetch('/api/categories');
            const data = await response.json();
            if (data.status === 'success') {
                this.categories = data.categories; // 카테고리 목록 저장
            }
            return data; // 응답 반환
        },

        // 소비 분석 데이터 조회
        async fetchConsumptionAnalysis(userId) {
            const response = await fetch(`/api/repayment/analysis?userId=${userId}`);
            const data = await response.json();
            this.consumptionAnalysis = data; // 소비 분석 데이터 저장
            return data; // 응답 반환
        },

        // 줄이기 어려운 카테고리와 상환 기간 저장
        async saveRepaymentPlan(userId, categories, repaymentPeriod) {
            const response = await fetch('/api/repayment/save-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, categories, repaymentPeriod }),
            });
            const data = await response.json();
            this.message = data.message; // "상환 계획이 저장되었습니다."
            return data; // 응답 반환
        },

        // 상환 플랜 리스트 조회
        async fetchRepaymentPlans(userId) {
            const response = await fetch(`/api/repayment/plans?userId=${userId}`);
            const data = await response.json();
            if (data.status === 'success') {
                this.repaymentPlans = data.plans; // 상환 플랜 목록 저장
            }
            return data; // 응답 반환
        },

        // 상환 플랜 선택
        async selectRepaymentPlan(userId, planId) {
            const response = await fetch('/api/repayment/select-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ userId, planId }),
            });
            const data = await response.json();
            this.message = data.message; // "선택한 상환 플랜이 시작되었습니다."
            return data; // 응답 반환
        },

        // 상환 요약 조회
        async fetchRepaymentStatus() {
            const response = await fetch('/api/dashboard/summary');
            const data = await response.json();
            this.repaymentStatus = data.summary; // 상환 현황 저장
            this.repaymentChart = data.repaymentChart; // 월별 상환 데이터 저장
            this.paidAmount = this.repaymentStatus.paidAmount; // 상환한 금액
            this.remainingAmount = this.repaymentStatus.remainingAmount; // 남은 금액
            this.completedPercentage = (this.paidAmount / this.totalAmount) * 100; // 상환 비율 계산
            return data; // 응답 반환
        },

        // 소비 분석 조회
        async fetchConsumptionAnalysis() {
            const response = await fetch('/api/dashboard/consumption-analysis');
            const data = await response.json();
            this.consumptionAnalysis = data; // 소비 분석 데이터 저장
            return data; // 응답 반환
        },

        // 사용자 알림 조회
        async fetchNotifications(userId) {
            const response = await fetch(`/api/notifications/${userId}`);
            const notifications = await response.json();
            this.notifications = notifications; // 알림 목록 저장
            return notifications; // 응답 반환
        },

        // 새 알림 생성
        async createNotification(userId, message) {
            const response = await fetch('/api/notifications', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, message }),
            });
            const data = await response.json();
            this.message = data.message; // "Notification created"
            return data; // 응답 반환
        }
    }
});