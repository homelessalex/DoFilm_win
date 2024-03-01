import numpy as np
from PIL import Image
from PIL.Image import Resampling
from colour import io,sRGB_to_XYZ,XYZ_to_ProLab,LUT3D,colour_correction,ProLab_to_XYZ,XYZ_to_sRGB,LUT1D, XYZ_to_RGB,RGB_to_RGB,RGB_to_XYZ
import rawpy
from scipy import ndimage,signal
import itertools
import time


def raw(raw_in,WB) -> np.array:

    cam=False
    auto=False
    if WB=="In camera WB":
        cam=True
    else:
        auto=True

    with rawpy.imread(raw_in) as raw:
            rgb = raw.postprocess(output_color=rawpy.ColorSpace(0),  demosaic_algorithm=rawpy.DemosaicAlgorithm(3), half_size=True,
                                use_camera_wb=cam, use_auto_wb=auto, highlight_mode=rawpy.HighlightMode(0),#user_wb=(1,1,1,1),
                                output_bps=16,  no_auto_scale=False, no_auto_bright=False,auto_bright_thr=0.000000001,
                                gamma=(1,1), chromatic_aberration=(1,1),)
    rgb=np.dstack((rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]))

    return rgb

def raw2(raw_in,WB) -> np.array:

    cam=False
    auto=False
    if WB=="In camera WB":
        cam=True
    else:
        auto=True

    with rawpy.imread(raw_in) as raw:
            rgb = raw.postprocess(output_color=rawpy.ColorSpace(0),  demosaic_algorithm=rawpy.DemosaicAlgorithm(3), half_size=False,
                                use_camera_wb=cam, use_auto_wb=auto, highlight_mode=rawpy.HighlightMode(0),#user_wb=(1,1,1,1),
                                output_bps=16,  no_auto_scale=False, no_auto_bright=False,auto_bright_thr=0.000000001,
                                gamma=(1,1), chromatic_aberration=(1,1),)
    rgb=np.dstack((rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]))

    return rgb

def zoom(rgb,resolution):
    img=ndimage.zoom(rgb,(float(resolution/float(np.max(np.shape(rgb)))),float(resolution/float(np.max(np.shape(rgb)))),1))






    



    return img

def add_corners(img):
    add=np.zeros((200,int(img.shape[1]),3),dtype=np.float32)
    for i in range(img.shape[1]):
        add[:,i,:]=img[int(img.shape[0]-10),i,:]
    img=np.vstack((img,add))
    for i in range(img.shape[1]):
        add[:,i,:]=img[10,i,:]
    img=np.vstack((add,img))
    add2=np.zeros((int(img.shape[0]),200,3),dtype=np.float32)

    for i in range(img.shape[0]):
        add2[i,:,:]=img[i,int(img.shape[1]-10),:]
    img=np.hstack((img,add2))
    for i in range(img.shape[0]):
        add2[i,:,:]=img[i,10,:]
    img=np.hstack((add2,img))
    return img


def pre_grain(image,gr_sample) -> np.array:
    image=image[200:int(image.shape[0]-200),200:int(image.shape[1]-200),:]
    if np.shape(image)[0]>np.shape(image)[1]:
        gr_sample=gr_sample.transpose(method=Image.Transpose.ROTATE_90)

    Grain_crop=gr_sample.resize((int(np.shape(image)[1]),int(np.shape(image)[0])),resample=Image.LANCZOS, )
    grain=np.array(Grain_crop,dtype=np.uint8)
    grain=io.convert_bit_depth(grain,"float64")
    grain_0=(grain-np.average(grain))
    return grain_0


