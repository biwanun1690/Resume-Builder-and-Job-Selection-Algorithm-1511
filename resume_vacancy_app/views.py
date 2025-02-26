import datetime
import json
# from tools import LanguageCodes, exception_catcher_decorator

from django.contrib.auth import logout, login
from django.shortcuts import render, redirect, get_object_or_404

from pymystem3 import Mystem
from nltk.corpus import stopwords
from gensim.models import Word2Vec

from resume_vacancy_app.forms import *
from resume_vacancy_app.models import *
from resume_vacancy_app.algorithm_transform import *
from django.http import JsonResponse, HttpResponseForbidden, Http404

from django.contrib.auth.decorators import login_required

# @exception_catcher_decorator(language=LanguageCodes.RUSSIAN)
def index_page(request):
    context = {
        "text": "В процессе разработки :)"
    }
    return render(request, "index.html", context)

# @exception_catcher_decorator(language=LanguageCodes.RUSSIAN)
def sign_up(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('index')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/signup.html', {'user_form': user_form})

# @exception_catcher_decorator(language=LanguageCodes.RUSSIAN)
def logout_view(request):
    logout(request)
    return redirect('/')

def create_resume(request):
    if request.method == 'POST':
        form1 = PersonalInfoForm(request.POST)
        form2 = EducationForm(request.POST)
        form3 = WorkForm(request.POST)
        form4 = ExperienceForm(request.POST)
        form5 = SkillsForm(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid():
            resume = Resume(fullname=form1.cleaned_data['fullname'], status=form3.cleaned_data['status'],
                            gender=form1.cleaned_data['gender'], date_of_birth=form1.cleaned_data['date_of_birth'],
                            phone=form1.cleaned_data['phone'], email=form1.cleaned_data['email'],
                            education=form2.cleaned_data['education'], faculty=form2.cleaned_data['faculty'],
                            institution=form2.cleaned_data['institution'], area_work=form3.cleaned_data['area_work'],
                            branch=form3.cleaned_data['branch'], year_graduation=form2.cleaned_data['year_graduation'],
                            experience=form4.cleaned_data['experience'], company=form4.cleaned_data['company'],
                            achievements=form4.cleaned_data['achievements'], skills=form5.cleaned_data['skills'],
                            address=form1.cleaned_data['address'], author=request.user)
            resume.save()
            return redirect('/')
    else:
        form1 = PersonalInfoForm()
        form2 = EducationForm()
        form3 = WorkForm()
        form4 = ExperienceForm()
        form5 = SkillsForm()
    return render(request, 'create_resume.html', {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4, 'form5': form5})

def list_resumes(request):
    list_resumes = Resume.objects.all()
    return render(request, 'list_resumes.html', {'resumes': list_resumes})

def view_my_resume(request):
    my_resumes = Resume.objects.filter(author_id=request.user.id)
    return render(request, 'my_resume.html', {'my_resumes': my_resumes})

def view_my_resume_detal(request, pk):
    my_resume = Resume.objects.get(id=pk)
    return render(request, 'my_resume_detal.html', {'my_resume': my_resume})

def edit_resume(request, pk):
    resume = get_object_or_404(Resume, id=pk)

    if request.method == 'POST':
        form = ResumeForm(request.POST, instance=resume)
        if form.is_valid():
            form.save()
            return redirect('my_resume_detal', pk=resume.id)
    else:
        form = ResumeForm(instance=resume)

    return render(request, 'resume_edit.html', {'form': form})

def delete_resume(request, pk):
    if request.method == "POST":
        resume = get_object_or_404(Resume, id=pk)
        resume.delete()
        return redirect('my_resume')

def list_vacancies(request):
    vacancies = Vacancy.objects.all()
    form = VacancyFilterForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            if form.cleaned_data['area']:
                vacancies = vacancies.filter(area=form.cleaned_data['area'])
            if form.cleaned_data['min_salary']:
                vacancies = vacancies.filter(salary_from=form.cleaned_data['min_salary'])
            if form.cleaned_data['max_salary']:
                vacancies = vacancies.filter(salary_to=form.cleaned_data['max_salary'])
            if form.cleaned_data['experience']:
                vacancies = vacancies.filter(experience=form.cleaned_data['experience'])
            if form.cleaned_data['branch']:
                vacancies = vacancies.filter(branch=form.cleaned_data['branch'])
            if form.cleaned_data['employment']:
                vacancies = vacancies.filter(employment=form.cleaned_data['employment'])

        else:
            form = VacancyFilterForm()

    return render(request, 'list_vacancies.html', {'form': form, 'vacancies': vacancies})

def view_vacancy(request, pk):
    vacancy = Vacancy.objects.get(id=pk)
    is_favorite = vacancy.favoritevacancy_set.filter(user=request.user).exists()

    return render(request, 'view_vacancy.html', {
        'vacancy': vacancy,
        'is_favorite': is_favorite,
    })

def toggle_favorite(request, pk):
    vacancy = get_object_or_404(Vacancy, id=pk)
    favorite, created = FavoriteVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
    print(favorite, created)
    if not created:
        favorite.delete()
    return redirect('vacancy', pk=vacancy.id)

def view_favorite_vacancies(request):
    favorites = FavoriteVacancy.objects.filter(user_id=request.user.id)

    return render(request, 'favorite_vacancies.html', {'favorites': favorites})

def vacancies_for_resume(request, pk):
    resume = Resume.objects.get(id=pk)
    vacancies = Vacancy.objects.filter(branch=resume.area_work, experience=resume.experience)

    resume_text = resume.branch + ' ' + resume.achievements + ' ' + resume.skills
    resume_text = processing(resume_text)

    need_vacancies = {}

    for vacancy in vacancies:
        vacancy_text = vacancy.name + ' ' + vacancy.professional_roles
        if vacancy.responsibility is not None:
            vacancy_text += ' ' + vacancy.responsibility
        if vacancy.requirement is not None:
            vacancy_text += ' ' + vacancy.requirement
        vacancy_text = processing(vacancy_text)

        need_vacancies[vacancy.id] = count_similar_word(resume_text, vacancy_text)

    need_vacancies = dict(sorted(need_vacancies.items(), key=lambda item: item[1], reverse=True)[:10])
    need_vacancies_models = [Vacancy.objects.get(id=key) for key, val in need_vacancies.items()]

    context = {'vacancies': need_vacancies_models}

    return render(request, 'need_vacancies.html', context)

def comment_page(request, pk):
    vacancy = Vacancy.objects.get(id=pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data["text"]
            comment = Comment(
                text=text,
                created_at=datetime.datetime.now(),
                author_id=request.user.id, vacancy_id=pk
            )
            comment.save()
    else:
        comment_form = CommentForm()

    comment_history = Comment.objects.filter(vacancy_id=pk)
    context = {
        "comment_history": comment_history,
        "comment_form": comment_form,
        'vacancy': vacancy
    }
    return render(request, "comments.html", context)


def complain_page(request, pk):
    vacancy = Vacancy.objects.get(id=pk)
    if request.method == "POST":
        complain_form = ComplainForm(request.POST)
        if complain_form.is_valid():
            text = complain_form.cleaned_data["text"]
            complain = Complain(
                text=text,
                created_at=datetime.datetime.now(),
                author_id=request.user.id, vacancy_id=pk
            )
            complain.save()
            return redirect('vacancy', pk=pk)
    else:
        complain_form = ComplainForm()
    return render(request, "complains.html", {'complain_form': complain_form})

def recomendation_page(request, pk):
    resume = Resume.objects.get(id=pk)
    if request.method == "POST" and resume not in Resume.objects.filter(author_id=request.user.id):
        recomendation_form = RecomendationForm(request.POST)
        if recomendation_form.is_valid():
            text = recomendation_form.cleaned_data["text"]
            recomendation = Recomendation(
                text=text,
                author_id=request.user.id, resume_id=pk
            )
            recomendation.save()
    else:
        recomendation_form = RecomendationForm()

    recomendation_history = Recomendation.objects.filter(resume_id=pk)
    context = {
        "recomendation_history": recomendation_history,
        "recomendation_form": recomendation_form,
        'resume': resume
    }
    return render(request, "recomendations.html", context)


#def dowland_resume(request, pk):

