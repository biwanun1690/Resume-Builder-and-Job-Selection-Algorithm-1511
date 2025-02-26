from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    fullname = models.CharField(
        max_length=200,
    )
    status = models.CharField(
        choices=[
            ('Студент', 'Студент'),
            ('Начинающий специалист', 'Начинающий специалист'),
            ('Средний работник с опытом', 'Средний работник с опытом'),
            ('Профессионал', 'Профессионал'),
        ],
        max_length=100,
    )
    gender = models.CharField(
        choices=[
            ('Мужской', 'Мужской'),
            ('Женский', 'Женский'),
        ],
        max_length=100,
    )
    date_of_birth = models.DateField()
    phone = models.IntegerField(
        default=0,
    )
    email = models.EmailField()
    education = models.CharField(
        choices=[
            ('Среднее', 'Среднее'),
            ('Среднее специальное', 'Среднее специальное'),
            ('Неокончанное высшее', 'Неокончанное высшее'),
            ('Высшее', 'Высшее'),
            ('Бакалавр', 'Бакалавр'),
            ('Магистр', 'Магистр'),
            ('Кандидат наук', 'Кандидат наук'),
            ('Доктор наук', 'Доктор наук'),
        ],
        max_length=100,
    )
    institution = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    area_work = models.CharField(max_length=100)
    branch = models.CharField(max_length=100)
    year_graduation = models.IntegerField()
    experience = models.CharField(
        choices=[
            ('Нет опыта', 'Нет опыта'),
            ('От 1 года до 3 лет', 'От 1 года до 3 лет'),
            ('От 3 до 6 лет', 'От 3 до 6 лет'),
            ('Более 6 лет', 'Более 6 лет'),
        ],
        max_length=100,
    )
    company = models.TextField(
        max_length=1000,
    )
    achievements = models.TextField(
        max_length=1000,
    )
    skills = models.TextField(
        max_length=1000,
    )
    address = models.CharField(
        max_length=100,
    )
    proximity_home = models.IntegerField()

    salary = models.IntegerField()

    internship = models.BooleanField()

    working_days = models.TextField(
        max_length=1000,
    )

    work_format = models.CharField(
        max_length=100,
        choices=[
            ('Полный день', 'Полный день'),
            ('Удалённая работа', 'Удалённая работа'),
            ('Сменный график', 'Сменный график'),
            ('Гибкий график', 'Гибкий график'),
        ],
    )

    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    # vacancies = models.ManyToManyField(to=Vacancy, related_name='resumes', blank=True)
    objects = models.Manager()


class Vacancy(models.Model):
    name = models.TextField(max_length=100)
    area = models.TextField(max_length=100)
    salary_from = models.TextField(default=0)
    salary_to = models.TextField(default=0)
    requirement = models.TextField(default=0)
    responsibility = models.TextField(default=0)
    address = models.TextField(max_length=1000)
    employer = models.TextField(max_length=10000)
    schedule = models.TextField(max_length=100)
    working_days = models.TextField(max_length=100)
    working_hours = models.TextField(max_length=100)
    night_shifts = models.BooleanField(max_length=100)
    professional_roles = models.TextField(max_length=100)
    experience = models.TextField(max_length=100)
    employment = models.TextField(max_length=100)
    branch = models.TextField(max_length=100)
    internship = models.BooleanField(max_length=100)

    objects = models.Manager()

class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)

class Complain(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)

class FavoriteVacancy(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(to=Vacancy, on_delete=models.CASCADE)

    objects = models.Manager()

class Recomendation(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    resume = models.ForeignKey(to=Resume, on_delete=models.CASCADE)

    objects = models.Manager()