"""
def colcol(img_in,wrong,right,w_ntr,r_ntr,delta,suttt):
    img_in2=np.array(img_in)

    wrong=np.nan_to_num(wrong)
    right=np.nan_to_num(right)

    poli_r=np.polynomial.polynomial.Polynomial.fit(w_ntr[:,0],r_ntr[:,0],deg=7)
    poli_g=np.polynomial.polynomial.Polynomial.fit(w_ntr[:,1],r_ntr[:,1],deg=7)
    poli_b=np.polynomial.polynomial.Polynomial.fit(w_ntr[:,2],r_ntr[:,2],deg=7)

    r_cor=poli_r(LUT1D.linear_table(64))
    g_cor=poli_g(LUT1D.linear_table(64))
    b_cor=poli_b(LUT1D.linear_table(64))
    r_cor=LUT1D(r_cor)
    g_cor=LUT1D(g_cor)
    b_cor=LUT1D(b_cor)

    img_in2[:,:,0]=r_cor.apply(img_in2[:,:,0])
    img_in2[:,:,1]=g_cor.apply(img_in2[:,:,1])
    img_in2[:,:,2]=b_cor.apply(img_in2[:,:,2])

    wrong[:,0]=r_cor.apply(wrong[:,0])
    wrong[:,1]=g_cor.apply(wrong[:,1])
    wrong[:,2]=b_cor.apply(wrong[:,2])


    wrong_0=np.array(wrong)
    right_0=np.array(right)

    a=1000
    a1=0
    a2=0
    a3=0


    g_r=0
    g_g=suttt
    g_b=0

    r_r=suttt
    r_g=0
    r_b=0

    b_r=0
    b_g=0
    b_b=suttt

    print(np.max(img_in2)," img_in2t")


    wrong=wrong[168:192,:]
    right=right[168:192,:]

    wrong2=np.array(wrong)
    wrong3=np.array(wrong)

    #pill=Image.fromarray(io.convert_bit_depth(np.reshape(right,(4,6,3)),"uint8"))
    #pill.show()

    def bw(samp):
        blwa=1-((samp[:,0]+samp[:,1]+samp[:,2])/3)
        #blwa=np.stack((blwa,blwa,blwa),-1)
        return blwa



    def average (wro,righ):
        delt=np.sum(np.fabs(righ-wro))
        return delt

    while a==a:
        wrong=np.array(wrong2)
        wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
        a1=abs(average(wrong[:,0],right[:,0]))
        wrong[:,0]=wrong3[:,0]*(r_r+0.0001)+wrong3[:,1]*r_g+wrong3[:,2]*r_b
        a1r=abs(average(wrong[:,0],right[:,0]))
        if a1r<a1:
            r_r+=0.0001
        else:
            r_r-=0.0001

        wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
        a1=abs(average(wrong[:,0],right[:,0]))
        wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*(r_g+0.0001)+wrong3[:,2]*r_b
        a1g=abs(average(wrong[:,0],right[:,0]))
        if a1g<a1:
            r_g+=0.0001
        else:
            r_g-=0.0001

        wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
        a1=abs(average(wrong[:,0],right[:,0]))
        wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*(r_b+0.0001)
        a1b=abs(average(wrong[:,0],right[:,0]))
        if a1b<a1:
            r_b+=0.0001
        else:
            r_b-=0.0001




        ################################
        #
        #
        #################################

        wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
        a2=abs(average(wrong[:,1],right[:,1]))
        wrong[:,1]=wrong3[:,0]*(g_r+0.0001)+wrong3[:,1]*g_g+wrong3[:,2]*g_b
        a2r=abs(average(wrong[:,1],right[:,1]))
        if a2r<a2:
            g_r+=0.0001
        else:
            g_r-=0.0001

        wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
        a2=abs(average(wrong[:,1],right[:,1]))
        wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*(g_g+0.0001)+wrong3[:,2]*g_b
        a2g=abs(average(wrong[:,1],right[:,1]))
        if a2g<a2:
            g_g+=0.0001
        else:
            g_g-=0.0001

        wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
        a2=abs(average(wrong[:,1],right[:,1]))
        wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*(g_b+0.0001)
        a2b=abs(average(wrong[:,1],right[:,1]))
        if a2b<a2:
            g_b+=0.0001
        else:
            g_b-=0.0001



        ################################
        #
        #
        #################################

        wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
        a3=abs(average(wrong[:,2],right[:,2]))
        wrong[:,2]=wrong3[:,0]*(b_r+0.0001)+wrong3[:,1]*b_g+wrong3[:,2]*b_b
        a3r=abs(average(wrong[:,2],right[:,2]))
        if a3r<a3:
            b_r+=0.0001
        else:
            b_r-=0.0001

        wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
        a3=abs(average(wrong[:,2],right[:,2]))
        wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*(b_g+0.0001)+wrong3[:,2]*b_b
        a3g=abs(average(wrong[:,2],right[:,2]))
        if a3g<a3:
            b_g+=0.0001
        else:
            b_g-=0.0001

        wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
        a3=abs(average(wrong[:,2],right[:,2]))
        wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*(b_b+0.0001)
        a3b=abs(average(wrong[:,2],right[:,2]))
        if a3b<a3:
            b_b+=0.0001
        else:
            b_b-=0.0001





        a=abs(average(wrong,right))
        if a<delta:
            break
        #print(a," its a")

    right=right_0
    wrong=wrong_0
    wrong[:,0]=wrong_0[:,0]*r_r+wrong_0[:,1]*r_g+wrong_0[:,2]*r_b
    wrong[:,1]=wrong_0[:,0]*g_r+wrong_0[:,1]*g_g+wrong_0[:,2]*g_b
    wrong[:,2]=wrong_0[:,0]*b_r+wrong_0[:,1]*b_g+wrong_0[:,2]*b_b


    img_in[:,:,:,0]=img_in2[:,:,:,0]*r_r+img_in2[:,:,:,1]*r_g+img_in2[:,:,:,2]*r_b
    img_in[:,:,:,1]=img_in2[:,:,:,0]*g_r+img_in2[:,:,:,1]*g_g+img_in2[:,:,:,2]*g_b
    img_in[:,:,:,2]=img_in2[:,:,:,0]*b_r+img_in2[:,:,:,1]*b_g+img_in2[:,:,:,2]*b_b

    return img_in,wrong

"""




def reduse_sharpness (input,Blur_rad,Halation,Blur_spred) -> np.array:

    def blur(size,k):
        #size=10 #радиус размытия
        #k=50  #коэффицент влияет на скорость угасания-чем выше тем быстрее
        x = np.fabs(np.linspace(-(size ), size , size*2+1)/size)#создаем последовательность 1...-0-...1
        x=1-x#гипербола отсюдова:https://habr.com/ru/articles/432622/
        x = np.outer(x, x)
        x=1-x
        kernel_2D=(((x-1)**2)*(x*k+k+1))/((k+1)*(k*x+1))  #превращаем его в 2d np.outer(kernel_1D.T, kernel_1D.T)
        suum=np.sum(kernel_2D)   #сумируем матрицу
        kernel_2D=kernel_2D/suum   #делим нашу матрицу на сумму для приведения в дщиапазон 0-1
        return kernel_2D
    blur_coef=float(np.max(np.shape(input))/1500)
    rgb_blur=np.dstack((
        signal.oaconvolve(input[:,:,0],blur(int(3*Blur_rad*Halation*blur_coef),(2**Blur_spred)*(blur_coef**2)),'same',None),
        signal.oaconvolve(input[:,:,1],blur(int(3*Blur_rad*blur_coef),(2**Blur_spred)*(blur_coef**2)),'same',None),
        signal.oaconvolve(input[:,:,2],blur(int(np.around((1/Halation)*3*Blur_rad*blur_coef)),(2**Blur_spred)*(blur_coef**2)),'same',None)
        ))

    rgb_blur=np.array(rgb_blur,dtype=np.float32)

    return rgb_blur


def bloom (input,bloom_rad,bloom_Halation,bloom_spred) -> np.array:

    def blur(size,k):
        #size=10 #радиус размытия
        #k=50  #коэффицент влияет на скорость угасания-чем выше тем быстрее
        x = np.fabs(np.linspace(-(size ), size , size*2+1)/size)#создаем последовательность 1...-0-...1
        x=1-x#гипербола отсюдова:https://habr.com/ru/articles/432622/
        x = np.outer(x, x)
        x=1-x
        kernel_2D=(((x-1)**2)*(x*k+k+1))/((k+1)*(k*x+1))  #превращаем его в 2d np.outer(kernel_1D.T, kernel_1D.T)
        suum=np.sum(kernel_2D)   #сумируем матрицу
        kernel_2D=kernel_2D/suum   #делим нашу матрицу на сумму для приведения в дщиапазон 0-1
        return kernel_2D
    blur_coef=float((np.max(np.shape(input))/1500))


    rgb_blur=np.dstack((
        signal.oaconvolve(input[:,:,0],blur(int(3*bloom_rad*bloom_Halation*blur_coef),(2**bloom_spred)*(blur_coef**2)),'same',None),
        signal.oaconvolve(input[:,:,1],blur(int(3*bloom_rad*blur_coef),(2**bloom_spred)*(blur_coef**2)),'same',None),
        signal.oaconvolve(input[:,:,2],blur(int(np.around((1/bloom_Halation)*3*bloom_rad*blur_coef)),(2**bloom_spred)*(blur_coef**2)),'same',None)
        ))

    rgb_blur=np.array(rgb_blur,dtype=np.float32)
    return rgb_blur

