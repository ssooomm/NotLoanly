// frontend/src/stores/apiStore.js

import { defineStore } from 'pinia';

export const useApiStore = defineStore('api', {
  state: () => ({
    categories: {
      1: "소득",
      2: "대출 상환",
      3: "금융",
      4: "주거 및 통신",
      5: "식비",
      6: "교통",
      7: "쇼핑",
      8: "여가",
      9: "건강",
      10: "기타",
    },
    repaymentPlans: [],
    repaymentStatus: {},
    repaymentHistories: [],
    consumptionAnalysis: {},
    notifications: [],
    showAlert: false, // 알림 표시 여부
    alertMessage: '', // 알림 메시지
    message: '',
    totalAmount: 0, // 총 대출 금액
    paidAmount: 0, // 상환한 총 금액
    remainingAmount: 0, // 남은 상환 금액
    completedPercentage: 0, // 상환 비율
    summary: [], // 월별 소비 요약 데이터 추가
    totalPeriod: 0, // 총 상환 기간
    paidPeriod: 0, // 상환한 기간 
    targetAmount: 0, //상환 원금
    interestAmount: 0, //상환 이자 
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
    async fetchConsumptionAnalysis(userId, month) {
      // 기본 URL 설정
      let url = `/api/dashboard/consumption-analysis?user_id=${userId}`;

      // month가 존재할 경우 URL에 추가
      if (month) {
        url += `&month=${month}`;
      }

      const response = await fetch(url); // 수정된 URL 사용
      const data = await response.json();
      this.consumptionAnalysis = data; // 소비 분석 데이터 저장
      return data; // 응답 반환
    },

    // 줄이기 어려운 카테고리와 상환 기간 저장
    async saveRepaymentPlan(userId, categories, repaymentPeriod) {
      const response = await fetch('/api/repayment/save-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          categories,
          repayment_period: repaymentPeriod
        }),
      });
      const data = await response.json();
      this.message = data.message;
      return data; // 응답 반환
    },

    async fetchRepaymentStatus(userId) {
      try {
        const response = await fetch(`/api/dashboard/repayment-status?user_id=${userId}`); // 사용자 ID 포함
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.totalPeriod = data.repayment_period
        this.paidPeriod = data.total_count
        this.totalAmount = data.loan_amount
        this.paidAmount = data.total_paid; // 상환한 금액
        this.targetAmount = data.repayment_amount
        this.interestAmount = data.interest_amount
        this.completedPercentage = data.total_paid_percenatage // 상환 비율 계산
        return data; // 응답 반환
      } catch (error) {
        console.error('Error fetching repayment status:', error);
        throw error; // 에러를 호출한 곳으로 전달
      }
    },

    // 상환 플랜 리스트 조회
    async fetchRepaymentPlans(userId) {
      const response = await fetch(`/api/repayment/plans?user_id=${userId}`);
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
    async fetchRepaymentSummary(userId) {
      try {
        const response = await fetch(`/api/dashboard/summary?user_id=${userId}`);
        const data = await response.json();

        // summary 데이터 저장
        this.summary = data.summary;

        // 현재 월의 데이터 찾기
        const today = new Date();
        const currentMonth = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`;
        const currentMonthData = data.summary.find(month => month.month === currentMonth);

        if (currentMonthData) {
          // 현재 월의 총 지출과 소득 저장
          this.totalSpent = currentMonthData.totalSpent;
          const incomeCategory = currentMonthData.categories.find(cat => cat.category === "소득");
          this.income = incomeCategory ? incomeCategory.totalAmount : 0;
        }

        return data;

      } catch (error) {
        console.error('Error fetching summary data:', error);
        throw error;
      }
    },


    async fetchNotifications(userId) {
      const response = await fetch(`/api/notifications/${userId}`);
      const notifications = await response.json();
      this.notifications = notifications;
      return notifications;
    },


    async createNotification(userId, message) {
      const response = await fetch('/api/notifications', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, message }),
      });
      const data = await response.json();
      this.message = data.message; // "Notification created"
      return data; // 응답 반환
    },


    calculateStatus(spent, budget) {
      const ratio = spent / budget;
      if (ratio < 0.6) return 'safe';
      if (ratio < 0.8) return 'warning';
      return 'danger';
    },

    // 사용자 알림 조회
    async fetchNotifications(userId) {
      try {
        const response = await fetch(`/api/notification/notifications/${userId}`, {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        });

        if (!response.ok) {
          throw new Error(`Error fetching notifications: ${response.status}`);
        }

        const data = await response.json();
        if (data.status === 'success') {
          this.notifications = data.notifications; // 알림 목록 저장
        }
        return data;
      } catch (error) {
        console.error('Error fetching notifications:', error);
        throw error; // 에러를 호출한 곳으로 전달
      }
    },

    // SSE 연결 설정
    connectSSE(userId) {
      const streamUrl = `http://127.0.0.1:8000/api/notification/stream/${userId}`;
      const eventSource = new EventSource(streamUrl);

      // SSE 연결 성공
      eventSource.onopen = () => {
        console.log("SSE connection opened.");
      };

      // SSE 데이터 수신
      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data); // JSON 파싱
          console.log("New Event:", data);

          // 알림 메시지 처리
          if (data.message) {
            this.alertMessage = data.message; // 메시지 저장
            this.showAlert = true; // 알림 표시

            // 5초 후 알림 숨김
            setTimeout(() => {
              this.showAlert = false;
            }, 150000);

            // 알림 목록에 추가
            this.notifications.unshift({
              message: data.message,
              date: new Date().toISOString(), // 현재 시간 저장
            });
          }
        } catch (e) {
          console.error("Error parsing event data:", e);
        }
      };

      // SSE 오류 처리
      eventSource.onerror = (error) => {
        console.error("Error occurred in SSE stream:", error);
        eventSource.close(); // 연결 닫기
      };
    },

    // 사용자 소비 데이터 조회
    async fetchUserExpenses(userId, month = 9) {
      const response = await fetch(`/api/dashboard/user-expenses?user_id=${userId}&month=${month}`);

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();

      if (data.status === 'success') {
        return data.data; // 소비 데이터 반환
      } else {
        throw new Error('Failed to fetch user expenses');
      }
    },

  }
});