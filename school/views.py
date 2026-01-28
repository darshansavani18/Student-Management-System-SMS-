from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import Student, Teacher, Attendance, Notice, ClassRoom,Notification
from .forms import StudentForm, TeacherForm
from django.contrib.auth.models import User,Group
from django.db.models import Q
from django.contrib import messages
from .decorators import admin_only, teacher_only, student_only, admin_or_teacher_only
from datetime import date
from django.utils.timezone import now
from .forms import ChangePasswordForm
from .utils import create_notification
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # later dashboard
        else:
            return render(request, 'school/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'school/login.html')

@login_required(login_url="login")
def dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_class = ClassRoom.objects.count()
    total_notice = Notice.objects.count()
    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "total_class": total_class,
        "total_notice": total_notice,
    }
    return render(request, "school/dashboard.html", context)

def logout_view(request):
    logout(request)
    return redirect("login")
@login_required
@admin_only
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                student_group = Group.objects.get(name='Student')
                user.groups.add(student_group)

                student = form.save(commit=False)
                student.user = user
                student.save()
                create_notification(
                user= request.user,
                title= "Student Added",
                message= f"student '{user.username}' added successfully"
                )

                return redirect('dashboard')

            except Exception as e:
                print("ERROR:", e)        
        else:
            print("FORM ERRORS:", form.errors)

    else:
        form = StudentForm()
   
    return render(request, 'school/add_student.html', {'form': form})

@login_required
@admin_only
def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose another one.")
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password
                )

                teacher_group = Group.objects.get(name='Teacher')
                user.groups.add(teacher_group)

                teacher = form.save(commit=False)
                teacher.user = user
                teacher.save()
                create_notification(
                user= request.user,
                title= "Teacher Added",
                message= f"teacher '{user.username}' added successfully"
                )
                messages.success(request, "Teacher added successfully.")
                return redirect('view_teachers')  # or dashboard

    else:
        form = TeacherForm()
    return render(request, 'school/add_teacher.html', {'form': form})

def view_students(request): 
    query = request.GET.get('q','').strip()

    students = Student.objects.select_related('user').all()

    if query:
        students = students.filter(
            Q(user__username__icontains=query) |
            Q(roll_number__icontains=query) |
            Q(class_name__icontains=query)
        )

    return render(request, 'school/view_students.html', {
       'students': students,
       'query': query
    })

def delete_student(request, id):
    student = Student.objects.get(id=id)

    # delete related user also
    student.user.delete()
    create_notification(
        request.user,
        "Student Delete",
        f"student '{student.user.username}' delete successfully"
    )
    return redirect('view_students')

def update_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == "POST":
        student.roll_number = request.POST.get('roll_number')
        student.class_name = request.POST.get('class_name')
        student.section = request.POST.get('section')
        student.gender = request.POST.get('gender')
        student.date_of_birth = request.POST.get('date_of_birth')
        student.address = request.POST.get('address')

        # ADD IMAGE HERE
        if 'profile_image' in request.FILES:
            student.profile_image = request.FILES['profile_image']

        student.save()
        create_notification(
        request.user,
        "Student Update",
        f"student '{student.user.username}' update successfully"
        )

        return redirect('view_students')

    return render(request, 'school/update_student.html', {
        'student': student
    })


def view_teachers(request): 
    query = request.GET.get('q','').strip()

    teachers = Teacher.objects.select_related('user').all()

    if query:
        teachers = teachers.filter(
            Q(user__username__icontains=query) |
            Q(full_name__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, 'school/view_teachers.html', {
       'teachers': teachers,
       'query': query
    })

def update_teacher(request, id):
    teacher = Teacher.objects.get(id=id)

    if request.method == "POST":
        teacher.full_name = request.POST.get('full_name')
        teacher.email = request.POST.get('email')
        teacher.subject = request.POST.get('subject')
        teacher.phone = request.POST.get('phone')
        teacher.joining_date = request.POST.get('joining_date')

        if 'profile_image' in request.FILES:
            teacher.profile_image = request.FILES['profile_image']
        
        teacher.save()
        create_notification(
        request.user,
        "Teacher Update",
        f"teacher '{teacher.user.username}' update successfully"
        )

        return redirect('view_teachers')

    return render(request, 'school/update_teacher.html', {
        'teacher': teacher
    })

def delete_teacher(request, id):
    teacher= Teacher.objects.get(id=id)

    # delete related user also
    teacher.user.delete()
    create_notification(
        request.user,
        "Teacher delete",
        f"teacher '{teacher.user.username}' delete successfully"
    )
    return redirect('view_teachers')

@login_required
@teacher_only
def mark_attendance(request):
    students = Student.objects.select_related('user').all()
    today = date.today()

    if request.method == "POST":
        for student in students :
            status = request.POST.get(str(student.id))
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={"status": status}
                )
        return redirect('view_attendance')

    return render(request, "school/mark_attendance.html", {
        "students": students,
        "today": today
    })

