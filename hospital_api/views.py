from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from .models import Doctor, Patient, PatientRecord, Department
from .serializers import DoctorSerializer, PatientSerializer, PatientRecordSerializer, DepartmentSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Doctor.objects.all()
        return Doctor.objects.filter(user=self.request.user)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Patient.objects.all()
        if hasattr(self.request.user, 'doctor'):
            return Patient.objects.filter(department=self.request.user.doctor.department)
        return Patient.objects.filter(user=self.request.user)

class PatientRecordViewSet(viewsets.ModelViewSet):
    queryset = PatientRecord.objects.all()
    serializer_class = PatientRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PatientRecord.objects.all()
        if hasattr(self.request.user, 'doctor'):
            return PatientRecord.objects.filter(department=self.request.user.doctor.department)
        return PatientRecord.objects.filter(patient__user=self.request.user)

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class RegisterAPI(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class LogoutAPI(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request._auth.delete()
        return Response({"message": "Logged out successfully"})
