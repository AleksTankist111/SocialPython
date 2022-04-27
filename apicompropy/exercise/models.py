import os

from django.contrib.auth.models import AbstractUser
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager

# Create your models here.
from transliterate import slugify
from django.template.defaultfilters import slugify as slg

import exercise.garbage_collector as gc
from apicompropy.settings import SUCCESS_STATUS

EXERCISES_DIR = 'exercises'


class User(AbstractUser):
    def get_avatar_path(self, filename):
        return os.path.join(
            'user_avatars',
            str(self.username),
            filename)
    town = models.CharField(max_length=255, verbose_name='Город', blank=True)
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    about = models.TextField(blank=True, verbose_name='Описание')
    skills = models.TextField(blank=True, verbose_name='Скилл-стек')
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, verbose_name='Аватар')
    email = models.EmailField(blank=False, null=False, unique=True, verbose_name='Email')
    last_online = models.DateTimeField(blank=True, null=True)

    # In this method, check that the date of the last visit is not older than 15 minutes
    def is_online(self):
        if self.last_online:
            return (timezone.now() - self.last_online) < timezone.timedelta(minutes=5)
        return False

    # If the user visited the site no more than 15 minutes ago,
    def get_online_info(self):
        if self.is_online():
            # then we return information that he is online
            return 'Online'
        if self.last_online:
            # otherwise we write a message about the last visit
            return 'Был в сети {}'.format(naturaltime(self.last_online))
            # If you have only recently added information about a user visiting the site
            # then for some users there may not be any information about the visit, we will return information that the last visit is unknown
        return 'Unknown'


class Subscription(models.Model):
    followed = models.ForeignKey('User', on_delete=models.CASCADE, related_name='subscribers', blank=False, null=False)
    subscriber = models.ForeignKey('User', on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return f"{self.followed.username} is followed by {self.subscriber.username}"


class Exercise(models.Model):
    """
    Класс "Задача". Имеет автора и теги.
    """
    def get_path(self, filename):
        return os.path.join(
            EXERCISES_DIR,
            str(self.slug),
            filename)

    def get_path_inputs(self, filename):
        return os.path.join(
            EXERCISES_DIR,
            str(self.slug),
            filename)

    def get_path_outputs(self, filename):
        return os.path.join(
            EXERCISES_DIR,
            str(self.slug),
            filename)

    def __str__(self):
        return self.title

    def _generate_slug(self):
        if slugify(self.title):
            slug_candidate = slug_original = slg(slugify(self.title))
        else:
            slug_candidate = slug_original = slg(self.title)
        i = 1
        while True:
            if not Exercise.objects.filter(slug=slug_candidate).exists():
                break
            slug_candidate = '{}-{}'.format(slug_original, i)
            i += 1

        self.slug = slug_candidate

    def save(self, *args, **kwargs):
        if not self.pk:
            self._generate_slug()
        super(Exercise, self).save(*args, **kwargs)

    title = models.CharField(max_length=255, verbose_name='Название задачи')
    tags = TaggableManager(blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL', default=None)
    description_main = models.TextField(blank=False, verbose_name='Описание')
    description_inputs = models.TextField(blank=False, verbose_name='Входные данные')
    description_outputs = models.TextField(blank=False, verbose_name='Выходные данные')
    example_inputs = models.TextField(blank=False, verbose_name='Пример входных данных')
    example_outputs = models.TextField(blank=False, verbose_name='Пример выходных данных')
    test_data_inputs = models.FileField(upload_to=get_path_inputs, blank=False, null=False,
                                        verbose_name='Файл тестов (input.txt)')
    test_data_outputs = models.FileField(upload_to=get_path_outputs, blank=False, null=False,
                                         verbose_name='Файл тестов (output.txt)')
    solution_file = models.FileField(upload_to=get_path, verbose_name='Решение задачи')
    time_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='is_author', blank=False)

    rating = models.FloatField(default=0, verbose_name='Рейтинг')
    n_votes = models.IntegerField(default=0, verbose_name='Кол-во оценивших')
    users_voted = models.JSONField(default=dict([('idxs', [])]))

    def delete(self, *args, **kwargs):
        gc.remove_dir(EXERCISES_DIR, self.slug)
        return super(Exercise, self).delete(*args, **kwargs)


    class Meta:
        verbose_name = 'Выложенные задачи'
        verbose_name_plural = 'Выложенные задачи'
        ordering = ['id']


class Record(models.Model):
    """
    Класс "Запись", определяющий присланное решение для задачи
    """
    def get_path(self, filename):
        path = os.path.join(EXERCISES_DIR,
                            str(self.task_solved.slug),
                            filename)
        if not os.path.isfile(path):
            return path
        else:
            filename = '_solution_' + filename
            return os.path.join(EXERCISES_DIR,
                                str(self.task_solved.slug),
                                filename)

    def is_success(self):
        return self.status == SUCCESS_STATUS

    user_solver = models.ForeignKey('User', on_delete=models.CASCADE, related_name='records', blank=False)
    task_solved = models.ForeignKey('Exercise', on_delete=models.CASCADE, related_name='records', blank=False)
    time_loaded = models.DateTimeField(auto_now_add=True)
    status = models.TextField(blank=True)
    solution_file = models.FileField(upload_to=get_path, verbose_name='Решение задачи')

    class Meta:
        verbose_name = 'Решенные задачи'
        verbose_name_plural = 'Решенные задачи'

    def __str__(self):              # Временно
        return self.task_solved.title


class Notification(models.Model):
    def __str__(self):
        return f'Уведомление от {self.sender.pk}'

    sender = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, related_name='notifications_created')
    receiver = models.ForeignKey('User', on_delete=models.CASCADE, blank=False, related_name='notifications')
    note = models.TextField(blank=False, verbose_name='Уведомление')
    time_create = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Comment(models.Model):
    def __str__(self):
        return f'{self.author.username} прокомментировал задачу {self.task.title}'

    author = models.ForeignKey('User', on_delete=models.DO_NOTHING, blank=False, related_name='comments')
    task = models.ForeignKey('Exercise', on_delete=models.CASCADE, blank=False, related_name='comments')
    content = models.TextField(blank=False, null=False, verbose_name="Комментарий")
    time_create = models.DateTimeField(auto_now_add=True)




