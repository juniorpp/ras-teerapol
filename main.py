#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
from google.appengine.api import rdbms
from datetime import datetime
from pytz import timezone
import pytz




JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

_Database = "prinya-th-2013:prinya-db"


class MainHandler(webapp2.RequestHandler):
    def get(self):


        conn = rdbms.connect(instance=_Database, database='Prinya_Project')
        cursor = conn.cursor()
        cursor.execute("select * from course")
        
        templates = {
    		'course' : cursor.fetchall(),
    	}
    	get_template = JINJA_ENVIRONMENT.get_template('course_create.html')
    	self.response.write(get_template.render(templates));

    	

class InsertHandler(webapp2.RequestHandler):
    def post(self):

        utc = pytz.utc
        date_object = datetime.today()
        utc_dt = utc.localize(date_object);
        bkk_tz = timezone("Asia/Bangkok");
        bkk_dt = bkk_tz.normalize(utc_dt.astimezone(bkk_tz))
        time_insert = bkk_dt.strftime("%H:%M:%S")

        data_code = self.request.get('course_code')

        

        conn4 = rdbms.connect(instance=_Database, database='Prinya_Project')
        cursor4 = conn4.cursor()
        cursor4.execute("select course_code from course")
       
        
        count=0
        for row in cursor4.fetchall():
            if row[0] in data_code:
                count=1
        

        if count==1:
            self.redirect("/Error")

        else:
            data_course_name = self.request.get('course_name')
            data_course_description = self.request.get('course_description')
            data_faculity_id = self.request.get('faculity')
            data_faculity = ""
            # data_total_capacity = self.request.get('total_capacity')
            data_department = self.request.get('department')
            data_credit_lecture = self.request.get('credit_lecture')
            data_credit_lab = self.request.get('credit_lab')
            data_credit_learning = self.request.get('credit_learning')
            data_credit_type = self.request.get('credit_type')
            data_credit_type2 = self.request.get('credit_type2')
            data_prerequisite = self.request.get('prerequisite')
            data_prerequisite=int(data_prerequisite)
            

            if data_faculity_id=="1":
                data_faculity = "Engineering";
            elif data_faculity_id=="2":
                data_faculity = "Information Technology";
            elif data_faculity_id=="3":
                data_faculity = "Business";
            elif data_faculity_id=="4":
                data_faculity = "Language";

            data_credit_type=int(data_credit_type)
            data_credit_type2=int(data_credit_type2)

            price = [0,1350,1350,1500,1500,1750,1350,1000,1500,1500,1350,1000,1000,1500]
            price1 = price[data_credit_type]
            price2 = price[data_credit_type2]

            # if data_credit_type in (1,2,6,10):
            #     price1=1350
            # elif data_credit_type in (3,4,8,9,13):
            #     price1=1500
            # elif data_credit_type==5:
            #     price1=1750
            # elif data_credit_type in (7,11,12):
            #     price1=3000

            # if data_credit_type2 in (1,2,6,10):
            #     price2=1350
            # elif data_credit_type2 in (3,4,8,9,13):
            #     price2=1500
            # elif data_credit_type2==5:
            #     price2=1750
            # elif data_credit_type2 in (7,11,12):
            #     price2=3000

            data_credit_lecture = int(data_credit_lecture)
            data_credit_lab = int(data_credit_lab)
            data_department = int(data_department)

            price1 =int(price1)
            price2 =int(price2)
            total=0
            total=(price1*data_credit_lecture)+(price2*data_credit_lab)

            data_department_full=""

            if data_department==1:
                data_department_full="Information Technology"
            elif data_department==2:
                data_department_full="Multimedia Technology"
            elif data_department==3:
                data_department_full="Business Information Technology"
            elif data_department==4:
                data_department_full="Accountancy"
            elif data_department==5:
                data_department_full="Industrial Management"
            elif data_department==6:
                data_department_full="International Business Management"
            elif data_department==7:
                data_department_full="Japanese Businees Administration"
            elif data_department==8:
                data_department_full="Computer Engineering"
            elif data_department==9:
                data_department_full="Production Engineering"
            elif data_department==10:
                data_department_full="Automotive Engineering"
            elif data_department==11:
                data_department_full="Electrical Engineering"
            elif data_department==12:
                data_department_full="Industrial Engineering"
            elif data_department==13:
                data_department_full="Language"

                    
            total=int(total)
            data_faculity_id=int(data_faculity_id)
            data_credit_lecture=int(data_credit_lecture)
            data_credit_lab=int(data_credit_lab)
            data_credit_learning=int(data_credit_learning)

            # data_credit_lecture = str(data_credit_lecture)
            # data_credit_lab = str(data_credit_lab)

            # price1 =str(price1)
            # price2 =str(price2)

            
            conn = rdbms.connect(instance=_Database, database='Prinya_Project')
            cursor = conn.cursor()
            cursor.execute("insert into course \
                (course_code,course_name,course_description,credit_lecture,credit_lab,credit_learning,type_credit_lecture,type_credit_lab,price,department,faculity,faculity_id) VALUES ('%s','%s','%s','%d','%d','%d','%d','%d','%d','%s','%s','%d')"%
                (data_code,data_course_name,data_course_description,data_credit_lecture,data_credit_lab,data_credit_learning,data_credit_type,data_credit_type2,total,data_department_full,data_faculity,data_faculity_id))
            conn.commit()

            conn2 = rdbms.connect(instance=_Database, database='Prinya_Project')
            cursor2 = conn2.cursor()
            cursor2.execute("insert into regiscourse\
                (course_id,semester,year,status) values((select course_id from course where course_code = '%s'),1,2556,1)"%
                (data_code))        
            conn2.commit()

            conn3 = rdbms.connect(instance=_Database, database='Prinya_Project')
            cursor3 = conn3.cursor()
            cursor3.execute("insert into log\
                (staff_id,course_id,day,time,type) values(2,(select course_id from course where course_code = '%s'),CURDATE(),'%s',1)"%
                (data_code,time_insert))        
            conn3.commit()

            if data_prerequisite!=0:                
                conn4 = rdbms.connect(instance=_Database, database='Prinya_Project')
                cursor4 = conn4.cursor()
                cursor4.execute("insert into prerequsite_course\
                    (course_id,type,prerequsite_id) values((select course_id from course where course_code = '%s'),1,'%s')"%
                    (data_code,data_prerequisite))        
                conn4.commit()

            # self.response.write(total)
            # self.response.write(price1)
            # self.response.write(price2)
            conn.close()
            conn2.close()
            conn3.close()
            conn4.close()
            self.redirect("http://prinya-ailada.appspot.com/")


class ErrorHandler(webapp2.RequestHandler):
    def get(self):
        templates = {
            # 'course' : cursor.fetchall(),
        }
        get_template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(get_template.render(templates));
        # self.redirect('/')
   

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Insert', InsertHandler),
    ('/Error', ErrorHandler)

], debug=True)
