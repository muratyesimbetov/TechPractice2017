# -*- coding: utf-8 -*-
"""
Definition of models.
"""

from django.db import models
import numpy as np

# Create your models here.

class USER(models.Model):
    userid = models.IntegerField(primary_key=True)
    name = models.CharField("name", max_length=20)
    login = models.CharField("nickname", max_length=20)
    email = models.CharField("e-mail", max_length=50)
    password = models.CharField("password", max_length=30)
    city = models.CharField("city", max_length=30, blank=True)
    pass

class EVENT(models.Model):
    eventid = models.AutoField("ID", primary_key=True)
    name = models.CharField("event name", max_length=50)
    details = models.TextField("details", blank=True)
    place = models.CharField("where", max_length=40, blank=True)
    date = models.DateField("when", blank=True)
    participants = models.ManyToManyField(USER, blank=True)
    votingStart = models.DateField(blank=True)
    votingEnd = models.DateField(blank=True)

    pass

class MDATE(models.Model):
    mdateid = models.AutoField("ID",primary_key=True)
    meetingDateTimeS = models.DateField()
    
class EVTDATE(models.Model):
    evtdateid = models.AutoField(primary_key=True)
    evt = models.ForeignKey(EVENT)
    dat = models.ForeignKey(MDATE)
    
class VOTE(models.Model):
    voteid = models.AutoField("ID",primary_key=True)
    edate = models.ForeignKey(EVTDATE)
    usr = models.ForeignKey(USER)
    
###############################################################################################################################
def MakeVote(evtdateId, userId):
    '''participant must be typeof USER!!!'''
    from app.models import USER
    from app.models import EVTDATE
    from app.models import VOTE

    evtdt = EVTDATE.objects.get(evtdateid = evtdateId)
    user = USER.objects.get(userid = userId)

    event = evtdt.evt
    event.participants.add(user)
    event.save()

    vt=VOTE(edate=evtdt, usr=user)
    vt.save()
    
def MakePossibleDate(date):
    from app.models import MDATE
    dt=MDATE(meetingDateTimeS=date)
    dt.save()
    return dt.mdateid

def MakePairDateEvent(mdateId, evntId):
    from app.models import MDATE
    from app.models import EVTDATE

    mdate = MDATE.objects.filter(mdateid=mdateId)[0]
    evnt = EVENT.objects.filter(eventid=evntId)[0]

    evtdt=EVTDATE(evt=evnt, dat=mdate)
    evtdt.save()
###############################################################################################################################


def CreateUser(id, n, l, e, pas, c):
    from app.models import USER
    usr = USER(id,name=n, login=l, email=e, password=pas, city=c)
    usr.save()

def GetUserInfo(uid):
    from app.models import USER
    person = USER.objects.get(userid=uid)
    pass

def EditUserName(uid, uname):
    from app.models import USER
    USER.objects.filter(userid=uid).update(name=uname)
    
def EditEmail(uid, mail):
    from app.models import USER
    USER.objects.filter(userid=uid).update(email=mail)
    
def EditCity(uid, c):
    from app.models import USER
    USER.objects.filter(userid=uid).update(city=c)

################################################################################################################################

def CreateEvent(nam): #event creation method
    from app.models import EVENT
    evt = EVENT(name=nam)
    evt.save()


def CreateEventTotal(name,descript,place,init_date,vote_start_date,vote_end_date):
    from app.models import EVENT
    evt = EVENT(name=name,details=descript,place=place,date=init_date,votingStart=vote_start_date,votingEnd=vote_end_date)
    evt.save()

    from app.models import MDATE
    from app.models import EVTDATE

    mdate = MDATE(meetingDateTimeS=init_date)
    mdate.save()

    evnt_date = EVTDATE(evt=evt,dat = mdate)
    evnt_date.save()

    return evt.eventid

    
def EditEvtDetails(detls, evid): #editing event details (can be NULL first)
    from app.models import EVENT
    EVENT.objects.filter(id=evid).update(details=detls)

def EditEvtPlace(pla, evid): #editing event place (can be NULL first)
    from app.models import EVENT
    EVENT.objects.filter(id=evid).update(place=pla)
    
def EditEvtVotingPeriod(vst, ven, evid): #editing event voting period (can be NULL first, requires both start and end dates)
    from app.models import EVENT
    EVENT.objects.filter(id=evid).update(votingStart=vst, votingEnd=ven)
    
def GetEventInfo(evtid):
    '''returns event object on necessary id'''
    from app.models import EVENT

    evtid = int(evtid)
    evt = EVENT.objects.get(eventid=evtid)
    return evt
    
def GetEventByName(evnt_name):
    from app.models import EVENT
    evt = EVENT.objects.filter(name__contains=evnt_name)
    #evt = EVENT.objects.extra(where=["name LIKE '%" + evnt_name + "%"])

    return evt
    

def GetAllEvent():
    '''return all event'''
    from app.models import EVENT 
    evt = EVENT.objects.all()
    return evt
    

def GetEvtDatesForEvent(evtid):
    event = EVENT.objects.get(eventid=evtid)
    event_date = EVTDATE.objects.filter(evt =event)    
    return event_date
    #return 

def GetMaxEvtDateFromEvent(evtid):
    from django.db.models import Max
    from django.db.models import Count

    try :
        event = EVENT.objects.get(eventid=evtid)
        event_date = EVTDATE.objects.filter(evt =event).annotate(vote_count=Count('vote')).order_by("-vote")
        event_date_max_vote = event_date[0]

        return event_date_max_vote.dat.meetingDateTimeS
    except Exception : 
        return 'No'

def GetAllEventOrder(order, reverse):
    '''return all event'''
    from app.models import EVENT
    evt = EVENT.objects.order_by(-order)
    return evt

def DisplayAll(event): #returns all events (not finished!)
    from app.models import EVENT
    allevents=[]
    for e in EVENT.objects.all():
         allevents.add(e)
    return allevents
        

def DisLessPop():
    from app.models import EVENT
    from django.db.models import Count
    
    all_evnt = EVENT.objects.annotate(part_count=Count('participants')).order_by('part_count')
    return all_evnt
    pass #finish!!!

def DisMostPop():
    from app.models import EVENT
    from django.db.models import Count
    
    all_evnt = EVENT.objects.annotate(part_count=Count('participants')).order_by('-part_count')
    return all_evnt
    pass  # finish!!!


def GetParticipantsCount(event):
    from app.models import EVENT
    partList=event.participants.all()
    return len(partList)

#Statistics ------------------------------------------------------################################
def GetAllEventsCount():
    from app.models import EVENT
    eList = (EVENT.objects.values('eventid').distinct())
    return len(eList)
 
def GetVotedUsersCount():
    from app.models import VOTE
    from django.db.models import Count
    uList = (VOTE.objects.values('usr').distinct())
    return len(uList) 

def UserDbSynhron(user_auth):
    CreateUser(user_auth.id,user_auth.first_name,user_auth.username,user_auth.email,user_auth.password[:30],'Kiev')


