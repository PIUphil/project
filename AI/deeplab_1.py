import urllib.request

url = "https://github.com/planxlabs/toheaven/blob/main/dog.jpg?raw=true"
filename = "dog.jpg"

urllib.request.urlretrieve(url, filename)

# 사진 다운로드