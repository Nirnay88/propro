from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import auth
import pyrebase
import pandas as pd 
import numpy as np
import datetime as dt
import math
from statistics import mean
from sklearn.cluster import AgglomerativeClustering

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from read_new import *

emailer = None 
passw = None
df = pd.read_csv("my.csv", header = None)
pract_df = pd.read_csv("TE COMP 1 1 SU PR.csv", header = None)



#Authentication and SignIn Part :

def index(request):
   return render(request, "selector.html")

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def alreadySigned(request):
    return render(request,'login.html')

def forget(request):
    return render(request,'forget.html')



#Calculating overall performance of a specified RollNo

def validate(request):
    
    roll = int(request.POST['rn'])
    users_ref = db.collection('students')
    myq = "student_rollno"
    aa = "=="
    roller = str(roll)
    data = next(users_ref.where(myq,aa,roller).get()).to_dict()

    subject_attendance = []
    
    cn_tot = calc_overall_attendance_subject(div='TE-1', subject='CN', start_roll='305001', end_roll='305013')
    subject_attendance.append(cn_tot[roller])

    dbms_tot = calc_overall_attendance_subject(div='TE-1', subject='DBMS', start_roll='305001', end_roll='305013')
    subject_attendance.append(dbms_tot[roller])

    toc_tot = calc_overall_attendance_subject(div='TE-1', subject='TOC', start_roll='305001', end_roll='305013')
    subject_attendance.append(toc_tot[roller])

    sepm_tot = calc_overall_attendance_subject(div='TE-1', subject='ISEE', start_roll='305001', end_roll='305013')
    subject_attendance.append(sepm_tot[roller])

    isee_tot = calc_overall_attendance_subject(div='TE-1', subject='SEPM', start_roll='305001', end_roll='305013')
    subject_attendance.append(isee_tot[roller])

    sdl_tot = calc_overall_attendance_subject(div='TE-1', subject='SDL', start_roll='305001', end_roll='305013')
    subject_attendance.append(sdl_tot[roller])


    ov_th = round((sum(subject_attendance)/6),2)

    prn = data['student_prn']
    name = data['student_name']
    division = data['student_year']

    subject_attendance_practical = []
    

    sdl = calc_overall_attendance_subject(div='TE-1', subject='SD LAB', start_roll='305001', end_roll='305013',type='Practical')
    subject_attendance_practical.append(sdl[roller])

    dbl = calc_overall_attendance_subject(div='TE-1', subject='DB LAB', start_roll='305001', end_roll='305013',type='Practical')
    subject_attendance_practical.append(dbl[roller])

    cnl = calc_overall_attendance_subject(div='TE-1', subject='CN LAB', start_roll='305001', end_roll='305013',type='Practical')
    subject_attendance_practical.append(cnl[roller])
    
    ov_pr = round((sum(subject_attendance_practical)/3),2)    
    ov_att = (ov_th+ov_pr)/2
    subjects = ['CN','DBMS','TOC','SEPM','ISEE','SDL']
      
    cn_attended =1
    dbms_attended =2
    toc_attended = 1
    sepm_attended =1 
    isee_attended =1 
    sdl_attended =1

    cn_absent = 2
    dbms_absent = 2
    toc_absent = 2
    sepm_absent =2
    isee_absent =2
    sdl_absent = 2


    return render(request, "Index.html",{'subject_attendance':subject_attendance , 'subjects':subjects, 'prn':prn, 'name':name, 'roll':roll, 'division':division, 'email':emailer, 'tot_attendance':ov_att,'subject_attendance_practical':subject_attendance_practical , 'cn':cn_attended, 'dbms':dbms_attended, 'toc':toc_attended, 'sepm':sepm_attended, 'isee':isee_attended, 'sdl':sdl_attended, 'cn1':cn_absent, 'dbms1':dbms_absent, 'toc1':toc_absent, 'sepm1':sepm_absent, 'isee1':isee_absent, 'sdl1':sdl_absent })
  





def about(request):
    return render(request, 'aboutus.html' )


# Caculating customized Defaulter list 
def defaulter(request):
    return render(request, 'defaulter.html')




def calculate_def(request):
    
    defaulter_value = request.POST['min_att'] 
    count = 0            
    temp = []
    ov_all = (calc_overall_attendance(type='Lecture',div='TE-1',start_roll='305001', end_roll='305013'))

    def_roll_list = []
    def_att_list = []
    for i in ov_all:
      if ov_all[i] <= 20:
        def_roll_list.append(i)
        def_att_list.append(ov_all[i])

    def_name_list = []

    for i in def_roll_list:
      count = count + 1
      users_ref = db.collection('students')
      data = next(users_ref.where('student_rollno','==',i).get()).to_dict()
      def_name_list.append(data['student_name'])


    for i, j, k in zip(def_roll_list,def_name_list,def_att_list):
        temp.append([i,j,k])

    return render(request, 'defaulter.html', { 'rolls':temp , 'count':count ,'val':defaulter_value})
    





#Calculating overall performance of a class for Admin/HOD