def sharpen (input,Sharp_rad,Sharp_spread,amplyfy):


    def blur(size,k):
        #size=10 #радиус размытия
        #k=50  #коэффицент влияет на скорость угасания-чем выше тем быстрее
        x = np.fabs(np.linspace(-(size ), size , size*2+1)/size)#создаем последовательность 1...-0-...1
        x=1-x#гипербола отсюдова:https://habr.com/ru/articles/432622/
        x = np.outer(x, x)
        x=1-x
        kernel_2D=(((x-1)**2)*(x*k+k+1))/((k+1)*(k*x+1))  #превращаем его в 2d np.outer(kernel_1D.T, kernel_1D.T)
        suum=np.sum(kernel_2D)   #сумируем матрицу
        kernel_2D=kernel_2D/suum   #делим нашу матрицу на сумму для приведения в дщиапазон 0-1
        return kernel_2D
    blur_coef=float(np.max(np.shape(input))/1500)
    rgb_blured=np.dstack((
        signal.fftconvolve(input[:,:,0],blur(int(3*Sharp_rad*blur_coef),(2**Sharp_spread)*(blur_coef**2)),'same',None),
        signal.fftconvolve(input[:,:,1],blur(int(3*Sharp_rad*blur_coef),(2**Sharp_spread)*(blur_coef**2)),'same',None),
        signal.fftconvolve(input[:,:,2],blur(int(3*Sharp_rad*blur_coef),(2**Sharp_spread)*(blur_coef**2)),'same',None)
        ))

    rgb_blured=np.array(rgb_blured,dtype=np.float32)

    blured=(input-rgb_blured)*(amplyfy/100)
    input+=blured
    input[input>=1]=1
    input[input<=0]=0
    input=input[200:int(input.shape[0]-200),200:int(input.shape[1]-200),:]
    return input

def rgb_mix( r_hue,
            r_sut,
            r_g,
            r_b,

            g_hue,
            g_sut,
            g_r,
            g_b,

            b_hue,
            b_sut,
            b_r,
            b_g
            ):
    hald=LUT3D.linear_table(64)
    hald=np.array(hald,np.float32)
    #hald/=3 #img/1=вся сцена занимает диапазон0-1 img/10=вся сцена занимает диапазон 0.45-0.55

    #                      RGB MIXER
    hald[:,:,:,0]=hald[:,:,:,0]*(1+r_sut)+(hald[:,:,:,1]*(-r_sut/2))+(hald[:,:,:,2]*(-r_sut/2))
    hald[:,:,:,0]=hald[:,:,:,0]+(hald[:,:,:,1]*r_hue)+(hald[:,:,:,2]*(-r_hue)) #r+-
    hald[:,:,:,0]=(hald[:,:,:,0]*(1-r_g))+(hald[:,:,:,1]*r_g)
    hald[:,:,:,0]=(hald[:,:,:,0]*(1-r_b))+(hald[:,:,:,2]*r_b)


    hald[:,:,:,1]=hald[:,:,:,1]*(1+g_sut)+(hald[:,:,:,0]*(-g_sut/2))+(hald[:,:,:,2]*(-g_sut/2))
    hald[:,:,:,1]=hald[:,:,:,1]+(hald[:,:,:,0]*g_hue)+(hald[:,:,:,2]*(-g_hue)) #r+-
    hald[:,:,:,1]=(hald[:,:,:,1]*(1-g_r))+(hald[:,:,:,0]*g_r)
    hald[:,:,:,1]=(hald[:,:,:,1]*(1-g_b))+(hald[:,:,:,2]*g_b)



    hald[:,:,:,2]=hald[:,:,:,2]*(1+b_sut)+(hald[:,:,:,0]*(-b_sut/2))+(hald[:,:,:,1]*(-b_sut/2))
    hald[:,:,:,2]=hald[:,:,:,2]+(hald[:,:,:,0]*b_hue)+(hald[:,:,:,1]*(-b_hue)) #r+-
    hald[:,:,:,2]=(hald[:,:,:,2]*(1-b_r))+(hald[:,:,:,0]*b_r)
    hald[:,:,:,2]=(hald[:,:,:,2]*(1-b_g))+(hald[:,:,:,1]*b_g)
    #hald+=((Exp_shift/9))
    

    

    return hald

