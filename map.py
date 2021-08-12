import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt



exhibit_n = 0  # 작품번호
#exhibit = ['금제관식','귀걸이','금동대향로','칠지도','','','']
exhibit = ['crown','earring','thurible','knife','','','','']


# 0:장애물, 1:통로, 2:시작점, 3:경유지, 4:작품, 5:충전, 8:화장실, 9:도착점
# area = np.array([[9,5,1,3,8],
#                  [0,0,0,1,0],
#                  [4,1,1,3,1],
#                  [0,0,0,1,0],
#                  [4,1,1,3,1],
#                  [1,1,1,2,1]])

# area = np.array([[2,1,1,1,1,1],
#                 [0,0,0,0,0,1],
#                 [1,1,1,1,0,1],
#                 [1,0,5,4,0,1],
#                 [1,0,0,0,0,1],
#                 [1,1,1,1,1,1]])

#area = np.ones((64,129))

# 지도배열
area = np.ones((16,32))

# End
end = (1,1)
for i in range(3):
    for j in range(3):
        area[i][j] = 9
# W.C
wc = (15,1)
for i in range(1,3):
    for j in range(2):
        area[-i][j] = 8
        
# X        
for i in range(9):
    for j in range(2):
        for k in range(5):
            area[0+i][4+j+(5*k)] = 0
            
for i in range(4):
    for j in range(2):
        for k in range(5):
            area[12+i][4+j+(5*k)] = 0

for i in range(12):
    for j in range(1,3):
        area[i][-j] = 0
            
# exhibit
ex = {}
for i in range(4):
    ex[exhibit[i]] = (0,7+5*i)
    area[0][7+5*i] = 4
            
# way_point
way = {}
for i in range(6):
    way[i] = (10,2+5*i)
    area[10][2+5*i] = 3
    
# charge
area[2][2] = 5

#Now
now = (10,28)
area[now[0]][now[1]]=2

#print(area)



# 지도 (색채우기)
height = area.shape[0]   # 6
width = area.shape[1]  # 5


# mpl.rc('font', family='NanumGothic')
#mpl.rc('font', family='Malgun Gothic')
#plt.rc('font', family='NanumGothic')
#plt.rcParams["font.family"] = 'NanumGothic'


for i in range(height):
    for j in range(width):        
        if area[i][j] == 0:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='#505050')           # 장애물
        elif area[i][j] == 1:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='#E6E6E6')          # 통로
        elif area[i][j] == 2:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='gold')             # 시작점
            plt.text(i+0.25, height-j-1+0.4, 'Start', fontdict={'family':'serif', 'weight':'bold'})
        elif area[i][j] == 3:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='skyblue')         # 경유지
        elif area[i][j] == 4:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='lightgreen')       # 작품
            plt.text(i+0.2, height-j-1+0.4, exhibit[exhibit_n], fontdict={'family':'serif', 'color':'green', 'weight':'bold'})
            exhibit_n += 1
        elif area[i][j] == 5:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='pink')            # 충전
            plt.text(i+0.17, height-j-1+0.43, 'charge', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
            #plt.text(2+0.17, 2-1+0.43, 'charge', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
        elif area[i][j] == 8:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='orange')             # 화장실
            #plt.text(j+0.3, height-i-1+0.43, 'W.C', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
            
        elif area[i][j] == 9:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='red')              # 도착점
            #plt.text(j+0.33, height-i-1+0.4, 'End', fontdict={'family':'serif', 'color':'white', 'weight':'bold'})
            
        else:
            plt.fill([i, i, i+1, i+1], [height-j, height-j+1, height-j+1, height-j], color='blue')             # 기타

plt.text(0.33, height-1+0.4, 'End', fontdict={'family':'serif', 'color':'white', 'weight':'bold'})
plt.text((width/2)-2+0.3, height-1+0.43, 'W.C', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
            
# for i in range(height):
#     for j in range(width):        
#         if area[i][j] == 0:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='#505050')          # 장애물
#         elif area[i][j] == 1:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='#E6E6E6')          # 통로
#         elif area[i][j] == 2:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='gold')             # 시작점
#             #plt.text(j+0.25, height-i-1+0.4, 'Start', fontdict={'family':'serif', 'weight':'bold'})
#         elif area[i][j] == 3:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='skyblue')          # 경유지
#         elif area[i][j] == 4:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='lightgreen')       # 작품
#             #plt.text(j+0.2, height-i-1+0.4, exhibit[exhibit_n], fontdict={'family':'serif', 'color':'green', 'weight':'bold'})
#             #exhibit_n += 1
#         elif area[i][j] == 5:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='pink')             # 충전
#             #plt.text(j+0.17, height-i-1+0.43, 'charge', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
#         elif area[i][j] == 8:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='orange')             # 화장실
#             #plt.text(j+0.3, height-i-1+0.43, 'W.C', fontdict={'family':'serif', 'color':'red', 'weight':'bold'})
#         elif area[i][j] == 9:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='red')              # 도착점
#             #plt.text(j+0.33, height-i-1+0.4, 'End', fontdict={'family':'serif', 'color':'white', 'weight':'bold'})
#         else:
#             plt.fill([j, j, j+1, j+1], [height-i-1, height-i, height-i, height-i-1], color='blue')             # 기타



# 노선 그리기
  # 1.now와 가까운 way_now 연결
  # 2 작품과 가까운 way_ex 연결
  # 3 way_now와 way_ex연결

now = (14,30)
destination = wc#ex['crown']        # wc, end

plt.fill([now[0], now[0], now[0]+1, now[0]+1], [height-now[1], height-now[1]+1, height-now[1]+1, height-now[1]], color='red')              # now
plt.text(now[0]-0.33, height-now[1]-0.4, 'Now', fontdict={'family':'serif', 'color':'black', 'weight':'bold'})

up = False
go_way = []
if now[1] >= destination[1]:
    up = True

for i in list(way.values()):
    if up:
        if now[1] >= i[1]:
            go_way.append(i)
    else:
        if now[1] <= i[1]:
            go_way.append(i)

length_way_now = [((now[0]-i[0])**2+(now[1]-i[1])**2)**0.5 for i in go_way]#list(way.values())]
min_length_way_now = min(length_way_now)
way_now = go_way[np.argmin(length_way_now)]

length_way_ex = [((destination[0]-i[0])**2+(destination[1]-i[1])**2)**0.5 for i in list(way.values())]
min_length_way_ex = min(length_way_ex)
way_ex = way[np.argmin(length_way_ex)]

# 거리짧으면 그냥 바로 이어지게,,, 고민해보자

#plt.plot([0, 5], [0, 5],color="red")
line_color = "blue"

if (way_now==way_ex) and (now[1]-destination[1])**2<5:
    plt.plot([now[0]+0.5, destination[0]+0.5], [height-now[1]+0.5, height-destination[1]+0.5], color=line_color)
else:
    plt.plot([now[0]+0.5, way_now[0]+0.5], [height-now[1]+0.5, height-way_now[1]+0.5], color=line_color)
    plt.plot([way_now[0]+0.5, way_ex[0]+0.5], [height-way_now[1]+0.5, height-way_ex[1]+0.5], color=line_color)
    plt.plot([destination[0]+0.5, way_ex[0]+0.5], [height-destination[1]+0.5, height-way_ex[1]+0.5], color=line_color)

plt.rcParams["figure.figsize"] = (6,12)
plt.axis('off')
plt.savefig('map.png')   # 이미지파일 저장
plt.show()

# print(list(way.values()))
# print(go_way)
# print(length_way_now)
# print(way_now)
