document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript 파일이 성공적으로 로드되었습니다!");
});

const app = Vue.createApp({
    data() {
        return {
            inputQuestion: '',     // 입력된 텍스트를 임시 저장
            inputSubject: '',     // 입력된 텍스트를 임시 저장
            chatHistory: [],   // 채팅 기록을 저장할 배열
            starRange: Array.from({ length: 15 }, (_, i) => i + 1), // 1부터 15까지의 숫자 배열 생성
            subjectResponse: ''    // 서버 응답을 저장할 변수
        };
    },
    methods: {
        async question_chk() {
            if (this.inputQuestion.trim() !== '') {
                // 사용자의 메시지를 추가
                this.chatHistory.push({ text: this.inputQuestion, sender: 'user' });

                // Django API에 메시지 전송
                try {
                    const response = await axios.post('http://127.0.0.1:8000/studyvue/send_message', { message: this.inputQuestion });
                    const botResponse = response.data.response;
                    
                    // 챗봇의 응답을 추가
                    this.chatHistory.push({ text: botResponse, sender: 'bot' });
                } catch (error) {
                    console.error("메시지 전송 오류:", error);
                    this.chatHistory.push({ text: `서버에 연결할 수 없습니다. 오류: ${error.message}`, sender: 'bot' });
                }
                // 입력 필드 초기화
                this.inputQuestion = '';
            }
        },
        async subject_chk() {
            if (this.inputSubject.trim() !== '') {
                try {
                    // Django API에 GET 요청 보내기 (전체 URL 사용)
                    const response = await axios.get('http://127.0.0.1:8000/studyvue/send_subject/', {
                        params: { subject: this.inputSubject }
                    });
                    this.subjectResponse = response.data.response;
                } catch (error) {
                    console.error("메시지 전송 오류:", error);
                    this.subjectResponse = "서버에 연결할 수 없습니다.";
                }
            }
        }
    },
    computed: {
        formattedSubject() {
            return `Game Title : ${this.subjectResponse || "🔍"}`;
        }
    }
}).mount("#app");