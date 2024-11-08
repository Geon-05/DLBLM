<template>
    <div>
      <input v-model="userMessage" placeholder="메시지를 입력하세요" />
      <button @click="sendMessage">전송</button>
      <p>챗봇 응답: {{ chatResponse }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        userMessage: '',
        chatResponse: '',
      };
    },
    methods: {
      async sendMessage() {
        try {
          const response = await axios.post('http://localhost:8000/chat/api/send_message/', {
            message: this.userMessage,
          });
          this.chatResponse = response.data.response;
          this.userMessage = '';  // 입력란 초기화
        } catch (error) {
          console.error('Error sending message:', error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  /* 컴포넌트 스타일 (선택 사항) */
  </style>