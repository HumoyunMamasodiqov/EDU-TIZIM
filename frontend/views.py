from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Course, Group, Student, MarketingSurvey, StudentLog, LessonTime
from .forms import LoginForm, CourseForm, GroupForm, StudentCreateForm, StudentEditForm, MarketingSurveyForm, FreezeForm, RemoveFromGroupForm, AddToGroupForm, LessonTimeForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data["phone"],
                password=form.cleaned_data["password"],
            )
            if user:
                login(request, user)
                return redirect("dashboard")
            messages.error(request, "Telefon raqam yoki parol noto'g'ri")
    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard(request):
    course_count = Course.objects.count()
    group_count = Group.objects.count()
    student_count = Student.objects.count()
    survey_count = MarketingSurvey.objects.count()
    active_groups = Group.objects.filter(status="aktiv").count()
    pending_groups = Group.objects.filter(status="kutilyotgan").count()
    pending_student_count = Student.objects.filter(group__isnull=True, status="kutilyotgan").count()
    recent_students = Student.objects.select_related("group").order_by("-created_at")[:5]
    survey_stats = MarketingSurvey.objects.annotate(
        student_count=Count("students")
    ).filter(student_count__gt=0).order_by("-student_count")
    return render(request, "dashboard.html", {
        "course_count": course_count,
        "group_count": group_count,
        "student_count": student_count,
        "survey_count": survey_count,
        "active_groups": active_groups,
        "pending_groups": pending_groups,
        "pending_student_count": pending_student_count,
        "recent_students": recent_students,
        "survey_stats": survey_stats,
    })


@login_required(login_url="login")
def course_list(request):
    courses = Course.objects.annotate(group_count=Count("groups")).order_by("-created_at")
    return render(request, "course/list.html", {"courses": courses})


@login_required(login_url="login")
def course_create(request):
    form = CourseForm()
    if request.method == "POST":
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kurs muvaffaqiyatli qo'shildi")
            return redirect("course_list")
    return render(request, "course/form.html", {"form": form, "title": "Kurs qo'shish"})


@login_required(login_url="login")
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(instance=course)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Kurs muvaffaqiyatli yangilandi")
            return redirect("course_list")
    return render(request, "course/form.html", {"form": form, "title": "Kursni tahrirlash"})


@login_required(login_url="login")
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        messages.success(request, "Kurs muvaffaqiyatli o'chirildi")
        return redirect("course_list")
    return render(request, "course/delete.html", {"object": course, "title": "Kursni o'chirish"})


@login_required(login_url="login")
def group_list(request):
    groups = Group.objects.select_related("course").annotate(
        student_count=Count("students")
    ).order_by("-created_at")
    return render(request, "group/list.html", {"groups": groups})


@login_required(login_url="login")
def group_create(request):
    form = GroupForm()
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Guruh muvaffaqiyatli qo'shildi")
            return redirect("group_list")
    return render(request, "group/form.html", {"form": form, "title": "Guruh qo'shish"})


@login_required(login_url="login")
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    form = GroupForm(instance=group)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Guruh muvaffaqiyatli yangilandi")
            return redirect("group_list")
    return render(request, "group/form.html", {"form": form, "title": "Guruhni tahrirlash"})


