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

import nexmo
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
#from read_new import *



cred = credentials.Certificate('./dep.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


#To get the timestamp
gettimestamp = lambda datestr : datetime.strptime(datestr, '%d-%m-%Y').timestamp()




emailer = None 
passw = None
df = pd.read_csv("my.csv", header = None)
pract_df = pd.read_csv("TE COMP 1 1 SU PR.csv", header = None)



def postsignUp(request):

    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    user = authe.create_user_with_email_and_password(email,passw)
    uid = user['localId']
    data = {"name":name , "status":"1"}
    database.child("users").child(uid).child("details").set(data)

    if email == "hod@gmail.com":
      return render(request, "Hodindex.html", {'email': email})
   
    elif email != "hod@gmail.com": 
        return render(request, "login.html", {'email': email})


#Authentication and SignIn Part :

def index(request):
   return render(request, "login.html")

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def alreadySigned(request):
    return render(request,'login.html')

def forget(request):
    return render(request,'forget.html')



#Calculating overall performance of a specified RollNo


def postsign(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    
    global emailer 
    emailer = email
    
    if email == "nirnay@gmail.com" and passw=="nirnay":
      return render(request, "selector.html", {'email': email})
    else:
      return render(request,"login.html")



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

def mycallIndex(request):
    return render(request, "myIndex.html", {'email': emailer})

def callIndex_admin(request):
    return render(request, "Hodindex.html", {'email': emailer})


def callIndexDefault(request):
    return render(request, "other.html", {'email': emailer})



def caller(request):
  phone=request.POST['pn']
  message=request.POST['msg']

  client = nexmo.Client(
  application_id='108df5ac-d953-4b65-bdb7-57d6216fefb5',
  private_key='./pri.key',)
  ncco = [
  {
    'action': 'talk',
    'voiceName': 'Aditi',
    'text': str(message)
  }
  ]
  response = client.create_call({
    'to': [{
      'type': 'phone',
      'number': '911234567890',
      'number': '91'+str(phone)
    }],
    'from': {
      'type': 'phone',
      'number': '1123456788'
  },
  'ncco': ncco
  })  



  return render(request, "myIndex1.html",)






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
































def calc_overall_attendance_student(**kwargs):
  student_roll = kwargs['rollno']
  try:
    type_of_lec = kwargs['type']
  except:
    type_of_lec = 'Lecture'
  pr_cnt = 0
  if student_roll[0:2] == '20':
    year = 'SE'
  elif student_roll[0:2] == '30':
    year = 'TE'
  elif student_roll[0:2] == '40':
    year = 'BE'
  if student_roll[2:4] == '50':
    div = '1'
  elif student_roll[2:4] == '51':
    div = '2'
  elif student_roll[2:4] == '52':
    div = '3'
  tot_cnt_coll_name = year + '-' + div 
  x = next(db.collection(u'stats').where(u'year', u'==', tot_cnt_coll_name).get()).to_dict()
  if type_of_lec == 'Lecture':
    tot_cnt = int(x['lecture_count'])
  else:
    tot_cnt = int(x['practical_count'])
  att_coll = db.collection(u'attendance')
  for doc in docs:
    data = doc.to_dict()
    if type_of_lec == data['attendance_type']:
      if student_roll in data['present_students']:
        pr_cnt += 1
  return (pr_cnt, tot_cnt)




#type,start_roll,end_roll,div,
def calc_overall_attendance(**kwargs):
  pr_cnt = 0
  try:
    type_of_lec = kwargs['type']
  except:
    type_of_lec = 'Lecture'
  start_roll = kwargs['start_roll']
  end_roll = kwargs['end_roll']
  div = kwargs['div']
  student_coll = db.collection(u'students')
  x = next(db.collection(u'stats').where(u'year', u'==', div).get()).to_dict()
  if type_of_lec == 'Lecture':
    tot_cnt = int(x['lecture_count'])
  else:
    tot_cnt = int(x['practical_count'])
  overall_att = {}
  for roll in range(int(start_roll), int(end_roll) + 1):
    overall_att[str(roll)] = 0
  docs = db.collection(u'attendance').where(u'class', u'==', div).get()
  for doc in docs:
    data = doc.to_dict()
    if type_of_lec == data['attendance_type']:
      for roll in overall_att.keys():
        if roll in data['present_students']:
          overall_att[roll] += 1
  for roll in overall_att.keys():
    overall_att[roll] = round(overall_att[roll] / tot_cnt * 100, 2)
  return overall_att




#type,start_roll,end_roll,div,subject
def calc_overall_attendance_subject(**kwargs):
  pr_cnt = 0
  try:
    type_of_lec = kwargs['type']
  except:
    type_of_lec = 'Lecture'
  start_roll = kwargs['start_roll']
  end_roll = kwargs['end_roll']
  div = kwargs['div']
  subject = kwargs['subject']
  x = db.collection(u'subjects').document(subject)
  student_coll = db.collection(u'students')
  if type_of_lec == 'Lecture':
    tot_cnt = x.collection('lecture_count').document(div).get().to_dict()['lecture_count']
  else:
    tot_cnt = x.collection('lecture_count').document(div).get().to_dict()['lecture_count']
  att = {}
  for roll in range(int(start_roll), int(end_roll) + 1):
    att[str(roll)] = 0
  docs = db.collection(u'attendance').where(u'class', u'==', div).where(u'subject_name', u'==', subject).get()
  for doc in docs:
    data = doc.to_dict()
    if type_of_lec == data['attendance_type']:
      for roll in att.keys():
        if roll in data['present_students']:
          att[roll] += 1
  for roll in att.keys():
    att[roll] = round(att[roll] / tot_cnt * 100, 2)
  return att







#Ranged attendance
def calc_overall_attendance_subject_ranged(**kwargs):
  pr_cnt = 0
  try:
    type_of_lec = kwargs['type']
  except:
    type_of_lec = 'Lecture'
  try:
    start_date_str = kwargs['start_date']
  except:
    start_date_str = ''
  try:
    end_date_str = kwargs['end_date']
  except:
    end_date_str = ''
  start_roll = kwargs['start_roll']
  end_roll = kwargs['end_roll']
  div = kwargs['div']
  subject = kwargs['subject']
  x = db.collection(u'subjects').document(subject)
  student_coll = db.collection(u'students')
  if type_of_lec == 'Lecture':
    tot_cnt = x.collection('lecture_count').document(div).get().to_dict()['lecture_count']
  else:
    tot_cnt = x.collection('practical_count').document(div).get().to_dict()['practical_count']
  att = {}
  for roll in range(int(start_roll), int(end_roll) + 1):
    att[str(roll)] = 0
  docs = db.collection(u'attendance').where(u'class', u'==', div).where(u'subject_name', u'==', subject).get()
  for doc in docs:
    if start_date_str != '':
      if gettimestamp(start_date_str) > gettimestamp(doc.id.split('Z')[1]):
        continue
    if end_date_str != '':
      if gettimestamp(end_date_str) < gettimestamp(doc.id.split('Z')[1]):
        continue
    data = doc.to_dict()
    if type_of_lec == data['attendance_type']:
      for roll in att.keys():
        if roll in data['present_students']:
          att[roll] += 1
  for roll in att.keys():
    att[roll] = round(att[roll] / tot_cnt * 100, 2)
  return att
