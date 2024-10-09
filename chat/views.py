from rest_framework import generics
from .models import Chat, User, User
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import Message
from .serializers import MessageSerializer
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken

class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["username", "phone_number"]

class OTPLogin(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")

        # Check OTP (use a fixed "12345" OTP for now as specified)
        if otp != "12345":
            return Response(
                {"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create user by mobile number
        user, created = User.objects.get_or_create(phone_number=phone_number)

        refresh = RefreshToken.for_user(user)

        print(refresh)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id
        }, status=status.HTTP_200_OK)

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class ChatMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        return Message.objects.filter(
            chat__participants=self.request.user, chat__participants__id=user_id
        )


class CreateChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        other_user = User.objects.get(id=user_id)
        chat, created = Chat.objects.get_or_create(
            participants__in=[request.user, other_user]
        )
        return Response({"chat_id": chat.id}, status=status.HTTP_201_CREATED)


class PreviousChatUsersView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chats = Chat.objects.filter(participants=self.request.user)
        return (
            User.objects.filter(chats__in=chats)
            .exclude(id=self.request.user.id)
            .distinct()
        )
