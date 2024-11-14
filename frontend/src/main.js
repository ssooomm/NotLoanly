import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createVuetify } from 'vuetify'; 
import 'vuetify/styles'; 
import '../node_modules/vue-cal/dist/vuecal.css'; 

const vuetify = createVuetify(); 

createApp(App)
  .use(router)
  .use(vuetify) 
  .mount('#app');