@login_required(login_url="login")
def group_delete(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.delete()
        messages.success(request, "Guruh muvaffaqiyatli o'chirildi")
        return redirect("group_list")
    return render(request, "group/delete.html", {"object": group, "title": "Guruhni o'chirish"})


@login_required(login_url="login")
def group_extend(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        days = request.POST.get("days")
        if days and days.isdigit() and int(days) > 0:
            from datetime import timedelta
            group.end_date += timedelta(days=int(days))
            group.save()
            messages.success(request, f"Guruh muddati {days} kunga uzaytirildi")
            return redirect("group_detail", pk=group.pk)
        messages.error(request, "Kunlar sonini to'g'ri kiriting")
    return render(request, "group/extend.html", {"group": group})


@login_required(login_url="login")
def student_list(request):
    students = Student.objects.select_related("group", "marketing_survey").order_by("-created_at")
    return render(request, "student/list.html", {"students": students})


@login_required(login_url="login")
def student_create(request):
    form = StudentCreateForm()
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            if student.group:
                messages.success(request, f"O'quvchi {student.group.name} guruhiga qo'shildi")
                return redirect("group_detail", pk=student.group.pk)
            else:
                messages.success(request, "O'quvchi kutilyotganlar ro'yxatiga qo'shildi")
                return redirect("pending_students")
    return render(request, "student/form.html", {"form": form, "title": "O'quvchi qo'shish"})


@login_required(login_url="login")
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentEditForm(instance=student)
    if request.method == "POST":
        form = StudentEditForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "O'quvchi muvaffaqiyatli yangilandi")
            return redirect("student_list")
    return render(request, "student/form.html", {"form": form, "title": "O'quvchini tahrirlash"})


@login_required(login_url="login")
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        messages.success(request, "O'quvchi muvaffaqiyatli o'chirildi")
        return redirect("student_list")
    return render(request, "student/delete.html", {"object": student, "title": "O'quvchini o'chirish"})


@login_required(login_url="login")
def pending_students(request):
    students = Student.objects.filter(group__isnull=True, status="kutilyotgan").select_related("marketing_survey").order_by("-created_at")
    return render(request, "student/pending.html", {"students": students})


@login_required(login_url="login")
def group_detail(request, pk):
    group = get_object_or_404(Group.objects.annotate(
        total_students=Count("students")
    ).select_related("course").prefetch_related("lesson_times"), pk=pk)
    students = group.students.all()
    pending = Student.objects.filter(group__isnull=True, status="kutilyotgan")
    return render(request, "group/detail.html", {
        "group": group,
        "students": students,
        "pending": pending,
    })


@login_required(login_url="login")
def add_student_to_group(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    student.group = group
    student.frozen_until = None
    student.status = "kutilyotgan"
    student.save()
    StudentLog.objects.create(
        student=student, group=group, action="joined",
        reason="Guruh sahifasidan qo'shildi"
    )
    messages.success(request, f"{student.first_name} {student.last_name} guruhga qo'shildi")
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def remove_student_from_group(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    student.group = None
    student.frozen_until = None
    student.status = "chiqarilgan"
    student.save()
    StudentLog.objects.create(
        student=student, group=group, action="removed",
        reason="Guruh sahifasidan chiqarildi"
    )
    messages.success(request, f"{student.first_name} {student.last_name} guruhdan chiqarildi")
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    logs = student.logs.select_related("group").all()
    groups = Group.objects.filter(status="aktiv").order_by("name")
    return render(request, "student/profile.html", {
        "student": student, "logs": logs, "groups": groups,
    })


@login_required(login_url="login")
def student_freeze(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = FreezeForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data["days"]
            reason = form.cleaned_data["reason"]
            student.frozen_until = date.today() + timedelta(days=days)
            student.save(update_fields=["frozen_until"])
            StudentLog.objects.create(
                student=student, group=student.group, action="frozen",
                reason=f"{days} kunga muzlatildi. {reason}" if reason else f"{days} kunga muzlatildi"
            )
            messages.success(request, f"{student.first_name} {student.last_name} {days} kunga muzlatildi")
            return redirect("student_profile", pk=student.pk)
    else:
        form = FreezeForm()
    return render(request, "student/freeze.html", {"form": form, "student": student})


@login_required(login_url="login")
def student_unfreeze(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.frozen_until = None
    student.save(update_fields=["frozen_until"])
    StudentLog.objects.create(
        student=student, group=student.group, action="unfrozen",
        reason="Muzlatish bekor qilindi"
    )
    messages.success(request, f"{student.first_name} {student.last_name} muzlatish bekor qilindi")
    return redirect("student_profile", pk=student.pk)


@login_required(login_url="login")
def student_remove_from_group(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = RemoveFromGroupForm(request.POST)
        if form.is_valid():
            reason = form.cleaned_data["reason"]
            group = student.group
            student.group = None
            student.frozen_until = None
            student.status = "chiqarilgan"
            student.save(update_fields=["group", "frozen_until", "status"])
            StudentLog.objects.create(
                student=student, group=group, action="removed", reason=reason
            )
            messages.success(request, f"{student.first_name} {student.last_name} guruhdan chiqarildi")
            if group:
                return redirect("group_detail", pk=group.pk)
            return redirect("student_profile", pk=student.pk)
    else:
        form = RemoveFromGroupForm()
    return render(request, "student/remove.html", {"form": form, "student": student})


@login_required(login_url="login")
def student_add_to_group(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = AddToGroupForm(request.POST)
        if form.is_valid():
            group = form.cleaned_data["group"]
            reason = form.cleaned_data["reason"]
            student.group = group
            student.frozen_until = None
            student.status = "kutilyotgan"
            student.save(update_fields=["group", "frozen_until", "status"])
            StudentLog.objects.create(
                student=student, group=group, action="joined", reason=reason or "Profil sahifasidan qo'shildi"
            )
            messages.success(request, f"{student.first_name} {student.last_name} {group.name} guruhiga qo'shildi")
            return redirect("group_detail", pk=group.pk)
    else:
        form = AddToGroupForm()
    return render(request, "student/add_to_group.html", {"form": form, "student": student})


@login_required(login_url="login")
def group_freeze(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        form = FreezeForm(request.POST)
        if form.is_valid():
            days = form.cleaned_data["days"]
            reason = form.cleaned_data["reason"]
            frozen_until = date.today() + timedelta(days=days)
            students = group.students.filter(
                Q(frozen_until__isnull=True) | Q(frozen_until__lt=date.today())
            )
            for student in students:
                student.frozen_until = frozen_until
                student.save(update_fields=["frozen_until"])
                StudentLog.objects.create(
                    student=student, group=group, action="frozen",
                    reason=f"Guruh bilan {days} kunga muzlatildi. {reason}" if reason else f"Guruh bilan {days} kunga muzlatildi"
                )
            messages.success(request, f"Guruh {days} kunga muzlatildi ({students.count()} ta o'quvchi)")
            return redirect("group_detail", pk=group.pk)
    else:
        form = FreezeForm()
    return render(request, "group/freeze.html", {"form": form, "group": group})


@login_required(login_url="login")
def group_close(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        students = group.students.all()
        for student in students:
            old_group = student.group
            student.group = None
            student.frozen_until = None
            student.status = "chiqarilgan"
            student.save()
            StudentLog.objects.create(
                student=student, group=old_group, action="removed",
                reason="Guruh yopildi"
            )
        group.status = "yopilgan"
        group.save()
        messages.success(request, f"Guruh yopildi va {students.count()} ta o'quvchi chiqarildi")
        return redirect("group_list")
    return render(request, "group/close.html", {"group": group})


@login_required(login_url="login")
def group_archive(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        group.status = "arxivlangan"
        group.save()
        messages.success(request, f"Guruh arxivlandi")
        return redirect("group_list")
    return render(request, "group/archive.html", {"group": group})


@login_required(login_url="login")
def group_settings(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(instance=group)
    lesson_form = LessonTimeForm()
    lesson_times = group.lesson_times.all()

    if request.method == "POST":
        if "update_group" in request.POST:
            group_form = GroupForm(request.POST, instance=group)
            if group_form.is_valid():
                group_form.save()
                messages.success(request, "Guruh sozlamalari saqlandi")
                return redirect("group_settings", pk=group.pk)
        elif "add_lesson" in request.POST:
            lesson_form = LessonTimeForm(request.POST)
            if lesson_form.is_valid():
                lesson = lesson_form.save(commit=False)
                lesson.group = group
                lesson.save()
                messages.success(request, "Dars vaqti qo'shildi")
                return redirect("group_settings", pk=group.pk)
        elif "delete_lesson" in request.POST:
            lesson_id = request.POST.get("lesson_id")
            if lesson_id:
                LessonTime.objects.filter(pk=lesson_id, group=group).delete()
                messages.success(request, "Dars vaqti o'chirildi")
                return redirect("group_settings", pk=group.pk)

    return render(request, "group/settings.html", {
        "group": group,
        "group_form": group_form,
        "lesson_form": lesson_form,
        "lesson_times": lesson_times,
    })


@login_required(login_url="login")
def statistics(request):
    total_courses = Course.objects.count()
    total_groups = Group.objects.count()
    total_students = Student.objects.count()
    total_surveys = MarketingSurvey.objects.count()
    pending_students = Student.objects.filter(group__isnull=True, status="kutilyotgan").count()
    active_groups = Group.objects.filter(status="aktiv").count()
    pending_groups_count = Group.objects.filter(status="kutilyotgan").count()
    online_groups = Group.objects.filter(education_type="onlayn").count()
    offline_groups = Group.objects.filter(education_type="oflayn").count()
    toq_groups = Group.objects.filter(day_type="toq").count()
    juft_groups = Group.objects.filter(day_type="juft").count()
    har_kun_groups = Group.objects.filter(day_type="har_kun").count()

    group_students = Group.objects.annotate(count=Count("students")).values("name", "count")
    survey_stats = MarketingSurvey.objects.annotate(
        count=Count("students")
    ).order_by("-count")
    total_survey_students = sum(s.count for s in survey_stats)

    recent_students = Student.objects.select_related("group", "marketing_survey").order_by("-created_at")[:10]

    return render(request, "statistics.html", {
        "total_courses": total_courses,
        "total_groups": total_groups,
        "total_students": total_students,
        "total_surveys": total_surveys,
        "pending_students": pending_students,
        "active_groups": active_groups,
        "pending_groups_count": pending_groups_count,
        "online_groups": online_groups,
        "offline_groups": offline_groups,
        "toq_groups": toq_groups,
        "juft_groups": juft_groups,
        "har_kun_groups": har_kun_groups,
        "group_students": group_students,
        "survey_stats": survey_stats,
        "total_survey_students": total_survey_students,
        "recent_students": recent_students,
    })


@login_required(login_url="login")
def survey_list(request):
    surveys = MarketingSurvey.objects.annotate(
        student_count=Count("students")
    ).order_by("-created_at")
    return render(request, "survey/list.html", {"surveys": surveys})


@login_required(login_url="login")
def survey_create(request):
    form = MarketingSurveyForm()
    if request.method == "POST":
        form = MarketingSurveyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "So'rovnoma muvaffaqiyatli qo'shildi")
            return redirect("survey_list")
    return render(request, "survey/form.html", {"form": form, "title": "So'rovnoma qo'shish"})


@login_required(login_url="login")
def survey_update(request, pk):
    survey = get_object_or_404(MarketingSurvey, pk=pk)
    form = MarketingSurveyForm(instance=survey)
    if request.method == "POST":
        form = MarketingSurveyForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            messages.success(request, "So'rovnoma muvaffaqiyatli yangilandi")
            return redirect("survey_list")
    return render(request, "survey/form.html", {"form": form, "title": "So'rovnomani tahrirlash"})


@login_required(login_url="login")
def survey_delete(request, pk):
    survey = get_object_or_404(MarketingSurvey, pk=pk)
    if request.method == "POST":
        survey.delete()
        messages.success(request, "So'rovnoma muvaffaqiyatli o'chirildi")
        return redirect("survey_list")
    return render(request, "survey/delete.html", {"object": survey, "title": "So'rovnomani o'chirish"})
