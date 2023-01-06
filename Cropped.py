# face detection with mtcnn on a photograph
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN
import cv2
from PIL import Image
#from pixellib.tune_bg import alter_bg
import PIL.Image
import numpy as np
import os
import glob
import tensorflow
from tkinter import *
from tensorflow import keras

warning = []
path1 = ""
path2 = ""
size = 0
img_array_input = [] #giriş resimleri
out_array = []


def read_img(path):
    
    st = os.path.join(path, "*.JPG")
    st_ = os.path.join(path, "*.jpg")
     

    for filename in glob.glob(st):
        print(st)
        #print("filename-------",filename)
        
        img_array_input.append(filename)
        print("image arraye eklendi : ", filename)
        
       
    for filename in glob.glob(st_):
        
        img_array_input.append(filename)
        #print("filename-------",filename)
        global size
        size = len(img_array_input)
        


    for i in img_array_input:   
        print("detection gidiliyor")     
        
        detection(i)
        print("detection çıktı") 
        
#size 0 = 6000 size1= 4000

def cropped(filename, nosex, nosey, width, height, yBox, xBox):
    
    img = PIL.Image.open(filename)
    w, h = img.size
    print("filename",filename)
    print("w,h, nosex",w, h, nosex)
    
    ortaNokta = w/2

        #resim boyutları küçük
    if ortaNokta - nosex > 0 and abs(ortaNokta - nosex)<220: #burun resmin solunda yani nosex <ortaNokta
            print("olasılık 1")
            print("aradaki fark",ortaNokta - nosex )
            print(w,xBox,width,yBox)
            print("ybox: if ",yBox)
            solaGisis = int(xBox/6)
            sagaGidis = nosex+nosex-(solaGisis)
            #int(w-(((w-(xBox + width))/4))) --------
            oran = int((sagaGidis-solaGisis)/3*4)
            #cuttingYdown-cutting = oran
            cuttingYdown = oran + int(yBox/4)
            if cuttingYdown<0:
                print("hatalı")
                out = path3
                head, tail = os.path.split(filename)
                img.save(os.path.join(out+"/",tail))
                

            elif yBox/4<350: #kafa tavana aşırı yakınsa 
                
                cuttingYdown = oran + int(yBox/5)

                cropFunc(filename, solaGisis, yBox/5, sagaGidis, cuttingYdown)

            elif yBox>2000: #kafa tavandan aşırı uzak 
                print("ybox>2000")
                oran = int((sagaGidis-solaGisis)/3*4)
                cuttingYdown = oran + yBox/2
                cropFunc(filename, solaGisis, yBox/2, sagaGidis, cuttingYdown)
                


            else:
                print(solaGisis, yBox/4, sagaGidis, cuttingYdown)
                print("oran", (sagaGidis-solaGisis)/3,"==?",(cuttingYdown-(yBox/4))/4)
                cropFunc(filename, solaGisis, yBox/4, sagaGidis, cuttingYdown)
                

    elif  ortaNokta - nosex < 0 and abs(ortaNokta - nosex)<220: #burun resmin sağında yani nosex > ortaNokta
        print("elif e geldndi")
        print("olasılık 2")
        print("aradaki fark",ortaNokta - nosex )
        print(w,xBox,width,yBox)
        sagaGidis = int(w-(((w-(xBox + width))/4)))  #>0 olma ihtimali yok 
        print("ybox: elif",yBox)
        solaGisis = nosex-(sagaGidis-nosex) 
        if solaGisis < 0:
            print("sola gidis<0")
            solaGisis == int(xBox/2)
        #solaGisis = int(xBox/4)#kafa kutusunun soluna 4 bölü 3 kadar gidilir
        print(solaGisis)
        oran = int((sagaGidis-solaGisis) / 3 * 4) #olması gerekn uzunluk
        cuttingYdown = oran + int(yBox/4)

        if yBox/4<350:
            
            print("if 2")
            sagaGidis = int(w-(((w-(xBox + width))/4)))  #>0 olma ihtimali yok 
            solaGisis = int(xBox/4)#kafa kutusunun soluna 4 bölü 3 kadar gidilir
            oran = int((sagaGidis-solaGisis) / 3 * 4) 
            cuttingYdown = oran + int(yBox/5)
            cropFunc(filename, solaGisis, yBox/5, sagaGidis, cuttingYdown)
        
        elif yBox>2000: #kafa tavandan aşırı uzak 
                cuttingYdown = oran + yBox/2
                cropFunc(filename, solaGisis, yBox/2, sagaGidis, cuttingYdown)
                
                
        else:

            print("else 2")
            cropFunc(filename, solaGisis, yBox/4, sagaGidis, cuttingYdown)
            print("oran", (sagaGidis-solaGisis)/3,"==?",(cuttingYdown-(yBox/4))/4)
            print(solaGisis, yBox/4, sagaGidis, cuttingYdown)
    
    else : 
        print("ybox: else",yBox/4)
        print("else gelindi.")
        print("olasılık 3 kafa çok eğik")
        #kafa hangi yönde bilmiyoruz, o zaman onu soralım

        if ortaNokta - nosex>0: #burun resmin çok solunda        
            solaGisis = int(xBox/6)
            sagaGidis = nosex+nosex-(solaGisis) #int(w-(((w-(xBox + width))/4))) 
            oran = int((sagaGidis-solaGisis)/3*4)
            cuttingYdown = oran + int(yBox/4)

            if yBox/4<350:
                print("kafa aşırı yakın")
                cuttingYdown = oran + int(yBox/5)
                cropFunc(filename, solaGisis, yBox/5, sagaGidis, cuttingYdown)

            elif yBox>2000: #kafa tavandan aşırı uzak 
                print("#kafa tavandan aşırı uzak ")
                cuttingYdown = oran + yBox/2
                cropFunc(filename, solaGisis, yBox/2, sagaGidis, cuttingYdown)
                
           

            else:
                cropFunc(filename, solaGisis, yBox/4, sagaGidis, cuttingYdown)

        elif ortaNokta - nosex<0: #burun resmin çok sağında 
            sagaGidis = int(w-(((w-(xBox + width))/6))) 
            solaGisis = nosex-(sagaGidis-nosex) #int(xBox/4*3)
            
            oran = int((sagaGidis-solaGisis)/3*4)
            cuttingYdown = oran + int(yBox/4)

            if yBox/4<350:
                cuttingYdown = oran + int(yBox/5)
                cropFunc(filename, solaGisis, yBox/5, sagaGidis, cuttingYdown)

            elif yBox>2000: #kafa tavandan aşırı uzak 
                cuttingYdown = oran + yBox/2
                cropFunc(filename, solaGisis, yBox/2, sagaGidis, cuttingYdown)
                
           
            else:
                cropFunc(filename, solaGisis, yBox/4, sagaGidis, cuttingYdown)




