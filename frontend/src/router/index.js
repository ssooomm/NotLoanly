import { createRouter, createWebHistory } from 'vue-router';
import MainView from '../views/MainView.vue';
import LoanInfoNotice from '../views/loanInfo/LoanInfoNotice.vue';
import LoanInput from '../views/LoanInput.vue';
import LoanComplete from '../views/LoanComplete.vue';
import RepaymentPlanSuggestion from '../views/plans/RepaymentPlanSuggestion.vue';
import RepaymentPlanSuggestionDetail from '../views/plans/RepaymentPlanSuggestionDetail.vue';
import ExpenseAnalysis from '../views/ExpenseAnalysis.vue';
import Notifications from '../views/Notifications.vue';

const routes = [
  {
    path: '/',
    name: 'LoanInfoNotice',
    component: LoanInfoNotice,
  },
  {
    path: '/dashboard',
    name: 'Main',
    component: MainView,
  },
  {
    path: '/loan-input',
    name: 'LoanInput',
    component: LoanInput,
  },
  {
    path: '/loan-complete',
    name: 'LoanComplete',
    component: LoanComplete,
    beforeEnter: (to, from, next) => {
      if (from.name === 'LoanInput') {
        next();
      } else {
        next('/loan-input');
      }
    },
  },
  {
    path: '/expense-analysis',
    name: 'ExpenseAnalysis',
    component: ExpenseAnalysis,
  },
  {
    path: '/repayment-plan-suggestion',
    name: 'RepaymentPlanSuggestion',
    component: RepaymentPlanSuggestion,
    beforeEnter: (to, from, next) => {
      if (from.name === 'ExpenseAnalysis' || from.name === 'RepaymentPlanSuggestionDetail' || from.name === 'Main') {
        next();
      } else {
        next('/expense-analysis');
      }
    },
  },
  {
    path: '/repayment-plan-suggestion/:id',
    name: 'RepaymentPlanSuggestionDetail',
    component: RepaymentPlanSuggestionDetail,
    beforeEnter: (to, from, next) => {
      if (from.name === 'RepaymentPlanSuggestion') {
        next();
      } else {
        next('/repayment-plan-suggestion');
      }
    },
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: Notifications,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;