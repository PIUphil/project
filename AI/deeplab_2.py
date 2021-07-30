import torch

# 모델 다운로드
model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
# vision - 영상알고리즘만 모아놓은것  # resnet101 사진 모아놓은것  # pretrained 이미 학습되어있는것

model.eval()        # 평가          # 여기까지 먼저 실행 ---------------------
# 모델 파일이 로드됨


from PIL import Image    # PIL 이미지 처리 라이브러리
from torchvision import transforms

input = Image.open("dog.jpg")

preprocess = transforms.Compose([
    transforms.ToTensor(), transforms.Normalize(mean=[
        0.485,0.456,0.406], std=[0.299, 0.224, 0.225]),])   # 하이퍼파라미터값 (가장 좋은 결과나온 것)

input_tensor = preprocess(input)
input_batch = input_tensor.unsqueeze(0)     # 미니배치 - 데이터를 부분부분 잘라서 처리

input_batch = input_batch.to('cuda')
model.to('cuda')

while torch.no_grad():
    output = model(input_batch)['out'][0]
output_predictions = output.argmax(0)





