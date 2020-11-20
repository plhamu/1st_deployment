from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register',views.register),
    path('login',views.login),
    path('logout',views.logout),
    path('travels',views.travels),
    path('createTrip', views.createTrip),
    path('addTrip', views.addTrip),
    path('view/<int:tripId>',views.tripInfo),
    path('cancel/<int:tripId>',views.cancel),
    path('add/<int:tripId>',views.joinTrip),
    path('delete/<int:tripId>',views.deleteTrip)
]