def apply_film(hald,
            wrong,
            right,
            accuracy,film

            ) -> np.array:
    degr=9
    lut_size=64
    wrong-=np.min(wrong)
    wrong*=(1/np.max(wrong))

    def ntrls(sourse_tif):
            ntrl_r=np.zeros((1,6,3))


            for i in range(1,17):
                z=(i*4)-1
                y=sourse_tif[z,:,:]
                y=y.reshape((1,6,3))
                ntrl_r=np.vstack((ntrl_r,y))
            ntrl_r=ntrl_r[1:17,:,:]
            ntrl_r=np.sort(ntrl_r)


            return ntrl_r


    wrong_0=np.array(wrong)
    right_0=np.array(right)
    wrong=ntrls(wrong)
    right=ntrls(right)
    wrong=np.nan_to_num(wrong)
    right=np.nan_to_num(right)

    a2r=100
    #a2=abs(avavrge(wrong,right))
    lut=np.stack((np.linspace(0,1,lut_size),np.linspace(0,1,lut_size),np.linspace(0,1,lut_size)),-1)
    lut2=np.array(lut)
    wrong2=np.array(wrong)
    
    def rgb_curve(lut,wrong,right,degr):
            def avavrge (wro,righ):
                    delt=np.fabs((righ-wro))
                    delt=np.nan_to_num(delt)
                    delt=np.average(delt)
                    return delt
            count=0
            wrong2=np.array(wrong)
            x=0.1
            lut2=np.array(lut)
            for i in range(20):
                    count+=1
                    if count==4:
                            a3=avavrge(wrong,right)
                            count=0
                            x=x/3
                    for a in range(lut_size):
                            for d in range(3):
                                    poli=np.polynomial.polynomial.Polynomial.fit(lut2[:,d],lut[:,d],deg=degr)
                                    wrong[:,:,d]=poli(wrong2[:,:,d])
                                    a2=avavrge(wrong[:,:,:],right[:,:,:])
                                    lut[a,d]+=x
                                    poli=np.polynomial.polynomial.Polynomial.fit(lut2[:,d],lut[:,d],deg=degr)
                                    wrong[:,:,d]=poli(wrong2[:,:,d])
                                    a2r=avavrge(wrong[:,:,:],right[:,:,:])
                                    if a2r>=a2:
                                            lut[a,d]-=(x)
                                            lut[a,d]-=(x)

                                            poli=np.polynomial.polynomial.Polynomial.fit(lut2[:,d],lut[:,d],deg=degr)
                                            wrong[:,:,d]=poli(wrong2[:,:,d])
                                            a2r=avavrge(wrong[:,:,:],right[:,:,:])
                                            if a2r>=a2:
                                                    lut[a,d]+=(x)



            return lut


    lut=rgb_curve(lut,wrong,right,degr)

    wrong=np.array(wrong_0)

    right=np.array(right_0)
    for d in range(3):
            poli=np.polynomial.polynomial.Polynomial.fit(lut2[:,1],lut[:,1],deg=degr)
            wrong[:,:,d]=poli(wrong[:,:,d])

    wrong2=np.array(wrong)
    lut_3d=np.array(hald)
    lut_3d_2=np.array(hald)
    wrong=wrong.reshape((384,3))
    right=right.reshape((384,3))

    for d in range(3):
            poli=np.polynomial.polynomial.Polynomial.fit(lut2[:,1],lut[:,1],deg=degr)
            lut_3d[:,:,:,d]=poli(lut_3d[:,:,:,d])


    
    def colcolo(img_in,wrong,right,):
            wrong_0=np.array(wrong)
            right_0=np.array(right)
            suttt=1
            coeff=0.1
            
            a=1000
            a1=0
            a2=0
            a3=0


            g_r=0
            g_g=suttt
            g_b=0

            r_r=suttt
            r_g=0
            r_b=0

            b_r=0
            b_g=0
            b_b=suttt
            img_in2=np.array(img_in)


            wrong=wrong[168:192,:]
            right=right[168:192,:]

            wrong2=np.array(wrong)
            wrong3=np.array(wrong)

            #pill=Image.fromarray(io.convert_bit_depth(np.reshape(right,(4,6,3)),"uint8"))
            #pill.show()

            def bw(samp):
                    blwa=1-((samp[:,0]+samp[:,1]+samp[:,2])/3)
                    #blwa=np.stack((blwa,blwa,blwa),-1)
                    return blwa



            def average (wro,righ):
                    delt=np.sum(np.fabs(righ-wro))
                    return delt
            count=0
            for i in range(10000):
                    a=abs(average(wrong,right))
                    count+=1
                    if count==100:
                            count=0
                            coeff*=0.95
                    wrong=np.array(wrong2)
                    wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
                    a1=abs(average(wrong[:,0],right[:,0]))
                    r_r+=coeff
                    wrong[:,0]=wrong3[:,0]*(r_r)+wrong3[:,1]*r_g+wrong3[:,2]*r_b
                    a1r=abs(average(wrong[:,0],right[:,0]))
                    if a1r>a1:
                            r_r-=(2*coeff)
                            wrong[:,0]=wrong3[:,0]*(r_r)+wrong3[:,1]*r_g+wrong3[:,2]*r_b
                            a1r=abs(average(wrong[:,0],right[:,0]))
                            if a1r>a1:
                                    r_r+=coeff

                    wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
                    a1=abs(average(wrong[:,0],right[:,0]))
                    r_g+=coeff
                    wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*(r_g)+wrong3[:,2]*r_b
                    a1g=abs(average(wrong[:,0],right[:,0]))
                    if a1g>a1:
                            r_g-=(2*coeff)
                            wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*(r_g)+wrong3[:,2]*r_b
                            a1g=abs(average(wrong[:,0],right[:,0]))
                            if a1g>a1:
                                    r_g+=coeff

                    wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*r_b
                    a1=abs(average(wrong[:,0],right[:,0]))
                    r_b+=coeff
                    wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*(r_b)
                    a1b=abs(average(wrong[:,0],right[:,0]))
                    if a1b>a1:
                            r_b-=(2*coeff)
                            wrong[:,0]=wrong3[:,0]*r_r+wrong3[:,1]*r_g+wrong3[:,2]*(r_b)
                            a1b=abs(average(wrong[:,0],right[:,0]))
                            if a1b>a1:
                                    r_b+=coeff




                    ################################
                    #
                    #
                    #################################

                    wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
                    a2=abs(average(wrong[:,1],right[:,1]))
                    g_r+=coeff
                    wrong[:,1]=wrong3[:,0]*(g_r)+wrong3[:,1]*g_g+wrong3[:,2]*g_b
                    a2r=abs(average(wrong[:,1],right[:,1]))
                    if a2r>a2:
                            g_r-=(2*coeff)
                            wrong[:,1]=wrong3[:,0]*(g_r)+wrong3[:,1]*g_g+wrong3[:,2]*g_b
                            a2r=abs(average(wrong[:,1],right[:,1]))
                            if a2r>a2:
                                    g_r+=coeff

                    wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
                    a2=abs(average(wrong[:,1],right[:,1]))
                    g_g+=coeff
                    wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*(g_g)+wrong3[:,2]*g_b
                    a2g=abs(average(wrong[:,1],right[:,1]))
                    if a2g>a2:
                            g_g-=(2*coeff)
                            wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*(g_g)+wrong3[:,2]*g_b
                            a2g=abs(average(wrong[:,1],right[:,1]))
                            if a2g>a2:
                                    g_g+=coeff

                    wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*g_b
                    a2=abs(average(wrong[:,1],right[:,1]))
                    g_b+=coeff
                    wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*(g_b)
                    a2b=abs(average(wrong[:,1],right[:,1]))
                    if a2b>a2:
                            g_b-=(2*coeff)
                            wrong[:,1]=wrong3[:,0]*g_r+wrong3[:,1]*g_g+wrong3[:,2]*(g_b)
                            a2b=abs(average(wrong[:,1],right[:,1]))
                            if a2b>a2:
                                    g_b+=coeff



                    ################################
                    #
                    #
                    #################################

                    wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
                    a3=abs(average(wrong[:,2],right[:,2]))
                    b_r+=coeff
                    wrong[:,2]=wrong3[:,0]*(b_r)+wrong3[:,1]*b_g+wrong3[:,2]*b_b
                    a3r=abs(average(wrong[:,2],right[:,2]))
                    if a3r>a3:
                            b_r-=(2*coeff)
                            wrong[:,2]=wrong3[:,0]*(b_r)+wrong3[:,1]*b_g+wrong3[:,2]*b_b
                            a3r=abs(average(wrong[:,2],right[:,2]))
                            if a3r>a3:
                                    b_r+=coeff

                    wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
                    a3=abs(average(wrong[:,2],right[:,2]))
                    b_g+=(coeff)
                    wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*(b_g)+wrong3[:,2]*b_b
                    a3g=abs(average(wrong[:,2],right[:,2]))
                    if a3g>a3:
                            b_g-=(2*coeff)
                            wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*(b_g)+wrong3[:,2]*b_b
                            a3g=abs(average(wrong[:,2],right[:,2]))
                            if a3g>a3:
                                b_g+=(coeff)

                    wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*b_b
                    a3=abs(average(wrong[:,2],right[:,2]))
                    b_b+=coeff
                    wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*(b_b)
                    a3b=abs(average(wrong[:,2],right[:,2]))
                    if a3b>a3:
                            b_b-=(2*coeff)
                            wrong[:,2]=wrong3[:,0]*b_r+wrong3[:,1]*b_g+wrong3[:,2]*(b_b)
                            a3b=abs(average(wrong[:,2],right[:,2]))
                            if a3b>a3:
                                    b_b+=coeff



                    

                    #print(a," its a")

            right=right_0
            wrong=wrong_0
            wrong[:,0]=wrong_0[:,0]*r_r+wrong_0[:,1]*r_g+wrong_0[:,2]*r_b
            wrong[:,1]=wrong_0[:,0]*g_r+wrong_0[:,1]*g_g+wrong_0[:,2]*g_b
            wrong[:,2]=wrong_0[:,0]*b_r+wrong_0[:,1]*b_g+wrong_0[:,2]*b_b
            wrong2 = Image.fromarray(io.convert_bit_depth(wrong.reshape(6,64,3),"uint8")).show()

            img_in[:,:,:,0]=img_in2[:,:,:,0]*r_r+img_in2[:,:,:,1]*r_g+img_in2[:,:,:,2]*r_b
            img_in[:,:,:,1]=img_in2[:,:,:,0]*g_r+img_in2[:,:,:,1]*g_g+img_in2[:,:,:,2]*g_b
            img_in[:,:,:,2]=img_in2[:,:,:,0]*b_r+img_in2[:,:,:,1]*b_g+img_in2[:,:,:,2]*b_b

            return img_in,wrong

    tempp=colcolo(lut_3d,wrong,right)
    lut_3d=tempp[0]
    #hald=tempp[0]
    wrong=tempp[1]

    acc=0
    if accuracy=="High":
            acc=22

    else:
            acc=35

    if film=="sRgb":
          acc=20
    
    #wrong=sRGB_to_XYZ(wrong)
    #right=sRGB_to_XYZ(right)
    #lut_3d=sRGB_to_XYZ(lut_3d)
    lut_3d=colour_correction(lut_3d,wrong,right,method='Cheung 2004', degree=4,root_polynomial_expansion=True,terms=acc)

    


    wrong=colour_correction(wrong,wrong,right,method='Cheung 2004', degree=4,root_polynomial_expansion=True,terms=acc)

    wrong[wrong<0]=0
    hald=colour_correction(lut_3d,wrong,right,method='Cheung 2004', degree=4,root_polynomial_expansion=True,terms=acc)
    #hald=XYZ_to_sRGB(hald)

    hald[hald<0]=0

    hald=np.array(hald,dtype=np.float32)
    
    #wrong[wrong>1]=1
    #wrong[wrong<0]=0

    hald=sRGB_to_XYZ(hald)
    hald=XYZ_to_ProLab(hald)


    return hald


