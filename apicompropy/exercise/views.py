from itertools import chain

from django.utils.encoding import uri_to_iri, iri_to_uri
from apicompropy.pagination import CustomPagination
from rest_framework.views import APIView

from apicompropy.settings import SUCCESS_STATUS
from rest_framework import viewsets, serializers, mixins, generics
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db.models import Q

from .models import *
from .permissions import *
from .serializers import *
from .checker import checker


COMMON_NOTIFICATION_TEMPLATES = {
    "create_exercise": "Пользователь {username} выложил новую задачу! Поспешите оценить {exercise_link}!",
    "exercise_solved": "Пользователь {username} решил вашу задачу!"
}


class Checker:

    @staticmethod
    def testing(inputs, outputs, file, slug):
        return checker(inputs, outputs, file, slug)

    @staticmethod
    def update_solution(decorated_method):
        def wrapper(self, request, *args, **kwargs):
            instance = self.get_object()
            test_data_inputs = instance.test_data_inputs
            test_data_outputs = instance.test_data_outputs
            solution_file = instance.solution_file

            result = decorated_method(self, request, *args, **kwargs)

            new_instance = self.get_object()
            new_inputs = new_instance.test_data_inputs
            new_outputs = new_instance.test_data_outputs
            new_solution = new_instance.solution_file
            test_result = Checker.testing(new_inputs, new_outputs, new_solution, new_instance.author.username)
            if test_result == SUCCESS_STATUS:
                gc.delete_files([str(test_data_inputs),
                                 str(test_data_outputs),
                                 str(solution_file)], abspath=True)
            else:
                new_instance.test_data_inputs = test_data_inputs
                new_instance.test_data_outputs = test_data_outputs
                new_instance.solution_file = solution_file
                new_instance.save()
                gc.delete_files([str(new_inputs),
                                 str(new_outputs),
                                 str(new_solution)], abspath=True)
            return result
        return wrapper


def increase_rating(decorated_method):
    def wrapper(self, request, *args, **kwargs):
        first_time_condition = not Record.objects.filter(user_solver=request.user,
                                     task_solved=request.data['task_solved'],
                                     status=SUCCESS_STATUS).exists()
        result = decorated_method(self, request, *args, **kwargs)
        if self.record_status == SUCCESS_STATUS:
            if first_time_condition:
                request.user.rating = request.user.rating + 1
                request.user.save()
        return result
    return wrapper


