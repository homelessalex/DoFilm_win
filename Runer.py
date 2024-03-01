
import os
from multiprocessing import active_children
import sys
from cash import q_in_zoom, q_out_zoom, q_in_blur, q_out_blur , q_in_lut, q_out_lut, q_in_film , q_out_film 
import cash
import time


os.system("source venv/bin/activate\n python3.10 flet_app.py")

if cash.close==True:

                    os._exit()