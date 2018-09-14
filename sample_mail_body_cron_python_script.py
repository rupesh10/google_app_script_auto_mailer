import psycopg2
import csv
import zipfile
import tarfile
import os
from smtplib import SMTPException
import smtplib
import mimetypes
import pandas as pd
#import emailer as E
import numpy as np
from premailer import Premailer, transform
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
import html


def cursor_mx_analytics():
    conn_string = "dbname='XX' user='XX' host='Data base host url' password='XXXXX' port='XXXX'"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
#    cursor.execute("set search_path to public,postgis")
    return cursor
pgcur = cursor_mx_analytics()
pgcur.execute('''
select android, country, region, installed from sample_table limit 10;
''')


results = pgcur.fetchall()
df1 = pd.DataFrame(results, columns = ['android', 'country', 'region' , 'installed'])

style = '''
<style>
th {
  text-align: center;
  text-transform: uppercase;
  background: #4A148C;
  color: white;
  padding: 20px;
  max-width:100px;
  font-size: 16px;
  font-weight:bold;
}
table {
  border: 1px solid #fff;
  border-collapse: collapse;
  font-family: Trebuchet Ms;
  background-color: #E1BEE7;
}
td {
  font-size: 14px;
  max-width:100px;
  text-align:center;
  padding:10px;
}
</style>
<center>
<h2>City Level Average TAT MTD</h2>
${table1}
</center>
'''
# <h2>Pending Cases MTD</h2>
# ${table2}
# <h2>Time Bucket Level MTD number of orders</h2>
# ${table3}
# NA Represents number of cases not assigned to the given team
# <h2>City Level Average TAT for Last 7 days orders</h2>
# ${table4}
# <h2>Pending Cases for Last 7 days orders</h2>
# ${table5}
# <h2>Time Bucket Level last 7 days number of orders</h2>
# ${table6}
# NA Represents number of cases not assigned to the given team
# </center>
# '''

html = style.replace('${table1}',df1.to_html(index=False))
# html = html.replace('${table2}',df2.to_html(index=False))
# html = html.replace('${table3}',df3.to_html(index=False))
# html = html.replace('${table4}',df4.to_html(index=False))
# html = html.replace('${table5}',df5.to_html(index=False))
# html = html.replace('${table6}',df6.to_html(index=False))


html = transform(html)
# html1 = transform(html1)
# html2 = transform(html2)
email_list = 'email list with comma seprated'
#email_list = 'rupesh.tiwari@housing.com'

# email_list = 'priyadarshini.kasarla@housing.com'
# email_list = 'gurbakshsingh.khalsa@housing.com'

##E.send_email(email_list,'Re: Cron: broker_sales_tat',html)

# writer = csv.writer(open('test1S.csv','wb'))
# writer.writerow(['month', 'phone',])
# for i in data1:
#     writer.writerow(data1[i])
       
def send_mail():
    smtp = SMTP("smtp.gmail.com:587")
    smtp.ehlo()
    smtp.starttls()
    smtp.login("email id", "password")
    text = ""
    msg1 = MIMEText(html,'html')
    # msg2 = MIMEText(html,'html')
    # msg3 = MIMEText(html,'html')
    msg = MIMEMultipart("html")
    # msg = MIMEMultipart("html")
    # msg = MIMEMultipart("html")
#        msg = MIMEMultipart()
    msg.preamble = 'Multipart message.\n'
    msg['Subject'] = 'sample mail Cron'
    msg['From'] = 'dsl@mailer.com'
    msg['Reply-to'] = 'reply email id'
    msg['To'] = email_list
    msg.attach(msg1)
        # msg.attach(msg2)
        # msg.attach(msg3)
    smtp.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
send_mail()


print ('mail sent')


