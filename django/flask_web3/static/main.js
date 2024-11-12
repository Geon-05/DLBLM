PetiteVue.createApp({
    isNavbarActivated: false, // 네비게이션 바 클래스 상태
    // testMessage: 'Hello Petite Vue!', // 초기값 설정,
    isFetched: false, // 데이터를 가져온 후 색상을 변경하기 위한 상태

    user_input: '',
    prediction: '',
    result: '',
    label: '',

    fetchData() {
        console.log("Fetching data from server...");
        fetch('/get_data', { method: 'POST' })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                this.result = data.result
                // console.log("data:", this.testMessage)
                // 1. 서버 응답 데이터를 testMessage에 할당
                // 2. 콘솔에 결과 표시
                this.isFetched = true; // 데이터를 가져온 후 isFetched를 true로 변경
                
            })
            .catch(error => console.error('Error fetching data:', error));
    },

    predict_sentiment(){
        fetch('/predict_sentiment', { method: 'POST',
                                        headers: { 'Content-Type': 'application/json' },
                                        body: JSON.stringify({ "key" : this.user_input })

         })
            .then(response => response.json())
            .then((data) => {  // 화살표 함수를 사용해 this 스코프 유지
                this.result = data.result[0]
                this.label = data.label

                console.log("data.result:", data.result)
                console.log("data.label:", data.label)  

                // this.testMessage = data.result              
                this.isFetched = true; // 데이터를 가져온 후 isFetched를 true로 변경                
            })
            .catch(error => console.error('Error fetching data:', error));
    },

    // 이미지 미리보기 함수
    previewImage(event, viewAreaId) {
        const preview = document.getElementById(viewAreaId);
        const file = event.target.files[0];
        
        if (file && file.type.startsWith("image/")) {
            // 기존의 미리보기 이미지 제거
            const existingImage = document.getElementById("prev_" + viewAreaId);
            if (existingImage) {
                preview.removeChild(existingImage);
            }
            // 새로운 이미지 생성 및 추가
            const img = document.createElement("img");
            img.id = "prev_" + viewAreaId;
            img.classList.add("obj");
            img.style.width = '700px';
            img.style.height = '400px';
            preview.appendChild(img);
            
            // 파일을 읽어 이미지로 표시
            const reader = new FileReader();
            reader.onload = (e) => {
                img.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            alert("이미지 파일만 업로드할 수 있습니다.");
        }
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
