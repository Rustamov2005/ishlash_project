from .models import User
from .models import Job, Chat, Company, Message, CheckCode, Notification, CV
from rest_framework import serializers


class CheckCodeSerializer(serializers.Serializer):
    class Meta:

        model = CheckCode
        fields = '__all__'
        read_only_fields = ('id',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ("id",)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            'owner': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Chat
        fields = "__all__"
        read_only_fields = ("id",)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            'owner': {'read_only': True},
            'company': {'read_only': True},
        }


class MessageSerializer(serializers.ModelSerializer):
    chat = ChatSerializer(read_only=True)
    owner = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id", 'owner', 'chat', 'timestamp')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("id", 'user', 'created_at')


class CVSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    user = UserSerializer()
    class Meta:
        model = CV
        fields = "__all__"
        read_only_fields = ("id", 'user', 'created_at', 'updated_at')


