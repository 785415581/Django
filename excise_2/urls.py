"""excise_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from class_func import views
from teacher_func import teacher_views
from student_views import student_views

urlpatterns = [

    url(r'^classes/',views.classes),
    url(r'^add_class/',views.add_class),
    url(r'^edit_class/',views.edit_class),
    url(r'^edit_modal_class/', views.edit_modal_class),

    url(r'^add_teacher/', views.add_teacher),
    url(r'^edit_teacher/', views.edit_teacher),

    url(r'^teachers/', views.teachers),

    url(r'^del_class/', views.del_class),
    url(r'^modal_add_class/', views.modal_add_class),
    url(r'^teacher/', teacher_views.teacher),
    #url(r'^add_teacher/', teacher_views.add_teacher),
    url(r'^del_teacher/', teacher_views.del_teacher),
    url(r'^student/', student_views.student),
    url(r'^add_student/', student_views.add_student),
    url(r'^modal_add_student/', student_views.modal_add_student),

    url(r'^edit_student/', student_views.edit_student),
    url(r'^modal_edit_student/', student_views.modal_edit_student),
    url(r'^modal_del_student/', student_views.modal_del_student),

    url(r'^get_all_class/', views.get_all_class),
    url(r'^modal_add_teacher/', views.modal_add_teacher),
    url(r'^transfrom_edit_teacher/', views.transfrom_edit_teacher),
    url(r'^rightToleft/', views.rightToleft),
    url(r'^leftToright/', views.leftToright),



    url(r'^login/', views.login),
    url(r'^layout/', views.layout),

]
