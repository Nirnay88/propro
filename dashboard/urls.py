from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
        path('', views.index),
        #path('postsign/', views.postsign),
        #path('signUp/', views.signUp,name="signUp"),
        path('validate/', views.validate, name = 'validate'),
        path('calculateAdmin/', views.calculateAdmin, name = 'calculateAdmin'),
        #path('postsignUp/',views.postsignUp,name="signUp"),
        path('forget/',views.forget,name="forget"),
        path('defaulter/',views.defaulter, name ="defaulter"),
        path('ranged/',views.callRanged, name ="ranged"),
        path('calculate_ranged/', views.calculate_ranged, name = 'calculate_ranged'),
        path('callIndex/',views.callIndex, name ="callIndex"),
        path('callIndex_admin/',views.callIndex_admin, name ="callIndex_admin"),
        path('callIndexDefault/',views.callIndexDefault, name ="callIndexDefault"),
        path('aboutus/',views.about,name="aboutus"),
        path('',views.logout,name="log"),
        path('calculate_def/', views.calculate_def, name = 'calculate_def'),
        path('',views.alreadySigned , name = "already")
]
