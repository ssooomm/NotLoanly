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
  .mount('#app');