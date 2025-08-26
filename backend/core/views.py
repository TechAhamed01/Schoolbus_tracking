from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Student, Bus, Route, StudentRouteAssignment, AttendanceRecord
from .serializers import (
    StudentSerializer, BusSerializer, RouteSerializer,
    StudentRouteAssignmentSerializer, AttendanceRecordSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['student_id', 'user__first_name', 'user__last_name', 'grade']
    filterset_fields = ['grade', 'is_active']
    ordering_fields = ['student_id', 'user__last_name', 'grade']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """
        Get attendance records for a specific student.
        """
        student = self.get_object()
        attendance_records = AttendanceRecord.objects.filter(student=student)
        serializer = AttendanceRecordSerializer(attendance_records, many=True)
        return Response(serializer.data)

class BusViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing buses.
    """
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['bus_number', 'driver_name']
    filterset_fields = ['is_active']
    ordering_fields = ['bus_number', 'capacity']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class RouteViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing routes.
    """
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'start_point', 'end_point']
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'distance']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """
        Get all students assigned to this route.
        """
        route = self.get_object()
        assignments = StudentRouteAssignment.objects.filter(route=route, is_active=True)
        students = [assignment.student for assignment in assignments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class StudentRouteAssignmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing student route assignments.
    """
    queryset = StudentRouteAssignment.objects.all()
    serializer_class = StudentRouteAssignmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'route', 'student']
    ordering_fields = ['assigned_date']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing attendance records.
    """
    queryset = AttendanceRecord.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'route', 'status', 'date']
    search_fields = ['student__user__first_name', 'student__user__last_name', 'student__student_id']
    ordering_fields = ['-date', 'student__user__last_name']

    def perform_create(self, serializer):
        """
        Set the recorded_by field to the current user when creating a new record.
        """
        serializer.save(recorded_by=self.request.user)

    def get_queryset(self):
        """
        Filter queryset based on user role.
        """
        queryset = super().get_queryset()
        user = self.request.user
        
        # If user is a bus staff, only show records for their assigned routes
        if user.role == 'bus_staff':
            # Get all routes assigned to this bus staff
            # This assumes you have a way to associate bus staff with routes
            # You'll need to implement this based on your requirements
            assigned_routes = Route.objects.filter(bus__driver_name__icontains=user.get_full_name())
            queryset = queryset.filter(route__in=assigned_routes)
        # If user is a parent, only show records for their children
        elif user.role == 'parent':
            # This assumes you have a way to associate parents with students
            # You'll need to implement this based on your requirements
            student_ids = Student.objects.filter(parent=user).values_list('id', flat=True)
            queryset = queryset.filter(student_id__in=student_ids)
        
        return queryset

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Create multiple attendance records at once.
        Expected payload: [{"student": 1, "date": "2023-01-01", "status": "present", "route": 1}, ...]
        """
        data = request.data
        if not isinstance(data, list):
            return Response(
                {"error": "Expected a list of attendance records"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save(recorded_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
