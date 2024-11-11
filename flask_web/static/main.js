PetiteVue.createApp({
    testMessage: 'Hello Petite Vue!', // 초기값 설정

    fetchData() {
        console.log("Fetching data from server...");
        fetch('/get_data', { method: 'POST' })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                console.log("data:",data)

                this.testMessage = data.result
            })
            .catch(error => console.error('Error fetching data:', error));
    }
}).mount();