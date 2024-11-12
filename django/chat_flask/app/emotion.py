import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# 모델과 토크나이저, 파이프라인 설정을 전역으로
num_labels = 3
model = AutoModelForSequenceClassification.from_pretrained("skt/kogpt2-base-v2", num_labels=num_labels)
device = torch.device('cpu')
model.load_state_dict(torch.load("D:\OneDrive\human\port-folio\personal_project\DLBLM\django\chat_flask\data\model\model_checkpoint.pt", map_location=device))
tokenizer = AutoTokenizer.from_pretrained('skt/kogpt2-base-v2')

pipe = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=-1,  # CPU에서 실행
    max_length=512,
    top_k=1,  # 최고 점수의 레이블만 반환
    function_to_apply='softmax'
)

# 레이블을 한국어로 매핑
label_dict = {'LABEL_0': '🤔중립', 'LABEL_1': '😍긍정', 'LABEL_2': '😤부정'}

def emotion_chk(sentence):
    result = pipe(sentence)
    return label_dict[result[0][0]['label']]
