from gc import get_objects
from rest_framework import generics
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.mail import send_mail
from random import randint
from django.contrib.auth.models import make_password
from .models import Job, Chat, Company, Message, CheckCode, Profile, Notification, User, CV
from .serializer import (JobSerializer, CompanySerializer, UserSerializer, MessageSerializer,
                         ChatSerializer, CheckCodeSerializer, NotificationSerializer, CVSerializer)
from django.core.mail import EmailMultiAlternatives
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from random import randint
import random
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["access"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserRegistration1View(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.filter(username=email)
        if users.exists():
            return Response({'error': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        code = str(randint(1000, 9999))
        subject = "Email Verification Code"
        from_email = "rotabek752@gmail.com"


        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Verification Code</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 500px; margin: auto; background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
                <h2 style="color: #333;">Assalomu alaykum!</h2>
                <p style="font-size: 16px;">Tasdiqlash kodi quyidagicha:</p>
                <div style="font-size: 28px; font-weight: bold; color: #2e6da4; margin: 20px 0;">{code}</div>
                <p style="font-size: 14px; color: #777;">Iltimos, ro'yxatdan o'tishni yakunlash uchun ushbu koddan foydalaning.</p>
            </div>
        </body>
        </html>
        """
        text_content = f"Your verification code is: {code}"  # Fallback text

        email_message = EmailMultiAlternatives(subject, text_content, from_email, [email])
        email_message.attach_alternative(html_content, "text/html")
        sent = email_message.send()

        if sent:
            check = CheckCode.objects.filter(email=email)
            check.delete()
            CheckCode.objects.create(email=email, code=code)
            return Response({"success": f"{email} ga kod yuborildi!"})
        else:
            return Response({"error": "Email yuborilmadi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRegistration2View(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        verify_code = request.data.get('verify_code')
        full_name = request.data.get('full_name')
        password = request.data.get('password')
        if not email or not verify_code:
            return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(verify_code, int):
            return Response({'error': 'Verification code must be numeric'}, status=status.HTTP_400_BAD_REQUEST)
        check = CheckCode.objects.filter(email=email).order_by('-id').first()
        if not check:
            return Response({'error': 'Verification code not found'}, status=status.HTTP_404_NOT_FOUND)
        if check.code != verify_code:
            return Response({'error': 'Verification code does not match'}, status=status.HTTP_400_BAD_REQUEST)
        if not email or not full_name:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        users = User.objects.filter(username=email)
        if users.exists():
            return Response({'error': 'username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'error': 'password is too short'}, status=status.HTTP_400_BAD_REQUEST)
        check.delete()
        check = CheckCode.objects.filter(email=email)
        check.delete()
        user = User.objects.create_user(username=email, email=email, first_name=full_name, last_name=full_name)
        user.password = make_password(password)
        user.save()
        return Response(data={"success": f"muvaffaqiyatli Ro'yhatdan o'tdingiz!"}, status=status.HTTP_200_OK)



class UserRegistration3View(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        email = request.data.get('email')
        full_name = request.data.get('full_name')
        username = request.data.get('username')
        password = request.data.get('password')
        if not email or not full_name or not username:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({'error': 'password is required'}, status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response({'error': 'password is too short'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, first_name=full_name, last_name=full_name)
        user.password = make_password(password)
        user.save()
        return Response(data={"success": f"muvaffaqiyatli Ro'yhatdan o'tdingiz!"}, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    permissions_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email kiritilishi shart."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response(
                {"error": "Bunday email ro'yxatdan o'tmagan. Iltimos, ro'yxatdan o'ting.",
                 "register_url": "/register/"},
                status=status.HTTP_400_BAD_REQUEST
            )


        code = str(random.randint(100000, 999999))


        CheckCode.objects.filter(email=email).delete()


        CheckCode.objects.create(
            code=code,
            email=email
        )


        # Emailga kod yuboramiz
        subject = "Parolni tiklash uchun kod"
        from_email = "no-reply@example.com"
        to_email = [email]

        text_content = f"""
        Hurmatli foydalanuvchi,

        Siz parolni tiklashni so‘radingiz. Kod: {code}

        Agar siz so‘ramagan bo‘lsangiz, bu xabarni e'tiborsiz qoldiring.
        """

        html_content = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
            <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1);">
              <h2 style="color: #333;">Salom!</h2>
              <p style="font-size: 16px;">Siz parolni tiklashni so‘radingiz.</p>
              <p style="font-size: 18px;">Quyidagi kodni kiriting:</p>
              <p style="font-size: 30px; font-weight: bold; color: #4CAF50; text-align: center;">{code}</p>
              <p style="font-size: 14px; color: #888;">Iltimos, bu kodni hech kimga bermang.</p>
              <hr style="margin: 20px 0;">
              <p style="font-size: 14px; color: #aaa;">Agar siz bu so‘rovni yubormagan bo‘lsangiz, xabarni e'tiborsiz qoldiring.</p>
              <p style="font-size: 14px;">Hurmat bilan, <br> Bizning jamoamiz.</p>
            </div>
          </body>
        </html>
        """

        msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return Response({"detail": "Kod emailga yuborildi."}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not all([email, code]):
            return Response({"error": "Barcha maydonlar to'ldirilishi shart (email, code, new_password)."},
                            status=status.HTTP_400_BAD_REQUEST)


        forgot_code = CheckCode.objects.filter(email=email, code=code).first()
        if not forgot_code:
            return Response({"error": "Kod noto‘g‘ri yoki muddati tugagan."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Userni topamiz
        try:
            user = User.objects.filter(username=email).first()
        except User.DoesNotExist:
            return Response({"error": "Foydalanuvchi topilmadi."},
                            status=status.HTTP_404_NOT_FOUND)


        user.password = make_password(code)
        user.save()


        forgot_code.delete()

        return Response({"detail": "Parolingiz muvaffaqiyatli o'zgartirildi."}, status=status.HTTP_200_OK)


class ChangePasswordAuthview(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        user = request.user
        password = self.request.data.get("password")
        user.password = make_password(password)
        user.save()
        return Response(data="Muvaffaqiyatli parol o'zgartirildi", status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        print(profile)
        profile = {
            "full_name": user.first_name,
            "username": user.email,
            "cv": profile.cv.url if profile else "",
            "status": user.is_active,
        }
        return Response(data=profile, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response(data="Foydalanuvchi o'chirildi", status=status.HTTP_200_OK)

class CVdownloadView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        user = request.user
        cv = request.FILES.get("cv")
        if not cv:
            return Response(data="Cv file yuklash shart", status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.filter(user=user).first()
        if profile:
            profile.cv = cv
            profile.save()
        Profile.objects.create(user=user, cv=cv)
        return Response(data="Cv muvofaqqiyatli yuklandi", status=status.HTTP_200_OK)

class CVdeleteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        profile.cv.delete()
        return  Response(data="Cv o'chirib yuborildi", status=status.HTTP_200_OK)


class CompanyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = CompanySerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyInfoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            return Response({"error": "Kompaniya topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, company_id):
        try:
            company = Company.objects.get(id=company_id)
            company.delete()
            return Response({"detail": "Kompaniya o'chirildi."}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"detail": "Kompaniya topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, company_id):
        try:
            company = Company.objects.get(pk=company_id)
        except Company.DoesNotExist:
            return Response({"detail": "Kompaniya topilmadi."}, status=status.HTTP_404_NOT_FOUND)


        if company.owner != request.user:
            return Response({"detail": "You do not have permission to edit this company."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(company, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class JobsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = JobSerializer

    def get_queryset(self):
        queryset = Job.objects.all()

        search = self.request.query_params.get("search")
        location = self.request.query_params.get("location")
        job_type = self.request.query_params.get("job_type")
        salary_min = self.request.query_params.get("salary_min")
        salary_max = self.request.query_params.get("salary_max")
        company = self.request.query_params.get("company")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )


        if location:
            queryset = queryset.filter(location__icontains=location)


        if job_type:
            queryset = queryset.filter(job_type__iexact=job_type)


        if salary_min:
            queryset = queryset.filter(salary_min__gte=salary_min)

        if salary_max:
            queryset = queryset.filter(salary_max__lte=salary_max)


        if company:
            queryset = queryset.filter(company__icontains=company)

        return queryset


    def get(self, request):
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        serializer = JobSerializer(data=request.data, context={'request': request})
        user = request.user
        company = Company.objects.filter(owner=user).first()
        if serializer.is_valid():
            serializer.save(owner=request.user, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class JobDetailView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
            job.delete()
            return Response({"detail": "Job o'chirildi."}, status=status.HTTP_200_OK)
        except Job.DoesNotExist:
            return Response({"detail": "Job topilmadi"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, job_id):
        try:
            job = Job.objects.get(pk=job_id)
        except Job.DoesNotExist:
            return Response({"detail": "Job not found."}, status=status.HTTP_404_NOT_FOUND)

        # Faqat egasi tahrir qila oladi
        if job.owner != request.user:
            return Response({"detail": "You do not have permission to edit this job."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = JobSerializer(job, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
       user = request.user
       chats = Chat.objects.filter(user=user)
       serializer = ChatSerializer(chats, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        user = request.user
        try:
            company = Company.objects.get(owner=user)
        except Company.DoesNotExist:
            return Response({'error': 'Userga tegishli kompaniya topilmadi'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'user': user.id,
            'company': company.id
        }

        serializer = ChatSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MessagesView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, chat_id):
       chat = get_object_or_404(Chat, id=chat_id, user=request.user)
       messages = Message.objects.filter(chat=chat).order_by('timestamp')
       serializer = MessageSerializer(messages, many=True)
       return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id, user=request.user)

        data = request.data.copy()
        data['chat'] = chat.id


        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        serializer = NotificationSerializer(notification, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, notification_id):
        notification = get_object_or_404(Notification, id=notification_id)
        notification.delete()
        return Response(data="Notification o'chirib yuborildi",  status=status.HTTP_204_NO_CONTENT)

class CVView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        cvs = CV.objects.filter(user=request.user)
        serializer = CVSerializer(cvs, many=True)
        return Response(serializer.data)

class CVUpdateView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = CVSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CVDeleteAPIView(generics.DestroyAPIView):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class BookAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):
        return Response(data="salom otabek", status=status.HTTP_200_OK)