def ProLab(after_lut,

            sut,


            end_a_plus,
            end_a_minus,
            end_b_plus,
            end_b_minus,


            a_min_sut,
            a_plus_sut,
            b_min_sut,
            b_plus_sut,


            

            a_m_hue,a_p_hue,b_m_hue,b_p_hue,sat_comp
                            ):
    # MAKE MASKS A/B CHAN
    """a_plus_mask=(np.array(2/(1+np.power(10**mask_compress,-after_lut[:,:,:,1])))-1)*100
    a_min_mask=(np.array(2/(1+np.power(10**mask_compress,-after_lut[:,:,:,1])))-1)*100
    b_plus_mask=(np.array(2/(1+np.power(10**mask_compress,-after_lut[:,:,:,2])))-1)*100
    b_min_mask=(np.array(2/(1+np.power(10**mask_compress,-after_lut[:,:,:,2])))-1)*100
    a_plus_mask[a_plus_mask<0]=0
    a_min_mask[a_min_mask>0]=0
    b_plus_mask[b_plus_mask<0]=0
    b_min_mask[b_min_mask>0]=0"""
    print(np.min(after_lut),"is it nan?")
    
    #     ProLab PARAMS
    after_lut[:,:,:,1]=(after_lut[:,:,:,1]*sut*4)
    after_lut[:,:,:,2]=(after_lut[:,:,:,2]*sut*4)

    after_lut[:,:,:,1][after_lut[:,:,:,1]<0]=after_lut[:,:,:,1][after_lut[:,:,:,1]<0]*a_min_sut
    after_lut[:,:,:,1][after_lut[:,:,:,1]<0]=((2/(1+(np.power((16**(end_a_minus*sat_comp)),-(((after_lut[:,:,:,1][after_lut[:,:,:,1]<0])))/100))))-1)*(31/(end_a_minus*sat_comp))#*mask[:,:,1][np.where(after_lut[:,:,:,1]<0)]     #a+ ибо обратились к 2 каналу где этот канал больше нуля

    #after_lut[:,:,:,0]+=a_min_L*(-a_min_mask/(mask_compress*100))

    after_lut[:,:,:,1][after_lut[:,:,:,1]>=0]=after_lut[:,:,:,1][after_lut[:,:,:,1]>=0]*a_plus_sut
    after_lut[:,:,:,1][after_lut[:,:,:,1]>=0]=((2/(1+(np.power((16**(end_a_plus*sat_comp)),-((after_lut[:,:,:,1][after_lut[:,:,:,1]>=0]))/100))))-1)*(31/(end_a_plus*sat_comp))#*mask[:,:,1][np.where(after_lut[:,:,:,1]>=0)]

    #after_lut[:,:,:,0]+=a_plus_L*a_plus_mask/(mask_compress*100)

    after_lut[:,:,:,2][after_lut[:,:,:,2]<0]=after_lut[:,:,:,2][after_lut[:,:,:,2]<0]*b_min_sut
    after_lut[:,:,:,2][after_lut[:,:,:,2]<0]=((2/(1+(np.power((16**(end_b_minus*sat_comp)),-((after_lut[:,:,:,2][after_lut[:,:,:,2]<0]))/100))))-1)*(31/(end_b_minus*sat_comp))#*mask[:,:,2][np.where(after_lut[:,:,:,2]<0)]

    #after_lut[:,:,:,0]+=b_min_mask*(-b_min_L)/(mask_compress*100)

    after_lut[:,:,:,2][after_lut[:,:,:,2]>=0]=after_lut[:,:,:,2][after_lut[:,:,:,2]>=0]*b_plus_sut
    after_lut[:,:,:,2][after_lut[:,:,:,2]>=0]=((2/(1+(np.power((16**(end_b_plus*sat_comp)),-((after_lut[:,:,:,2][after_lut[:,:,:,2]>=0]))/100))))-1)*(31/(end_b_plus*sat_comp))#*mask[:,:,2][np.where(after_lut[:,:,:,2]>=0)]                 #((2/1+16**yx)-1)*100/y'''

    #after_lut[:,:,:,0]+=b_plus_L*b_plus_mask/(mask_compress*100)
    
    #HUE MiX
    a_min=np.array(after_lut[:,:,:,1])
    a_plus=np.array(after_lut[:,:,:,1])
    b_min=np.array(after_lut[:,:,:,2])
    b_plus=np.array(after_lut[:,:,:,2])

    a_min=a_min*(1-a_m_hue)+after_lut[:,:,:,2]*a_m_hue
    a_plus=a_plus*(1-a_p_hue)+after_lut[:,:,:,2]*a_p_hue
    b_min=b_min*(1-b_m_hue)+after_lut[:,:,:,1]*b_m_hue
    b_plus=b_plus*(1-b_p_hue)+after_lut[:,:,:,1]*b_p_hue

    a_min[a_min>0]=0
    a_plus[a_plus<0]=0
    b_min[b_min>0]=0
    b_plus[b_plus<0]=0

    a=a_min+a_plus
    b=b_min+b_plus

    after_lut[:,:,:,1]=a
    after_lut[:,:,:,2]=b
    after_lut=np.nan_to_num(after_lut)
    
    return after_lut

