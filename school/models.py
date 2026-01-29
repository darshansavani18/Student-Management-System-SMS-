from django.db import models
from django.contrib.auth.models import User

# =========================
# Teacher Model
# =========================
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    joining_date = models.DateField(auto_now_add=True)
    profile_image = models.ImageField(
        upload_to='teacher_profiles/', 
        default='teacher_profiles.default.png',
        blank=True, null=True)
    
    def __str__(self):
        return self.full_name
class ClassRoom(models.Model):
    #Represents a physical or logical classroom.
    #Example: Class 10 - Section A
    class_name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)
    class_teacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_teacher'
    )

    # Total number of students in the class
    total_students = models.PositiveIntegerField()

    capacity = models.PositiveIntegerField()

    class meta :
        unique_together = ('class_name', 'section')
        ordering = ('class_name', 'section')

    def __str__(self):
        return f"{self.class_name} - {self.section}"
# =========================
# Student Model
# =========================
class Student(models.Model):
    """
    Stores student-related information.
    Linked to Django's User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.IntegerField(unique=True)
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    gender = models.CharField(
        max_length=10,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    profile_image = models.ImageField(
        upload_to = 'student_profiles/',
        default='student_profiles.default.png',
        blank = True,
        null = True
    )
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

class Attendance(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendance"
    )
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[
            ("Present", "Present"),
            ("Absent", "Absent"),
        ]
    )
    #A student can have ONLY ONE attendance record per date
    class Meta:         
        unique_together = ('student', 'date')
        ordering = ['-date']
    #__str__ controls how an Attendance object is displayed as readable text.
    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notices"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    class meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


    
class Notification(models.Model):
    title = models.CharField(max_length=50)
    message = models.TextField()

    # If notification is for a specific user (optional)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    