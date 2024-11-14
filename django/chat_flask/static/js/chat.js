document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript 파일이 성공적으로 로드되었습니다!");
});

const app = Vue.createApp({
    data() {
        return {
            inputQuestion: '',
            inputSubject: '',
            chatHistory: [],
            starRange: Array.from({ length: 15 }, (_, i) => i + 1),
            subjectResponse: '',
        };
    },
    methods: {
        async subject_chk() {
            if (this.inputSubject.trim() !== '') {
                try {
                    // Flask API에 GET 요청 보내기
                    const response = await fetch(`/get_subject?gameTitle=${encodeURIComponent(this.inputSubject)}`, {
                        method: 'GET'
                    });
        
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
        
                    const data = await response.json();
                    this.subjectResponse = data.gametitle;
                } catch (error) {
                    console.error("메시지 전송 오류:", error);
                    this.subjectResponse = "서버에 연결할 수 없습니다.";
                }
            }
        },
        async question_chk() {
            if (this.inputQuestion.trim() !== '' && this.inputSubject.trim() !== '') {
                // 사용자의 메시지를 추가
                this.chatHistory.push({ text: this.inputQuestion, sender: 'user' });
    
                // Django API에 메시지 전송
                try {
                    const response = await fetch('http://127.0.0.1:8000/studyvue/send_message/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            message: this.inputQuestion,
                            subject: this.inputSubject
                        })
                    });
    
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
    
                    const data = await response.json();
                    const botResponse = data.response;
                    
                    // 챗봇의 응답을 추가
                    this.chatHistory.push({ text: botResponse, sender: 'bot' });
                } catch (error) {
                    console.error("메시지 전송 오류:", error);
                    this.chatHistory.push({ text: `서버에 연결할 수 없습니다. 오류: ${error.message}`, sender: 'bot' });
                }
    
                // 입력 필드 초기화
                this.inputQuestion = '';
            } else {
                console.error("게임 타이틀과 질문을 모두 입력해야 합니다.");
                this.chatHistory.push({ text: '게임 타이틀과 질문을 모두 입력해주세요.', sender: 'bot' });
            }
        },
        scrollToBottom() {
            const chatScreen = document.getElementById('chat-screen');
            chatScreen.scrollTo({
                top: chatScreen.scrollHeight,
                behavior: 'smooth'
            });
        }
    }
    ,
    computed: {
        formattedSubject() {
            return `Game Title : ${this.subjectResponse || "🔍"}`;
        }
    }
}).mount("#app");