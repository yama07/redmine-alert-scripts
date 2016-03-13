#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redmine import Redmine
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate
from datetime import datetime

REDMINE_URL = "http://localhost/redmine"
API_KEY = "58f015fda60cdcfc2850f6f27b4607c4bf06ab28"

TARGET_GROUP = u'Adminグループ'
MAIL_ENCODING = "iso-2022-jp"
MAIL_FROM_ADDRESS = "redmine@localhost.localdomain"
MAIL_SMTP_SERVER = "localhost"
redmine = Redmine(REDMINE_URL, key=API_KEY)

def getGroupMembersByName(name):
    """ グループ名(name)のグループメンバーリストを返す。"""
    groups = redmine.group.all()
    groupId = filter(lambda g:g.name==name, groups).pop().id
    members = [redmine.user.get(u.id) for u in redmine.group.get(groupId, include='users').users]
    return members

def sendMail(user):
    """ユーザ(user)にメールを送信する。"""
    msg = MIMEText(u'テストメール本文'.encode(MAIL_ENCODING), 'plain', MAIL_ENCODING)
    msg['Subject'] = Header(u'テストメール題名'.encode(MAIL_ENCODING), MAIL_ENCODING)
    msg['From'] = MAIL_FROM_ADDRESS
    msg['To'] = user.mail
    msg['Date'] = formatdate()
    s = smtplib.SMTP(MAIL_SMTP_SERVER)
    s.sendmail(MAIL_FROM_ADDRESS, [user.mail, ], msg.as_string())
    s.close()

def isTargetUser(user):
    now = datetime.now()
    print user.id, user.firstname, user.last_login_on if hasattr(user, "last_login_on") else "None"
    if not hasattr(user, "last_login_on"):
        return True
    elif user.last_login_on < datetime(now.year, now.month, now.day):
        return True
    else:
        return False

def main():
    memberList = getGroupMembersByName(TARGET_GROUP)
    for user in filter(isTargetUser ,memberList):
        print user.id, user.firstname
#        sendMail(user)

if __name__ == '__main__':
    main()
