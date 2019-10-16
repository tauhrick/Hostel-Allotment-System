from selenium import webdriver
import pandas as pd
import numpy as np
import seaborn as sns
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

def extract():
    url = "https://github.com/srbcheema1/Nith_results/blob/master/result/text/Cse/batch_17_cgpi.txt"
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    fin = "LC"
    cnt = 0;
    dict = {}
    for i in range(94):
        Roll_no = (soup.select_one("#"+fin+str(cnt+1))).text.strip()
        Roll_no = Roll_no[Roll_no.find(" ")+1:]
        name = (soup.select_one("#"+fin+str(cnt+2))).text.strip()
        name = name[:name.find("S/D")].strip()
        gpa = (soup.select_one("#"+fin+str(cnt+5))).text.strip()
        cnt = cnt + 6
        dict[Roll_no] = {"Name": name, "CGPA": gpa}
    print(dict)
    return dict

extract()
