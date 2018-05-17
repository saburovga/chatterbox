#!/usr/bin/env python
import sleekxmpp
import re
import datetime

xmpp_hostname='openfire.ufk09.local'
xmpp_jid='test2@'+xmpp_hostname
xmpp_pwd='test2'
birthdays_file='birthdates.csv'
xmpp_to='all@broadcast.openfire.ufk09.local'
msg=''
celebrating_people=[]
currentdate=datetime.date.today().strftime('%d.%m')

birthdays=open(birthdays_file, "r")
for line in birthdays:
    result=re.split(r';',line)
    birthdate=re.findall(r'\d\d\.\d\d',result[3])
    fullname=result[0]+" "+result[1]+" "+result[2]
    if birthdate[0]==currentdate: 
        celebrating_people.append(fullname)
birthdays.close()

celebrating_people.sort()
if len(celebrating_people)==0:
    exit(0)
elif len(celebrating_people)==1:
    msg='\nСегодня, '+currentdate+', свой День Рождения празднует '
    for person in celebrating_people:
        msg+=person
    msg+='. Искренне поздравляем'
    if re.search(r'^.*ч$', person): 
        msg+=' его :-)'
    if re.search(r'^.*а$', person):
        msg+=' ее :-)'
else:
    msg='Сегодня, '+currentdate+', свой день рождения празднуют: '
    for person in celebrating_people:
        if celebrating_people.index(person)==len(celebrating_people)-1:
            msg+=person+". "
        else:
            msg+=person+", "
    msg+='Искренне поздравляем их :-)'

xmpp=sleekxmpp.ClientXMPP(xmpp_jid, xmpp_pwd)
xmpp.add_event_handler("session_start",xmpp)
xmpp.connect((xmpp_hostname, 5222))
xmpp.process(block=False)
xmpp.send_presence()
xmpp.get_roster()
xmpp.send_message(xmpp_to,msg,'chat')
xmpp.disconnect(wait=True)
