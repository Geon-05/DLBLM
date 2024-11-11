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
            fetch('/send_subject', { method: 'POST' })
                .then(response => response.json())
                .then((data) => {
                    
                })
        }
    },
    computed: {

    }
})