from django.shortcuts import render,redirect
from django.contrib import messages
from .models import User, Trip

# Create your views here
def index(request):
    return render(request, "login.html")

def register(request):
    print(request.POST)
    errorsFromValidator=User.objects.registerValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)> 0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        newUser= User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['e'], password=request.POST['pw'])
        request.session['loggedinUserId']= newUser.id
        return redirect('/travels')
    

def login(request):
    print(request.POST)
    errorsFromValidator= User.objects.loginValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        matchingEmail=User.objects.filter(email=request.POST['e'])
        request.session['loggedinUserId']=matchingEmail[0].id
        return redirect('/travels')

def logout(request):
    request.session.clear()
    return redirect('/')

def travels(request):
    if 'loggedinUserId' not in request.session:
        messages.error(request, "Login First!")
        return redirect('/')
    context = {
        'loggedinUser': User.objects.get(id=request.session['loggedinUserId']),
        'allTrips':Trip.objects.all(),
        'myTrips':Trip.objects.filter(travelor=User.objects.get(id=request.session['loggedinUserId'])),
        'otherUserTrips': Trip.objects.exclude(travelor=User.objects.get(id=request.session['loggedinUserId']))
    }
    return render(request, "traveltables.html",context)

def createTrip(request):
    return render(request, "createTrip.html")

def addTrip(request):
    print(request.POST)
    errorsFromValidator=Trip.objects.createTripValidator(request.POST)
    print(errorsFromValidator)
    if len(errorsFromValidator)>0:
        for key, value in errorsFromValidator.items():
            messages.error(request, value)
        return redirect('/createTrip')
    else:
        Trip.objects.create(name=request.POST['dest'], start_date=request.POST['date_from'], end_date=request.POST['date_to'], plan=request.POST['desc'], creator=User.objects.get(id=request.session['loggedinUserId']))
    return redirect('/travels')

def tripInfo(request, tripId):
    context={
        'eachTrip':Trip.objects.get(id=tripId)
    }
    return render(request, "tripInfo.html", context)

def cancel(request, tripId):
    Trip.objects.get(id=tripId).travelor.remove(User.objects.get(id=request.session['loggedinUserId']))
    return redirect('/travels')

def joinTrip(request, tripId):
    Trip.objects.get(id=tripId).travelor.add(User.objects.get(id=request.session['loggedinUserId']))
    return redirect('/travels')

def deleteTrip(request, tripId):
    tripDelete= Trip.objects.get(id=tripId)
    tripDelete.delete()
    return redirect('/travels')
