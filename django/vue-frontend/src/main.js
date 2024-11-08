import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

const app = createApp(App)

// Axios를 전역 설정으로 추가하기
app.config.globalProperties.$axios = axios

// Vue 애플리케이션을 #app에 마운트
app.mount('#app')