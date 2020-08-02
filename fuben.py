# -*- coding: utf-8 -*-
#导入包
#图形化
import tkinter as tk
from tkinter import filedialog
#文件夹
import os
#图像处理
from PIL import Image,ImageTk
import cv2
#数据处理
import pandas as pd
#OCR分析
from aip import AipOcr
import win32api,win32con
#爬虫
import re
import urllib
from urllib import request
import requests

#设置界面
#网页操作
class urlget():
    def __init__(self):
        #设计GUI界面布局
        self.win=tk.Tk()
        self.win.title("网络图片查询")
        self.canvas=tk.Canvas(self.win,width=500,height=300,bd=0,highlightthickness=0)
        self.imgpath='background.jpg'
        self.img=Image.open(self.imgpath)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(300, 200, image=self.photo)
        self.canvas.pack()
        self.label=tk.Label(self.win,text="请输入您的关键词")
        self.e1=tk.Variable()
        self.entry=tk.Entry(self.win,textvariable=self.e1,insertbackground='blue', highlightthickness =2)
        self.entry.pack()
        self.b0=tk.Button(self.win,text="查询",command=self.searchurl)
        self.b0.pack()
        self.br=tk.Button(self.win,text='切换到本机',command=self.return_benji)
        self.br.pack()
        self.bc=tk.Button(self.win,text='点击打开网页链接',command=self.openup)
        self.bc.pack()
        self.canvas.create_window(100,50,width=90,height=30,window=self.entry)
        self.canvas.create_window(100,90,width=80,height=30,window=self.b0)
        self.canvas.create_window(100,130,width=90,height=30,window=self.br)
        self.canvas.create_window(100,170,width=100,height=30,window=self.bc)
    def openup(self):
        os.system('target.html')
    def return_benji(self):#切换
        self.win.destroy()
        rename_next()
    def searchurl(self):#利用爬虫技术查找网址
        self.key=self.e1.get()
        dat={'wrd':self.key}#关键词字典
        self.key=urllib.parse.urlencode(dat)
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + self.key + '&ct=201326592&v=flip'#网址
        url_request=request.Request(url)
        url_response = request.urlopen(url_request)   # 请求数据，可以和上一句合并
        html = url_response.read().decode('utf-8')  # 加编码，重要！转换为字符串编码，read()得到的是byte格式的。
        jpglist = re.findall('"objURL":"(.*?)",',html,re.S)	#re.S将字符串作为整体,在整体中进行匹配。
        with open("target.html","w",encoding="utf-8")as f:#将链接写入HTML文件中，可以在浏览器打开
           # 将爬取的页面
           #print(html)
           start='<html>\n    <body>\n'
           f.write(start)
           count=1
           for i in jpglist:
               link='        <a href="'+i+'">目标图片第%d张</a></br>\n'%count 
               f.write(link)
               count+=1
           end='    </body>\n</html>'
           f.write(end)
        self.stp='查询完毕'
        self.text2=tk.Text(self.win,width=30,height=1)
        self.text2.insert(tk.INSERT,self.stp)
        self.text2.pack()
        #print(jpglist)


#重命名操作
class rename_next():
    def __init__(self):
        self.win=tk.Tk()
        self.win.title("搜图")
        self.canvas=tk.Canvas(self.win, width=500,height=300,bd=0, highlightthickness=0)
        self.imgpath = 'background.jpg'
        self.img = Image.open(self.imgpath)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(300, 200, image=self.photo)
        self.canvas.pack()
        self.label=tk.Label(self.win,text="亲爱的用户，如果您是初次使用，建议您先进行预处理操作。若非首次操作，可以进行下一步")
        self.label.pack()
        self.b3=tk.Button(self.win,text="预处理",command=self.rename)
        self.b4=tk.Button(self.win,text="下一步",command=self.change2)
        self.b3.pack()
        self.b4.pack()
        self.canvas.create_window(100,50,width=90,height=30,window=self.b3)
        self.canvas.create_window(100,90,width=80,height=30,window=self.b4)
        self.win.mainloop()
    def rename(self):
        #确定路径
        path=folderpath
        self.files=os.listdir(path)
        self.i=0
        #重命名
        #要加一个断言调试
        try:
            for self.file in self.files:
                #重命名
                self.olddir=os.path.join(path,self.file)
                self.filename=os.path.splitext(self.file)[0]   #文件名
                self.filetype=os.path.splitext(self.file)[1]   #文件扩展名
                self.Newdir=os.path.join(path,str(self.i)+'.jpg')
                os.rename(self.olddir,self.Newdir)#重命名
                self.i+=1
            self.stp='文件预处理已经完毕'
            self.text1=tk.Text(self.win,width=30,height=1)
            self.text1.insert(tk.INSERT,self.stp)
            self.text1.pack()
        except FileExistsError as identifier:
            self.stp='文件已经处理过'
            self.text2=tk.Text(self.win,width=30,height=1)
            self.text2.insert(tk.INSERT,self.stp)
            self.text2.pack()
    def change2(self):
        self.win.destroy()
        check_and_in()
