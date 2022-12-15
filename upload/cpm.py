import csv
import glob
import os
import pandas as pd
import time
import numpy as np

PATH = "/var/www/html/spkproyeksiumkt/upload/"
os.chdir(PATH)

df = pd.read_csv('data.xlsx', engine='python')
sheet = pd.read_excel(df, sheet_name='Sheet1')
