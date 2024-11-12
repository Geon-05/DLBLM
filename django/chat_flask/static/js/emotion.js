document.addEventListener('DOMContentLoaded', function() {
    console.log("JavaScript 파일이 성공적으로 로드되었습니다!");
});

const app = PetiteVue.createApp({
    sentence: '',
    emotion_result: '',

    emotion_chk() {
        fetch('/post_sentence', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sentence: this.sentence })
        })
        .then(response => response.json())
        .then((data) => {
            this.emotion_result = data.emotion_result; // 수정된 부분
        })
        .catch(error => console.error('Error fetching data:', error));
    }
}).mount("#app")