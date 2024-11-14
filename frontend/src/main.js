import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import '../node_modules/vue-cal/dist/vuecal.css';
import './style.css';

const app = createApp(App);

app.use(router)
  .use(vuetify)
  .mount('#app');