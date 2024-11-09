PetiteVue.createApp({
    testMessage: 'Hello Petite Vue!', // 초기값 설정
    fetchData() {
        console.log("Fetching data from server...");
        fetch('/DOCOMETHING', { method: 'POST' })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                
                DOCOMETHING // 서버 응답 데이터를 testMessage에 할당
                DOCOMETHING // 콘솔에 결과 표시
            })
            .catch(error => console.error('Error fetching data:', error));
    }
}).mount();