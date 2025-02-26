"""
URL configuration for first_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from resume_vacancy_app.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', sign_up, name='signup'),
    path('create_resume/', create_resume, name='create_resume'),
    path('list_resumes/', list_resumes, name='list_resumes'),
    #path('list_resumes/<int:pk>', view_resume, name='view_resume'),
    path('list_resumes/recomendation/<int:pk>', recomendation_page, name='recomendations'),
    path('my_resume/', view_my_resume, name='my_resume'),
    path('my_resume/<int:pk>', view_my_resume_detal, name='my_resume_detal'),
    path('my_resume/edit/<int:pk>', edit_resume, name='edit_resume'),
    path('my_resume/delete/<int:pk>/', delete_resume, name='delete_resume'),
    path('list_vacancies/', list_vacancies, name='list_vacancies'),
    path('list_vacancies/<int:pk>', view_vacancy, name='vacancy'),
    path('list_vacancies/comments/<int:pk>', comment_page, name='comments'),
    path('list_vacancies/complains/<int:pk>', complain_page, name='complains'),
    path('list_vacancies/toggle_favorite/<int:pk>', toggle_favorite, name='toggle_favorite'),
    path('favorites/', view_favorite_vacancies, name='favorites_vacancies'),
    path('my_resume/need_vacancies/<int:pk>', vacancies_for_resume, name='need_vacancies'),
]
