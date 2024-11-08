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
        async click() {
            if (this.inputText.trim() !== '') {
                // 사용자의 메시지를 추가
                this.chatHistory.push({ text: this.inputText, sender: 'user' });

                // Django API에 메시지 전송
                try {
                    const response = await axios.post('/send_message/', { message: this.inputText });
                    const botResponse = response.data.response;
                    
                    // 챗봇의 응답을 추가
                    this.chatHistory.push({ text: botResponse, sender: 'bot' });
                } catch (error) {
                    console.error("메시지 전송 오류:", error);
                }
                console.log(this.inputText, botResponse)
                // 입력 필드 초기화
                this.inputText = '';
            }
        }
    }
}).mount("#app");