class NotificationDecorators:

    @staticmethod
    def create_note(self, request, aim='SUBSCRIBERS', *args, **kwargs):
        if aim == 'SUBSCRIBERS':
            subscribers = request.user.subscribers.all()
            result = []
            for subscriber in subscribers:
                subs = subscriber.subscriber
                serializer = NotificationSerializer(data=request.data, context={'request': request})
                if serializer.is_valid():
                    serializer.save(sender=request.user, receiver=subs)
                    result.append(serializer.data)
                else:
                    raise APIException(detail=serializer.errors)
            return Response(result, status=status.HTTP_201_CREATED)
        else:
            serializer = NotificationSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(sender=request.user, receiver=aim)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            raise APIException(detail=serializer.errors)


    @staticmethod
    def create_exercise_note(decorated_method):
        def wrapper(self, request, *args, **kwargs):
            result = decorated_method(self, request, *args, **kwargs)
            if self.record_status == SUCCESS_STATUS:
                note = COMMON_NOTIFICATION_TEMPLATES['create_exercise'].format(username=request.user.username,
                                                                               exercise_link='link')
                _mutable = request.data._mutable
                request.data._mutable = True
                request.data["note"] = note
                note_response = NotificationDecorators.create_note(self, request, *args, **kwargs)
                request.data.pop("note")
                request.data._mutable = _mutable
            return result
        return wrapper

    @staticmethod
    def exercise_solved_note(decorated_method):
        def wrapper(self, request, *args, **kwargs):
            result = decorated_method(self, request, *args, **kwargs)
            if self.record_status == SUCCESS_STATUS:
                note = COMMON_NOTIFICATION_TEMPLATES['exercise_solved'].format(username=request.user.username)
                _mutable = request.data._mutable
                request.data._mutable = True
                request.data["note"] = note
                author = Exercise.objects.get(pk=request.data.get('task_solved')).author
                note_response = NotificationDecorators.create_note(self, request, author, *args, **kwargs)
                request.data.pop("note")
                request.data._mutable = _mutable
            return result
        return wrapper


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (HasExercisePermission,)
    lookup_field = 'slug'

    def get_queryset(self):
        q = self.request.query_params.get('tags')
        if q:
            q = q.split('_')
            query = Q()
            for word in q:
                query = query | Q(title__icontains=word) | Q(tags__name__icontains=word)
            return self.queryset.filter(query)
        return self.queryset

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        return serializer.save(author=self.request.user)

    @NotificationDecorators.create_exercise_note
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        exercise_created = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.record_status = Checker.testing(exercise_created.test_data_inputs,
                                             exercise_created.test_data_outputs,
                                             exercise_created.solution_file,
                                             exercise_created.author.username)
        if self.record_status != SUCCESS_STATUS:
            exercise_created.delete()
            return Response({"detail": self.record_status}, status=status.HTTP_412_PRECONDITION_FAILED)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @Checker.update_solution
    def update(self, request, *args, **kwargs):
        return super(ExerciseViewSet, self).update(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def rate(self, request, slug):
        grade = int(request.data.get('grade'))
        if 1 <= int(grade) <= 5:
            task = Exercise.objects.filter(slug=slug).first()
            if task:
                user_pk = request.user.pk
                if user_pk not in task.users_voted['idxs'] and request.user != task.author:
                    task.users_voted['idxs'].append(user_pk)
                    rating = task.rating
                    num = task.n_votes + 1
                    rating = (rating * (num - 1) + grade) / num
                    task.rating = rating
                    task.n_votes = num
                    task.save()
                    return Response(ExerciseSerializer(task).data,status=status.HTTP_200_OK)
                return Response({'detail': "This user have already rated this task or authored it. "},
                                status=status.HTTP_412_PRECONDITION_FAILED)
            return Response({'detail': "Task with such id doesn't exist."},
                            status=status.HTTP_412_PRECONDITION_FAILED)
        return Response({"detail": "You didn't specify 'grade' field correctly. It should be integer in range 1 to 5."},
                        status=status.HTTP_412_PRECONDITION_FAILED)

    @action(detail=False, methods=['get'])
    def meta(self, request):
        q = self.request.query_params.get('tags')
        if q:
            q = q.split('_')
            query = Q()
            for word in q:
                query = query | Q(title__icontains=word) | Q(tags__name__icontains=word)
            return Response({"tasks_amount": Exercise.objects.filter(query).count()}, status=status.HTTP_200_OK)
        return Response({"tasks_amount": Exercise.objects.all().count()}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def task_meta(self, request, slug):
        task = Exercise.objects.filter(slug=slug).first()
        if task:
            general = task.records.count()
            if general:
                result = task.records.filter(status=SUCCESS_STATUS).count()/general
            else:
                result = 0
            return Response({"percent_of_correct_solutions": result}, status=status.HTTP_200_OK)
        return Response({"detail": "This task doesn't exist"}, status=status.HTTP_412_PRECONDITION_FAILED)

    @action(detail=False, methods=['get'])
    def headers(self, request):
        queryset = self.get_queryset()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        data = ExerciseHeaderSerializer(page, many=True).data
        return paginator.get_paginated_response(data)

    @action(detail=True, methods=['get'])
    def header(self, request, slug):
        query = Exercise.objects.get(slug=slug)
        return Response(ExerciseHeaderSerializer(query).data, status=status.HTTP_200_OK)


class RecordsViewSet(mixins.CreateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    queryset = Record.objects.all()
    serializer_class = RecordSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        if 'user' in self.request.query_params and 'task' in self.request.query_params:
            user = User.objects.filter(pk=self.request.query_params['user'])
            if user:
                return user[0].records.filter(task_solved=self.request.query_params['task'])
            raise APIException(detail='User with such id is not exist')
        elif 'user' in self.request.query_params:
            user = User.objects.filter(pk=self.request.query_params['user'])
            if user:
                return user[0].records.all()
            raise APIException(detail='User with such id is not exist')
        elif 'task' in self.request.query_params:
            task = Exercise.objects.filter(pk=self.request.query_params['task'])
            if task:
                return task[0].records.all()
            raise APIException(detail='Task with such id is not exist')
        else:
            return super().get_queryset()

    @increase_rating
    @NotificationDecorators.exercise_solved_note
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        task = Exercise.objects.filter(pk=request.data['task_solved']).first()
        self.record_status = None
        if task:
            if task.author != request.user:
                if serializer.is_valid():
                    solution = serializer.save(user_solver=self.request.user)
                    self.record_status = Checker.testing(solution.task_solved.test_data_inputs,
                                                         solution.task_solved.test_data_outputs,
                                                         solution.solution_file,
                                                         request.user.username)
                    if self.record_status != SUCCESS_STATUS:
                        gc.delete_files(filenames=[str(solution.solution_file)], abspath=True)
                    serializer.save(status=self.record_status)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                raise APIException(detail=serializer.errors)
            return Response({"detail": "You can't solve the exercise you created"}, status=status.HTTP_412_PRECONDITION_FAILED)
        return Response({"detail": "Task with this id foes not exist"}, status=status.HTTP_412_PRECONDITION_FAILED)


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrAdminOrReadOnly, AllowUnauthorised,)

    @action(detail=False, methods=['get'])
    def headers(self, request):
        queryset = self.get_queryset()
        paginator = CustomPagination()
        page = paginator.paginate_queryset(queryset, request)
        data = UserHeaderSerializer(page, many=True).data
        return paginator.get_paginated_response(data)

    @action(detail=True, methods=['get'])
    def header(self, request, pk):
        query = User.objects.get(pk=pk)
        return Response(UserHeaderSerializer(query).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def authored(self, request, pk):
        serializer = ExerciseHeaderSerializer
        queryset = User.objects.filter(pk=pk).first()
        if queryset:
            queryset = queryset.is_author.order_by("-time_create")
            return Response(serializer(queryset, many=True).data)
        else:
            return Response(None)

    @action(detail=True, methods=['get'])
    def solved(self, request, pk):
        serializer = ExerciseHeaderSerializer
        queryset = User.objects.filter(pk=pk).first()
        if queryset:
            queryset = queryset.records.values_list("task_solved")
            queryset = Exercise.objects.filter(pk__in=queryset)
            return Response(serializer(queryset, many=True).data)
        else:
            return Response(None)


class SubscriptionViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsSubscriberOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(subscriber=self.request.user)


class NotificationViewSet(mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (AllowReceiverOnlyToDelete, )

    def get_queryset(self):
        return self.request.user.notifications.order_by('is_read', '-time_create')


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        if 'task' in self.request.query_params:
            task = Exercise.objects.filter(slug=self.request.query_params['task']).first()
            if task:
                return task.comments.all()
            raise APIException(detail='Task with such id does not exist')
        return super().get_queryset()


@api_view(['GET'])
@permission_classes([AllowAny])
def search_users(request):
    searchline = request.query_params.get('search')
    if not searchline:
        searchline = ''
    query = Q(username__icontains=searchline) | Q(first_name__icontains=searchline) | Q(last_name__icontains=searchline)
    user_serializer = UserHeaderSerializer
    users_queryset = User.objects.filter(query).distinct()
    paginator_user = CustomPagination()
    users_page = paginator_user.paginate_queryset(users_queryset, request)
    users = user_serializer(users_page, many=True).data
    return paginator_user.get_paginated_response(users)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_tasks(request):
    searchline = request.query_params.get('search')

    if not searchline:
        searchline = ''
    task_serializer = ExerciseHeaderSerializer
    query = Q(title__icontains=searchline) | Q(tags__name__icontains=searchline)
    tasks_queryset = Exercise.objects.filter(query).distinct()
    paginator_task = CustomPagination()
    task_page = paginator_task.paginate_queryset(tasks_queryset, request)
    tasks = task_serializer(task_page, many=True).data
    return paginator_task.get_paginated_response(tasks)


@api_view(['GET'])
@permission_classes([AllowAny])
def TOPExercisesView(request):
    serializer = TOPExercisesSerializer
    queryset = Exercise.objects.order_by('-rating')[:5]
    return Response(serializer(queryset, many=True).data)

@api_view(['GET'])
@permission_classes([AllowAny])
def TOPUsersView(request):
    serializer = UserHeaderSerializer
    queryset = User.objects.order_by('-rating')[:5]
    return Response(serializer(queryset, many=True).data)


@api_view(['GET'])
@permission_classes([AuthenticatedOnly])
def CurrentUserView(request):
    serializer = UserSelfSerializer
    if request.user.is_authenticated:
        request.user.last_online = timezone.now()  # At the request of the user, we will update the date and time of the last visit
        request.user.save(update_fields=['last_online'])
        return Response(serializer(request.user).data)
    else:
        return Response(None)

