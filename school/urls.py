from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path("",views.login_view, name="login"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add-student/", views.add_student, name="add_student"),
    path("add-teacher/", views.add_teacher, name="add_teacher"),
    path("students/", views.view_students, name="view_students"),
    path("teachers/",views.view_teachers, name="view_teachers"),
    path("logout/", views.logout_view, name="logout"),
    path('student/update/<int:id>/', views.update_student, name='update_student'),
    path('student/delete/<int:id>/', views.delete_student, name='delete_student'),
    path('teacher/update/<int:id>/', views.update_teacher, name='update_teacher'),
    path('teacher/delete/<int:id>/', views.delete_teacher, name='delete_teacher'),
    path('mark_attendance/', views.mark_attendance, name='mark_attendance'),
    path("view_attendance/", views.view_attendance, name='view_attendance'),
    path("notices/", views.notice_list, name="notice_list"),
    path("notices/add/", views.add_notice, name="add_notice"),
    path("notices/delete/<int:pk>/", views.delete_notice, name="delete_notice"),
    path("notices/edit/<int:pk>/", views.edit_notice, name="edit_notice"),
    path('settings/', views.settings_view, name='settings'),
    path('change_password/', views.change_password, name="change_password"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('view_classroom/', views.view_classroom, name="view_classroom"),
    path('add_classroom/', views.add_classroom, name="add_classroom"),
    path('students/<int:student_id>/', views.student_profile, name="student_profile"),
    path('teachers/<int:teacher_id>/', views.teacher_profile, name='teacher_profile'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/read/<int:id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notification/delete/<int:id>/', views.delete_notification, name="delete_notification"),
]

