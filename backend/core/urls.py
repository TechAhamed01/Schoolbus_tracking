from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router for our viewsets
router = DefaultRouter()
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'buses', views.BusViewSet, basename='bus')
router.register(r'routes', views.RouteViewSet, basename='route')
router.register(r'student-route-assignments', views.StudentRouteAssignmentViewSet, 
                basename='studentrouteassignment')
router.register(r'attendance-records', views.AttendanceRecordViewSet, 
                basename='attendancerecord')

urlpatterns = [
    # Include all the router URLs
    path('', include(router.urls)),
    
    # Additional custom endpoints can be added here
    # Example:
    # path('custom-endpoint/', views.CustomView.as_view(), name='custom-endpoint'),
]
