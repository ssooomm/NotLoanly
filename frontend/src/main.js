import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import './style.css';
import { createPinia } from 'pinia';

const app = createApp(App);
const pinia = createPinia();
app
  .use(pinia)
  .use(router)
  .use(vuetify)
  .provide('categoryColors', [
    "#FF9F40", // 금융
    "#FFCE56", // 주거 및 통신
    "#FF6384", // 식비
    "#9966FF", // 교통
    "#36A2EB", // 쇼핑
    "#4BC0C0", // 여가
    "#66BB6A", // 건강
    "#C9CBCF", // 기타
  ])
  .mount('#app');