def wheels(after_lut,
            steepness_shad,width_shad,
            steepness_light,width_light,
            shad_a,shad_b,mid_a,mid_b,light_a,light_b,
            neutral_mask,amplyfy_wheel
            ):

    #     MASK FOR WHEELS
    wheel_sut_mask=np.fabs(np.array(after_lut[:,:,:,1]+after_lut[:,:,:,2]))
    wheel_sut_mask/=np.max(wheel_sut_mask)
    wheel_sut_mask=np.stack((wheel_sut_mask,wheel_sut_mask,wheel_sut_mask),axis=-1)


    shad_mask=np.array(after_lut[:,:,:,0])/100
    mid_mask=np.array(after_lut[:,:,:,0])/100
    mid_mask=(mid_mask*0)+1
    light_mask=np.array(after_lut[:,:,:,0])/100
    def curve(img,steepness,width,apex):
        img=(2/(1+np.power(10**steepness,(-width-apex+img))))*(2/(1+np.power(10**steepness,(-width+apex-img))))
        return img

    shad_mask=curve(shad_mask,steepness_shad,width_shad,0.0)
    shad_mask*=(1/np.max(shad_mask))
    light_mask=curve(light_mask,steepness_light,width_light,1.)
    light_mask*=(1/np.max(light_mask))
    mid_mask=(mid_mask-shad_mask-light_mask)
    #mid_mask[mid_mask<0]=0
    shad_mask=np.stack((shad_mask,shad_mask,shad_mask),axis=-1)
    light_mask=np.stack((light_mask,light_mask,light_mask),axis=-1)
    mid_mask=np.stack((mid_mask,mid_mask,mid_mask),axis=-1)

    shad_mask=np.nan_to_num(shad_mask)
    light_mask=np.nan_to_num(light_mask)
    mid_mask=np.nan_to_num(mid_mask)




    #      WHEELS
    shad=np.array(after_lut)
    mid=np.array(after_lut)
    light=np.array(after_lut)

    shad[:,:,:,1]+=shad_a*(((1-neutral_mask)+1)**2)*amplyfy_wheel
    shad[:,:,:,2]+=shad_b*(((1-neutral_mask)+1)**2)*amplyfy_wheel
    mid[:,:,:,1]+=mid_a*(((1-neutral_mask)+1)**2)*amplyfy_wheel
    mid[:,:,:,2]+=mid_b*(((1-neutral_mask)+1)**2)*amplyfy_wheel
    light[:,:,:,1]+=light_a*(((1-neutral_mask)+1)**2)*amplyfy_wheel
    light[:,:,:,2]+=light_b*(((1-neutral_mask)+1)**2)*amplyfy_wheel

    shad*=shad_mask
    mid*=mid_mask
    light*=light_mask
    wheel_sut_mask=(wheel_sut_mask+10**(1-neutral_mask))/(10**(1-neutral_mask)+1)
    after_wheel=shad+mid+light
    after_wheel*=(1-wheel_sut_mask)
    after_lut*=wheel_sut_mask
    after_lut=after_lut+after_wheel



    return after_lut



