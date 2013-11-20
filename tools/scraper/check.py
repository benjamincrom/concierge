#!/usr/bin/python

import datetime
import smtplib
import time
import subprocess


def send_email():
    sender = "concierge@kronos.com"
    receivers = ["benjamincrom@gmail.com"]
    
    message = """From: Benjamin <bcrom@utk.edu>
    To: To Benjamin <benjamincrom@gmail.com>
    Subject: Script is stuck
    
    STUUUUUCK!!!
    """
    
    try:
       smtpObj = smtplib.SMTP("localhost")
       smtpObj.sendmail(sender, receivers, message)         
       print "Successfully sent email"
    except:
       print "Error: unable to send email"


old_output = ""
send_email()


while True:
    time.sleep(210)
    new_output = subprocess.check_output(["ssh", "cromulus@benjamincrom.com", "wc", "-l", "/home/cromulus/repos/concierge/formatted_titles.txt"])
    print new_output
    now = str(datetime.datetime.now())
    if new_output == old_output:
        print "STUCK!!!     %s" % now
        send_email()
        break
    else:
        print "all cool     %s" % now
        old_output = new_output
    print new_output

