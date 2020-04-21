import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

cred = credentials.Certificate('./dep.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


#To get the timestamp
gettimestamp = lambda datestr : datetime.strptime(datestr, '%d-%m-%Y').timestamp()

# rollno,type,
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
