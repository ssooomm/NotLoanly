import { createRouter, createWebHistory } from 'vue-router';
import MainView from '../views/MainView.vue';
import LoanInfoNotice from '../views/loanInfo/LoanInfoNotice.vue';
// import LoanInfoCollection from '../views/LoanInfoCollection.vue';
// import LoanInput from '../views/LoanInput.vue';
// import LoanComplete from '../views/LoanComplete.vue';
// import ExpenseAnalysis from '../views/ExpenseAnalysis.vue';
import RepaymentPlanSuggestion from '../views/plans/RepaymentPlanSuggestion.vue';
// import RepaymentPlanSuggestionDetail from '../views/RepaymentPlanSuggestionDetail.vue';
// import RepaymentDashboardSummary from '../views/RepaymentDashboardSummary.vue';
// import RepaymentDashboardExpenseRatioChange from '../views/RepaymentDashboardExpenseRatioChange.vue';
// import RepaymentStatus from '../views/RepaymentStatus.vue';
// import RepaymentDashboardExpenseAnalysis from '../views/RepaymentDashboardExpenseAnalysis.vue';
import Notifications from '../views/Notifications.vue';

const routes = [
  {
    path: '/',
    name: 'Main',
    component: MainView,
  },
  {
    path: '/loan-info-notice',
    name: 'LoanInfoNotice',
    component: LoanInfoNotice,
  },
  // {
  //   path: '/loan-info-collection',
  //   name: 'LoanInfoCollection',
  //   component: LoanInfoCollection,
  // },
  // {
  //   path: '/loan-input',
  //   name: 'LoanInput',
  //   component: LoanInput,
  // },
  // {
  //   path: '/loan-complete',
  //   name: 'LoanComplete',
  //   component: LoanComplete,
  // },
  // {
  //   path: '/expense-analysis',
  //   name: 'ExpenseAnalysis',
  //   component: ExpenseAnalysis,
  // },
  {
    path: '/repayment-plan-suggestion',
    name: 'RepaymentPlanSuggestion',
    component: RepaymentPlanSuggestion,
  },
  // {
  //   path: '/repayment-plan-suggestion/detail',
  //   name: 'RepaymentPlanSuggestionDetail',
  //   component: RepaymentPlanSuggestionDetail,
  // },
  // {
  //   path: '/repayment-dashboard-summary',
  //   name: 'RepaymentDashboardSummary',
  //   component: RepaymentDashboardSummary,
  // },
  // {
  //   path: '/repayment-dashboard-expense-ratio-change',
  //   name: 'RepaymentDashboardExpenseRatioChange',
  //   component: RepaymentDashboardExpenseRatioChange,
  // },
  // {
  //   path: '/repayment-status',
  //   name: 'RepaymentStatus',
  //   component: RepaymentStatus,
  // },
  // {
  //   path: '/repayment-dashboard-expense-analysis',
  //   name: 'RepaymentDashboardExpenseAnalysis',
  //   component: RepaymentDashboardExpenseAnalysis,
  // },
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