def draw_image_with_boxes(filename, result_list):
    # load the image
    img = PIL.Image.open(filename)
    w, h = img.size
    data = pyplot.imread(filename)
    # plot the image
    #pyplot.imshow(data)
    # get the context for drawing boxes
    #ax = pyplot.gca()
    # plot each box
    for result in result_list:
# get coordinates
        x, y, width, height = result['box']
        print("resulm box--",result)
       
        nosex, nosey = result['keypoints']['nose']
        print("nose:",nosex,nosey)
        maxFarkY = 0 
        maxFarkX = 0 
        if width*height<100000 or (abs(w/2-nosex)>500) or abs(h/2-nosey)>2000:
            print("hatalıya gelindi")
            print("width*height",width*height)
            print("abs(w/2-nosex)>500",abs(w/2-nosex))
            print("abs(h/2-nosey)>2000",abs(h/2-nosey))
            warning.append(filename)
            out = path3
            head, tail = os.path.split(filename)
            img.save(os.path.join(out+"/",tail))
            continue
        
        elif len(result) == 0:
            print("face yok gelindi", width, height)
            warning.append(filename)
            out = path3
            head, tail = os.path.split(filename)
            img.save(os.path.join(out+"/",tail))
            continue

        
        #print("rect--",rect)5
        
        else:
            print(result["box"])
            #rect = Rectangle((x, y), width, height, fill=False, color='red')
            #ax.add_patch(rect)
            #pyplot.show()
        #pyplot.show()
            cropped(filename, nosex, nosey, width, height, y, x)
        #print(filename, x, y, width, height)
        #cv2.imshow("cropped", cropped_image)
        # create the shape
        #rect = Rectangle((x, y), width, height, fill=False, color='red')
        #print("rect--",rect)5
        #ax.add_patch(rect)
        #pyplot.show()
    # show the plot
    

def cropFunc(filename, x0, y0, x1, y1):
    print("croppedfunc gelindi")
    img = PIL.Image.open(filename)
    cropped_img = img.crop((x0, y0, x1, y1))
    head, tail = os.path.split(filename)
    cropped_img.save(os.path.join(outpath+"/",tail))
    wid,hei = cropped_img.size
    print("yeni resim uzunlluk :",wid,hei)
   


def detection(filename):
     
# load image from file
    pixels = pyplot.imread(filename)
