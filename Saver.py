from tkinter.filedialog import askopenfilename,askdirectory
import pathlib
import rawpy
from PIL import Image
import numpy as np
import pickle as pkl
import copy
import tkinter as tk 
import tkinter.ttk as ttk 
import os
import pickle
import time
from Do_film import raw2,zoom,pre_grain,reduse_sharpness,film_em,grain,show,bloom,sharpen,log,plot_zone,rgb_mix,apply_film,ProLab,wheels,to_rgb,crop,add_corners
import cash
from colour import io
params=pickle.load(open("params.pkl",'rb'))
Gr_sample = cash.Gr_sample
Grain_curve = cash.Grain_curve

cameras = cash.cameras
Films = cash.Films
names=pickle.load(open("names.pkl",'rb'))
save_params=pickle.load(open("save_params.pkl",'rb'))

print(names)

master = tk.Tk()
master.geometry("900x50")
master.title("Progress Bar")
progress_bar = ttk.Progressbar(master, orient="horizontal", mode="determinate", maximum=100, value=0)
progress_bar.place(relx=0.5, rely=0.5,anchor="c", relwidth=0.9, relheight=1) 



master.update()

filepath = askdirectory()
path = pathlib.Path(filepath)




def magic(path,name,wight_balance, rotate, rotate_thin, crop_sl, y_shift, x_shift, aspect, blur_rad, halation, blur_spred, bloom_rad, bloom_Halation, bloom_spred, r_hue, r_sut, r_g, r_b, g_hue, g_sut, g_r, g_b, b_hue, b_sut, b_r, b_g, camera, film, accuracy, sut, END_A_PLUS, END_A_MINUS, END_B_PLUS, END_B_MINUS, a_min_sut, a_plus_sut, b_min_sut, b_plus_sut, a_m_hue, a_p_hue, b_m_hue, b_p_hue, sut_compress, steepness_shad, width_shad, steepness_light, width_light, shad_a, shad_b, mid_a, mid_b, light_a, light_b, neutral_mask, amply_wheel, gamma, sharp_rad, sharp_spred, sharp_amplif, WB_b, WB_r, print_cont, print_exp, light_compr, WB_r2, WB_b2, zone, AMPLIFY_GRAIN, AMPLIFY_GRAIN_MASK):

        
        wrong=cameras[camera]
        right=Films[film]

        img=raw2(path,wight_balance)

        img=zoom(img,save_params["resolution"])

        img=crop(img,rotate,rotate_thin,crop_sl,y_shift,x_shift,aspect)

        img=add_corners(img)
        prep_grain=pre_grain(img,Gr_sample)

        img=reduse_sharpness(img, blur_rad, halation, blur_spred)

        img=bloom(img,bloom_rad,bloom_Halation,bloom_spred)

        p_lut=rgb_mix( r_hue,r_sut,r_g,r_b,g_hue,g_sut,g_r,g_b,b_hue,b_sut,b_r,b_g)

        p_lut=apply_film(p_lut,wrong,right,accuracy,film)

        p_lut=ProLab(p_lut,sut,END_A_PLUS,END_A_MINUS,END_B_PLUS,END_B_MINUS,a_min_sut,a_plus_sut,b_min_sut,b_plus_sut
                ,a_m_hue,a_p_hue,b_m_hue,b_p_hue,sut_compress)

        p_lut=wheels(p_lut,steepness_shad,width_shad,steepness_light,width_light,shad_a,shad_b,mid_a,mid_b,light_a,light_b,neutral_mask,amply_wheel)

        p_lut=to_rgb(p_lut)

        p_image=log(img,gamma)

        p_image=sharpen(p_image,sharp_rad,sharp_spred,sharp_amplif)

        p_image=film_em(p_image,WB_b,WB_r,print_cont,print_exp,p_lut,gamma,light_compr,WB_r2,WB_b2,zone)
        start = time.time()
        p_image=grain(p_image,Grain_curve,prep_grain,AMPLIFY_GRAIN,AMPLIFY_GRAIN_MASK)
        end = time.time()  
        return p_image

itteration=0
for i in names:
        
        param=params[names[i][2]]
        print(names[str(param['name'])][1])
        if names[str(param['name'])][1]==False:
                continue

        img=magic(param['path'],          param['name'],           param['wight_balance'],
                  param['rotate'],        param['rotate_thin'],    param['crop_sl'],
                  param['y_shift'],       param['x_shift'],        param['aspect'],
                  param['blur_rad'],      param['halation'],       param['blur_spred'],
                  param['bloom_rad'],     param['bloom_Halation'], param['bloom_spred'],
                  param['r_hue'],         param['r_sut'],          param['r_g'],                 param['r_b'],
                  param['g_hue'],         param['g_sut'],          param['g_r'],                 param['g_b'],
                  param['b_hue'],         param['b_sut'],          param['b_r'],                 param['b_g'],
                  param['camera'],        param['film'],           param['accuracy'],            param['sut'],
                  param['END_A_PLUS'],    param['END_A_MINUS'],    param['END_B_PLUS'],
                  param['END_B_MINUS'],   param['a_min_sut'],      param['a_plus_sut'],
                  param['b_min_sut'],     param['b_plus_sut'],     param['a_m_hue'],
                  param['a_p_hue'],       param['b_m_hue'],        param['b_p_hue'],             param['sut_compress'],
                  param['steepness_shad'],param['width_shad'],     param['steepness_light'],
                  param['width_light'],   param['shad_a'],         param['shad_b'],              param['mid_a'],
                  param['mid_b'],         param['light_a'],        param['light_b'],             param['neutral_mask'],
                  param['amply_wheel'],   param['gamma'],          param['sharp_rad'],           param['sharp_spred'],
                  param['sharp_amplif'],  param['WB_b'],           param['WB_r'],                param['print_cont'],         
                  param['print_exp'],
                  param['light_compr'],   param['WB_r2'],          param['WB_b2'],               param['zone'],
                  param['AMPLIFY_GRAIN'], param['AMPLIFY_GRAIN_MASK'])
        
        if save_params["type"]==".tiff":        
            io.write_image(io.convert_bit_depth(img,"uint16"),str(filepath)+"/"+str(param["name"])+".tiff", "uint16" )
        elif save_params["type"]==".jpeg":
                pill=Image.fromarray(io.convert_bit_depth(img,"uint8"))
                for_icc = Image.open("IMG_4799.jpg")
                icc = for_icc.info.get('icc_profile')
                pill.save(str(filepath)+"/"+str(param["name"])+".jpeg", format="JPEG", quality=95, icc_profile=icc)
                print(pill,"jpeg saved")
        itteration+=1
        progress_bar['value'] = ((itteration/len(names.keys()))*100)
        master.update()

exit()