#OCR操作
class check_and_in():
    def __init__(self):
        self.win=tk.Tk()
        self.win.title("搜图")
        self.canvas=tk.Canvas(self.win, width=500,height=300,bd=0, highlightthickness=0)
        self.imgpath = 'background.jpg'
        self.img = Image.open(self.imgpath)
        self.photo = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(300, 200, image=self.photo)
        self.canvas.pack()
        self.b5=tk.Button(self.win,text="OCR处理",command=self.ocr_test)
        self.b6=tk.Button(self.win,text="查询",command=self.search)
        self.label=tk.Label(self.win,text="请输入你的关键词")
        self.e2=tk.Variable()
        self.entry=tk.Entry(self.win,textvariable=self.e2,insertbackground='blue', highlightthickness =2)
        self.b5.pack()
        self.b6.pack()
        self.b7=tk.Button(self.win,text="切换至网页",command=self.change_to_web)
        self.b7.pack()
        self.label.pack()
        self.entry.pack()
        self.canvas.create_window(100,90,width=80,height=30,window=self.b5)
        self.canvas.create_window(100,130,width=90,height=30,window=self.b6)
        self.canvas.create_window(100,170,width=100,height=30,window=self.b7)
    
    def ocr_test(self):
        try:
            self.ocr()
        except KeyError as identifier:
            win32api.MessageBox(0,"阿偶，服务出错了，尝试切换到网页端再切回来或者等待一下下","提醒",win32con.MB_ICONWARNING)
    def ocr(self):#等待优化中
        self.APP_ID = '21176389'
        self.API_KEY = 'LO0dFlHgoWF8T6iwtZEjGXjv'
        self.SECRET_KEY = 'dA71y4UebM5g2CCowN9SUs8abqtSg0Ru'
        self.client= AipOcr(self.APP_ID, self.API_KEY, self.SECRET_KEY)#百度API直接套用，以后可以更改
        self.path=folderpath
        self.filelist=os.listdir(self.path)#打开文件夹
        self.count=0
        self.text=[]#文字内容
        for self.file in self.filelist:
               self.count+=1
        for self.i in range(self.count):
               self.file='%d.jpg'%self.i
               self.image=self.get_file_content(self.path+'/'+self.file)
               self.res=self.client.basicAccurate(self.image)
               self.string=''
               for self.item in self.res['words_result']:
                    self.string+=self.item['words']
               if self.string=='':
                       self.string='NaN'
               self.text.append(self.string)
               self.i+=1
        #生成数据库
        self.num=range(self.count)
        self.number_column = pd.Series(self.num, name='number')
        self.text_column = pd.Series(self.text, name='text')
        self.predictions = pd.concat([self.number_column, self.text_column], axis=1)
        self.save = pd.DataFrame({'number':self.num,'text':self.text})
        self.save.to_csv('database.csv')
        self.str='图片与OCR工作已经完成'
        self.text1=tk.Text(self.win,width=30,height=1)
        self.text1.insert(tk.INSERT,self.str)
        self.text1.pack()
     #网页端切换          
    def change_to_web(self):
        self.win.destroy()
        urlget()  
    #数据查询  
    def search(self):
        #self.path=folderpath
        self.path=folderpath
        self.df=pd.read_csv('database.csv')
        self.key=self.e2.get()
        self.count=0
        self.search_pos=False
        #记得在这里加一个TypeError的断言，当然，报错是越少越好，也要想办法解决TypeError
        
        try:
            for self.i in self.df.text:
                if self.key in self.i:
                    self.search_pos=True
                    self.img=cv2.imread(self.path+'/%d.jpg'%self.count)
                    cv2.imshow("target",self.img)
                    cv2.waitKey()
                    cv2.destroyAllWindows()
                self.count+=1
            if self.search_pos==False:
                self.str='很可惜没能找到呢，搜索NaN看看，再搜不出来就是识别问题'
                self.text2=tk.Text(self.win,width=70,height=1)
                self.text2.insert(tk.INSERT,self.str)
                self.text2.pack()
        except Exception as error:
            win32api.MessageBox(0, "出错了,重试一下或者试试搜搜别的", "提醒",win32con.MB_ICONWARNING)
        
    #内容读取                                    
    def get_file_content(self,filePath):
        self.filePath=filePath
        with open(self.filePath, 'rb') as fp:
            return fp.read()

#起始页面
if __name__=='__main__':
    win=tk.Tk()
    win.title("搜图")
    canvas=tk.Canvas(win, width=500,height=300,bd=0, highlightthickness=0)
    imgpath = 'background.jpg'
    img = Image.open(imgpath)
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(300, 200, image=photo)
    canvas.pack()
    
    label=tk.Label(win,text="请输入路径")
    label.pack()
    folderpath=filedialog.askdirectory()
    def change1():
        win.destroy()
        #进入下一个界面
        rename_next()
    def change2():
        win.destroy()
        urlget()

    b2=tk.Button(win,text="本机搜索下一步",command=change1)
    b2.pack()
    b3=tk.Button(win,text='网页端',command=change2)
    b3.pack()
    canvas.create_window(100,50,width=90,height=30,window=b2)
    canvas.create_window(100,90,width=80,height=30,window=b3)
    win.mainloop() 
