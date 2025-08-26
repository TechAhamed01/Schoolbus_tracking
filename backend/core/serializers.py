from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Bus, Route, StudentRouteAssignment, AttendanceRecord

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='student'))
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_user_details(self, obj):
        user = obj.user
        return {
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number
        }

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class RouteSerializer(serializers.ModelSerializer):
    bus_details = serializers.SerializerMethodField()

    class Meta:
        model = Route
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_bus_details(self, obj):
        if obj.bus:
            return {
                'bus_number': obj.bus.bus_number,
                'driver_name': obj.bus.driver_name,
                'driver_contact': obj.bus.driver_contact
            }
        return None

class StudentRouteAssignmentSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField()
    route_details = serializers.SerializerMethodField()

    class Meta:
        model = StudentRouteAssignment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_student_details(self, obj):
        return {
            'id': obj.student.id,
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'student_id': obj.student.student_id,
            'grade': obj.student.grade
        }

    def get_route_details(self, obj):
        return {
            'id': obj.route.id,
            'name': obj.route.name,
            'bus_number': obj.route.bus.bus_number if obj.route.bus else None
        }

class AttendanceRecordSerializer(serializers.ModelSerializer):
    student_details = serializers.SerializerMethodField()
    recorded_by_details = serializers.SerializerMethodField()
    route_details = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def get_student_details(self, obj):
        return {
            'id': obj.student.id,
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'student_id': obj.student.student_id,
            'grade': obj.student.grade
        }

    def get_recorded_by_details(self, obj):
        if obj.recorded_by:
            return {
                'id': obj.recorded_by.id,
                'name': f"{obj.recorded_by.first_name} {obj.recorded_by.last_name}",
                'role': obj.recorded_by.role
            }
        return None

    def get_route_details(self, obj):
        if obj.route:
            return {
                'id': obj.route.id,
                'name': obj.route.name,
                'bus_number': obj.route.bus.bus_number if obj.route.bus else None
            }
        return None
