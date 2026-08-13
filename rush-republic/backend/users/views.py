from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import SignupSerializer, UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsAdmin, IsSocialMedia, IsProductionCoordinator, IsClientServicing


class SignupView(generics.CreateAPIView):
    """POST /api/signup/ - register a new employee."""

    queryset = CustomUser.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                'message': 'Account created successfully. Please log in.',
                'user': UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    """POST /api/login/ - authenticate with email + password, returns JWT pair + user info."""

    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    """POST /api/logout/ - blacklists the refresh token to invalidate the session."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveAPIView):
    """GET /api/profile/ - returns the logged-in user's details."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminDashboardView(APIView):
    """GET /api/admin-dashboard/ - Admin-only: total users + breakdown by department."""

    permission_classes = [IsAdmin]

    def get(self, request):
        total_users = CustomUser.objects.count()
        users_by_department = {
            label: CustomUser.objects.filter(department=value).count()
            for value, label in CustomUser.Department.choices
        }
        all_users = UserSerializer(CustomUser.objects.all().order_by('-created_at'), many=True).data

        return Response({
            'message': 'This is Admin Home Page',
            'total_users': total_users,
            'users_by_department': users_by_department,
            'all_users': all_users,
        })


class SocialMediaView(APIView):
    """GET /api/social-media/ - Social Media department (+ Admin)."""

    permission_classes = [IsSocialMedia]

    def get(self, request):
        return Response({
            'message': 'This is Social Media Home Page',
            'user': UserSerializer(request.user).data,
        })


class ProductionCoordinatorView(APIView):
    """GET /api/production-coordinator/ - Production Co-Ordinator department (+ Admin)."""

    permission_classes = [IsProductionCoordinator]

    def get(self, request):
        return Response({
            'message': 'This is Production Co-Ordinator Home Page',
            'user': UserSerializer(request.user).data,
        })


class ClientServicingView(APIView):
    """GET /api/client-servicing/ - Client-Servicing department (+ Admin)."""

    permission_classes = [IsClientServicing]

    def get(self, request):
        return Response({
            'message': 'This is Client-Servicing Home Page',
            'user': UserSerializer(request.user).data,
        })
