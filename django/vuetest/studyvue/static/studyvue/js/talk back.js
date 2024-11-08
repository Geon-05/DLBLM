document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript 파일이 성공적으로 로드되었습니다!");
});

const app = Vue.createApp({
    data() {
        return {
            inputText: '',     // 입력된 텍스트를 임시 저장
            chatHistory: [],   // 채팅 기록을 저장할 배열
            starRange: Array.from({ length: 20 }, (_, i) => i + 1) // 1부터 20까지의 숫자 배열 생성
        };
    },
    methods: {
        click() {
            if (this.inputText.trim() !== '') {
                this.chatHistory.push({ text: this.inputText, sender: 'user' });
                this.inputText = '';
            }
        }
    }
}).mount("#app");