# create the detector, using default weights
    detector = MTCNN()
# detect faces in the image
    faces = detector.detect_faces(pixels)
    
    #print("faces:",faces)
# display faces on the original image
    #print("faces--",faces)
    if len(faces) == 0 :
        
        img = PIL.Image.open(filename)
        print("face bulunamadı !!hatalı")
        out = path3
        head, tail = os.path.split(filename)
        img.save(os.path.join(out+"/",tail))
    
    else:
        draw_image_with_boxes(filename, faces)
    
    #img = cv2.imread(filename)
    
# Cropping an imaged
    #cropped_image = img[800:2500, 800:2400]
 
# Display cropped image
    #cv2.imshow("cropped", cropped_image)
    
# Save the cropped image
   

window = Tk()
def tkinter():
    
    window.config(bg='#e0eeee')
    window.title("Resim Kırpma Programı")
    window.geometry('550x200')
    #window.resizable(width=False, height=False)
    


    lbl1 = Label(window, text="Kırpılacak resimlerin olduğu dosyanın adresi")
    lbl1.grid(column=0, row=0)

    lbl2 = Label(window, text="Kırpılacak resimlerin kaydedileceği dosyanın adresi")
    lbl2.grid(column=0, row=1)
  
    lbl3 = Label(window, text="Hatalı resimlerin kaydedileceği dosyanın adresi")
    lbl3.grid(column=0, row=2)
    
    txt1 = Entry(window,width=10)
    txt1.grid(column=1, row=0)

    txt2 = Entry(window,width=10)
    txt2.grid(column=1, row=1)

    txt3 = Entry(window,width=10)
    txt3.grid(column=1, row=2)
   
    def clicked():
      
        global path1
        path1 = txt1.get()
        global path2
        path2 = txt2.get()
        global path3
        path3 = txt3.get()
        global outpath
        outpath = path2
        
        read_img(path1)
        
        control(path2)
        orancontrol()
        
        remove_img()
        label_break()
        
    
    btn = Button(window, text="Çalıştır", command=clicked)
    btn.grid(column=2, row=3)
    window.mainloop()

def label_break():
    # lbl3.pack_forget()
      print("label break gelindi")
     
      lbla = Label(window, text="İşleminiz Tamamlandı. Lütfen klasörlerinizi kontrol edin.")
      lbla.grid(column=1,row=5)
    #   lbl4.place(relx = 0.5,
    #               rely = 0.5,
    #               anchor = 'center')


def control(path):
    st = os.path.join(path, "*.JPG" or "*.jpg")
    sayı = 0
    for filename in glob.glob(st):
        sayı = sayı + 1
        #print("sayı: ", sayı)
    
    hatalı = size - sayı
    print("hatalı resim sayısı:",hatalı)

def orancontrol():
    st = os.path.join(outpath, "*.JPG" )
    for filename in glob.glob(st):
        img = PIL.Image.open(filename)
        we, he = img.size 
        print("new sizes:", we, he)
        if int(he/4) != int(we/3):
            print("oran eşit değil",filename)
            head, tail = os.path.split(filename)
            img.save(os.path.join(path3+"/",tail))
        else:
            print("oransız resim bulunamadı.")

    print("kayıt başarılı")

def remove_img():
    global path
    path = path2
    global path_
    path_ = path3
    #out dosyasındaki resimleri oku.
    #hatali klasöründeki resimleri oku
    #path i aynı olan resimleri sil
    st = os.path.join(path, "*.JPG" or "*.jpg")
    st2 = os.path.join(path_, "*.JPG" or "*.jpg")

    for filename in glob.glob(st):
        degisken1 = filename.split("/")[-1:]
        #print("degisken 1",degisken1)
        for filename2 in glob.glob(st2):
            degisken2 = filename2.split("/")[-1:]
            #print("degisken2",degisken2)
            if degisken2[0] == degisken1[0]:
                a = degisken1[0]
                os.remove(path_+'/'+a)
                print("silindi")
            else:
                continue
                

    st_ = os.path.join(path, "*.jpg")
    st2_ = os.path.join(path_, "*.jpg")

    for filename in glob.glob(st_):
        degisken1 = filename.split("/")[-1:]
        print("degisken 1",degisken1)
        for filename2 in glob.glob(st2_):
            degisken2 = filename2.split("/")[-1:]
            print("degisken2",degisken2)
            if degisken2[0] == degisken1[0]:
                a = degisken1[0]
                os.remove(path_+'/'+a)
                print("silindi")
            else:
                continue


    
if __name__ == '__main__':
    tkinter()
    
    
   