def to_rgb(after_lut):
    to_XYZ=ProLab_to_XYZ(after_lut)
    to_XYZ[to_XYZ>1]=1
    to_XYZ[to_XYZ<0]=0
    after_lut=XYZ_to_sRGB(to_XYZ)

    #after_lut=(after_lut-0.2-Exp_shift/9)*3
    after_lut[after_lut>1]=1
    after_lut[after_lut<0]=0
    after_lut=np.array(after_lut,dtype=np.float32)
    
    return after_lut



def my_interpolation_trilinear(
    V_xyz,table):
    V_xyz = np.clip(V_xyz, 0, 1)

    V_xyz2 = np.reshape(V_xyz, (-1, 3))
    i_m = np.array(table.shape[0:-1],np.uint8) - 1
    i_f = np.floor(V_xyz2 * i_m)
    i_f = np.array(i_f,np.uint8)
    i_f = np.clip(i_f, 0, i_m)
    i_c = np.clip(i_f + 1, 0, i_m)
    i_f_c = i_f, i_c
    vertices = np.array(
        [
            table[
                i_f_c[i[0]][..., 0], i_f_c[i[1]][..., 1], i_f_c[i[2]][..., 2]
            ]
            for i in itertools.product(*zip([0, 0, 0], [1, 1, 1]))
        ]
    )


    # Relative to indexes ``V_xyz`` values.
    V_xyzr = i_m * V_xyz2 - i_f


    vertices = np.moveaxis(vertices, 0, 1)

    x, y, z = (f[:, None] for f in np.transpose(V_xyzr,np.concatenate([[V_xyzr.ndim - 1], np.arange(0, V_xyzr.ndim - 1)]),))
    weights = np.moveaxis(
        np.transpose(
            [
                (1 - x) * (1 - y) * (1 - z),
                (1 - x) * (1 - y) * z,
                (1 - x) * y * (1 - z),
                (1 - x) * y * z,
                x * (1 - y) * (1 - z),
                x * (1 - y) * z,
                x * y * (1 - z),
                x * y * z,
            ]
        ),
        0,
        -1,
    )

    xyz_o = np.reshape(np.sum(vertices * weights, 1), V_xyz.shape)
    return xyz_o



def log(iimg,gamma) -> np.array:

    rgb_autoscale=(iimg*((13*(10**gamma))/np.average(iimg)))

    rgb_autoscale+=(200-np.min(rgb_autoscale)) #(np.log(gamma+2.7)-1)

    rgblog=(np.log10(rgb_autoscale))
    rgblog=(((rgblog-np.min(rgblog))/(np.max(rgblog)-np.min(rgblog))))

    #in_img=(((rgblog-2.3)/(np.max(rgblog)-2.3)))
    return rgblog



def film_em(in_img,Wb_b,Wb_r,print_cont,print_exp,Lut,gamma,light_compr,Wb_r2,Wb_b2,zone) -> np.array:
    '''                                 WB               '''


    qwert=time.perf_counter()
    in_img=(((in_img-np.min(in_img))/(np.max(in_img)-np.min(in_img))))
    #in_img=np.nan_to_num(in_img)
    in_img[:,:,0]-=Wb_b/90
    in_img[:,:,1]-=((Wb_b/90)+(Wb_r/90))
    in_img[:,:,2]-=Wb_r/90

    
     #table=

    #in_img=colmap(in_img,Lut)
    in_img=(in_img-0.82)+(print_exp/9)


    in_img+=((gamma-3.1)/18)
    in_img[in_img<-0.6]=-0.6
    gamma=np.sqrt(np.sqrt(gamma))

    '''                         CONTRAST                    '''
    in_img-=zone
    in_img[in_img>0]=(((light_compr)/(-in_img[in_img>0]-(light_compr)))+1)*(light_compr)
    in_img+=zone

    #img_contrast=1/(1+(np.power(55,(-in_img))))
    img_contrast=1/(1+(np.power((10**(gamma*print_cont*3)),(-in_img))))
 

    #img_contrast+=0.16
    #img_contrast-=np.min(img_contrast)
    #img_contrast*=(1/np.max(img_contrast))

    img_contrast=my_interpolation_trilinear(img_contrast,table=Lut)
    print(img_contrast.dtype, "")
    #img_contrast-=((gamma-3.1)/24)
    img_contrast[:,:,0]-=((Wb_b2/90)+(Wb_r2/90))
    img_contrast[:,:,1]-=Wb_b2/90
    img_contrast[:,:,2]-=Wb_r2/90

    img_contrast[img_contrast<0]=0
    qwerty=time.perf_counter()
    print(f"Вычисление заняло {qwerty - qwert:0.4f} секунд")   

    return img_contrast




def grain(image,grain_curve,prep_grain,amplify,amplify_mask) -> np.array:

    Mask_gr=grain_curve.apply(image)
    grain=((prep_grain*amplify*(Mask_gr**amplify_mask)))/(amplify_mask**1.5)+1
    grain=np.array(grain,dtype=np.float32)
    grained=image*grain
    grained[grained>=1]=1
    grained[grained<=0]=0
    #grained=(grained+np.fabs(np.min(grained)))*(1/np.max(grained+np.fabs(np.min(grained))))
    return grained

#p_image=grain(p_image,gr_curve,prep_grain,0.15,6)

def show(image):
    image=io.convert_bit_depth(image,'uint8')
    return image

