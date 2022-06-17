# -*- coding: utf-8 -*-
import cv2
#载入并显示图片
import os

def get_allfile(path):  # 获取所有文件
    all_file = []
    for f in os.listdir(path):  #listdir返回文件中所有目录
        f_name = os.path.join(path, f)
        all_file.append(f_name)
    return all_file

tickets='test3'
all_file=get_allfile(tickets)  #tickets要获取文件夹名
#print(all_file)
file = open('result3\\result3.txt','w')

for i in all_file:
    print('------------------------------')
    if(i[-4:]!='.bmp'):continue  #如果图片不是bmp格式则跳过
    inputaddress=i#'10 (164).bmp'#i#
    outputaddress='result3'+i[5:]
    img=cv2.imread(inputaddress,1)
    if(img is None):continue    #如果图片无法读入则跳过
    #降噪（模糊处理用来减少瑕疵点）
    result = cv2.blur(img, (6,6))
    #灰度化,就是去色（类似老式照片）
    gray=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    #先检测电容范围
    #circles1= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT_ALT,1,50,param1=20,param2=0.6,minRadius=30,maxRadius=190)#190 220
    circles1= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,50,param1=20,param2=30,minRadius=190,maxRadius=220)#190 220

    
    if circles1 is None:
        print('未检测到电容')
        file.write(i[6:]+' 未检测到电容'+'\n')
        #cv2.imwrite(outputaddress,img)
        continue;
    else:
        file.write(i[6:])
        for circle1 in circles1[0]:

            x1=int(circle1[0])
            y1=int(circle1[1])
        #半径
            r1=int(circle1[2]*19/30)#-80
            gray = gray[y1-r1:y1+r1, x1-r1:x1+r1].copy()  # 切片获得裁剪后保留的图像区域
            #cv2.imwrite('showgray.png',gray)
        #在电容范围的ROI内检测管脚        
            ret, gray = cv2.threshold(gray, 170, 255, cv2.THRESH_BINARY)#二值化160
            contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)#获取图像轮廓
            result=[]
            for cnt in contours:
                print('找到一个')
                # 轮廓外接圆
                # 返回圆心坐标和半径
                (x,y),radius = cv2.minEnclosingCircle(cnt)
                # 圆心坐标
                center = (int(x),int(y))
                # 半径
                radius = int(radius)
                print(radius)
                # 绘制外接圆，输入整型
                if(radius>9 and radius<25 and ((-r1+x)*(-r1+x)+(-r1+y)*(-r1+y))<r1*r1):
                    result.append(((-r1+x)*(-r1+x)+(-r1+y)*(-r1+y),int(x1-r1+x),int(y1-r1+y),radius))
                   
                                    
            break
        if(len(result)>1):
            #file.write(' '+len(result))
            result.sort()
            res=result[0:2]#取前两个，用于左右排序
            res.sort(key=lambda x:x[1])
            file.write(' ('+str(res[0][1])+','+str(int(res[0][2]))+') '+str(res[0][3]))
            file.write(' ('+str(res[1][1])+','+str(int(res[1][2]))+') '+str(res[1][3]))
            img = cv2.circle(img,(int(res[0][1]),int(res[0][2])),res[0][3],(0,0,255),2)    
            img = cv2.circle(img,(int(res[1][1]),int(res[1][2])),res[1][3],(0,0,255),2)    
        else:
            file.write('只检测到一个管脚')                        
        file.write('\n')
        cv2.imwrite(outputaddress,img)