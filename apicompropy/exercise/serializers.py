from rest_framework import serializers

from .models import *
import exercise.garbage_collector as gc


class StringListField(serializers.ListField):  # http://www.django-rest-framework.org/api-guide/fields/#listfield
    child = serializers.CharField()

    def to_representation(self, data):
        return ' '.join(data.values_list('name', flat=True))  # you change the representation style here.


class ExerciseSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    rating = serializers.FloatField(read_only=True)
    tags = StringListField(required=False)
    solution_file = serializers.FileField(write_only=True)
    test_data_inputs = serializers.FileField(write_only=True)
    test_data_outputs = serializers.FileField(write_only=True)

    class Meta:
        model = Exercise
        exclude = ('n_votes', 'users_voted', 'slug')
        # lookup_field = 'slug'
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }

    def create(self, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            tags = tags[0].split()
            instance = super(ExerciseSerializer, self).create(validated_data)
            instance.tags.set(tags)
        else:
            instance = super(ExerciseSerializer, self).create(validated_data)
        return instance

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            tags = tags[0].split()
            instance.tags.set(tags)
        super().update(instance=instance, validated_data=validated_data)
        return instance

    def to_representation(self, instance):
        to_repr = super(ExerciseSerializer, self).to_representation(instance)
        to_repr['solutions_count'] = instance.records.filter(status=SUCCESS_STATUS).distinct().count()
        to_repr['author_username'] = instance.author.username
        to_repr['tags'] = list(name[0] for name in instance.tags.values_list('name'))
        return to_repr


class ExerciseHeaderSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'slug': instance.slug,
            'title': instance.title,
            'rating': instance.rating,
            'author_id': instance.author.pk,
            'author': instance.author.username,
            'time_create': instance.time_create,
            'tags': list(name[0] for name in instance.tags.values_list('name')),
            'solutions_count': instance.records.filter(status=SUCCESS_STATUS).distinct().count()
        }


class RecordSerializer(serializers.ModelSerializer):
    user_solver = serializers.PrimaryKeyRelatedField(read_only=True)
    status = serializers.CharField(read_only=True)
    time_loaded = serializers.DateTimeField(read_only=True)
    solution_file = serializers.FileField(write_only=True, required=True)
    task_solved = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), required=True)

    class Meta:
        model = Record
        fields = ('user_solver', 'status', 'task_solved', 'time_loaded', 'solution_file')


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    rating = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    online_status = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('avatar', 'username', 'first_name', 'last_name', 'email',
                  'date_joined', 'town', 'rating', 'about', 'skills', 'online_status', 'is_subscribed')

    def get_online_status(self, instance):
        return instance.get_online_info()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        if user.is_authenticated and user != instance:
            subscript = instance.subscribers.filter(subscriber=user)
            if subscript.exists():
                return subscript.first().pk
        return False


class UserHeaderSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'username': instance.username
        }

class UserSelfSerializer(serializers.ModelSerializer):
    notifications_number = serializers.SerializerMethodField()
    class Meta:
        model = User
        exclude = ('is_staff', 'password', 'is_superuser', 'is_active', )

    def get_notifications_number(self, instance):
        return instance.notifications.filter(is_read=0).count()

class SubscriptionSerializer(serializers.ModelSerializer):
    followed = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    subscriber = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(read_only=True)
    note = serializers.CharField(required=False)

    class Meta:
        model = Notification
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data['note'] = instance.note
        super().update(instance=instance, validated_data=validated_data)
        return instance


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'

    def get_author_name(self, instance):
        return instance.author.username


class TOPExercisesSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'slug': instance.slug,
            'title': instance.title,
            'rating': instance.rating,
        }

# class TestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exercise
#         fields = ('title', 'description_main', "description_input", "description_output",)
    # title = serializers.CharField(max_length=255)
    # description_main = serializers.CharField()
    # description_input = serializers.CharField()
    # description_output = serializers.CharField()
    # time_create = serializers.DateTimeField(read_only=True)
    # is_published = serializers.BooleanField(default=True)
    #
    # def create(self, validated_data):
    #     return Exercise.objects.create(**validated_data)
    #
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get("title", instance.title)
    #     instance.description_main = validated_data.get("description_main", instance.description_main)
    #     instance.save()
    #     return instance

