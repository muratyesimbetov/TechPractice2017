# -*- coding: utf-8 -*-
"""
Definition of views.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app import models


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    all_event = models.GetAllEvent()

    return render(
        request,
        'app/index.html',
        {
            'title': 'Домашня сторінка',
            'year': datetime.now().year,
            'all_event': all_event
        }
    )


def order_asc(request):
    """Renders the order_asc page."""
    assert isinstance(request, HttpRequest)

    all_event = models.DisMostPop()

    return render(
        request,
        'app/index.html',
        {
            'title': 'Найбільш популярні',
            'year': datetime.now().year,
            'all_event': all_event
        }
    )


def order_desc(request):
    """Renders the order_desc page."""
    assert isinstance(request, HttpRequest)

    all_event = models.DisLessPop()

    return render(
        request,
        'app/index.html',
        {
            'title': 'Найменш популярні',
            'year': datetime.now().year,
            'all_event': all_event
        }
    )


def rnd_evnt(request):
    """Renders the random event page."""
    assert isinstance(request, HttpRequest)

    all_event = models.GetAllEvent()

    from random import randint
    ent_indx = randint(0, len(all_event) - 1)
    rnd_event = all_event[ent_indx]

    meet_event_date_max = models.GetMaxEvtDateFromEvent(rnd_event.eventid)

    return render(
        request,
        'app/event.html',
        {
            'title': 'Випадкова подія',
            'message': 'Your application description page.',
            'view_decript': 'Найвипадковіша подія у світі, зустрічайте',
            'year': datetime.now().year,
            'event': rnd_event,
            'date_now': datetime.now(),
            'meet_event_date_max':meet_event_date_max
        }
    )

from app.forms import SearchForm
def search(request):
    if request.method == "POST":
        # Get the posted form

        search_form = SearchForm(request.POST)
        if search_form.is_valid():

            evnt_name = search_form.cleaned_data['evnt_name']
            evnt = models.GetEventByName(evnt_name)

            return render(
                request,
                'app/index.html',
                {
                    'title': 'Сторынка пошуку',
                    'year': datetime.now().year,
                    'all_event': evnt
                }
            )

@login_required         
def creating(request):
    return render(
        request,
        'app/creating.html',
        {
            'title': 'створення нової події'
        }
    )


def stats(request):
    all_evnt_count = models.GetAllEventsCount()
    vouted_user_count = models.GetVotedUsersCount()

    return render(
        request,
        'app/stats.html',
        {
            'title': 'Статисика створенних подій',
            'all_evnt_count': all_evnt_count,
            'vouted_user_count': vouted_user_count
        }
    )



def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О чому?',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


from app.forms import NewEventForm

@login_required   
def creating(request):
    
    evt_title = "no title"
    evt_description = "no description"
    evt_place = "no place"
    evt_date = datetime.now()
    evt_vote_start = datetime.now()
    evt_vote_end = datetime.now()

    evt_id = 0

    if request.method == "POST":
        # Get the posted form
        eventForm = NewEventForm(request.POST)

        if eventForm.is_valid():
            evt_title = eventForm.cleaned_data['evt_title']
            evt_description = eventForm.cleaned_data['evt_description']
            evt_date = eventForm.cleaned_data['evt_date']
            evt_vote_start = eventForm.cleaned_data['evt_vote_start']
            evt_vote_end = eventForm.cleaned_data['evt_vote_end']
            evt_place = eventForm.cleaned_data['evt_place']

            evt_id = models.CreateEventTotal(evt_title, evt_description, evt_place, evt_date, evt_vote_start,
                                             evt_vote_end)

            return render(
                request,
                'app/event_date_creating.html',
                {
                    'title': 'створення дат для події',
                    'evt_id': evt_id,
                    'evt_title': evt_title
                }
            )
    else:
        eventForm = NewEventForm()

    return render(
        request,
        'app/creating.html',
        {
            'title': 'створення нової події',
            'evt_title': evt_title,
            'evt_description': evt_description,
            'evt_place': evt_place,
            'evt_date': evt_date,
            'evt_vote_start': evt_vote_start,
            'evt_vote_end': evt_vote_end
        }
    )


from app.forms import EventDateForm

@login_required   
def event_date_creating(request):
    evt_date = datetime.now()

    if 'evt_id' in request:
        evt_id = request['evt_id']

    if 'evt_title' in request:
        evt_title = request['evt_title']

    if request.method == "POST":
        # Get the posted form
        eventForm = EventDateForm(request.POST)

        if eventForm.is_valid():
            evt_date = eventForm.cleaned_data['evt_date']
            evt_id = eventForm.cleaned_data['evt_id']
            evt_title = eventForm.cleaned_data['evt_title']

            mid = models.MakePossibleDate(evt_date)
            models.MakePairDateEvent(mid, evt_id)
    else:
        eventForm = EventDateForm()

    return render(
        request,
        'app/event_date_creating.html',
        {
            'title': 'створення дат для події',
            'evt_title': evt_title,
            'evt_id': evt_id,
            'evt_date': evt_date
        }
    )


def evnt(request, id):
    evnt = models.GetEventInfo(id)

    meet_event_date_max = models.GetMaxEvtDateFromEvent(id)

    date_now = datetime.today().date()

    return render(
        request,
        'app/event.html',
        {
            'title': evnt.name,
            'view_decript': 'Подія',
            'message': 'Your application description page.',
            'year': datetime.now().year,
            'event': evnt,
             'date_now': date_now,
            'meet_event_date_max': meet_event_date_max
        }
    )


from app.forms import VotingForm

@login_required
def voting(request):
    if request.method == "POST":
        # Get the posted form
        votingForm = VotingForm(request.POST)

        if votingForm.is_valid():
            evt_id = votingForm.cleaned_data['evt_id']
            evt_id = int(evt_id)

            dates = models.GetEvtDatesForEvent(evt_id)
            evnt = models.GetEventInfo(evt_id)

            return render(
                request,
                'app/voting.html',
                {
                    'evnt': evnt,
                    'evt_dates': dates
                }
            )

        else:
            votingForm = VotingForm()
            return render(request, 'app/home.html')

@login_required
def votedate(request, evtdateid):
    evtdateid = int(evtdateid)
     
    user_auth = request.user # login TODO
    models.UserDbSynhron(user_auth)
    userId =  user_auth.id  

    models.MakeVote(evtdateid, userId)


    all_event = models.GetAllEvent()
    return render(
        request,
        'app/index.html',
        {
            'title': 'Домашня сторінка',
            'year': datetime.now().year,
            'all_event': all_event
        }
    )



from django.views import generic
class LoginView(generic.TemplateView):
    template_name = "app/login.html"
