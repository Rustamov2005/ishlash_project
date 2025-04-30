from .models import User
from .models import Job, Chat, Company, Message, CheckCode, Notification, CV
from rest_framework import serializers



class CVSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = "__all__"
        read_only_fields = ("id", 'user', 'created_at', 'updated_at')

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

class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField(source='company.name', read_only=True)
    class Meta:
        model = Job
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            'owner': {'read_only': True},
            'company': {'read_only': True}, # owner clientdan kelmaydi, server qo'yadi
        }

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
        read_only_fields = ("id",)

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"
        read_only_fields = ("id",)
        extra_kwargs = {
            'owner': {'read_only': True}  # owner clientdan kelmaydi, server qo'yadi
        }

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ("id", 'owner', 'timestamp')

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"
        read_only_fields = ("id", 'user', 'created_at')