def plot_zone(
            width_shad,
            steepness_shad,

            width_light,
            steepness_light,):
    def curve(img,steepness,width,apex):
        img=(2/(1+np.power(10**steepness,(-width-apex+img))))*(2/(1+np.power(10**steepness,(-width+apex-img))))
        return img
    plot_shad=np.linspace(0,1,100)
    plot_mid=np.linspace(0,1,100)
    plot_mid=(plot_mid*0)+1
    plot_light=np.linspace(0,1,100)

    shad=curve(plot_shad,steepness_shad,width_shad,0)
    shad*=(1/np.max(shad))
    light=curve(plot_light,steepness_light,width_light,1)
    light*=(1/np.max(light))
    mid=(plot_mid-shad-light)
    mid[mid<0]=0

    all={"Shadow": shad,"Mid":mid,"Hilight":light}

    return all

def crop(img,rotate,rotate_thin,crop_sl,y_shift,x_shift,aspect):
    img=ndimage.rotate(img,rotate )
    img=ndimage.rotate(img, rotate_thin)


    shape=np.shape(img)
    coef=float(np.max(shape)/1400)
    """    crop_sl*=(coef/300)

    y_shift*=crop_sl*10
    x_shift*=crop_sl*10"""
    y=int(shape[0])

    y_2=shape[0]-y
    x=int(shape[1])
    x_2=shape[1]-x
    img=img[(y_2+int(y_shift)):(y+int(y_shift)),(x_2+int(x_shift)):(x+int(x_shift)),:]


    shape_2=(np.shape(img))
    print(aspect)
    if aspect!=[3, 2]:
        if shape_2[0]<shape_2[1]:
            z=aspect[0]/aspect[1]
            x_3=int(shape_2[0]*z)-3*coef
            sup=(shape_2[1]-x_3)/2
            img=img[:,int(sup):int(x_3+sup),:]

        else:
            z=aspect[0]/aspect[1]

            x_3=(shape_2[1]*z)-3*coef
            sup=(shape_2[0]-x_3)/2
            img=img[int(sup):int(x_3+sup),:,:]


    return img



def done1():
    print("done1")
#show(p_image)



'''    qwert=time.perf_counter()
    qwerty=time.perf_counter()
    print(f"Вычисление заняло {qwerty - qwert:0.4f} секунд")'''

'''def my_interpolation_trilinear(
    V_xyz,table):
    V_xyz = np.clip(V_xyz, 0, 1)

    V_xyz2 = np.reshape(V_xyz, (-1, 3))
    i_m = np.array(table.shape[0:-1],np.uint8) - 1
    i_f = np.floor(V_xyz2 * i_m)
    i_f = np.array(i_f,np.uint8)
    i_f = np.clip(i_f, 0, i_m)
    i_c = np.clip(i_f + 1, 0, i_m)
    i_f_c = i_f, i_c
    vertices = np.array(
        [
            table[
                i_f_c[i[0]][..., 0], i_f_c[i[1]][..., 1], i_f_c[i[2]][..., 2]
            ]
            for i in itertools.product(*zip([0, 0, 0], [1, 1, 1]))
        ]
    )


    # Relative to indexes ``V_xyz`` values.
    V_xyzr = i_m * V_xyz2 - i_f


    vertices = np.moveaxis(vertices, 0, 1)

    x, y, z = (f[:, None] for f in np.transpose(V_xyzr,np.concatenate([[V_xyzr.ndim - 1], np.arange(0, V_xyzr.ndim - 1)]),))
    weights = np.moveaxis(
        np.transpose(
            [
                (1 - x) * (1 - y) * (1 - z),
                (1 - x) * (1 - y) * z,
                (1 - x) * y * (1 - z),
                (1 - x) * y * z,
                x * (1 - y) * (1 - z),
                x * (1 - y) * z,
                x * y * (1 - z),
                x * y * z,
            ]
        ),
        0,
        -1,
    )

    xyz_o = np.reshape(np.sum(vertices * weights, 1), V_xyz.shape)
    return xyz_o
'''
'''
()
@jit(nopython=True)
def colmap(img,lut) -> np.array:
    shape=img.shape
    size=lut.shape[0]-1.1
    img=np.reshape(img,((img.shape[0]*img.shape[1]),3))
    img = np.clip(img, 0, 1)
    img*=size
    img_i=img%1
    img_c=np.trunc(img)
    img_c=img_c.astype(np.uint8)
    for i in range(img.shape[0]):
        coef=lut[img_c[i,0]+1,img_c[i,1]+1,img_c[i,2]+1]-lut[img_c[i,0],img_c[i,1],img_c[i,2]]
        #coef=np.array(lut[(int(img_c[i,0])+1),(int(img_c[i,1])+1),(int(img_c[i,2])+1)])-(lut[img_c[i,0],img_c[i,1],img_c[i,2]])

        #print(lut[img_c[i,0],img_c[i,1],img_c[i,2]])
        #coef*=10

        pers=np.array([img_i[i,0],img_i[i,1],img_i[i,2]])
        #print(pers)
        coef=pers*coef
        #print(coef)
        img[i]=lut[img_c[i,0],img_c[i,1],img_c[i,2]]
        img[i]+=coef
    img=np.reshape(img,shape)
    return img'''


'''
def film_pill(iimg,Wb_b,Wb_r,print_cont,print_exp,Lut,gamma):
    rgb_autoscale=(iimg*(((np.log(gamma+2.7)-1)*10000)/np.average(iimg)))+200
    rgblog=(np.log10(rgb_autoscale))
    in_img=(((rgblog-2.3)/(np.max(rgblog)-2.3)))


                                     WB
    in_img[:,:,0]-=Wb_b/90
    in_img[:,:,1]-=((Wb_b/90)+(Wb_r/90))
    in_img[:,:,2]-=Wb_r/90

    in_img=((in_img-np.average(in_img)))+0.4
    qwert=time.perf_counter()
    in_img=my_interpolation_trilinear(in_img,Lut)
    in_img=(in_img-np.average(in_img))+(print_exp/9)
    print(in_img.dtype)
    qwerty=time.perf_counter()
    print(f"Вычисление заняло {qwerty - qwert:0.4f} секунд")

    print_cont*=gamma*100
    print_cont=10**print_cont


                             CONTRAST

    img_contrast=1/(1+(np.power((print_cont),(2*(-in_img)))))


    return img_contrast'''
