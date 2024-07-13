from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import DoctorViewSet, PatientViewSet, PatientRecordViewSet, DepartmentViewSet
from rest_framework_jwt.views import obtain_jwt_token

router = routers.DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)
router.register(r'patient_records', PatientRecordViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_jwt_token),
]