@login_required
def view_attendance(request):
    # Get selected date or default to today
    selected_date = request.GET.get('date') or now().date()

    # ALWAYS define records (no condition)
    records = Attendance.objects.filter(date=selected_date)

    # Safe usage
    total_present = records.filter(status='Present').count()
    total_absent = records.filter(status='Absent').count()

    context = {
        'records': records,
        'selected_date': selected_date,
        'total_present': total_present,
        'total_absent': total_absent,
    }

    return render(request, 'school/view_attendance.html', context)


def notice_list(request):
    notices = Notice.objects.select_related('created_by')
    return render(request, "school/notice_list.html", {
        "notices": notices
    })

@login_required
@admin_or_teacher_only
def add_notice(request):
    if request.method == "POST":
        title = request.POST.get("title")
        message = request.POST.get("message")

        Notice.objects.create(
            title=title,
            message=message,
            created_by = request.user
        )
        create_notification(
        request.user,
        "Notice Added",
        f"Notice '{title}' Added successfully"
        )  
        return redirect("notice_list")
    return render(request, "school/add_notice.html")

@login_required
@admin_or_teacher_only
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == "POST":
        notice.title = request.POST.get("title")
        notice.message = request.POST.get("message")
        notice.save()
        create_notification(
        request.user,
        "Notice Edited",
        f"Notice '{notice.title}' Edited successfully"
        )  
        return redirect("notice_list")

    return render(request, "school/edit_notice.html", {
        "notice": notice
    })

@login_required
@admin_or_teacher_only
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    create_notification(
        request.user,
        "Notice delete",
        f"Notice '{notice.title}' Delete successfully"
        )  
    return redirect("notice_list")

@login_required
def settings_view(request):
    if request.method == "POST":
        request.session['dark_mode'] = 'dark_mode' in request.POST
        return redirect('settings')
    return render(request, "school/settings.html")

@login_required
def change_password(request):
    """View to handle password change for logged-in users."""
    form = ChangePasswordForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():

            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')

            # Check if old password is correct
            if not request.user.check_password(old_password):
                form.add_error(
                    'old_password',
                    'Old password is incorrect'
                )
            else:
                request.user.set_password(new_password)
                request.user.save()

                # Keep user logged in after password change
                update_session_auth_hash(request, request.user)

            
            messages.success(
                request,
                'Password updated successfully'
            )
            return redirect('dashboard')
    else:
    # Load empty form for GET request
        form = ChangePasswordForm()

    return render(
        request,
        'school/change_password.html',
        {'form': form}
)

@login_required
def my_profile(request):
    """
    Displays the logged-in user's profile information.
    """
    user = request.user

    return render(
        request,
        'school/my_profile.html',
        {'user': user}
    )

@login_required
def view_classrooms(request):
    query = request.GET.get('q')

    classrooms = ClassRoom.objects.all()

    if query:
        classrooms = classrooms.filter(
            class_name__icontains=query
        ) | classrooms.filter(
            section__icontains=query
        )

    return render(request, 'school/view_classroom.html', {
        'classroom': classrooms
    })


@login_required
def add_classroom(request):
    """
    Add a new classroom.
    """
    teachers = User.objects.filter(groups__name='Teacher')

    if request.method == 'POST':
        class_name = request.POST.get('class_name')
        section = request.POST.get('section')
        capacity = request.POST.get('capacity')
        total_students = request.POST.get('total_students')
        teacher_id = request.POST.get('class_teacher')

        class_teacher = User.objects.get(id=teacher_id) if teacher_id else None

        ClassRoom.objects.create(
            class_name=class_name,
            section=section,
            capacity=capacity,
            total_students=total_students,
            class_teacher=class_teacher
        )

        return redirect('view_classroom')

    # ✅ THIS RETURN FIXES YOUR ERROR
    return render(
        request,
        'school/add_classroom.html',
        {'teachers': teachers}
    )

@login_required
def student_profile(request, student_id):
   """
    Displays the profile of a single student.
    """
   student = get_object_or_404(Student, id=student_id)

   return render(
       request,
       'school/student_profile.html',
       {'student': student}
   ) 
@login_required
def teacher_profile(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    return render(
        request,
        'school/teacher_profile.html',
        {'teacher': teacher}
    )
@login_required
def notifications(request):
    notifications = Notification.objects.filter(
        user = request.user
    ).order_by('-created_at')

    return render(
        request,
        'school/notifications.html',
        {'notifications': notifications}
    )
@login_required
def mark_notification_read(request, id):
    notification = Notification.objects.get(id=id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')

def delete_notification(request, id):
    # Only allow user to delete their own notification
    notification = get_object_or_404(Notification, id=id, user=request.user)
    notification.delete()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