def calculateAdmin(request):

    cn_th_att = round(mean(df[6]),2)
    dbms_th_att = round(mean(df[8]),2)
    toc_th_att = round(mean(df[10]),2)
    sepm_th_att = round(mean(df[12]),2)
    isee_th_att = round(mean(df[14]),2)
    sdl_th_att = round(mean(df[16]),2)

    sdl_pr_att = round(mean(pract_df[6]),2)
    dbms_pr_att = round(mean(pract_df[8]),2)
    cn_pr_att = round(mean(pract_df[10]),2)

    tot = [cn_th_att,dbms_th_att,toc_th_att,sepm_th_att ,isee_th_att,sdl_th_att]   
    tot_p = [sdl_pr_att,dbms_pr_att,cn_pr_att]
    tot_theorey = []
    for i in range(6,16,2):
        tot_theorey.append(round(mean(df[i]),2)) 
    tot_prac = []
    for i in range(6,10 ,2):
        tot_prac.append(round(mean(pract_df[i]),2))    
    
    theory_total = round(mean(df[18]),2)
    practical_total = round(mean(pract_df[12]),2)


    total_individual_attendance = round((theory_total + practical_total)/2 , 2)



    #calling ML k-means Clustering
    new = get_result_analysis('SE COMP 1 1 SU TH.csv', 'SE COMP 1 1 RE.csv')
    
    return render(request, 'Hodindex.html' ,{'total':tot,  'prac':tot_p, 'tot_attendance':total_individual_attendance, 'new':new })






def callIndex(request):
    return render(request, "Index.html", {'email': emailer})

def callIndex_admin(request):
    return render(request, "Hodindex.html", {'email': emailer})


def callIndexDefault(request):
    return render(request, "other.html", {'email': emailer})










#calculating ranged attendance of a specific rollno

def callRanged(request):
    return render(request, "Index1.html")

def calculate_ranged(request):
    roll = request.POST['rn']
    from_date = request.POST['from_date']
    to_date = request.POST['to_date']   


    users_ref = db.collection('students')
    myq = "student_rollno"
    aa = "=="
    roller = str(roll)
    data = next(users_ref.where(myq,aa,roller).get()).to_dict()

    subject_attendance = []
    
    cn_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='CN', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(cn_tot[roller])

    dbms_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='DBMS', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(dbms_tot[roller])

    toc_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='TOC', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(toc_tot[roller])

    sepm_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='ISEE', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(sepm_tot[roller])

    isee_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='SEPM', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(isee_tot[roller])

    sdl_tot = calc_overall_attendance_subject_ranged(div='TE-1', subject='SDL', start_roll='305001', end_roll='305013',start_date=from_date,end_date=to_date)
    subject_attendance.append(sdl_tot[roller])


    ov_th = round((sum(subject_attendance)/6),2)

    prn = data['student_prn']
    name = data['student_name']
    division = data['student_year']

    subject_attendance_practical = []
    

    sdl = calc_overall_attendance_subject(div='TE-1', subject='SD LAB', start_roll='305001', end_roll='305013',type='Practical',start_date=from_date,end_date=to_date)
    subject_attendance_practical.append(sdl[roller])

    dbl = calc_overall_attendance_subject(div='TE-1', subject='DB LAB', start_roll='305001', end_roll='305013',type='Practical',start_date=from_date,end_date=to_date)
    subject_attendance_practical.append(dbl[roller])

    cnl = calc_overall_attendance_subject(div='TE-1', subject='CN LAB', start_roll='305001', end_roll='305013',type='Practical',start_date=from_date,end_date=to_date)
    subject_attendance_practical.append(cnl[roller])
    
    ov_pr = round((sum(subject_attendance_practical)/3),2)    
    ov_att = (ov_th+ov_pr)/2
    


    return render(request, "Index1.html", {'present':ov_att, 'total':(100-ov_att), 'roll':roll , 'name':name , 'prn':prn , 'division':division, 'fd':from_date, 'td':to_date})




#Maybe ML k-Means clustering

def get_result_analysis(attendance_summary_filename, result_file_name):
    
    #DATA INPUT
    attendance_df = pd.read_csv(attendance_summary_filename, header = None)
    result_df = pd.read_csv(result_file_name, header = None) # SGPA of students
    bounds = attendance_df.shape
    data = np.zeros((bounds[0], 2))
    num_students = 0
    
    # DATA CLEANING
    for i in range(bounds[0]): # normalized data @ 100:100
        data[i][0] = attendance_df[bounds[1] - 1][i]
        prn = attendance_df[1][i]
        try:
            data[i][1] = result_df[result_df[0] == prn][1] * 10
            num_students += 1
        except:
            np.delete(data, i, axis=0)
            print('get_result_analysis : PRN %s not found in Results !' % prn)
        
    # DATA ANALYSIS
    cluster_ids = AgglomerativeClustering(n_clusters = 4, affinity = 'euclidean', linkage = 'ward').fit_predict(data)
    print(cluster_ids)
    colors = ['red', 'green', 'yellow', 'blue']
    out = [[] for i in range(num_students)]
    for i in range(num_students):
       out[i].append(data[i][0])
       out[i].append(data[i][1] / 10)
       out[i].append(attendance_df[4][i])
       out[i].append(colors[cluster_ids[i]])
       
    return out
