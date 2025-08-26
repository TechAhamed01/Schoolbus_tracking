from django.contrib import admin
from .models import Student, Bus, Route, StudentRouteAssignment, AttendanceRecord

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'user', 'grade', 'emergency_contact')
    list_filter = ('grade', 'created_at')
    search_fields = ('student_id', 'user__first_name', 'user__last_name', 'user__email')
    raw_id_fields = ('user',)
    date_hierarchy = 'created_at'

@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'driver_name', 'driver_contact', 'capacity', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('bus_number', 'driver_name', 'driver_contact')
    date_hierarchy = 'created_at'

class StudentRouteAssignmentInline(admin.TabularInline):
    model = StudentRouteAssignment
    extra = 1
    raw_id_fields = ('student',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus', 'start_point', 'end_point', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'start_point', 'end_point', 'bus__bus_number')
    raw_id_fields = ('bus',)
    inlines = [StudentRouteAssignmentInline]
    date_hierarchy = 'created_at'

@admin.register(StudentRouteAssignment)
class StudentRouteAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'route', 'pickup_point', 'drop_point', 'is_active')
    list_filter = ('is_active', 'assigned_date')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'route__name')
    raw_id_fields = ('student', 'route')
    date_hierarchy = 'assigned_date'

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'route', 'recorded_by')
    list_filter = ('status', 'date', 'route')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'route__name')
    raw_id_fields = ('student', 'route', 'recorded_by')
    date_hierarchy = 'date'
