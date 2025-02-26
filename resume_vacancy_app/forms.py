from django import forms
from resume_vacancy_app.models import *
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class UserAuthorizationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
                if not user.check_password(password):
                    raise forms.ValidationError("Неверный пароль.")
            except User.DoesNotExist:
                raise forms.ValidationError("Пользователь не найден.")

        return cleaned_data

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['fullname', 'date_of_birth', 'gender', 'email', 'phone', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class EducationForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['education', 'institution', 'faculty', 'year_graduation']

class WorkForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['status', 'area_work', 'branch']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['experience', 'achievements', 'company']

class SkillsForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['skills']

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['fullname', 'status', 'gender', 'date_of_birth', 'phone',
                  'email', 'education', 'institution', 'faculty', 'area_work',
                  'branch', 'year_graduation', 'experience', 'company',
                  'achievements', 'skills', 'address', 'proximity_home', 'working_days',
                  'work_format', 'salary', 'internship']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class CommentForm(forms.Form):
    text = forms.CharField(label="Комментарий", max_length=100)

class ComplainForm(forms.Form):
    text = forms.CharField(label="Жалоба", max_length=100)

class RecomendationForm(forms.Form):
    text = forms.CharField(label="Рекомендация", max_length=100)


class VacancyFilterForm(forms.Form):
    #title = forms.CharField(required=False)
    area = forms.CharField(required=False)
    min_salary = forms.DecimalField(required=False)
    max_salary = forms.DecimalField(required=False)
    experience = forms.CharField(required=False)
    branch = forms.CharField(required=False)
    employment = forms.CharField(required=False)

