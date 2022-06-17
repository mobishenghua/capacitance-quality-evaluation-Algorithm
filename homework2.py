# -*- coding: utf-8 -*-
import cv2
import numpy
import os

def get_allfile(path):  # 获取所有文件
    all_file = []
    for f in os.listdir(path):  #listdir返回文件中所有目录
        f_name = os.path.join(path, f)
        all_file.append(f_name)
    return all_file

tickets='test2'
all_file=get_allfile(tickets)  #tickets要获取文件夹名
print(all_file)
file = open('result2\\result2.txt','w')  #创建txt文档

for i in all_file:
    print('------------------------------')
    if(i[-4:]!='.bmp'):continue
    inputaddress=i
    outputaddress='result2'+i[5:]
    img=cv2.imread(inputaddress,1) #载入图片
    if(img is None):continue
    #降噪（模糊处理用来减少瑕疵点）
    result = cv2.blur(img, (5,5))
    #灰度化,就是去色（类似老式照片）
    gray=cv2.cvtColor(result,cv2.COLOR_BGR2GRAY)
    #param1的具体实现，用于边缘检测   
    canny = cv2.Canny(img, 40, 80)  
    #霍夫变换圆检测
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,50,param1=80,param2=30,minRadius=190,maxRadius=220)
    #输出返回值，方便查看类型
    if circles is None:  #如果没有找到圆形输出报错信息
        file.write(''+i[6:]+'未检测到电容'+'\n')
        cv2.imwrite(outputaddress,img)
        continue;
    else:
        print(circles)
    #输出检测到圆的个数
        print('检测到电容的个数为'+str(len(circles[0])))   
        #根据检测到圆的信息，画出每一个圆 
        for circle in circles[0]:
        #圆的基本信息
            print(circle[2])
        #坐标行列(就是圆心)
            x=int(circle[0])
            y=int(circle[1])
        #半径
            r=int(circle[2])
            file.write(i[6:]+' ('+str(x)+','+str(y)+') '+str(r)+'\n')
        #在原图用指定颜色圈出圆，参数设定为int所以圈画存在误差
            img=cv2.circle(img,(x,y),r,(0,0,255),10,8,0)  
        cv2.imwrite(outputaddress,img) #输出标出电容的图片