PetiteVue.createApp({
    testMessage: 'Hello Petite Vue!', // 초기값 설정
    square_value: 2,
    num1: 0,
    num2: 0,
    add_value: 0,

    fetchData() {
        console.log("Fetching data from server...");
        fetch('/get_data', { method: 'POST' })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                console.log("data:",data)

                this.testMessage = data.result
            })
            .catch(error => console.error('Error fetching data:', error));
    },
    squareData() {
        fetch('/get_square_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ square_value: this.square_value })  // 현재 add_value를 서버로 전송
        })
        .then(response => response.json())
        .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
            console.log("data:",data)

            this.square_value = data.result  // 제곱된 결과로 add_value 업데이트
        })
        .catch(error => console.error('Error fetching data:', error));
    },
    addData() {
        this.add_value = Number(this.num1) + Number(this.num2)
    }
}).mount();