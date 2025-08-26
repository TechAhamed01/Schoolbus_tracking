from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    grade = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    address = models.TextField()
    emergency_contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

class Bus(models.Model):
    bus_number = models.CharField(max_length=20, unique=True)
    capacity = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=100)
    driver_contact = models.CharField(max_length=15)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bus {self.bus_number}"

class Route(models.Model):
    name = models.CharField(max_length=100)
    bus = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, related_name='routes')
    start_point = models.CharField(max_length=255)
    end_point = models.CharField(max_length=255)
    stops = models.JSONField()  # Store list of stops as JSON
    distance = models.FloatField(help_text="Distance in kilometers")
    estimated_duration = models.DurationField(help_text="Estimated duration of the route")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Bus: {self.bus.bus_number if self.bus else 'Unassigned'})"

class StudentRouteAssignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='route_assignments')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='student_assignments')
    pickup_point = models.CharField(max_length=255)
    pickup_time = models.TimeField()
    drop_point = models.CharField(max_length=255)
    drop_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    assigned_date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'route')

    def __str__(self):
        return f"{self.student} - {self.route}"

class AttendanceRecord(models.Model):
    ATTENDANCE_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)
    route = models.ForeignKey(Route, on_delete=models.SET_NULL, null=True, related_name='attendance_records')
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='recorded_attendances')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student__user__first_name']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"
