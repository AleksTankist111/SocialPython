from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'users', UserViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'records', RecordsViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('search/users/', search_users, name='search_users'),
    path('search/exercises/', search_tasks, name='search_tasks'),
    path('top_exercises/', TOPExercisesView, name='top_exercises'),
    path('top_users/', TOPUsersView, name='top_users'),
    path('current_user/', CurrentUserView, name='current_user')
]