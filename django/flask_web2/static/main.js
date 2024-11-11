PetiteVue.createApp({
    isNavbarActivated: false, // 네비게이션 바 클래스 상태
    testMessage: 'Hello Petite Vue!', // 초기값 설정,
    isFetched: false, // 데이터를 가져온 후 색상을 변경하기 위한 상태

    fetchData() {
        console.log("Fetching data from server...");
        fetch('/get_data', { method: 'POST' })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                // 1. 서버 응답 데이터를 testMessage에 할당
                this.testMessage = data.result
                // 2. 콘솔에 결과 표시
                console.log('data:',this.testMessage)
                this.isFetched = true; // 데이터를 가져온 후 isFetched를 true로 변경
                
            })
            .catch(error => console.error('Error fetching data:', error));
    },
    // 스크롤 이벤트 핸들러
    handleScroll() {
        this.isNavbarActivated = window.scrollY > 10;
    },

    // 컴포넌트 초기화 시 스크롤 이벤트 리스너 추가
    mounted() {
        window.addEventListener('scroll', this.handleScroll);
    }
}).mount("#app");
