from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from datetime import date, timedelta
from .models import Course, Group, Student, MarketingSurvey, StudentLog, LessonTime, Branch, Room, Role, Position, Employee
from .forms import LoginForm, CourseForm, GroupForm, StudentCreateForm, StudentEditForm, MarketingSurveyForm, FreezeForm, RemoveFromGroupForm, AddToGroupForm, LessonTimeForm, BranchForm, RoomForm, RoleForm, PositionForm, EmployeeForm


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
    pending_student_count = Student.objects.filter(groups__isnull=True, status="kutilyotgan").count()
    recent_students = Student.objects.prefetch_related("groups").order_by("-created_at")[:5]
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
    status = request.GET.get("status")
    day = request.GET.get("day")
    day_type = request.GET.get("day_type")
    time_from = request.GET.get("time_from")
    time_to = request.GET.get("time_to")
    course_id = request.GET.get("course")
    teacher_id = request.GET.get("teacher")
    room_id = request.GET.get("room")
    search = request.GET.get("search")

    if status == "arxivlangan":
        status_filter = ["arxivlangan"]
        page_title = "Arxivlangan guruhlar"
    else:
        status_filter = ["aktiv", "kutilyotgan"]
        page_title = "Oddiy guruhlar"

    groups = Group.objects.select_related("course", "room", "teacher").prefetch_related(
        "lesson_times"
    ).annotate(
        student_count=Count("students")
    ).filter(status__in=status_filter)

    if day_type:
        groups = groups.filter(day_type=day_type)

    if day:
        groups = groups.filter(lesson_times__days__contains=day)

    if time_from:
        groups = groups.filter(lesson_times__start_time__gte=time_from)

    if time_to:
        groups = groups.filter(lesson_times__end_time__lte=time_to)

    if course_id:
        groups = groups.filter(course_id=course_id)

    if teacher_id:
        groups = groups.filter(teacher_id=teacher_id)

    if room_id:
        groups = groups.filter(room_id=room_id)

    if search:
        groups = groups.filter(name__icontains=search)

    groups = groups.distinct().order_by("-created_at")

    courses = Course.objects.all()
    teachers = Employee.objects.filter(role__name="O'qituvchi")
    rooms = Room.objects.all()

    return render(request, "group/list.html", {
        "groups": groups,
        "page_title": page_title,
        "courses": courses,
        "teachers": teachers,
        "rooms": rooms,
    })


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
    students = Student.objects.prefetch_related("groups", "marketing_survey").order_by("-created_at")
    return render(request, "student/list.html", {"students": students})


@login_required(login_url="login")
def student_create(request):
    form = StudentCreateForm()
    if request.method == "POST":
        form = StudentCreateForm(request.POST)
        if form.is_valid():
            student = form.save()
            groups = form.cleaned_data.get("groups")
            if groups:
                student.groups.set(groups)
                first_group = groups[0]
                messages.success(request, f"O'quvchi {first_group.name} guruhiga qo'shildi")
                return redirect("group_detail", pk=first_group.pk)
            else:
                messages.success(request, "O'quvchi kutilyotganlar ro'yxatiga qo'shildi")
                return redirect("pending_students")
    else:
        initial_group = request.GET.get("group")
        if initial_group:
            form = StudentCreateForm(initial={"groups": [initial_group]})
    group_data = list(Group.objects.filter(status__in=["aktiv", "kutilyotgan"]).values("pk", "name", "course_id"))
    return render(request, "student/form.html", {"form": form, "title": "O'quvchi qo'shish", "group_data": group_data})


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
    group_data = list(Group.objects.filter(status__in=["aktiv", "kutilyotgan"]).values("pk", "name", "course_id"))
    return render(request, "student/form.html", {"form": form, "title": "O'quvchini tahrirlash", "group_data": group_data})


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
    students = Student.objects.filter(groups__isnull=True, status="kutilyotgan").select_related("marketing_survey", "desired_course").order_by("desired_course__name", "-created_at")
    return render(request, "student/pending.html", {"students": students})


@login_required(login_url="login")
def group_detail(request, pk):
    group = get_object_or_404(Group.objects.annotate(
        total_students=Count("students")
    ).select_related("course", "room", "teacher").prefetch_related("lesson_times"), pk=pk)
    students = group.students.all()
    q = request.GET.get("q", "").strip()
    all_students = Student.objects.exclude(pk__in=students.values_list("pk", flat=True))
    if q:
        all_students = all_students.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(phone__endswith=q)
        )
    all_students = all_students.prefetch_related("groups").order_by("-created_at")
    pending_students = Student.objects.filter(
        groups__isnull=True, status="kutilyotgan"
    ).select_related("desired_course").prefetch_related("groups").order_by("-created_at")
    courses = Course.objects.all()
    removed_logs = StudentLog.objects.filter(group=group, action="removed").select_related("student").order_by("-created_at")[:50]
    return render(request, "group/detail.html", {
        "group": group,
        "students": students,
        "all_students": all_students,
        "pending_students": pending_students,
        "removed_logs": removed_logs,
        "courses": courses,
        "q": q,
    })


def _add_student_to_group(student, group, reason="Guruh sahifasidan qo'shildi"):
    if group in student.groups.all():
        return False
    student.groups.add(group)
    student.frozen_until = None
    student.status = "kutilyotgan"
    student.save(update_fields=["frozen_until", "status"])
    StudentLog.objects.create(
        student=student, group=group, action="joined", reason=reason
    )
    return True


@login_required(login_url="login")
def add_student_to_group(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    if not _add_student_to_group(student, group):
        messages.warning(request, f"{student.first_name} {student.last_name} allaqachon {group.name} guruhiga qo'shilgan!")
        return redirect("group_detail", pk=group_pk)
    messages.success(request, f"{student.first_name} {student.last_name} {group.name} guruhiga qo'shildi")
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def add_pending_to_group(request, group_pk, course_pk):
    group = get_object_or_404(Group, pk=group_pk)
    course = get_object_or_404(Course, pk=course_pk)
    students = Student.objects.filter(groups__isnull=True, status="kutilyotgan", desired_course=course)
    count = 0
    for student in students:
        if _add_student_to_group(student, group, f"{group.name} guruhiga kurs bo'yicha qo'shildi"):
            count += 1
    if count:
        messages.success(request, f"{count} ta o'quvchi {group.name} guruhiga qo'shildi")
    else:
        messages.info(request, "Qo'shiladigan o'quvchi topilmadi")
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def remove_student_from_group(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        if not reason:
            messages.error(request, "Chiqarish sababini yozing!")
            return redirect("group_detail", pk=group_pk)
        student.groups.remove(group)
        student.frozen_until = None
        student.status = "chiqarilgan"
        student.save(update_fields=["frozen_until", "status"])
        group_count = student.groups.count()
        if group_count == 0:
            student.status = "chiqarilgan"
            student.save(update_fields=["status"])
        StudentLog.objects.create(
            student=student, group=group, action="removed", reason=reason
        )
        messages.success(request, f"{student.first_name} {student.last_name} guruhdan chiqarildi")
        return redirect("group_detail", pk=group_pk)
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def graduate_student(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    if group not in student.groups.all():
        messages.warning(request, f"{student.first_name} {student.last_name} bu guruhda emas!")
        return redirect("group_detail", pk=group_pk)
    if group in student.graduated_groups.all():
        messages.warning(request, f"{student.first_name} {student.last_name} allaqachon {group.name} dan bitirilgan!")
        return redirect("group_detail", pk=group_pk)
    student.groups.remove(group)
    student.graduated_groups.add(group)
    StudentLog.objects.create(
        student=student, group=group, action="graduated",
        reason=f"{group.name} guruhini bitirdi"
    )
    messages.success(request, f"{student.first_name} {student.last_name} {group.name} guruhini bitirdi!")
    return redirect("group_detail", pk=group_pk)


@login_required(login_url="login")
def transfer_student(request, group_pk, student_pk):
    group = get_object_or_404(Group, pk=group_pk)
    student = get_object_or_404(Student, pk=student_pk)
    if group not in student.groups.all():
        messages.warning(request, f"{student.first_name} {student.last_name} bu guruhda emas!")
        return redirect("group_detail", pk=group_pk)

    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        new_group_id = request.POST.get("new_group")
        if new_group_id == "pending":
            old_name = group.name
            student.groups.remove(group)
            student.frozen_until = None
            student.status = "kutilyotgan"
            student.save(update_fields=["frozen_until", "status"])
            StudentLog.objects.create(
                student=student, group=group, action="transferred",
                reason=reason or f"{old_name} → Kutilyotganlar"
            )
            messages.success(request, f"{student.first_name} {student.last_name} {old_name} dan kutilyotganlarga o'tkazildi!")
            return redirect("pending_students")
        if not new_group_id:
            messages.error(request, "Yangi guruhni tanlang!")
            return redirect("transfer_student", group_pk=group_pk, student_pk=student_pk)
        new_group = get_object_or_404(Group, pk=new_group_id)
        trans_info = f"{group.name} → {new_group.name}"
        full_reason = f"{reason} | {trans_info}" if reason else trans_info
        student.groups.remove(group)
        student.groups.add(new_group)
        student.frozen_until = None
        student.status = "kutilyotgan"
        student.save(update_fields=["frozen_until", "status"])
        StudentLog.objects.create(
            student=student, group=group, action="transferred",
            reason=full_reason
        )
        messages.success(request, f"{student.first_name} {student.last_name} {group.name} dan {new_group.name} ga o'tkazildi!")
        return redirect("group_detail", pk=new_group.pk)

    course_id = request.GET.get("course_id")
    teacher_id = request.GET.get("teacher_id")

    courses = Course.objects.all().order_by("name")
    teachers = Employee.objects.none()
    groups = Group.objects.none()

    if course_id:
        teachers = Employee.objects.filter(
            role__name="O'qituvchi",
            teacher_groups__course_id=course_id
        ).exclude(teacher_groups__isnull=True).distinct().order_by("first_name")

    if teacher_id and course_id:
        groups = Group.objects.filter(
            status__in=["aktiv", "kutilyotgan"],
            course_id=course_id,
            teacher_id=teacher_id,
        ).exclude(pk=group.pk).select_related(
            "course", "room", "teacher"
        ).prefetch_related("lesson_times").order_by("name")

    return render(request, "student/transfer.html", {
        "student": student,
        "group": group,
        "courses": courses,
        "teachers": teachers,
        "groups": groups,
        "selected_course_id": course_id,
        "selected_teacher_id": teacher_id,
    })


@login_required(login_url="login")
def transfer_all_students(request, pk):
    group = get_object_or_404(Group, pk=pk)
    students = group.students.all()
    if request.method == "POST":
        reason = request.POST.get("reason", "").strip()
        new_group_id = request.POST.get("new_group")
        if not new_group_id or new_group_id == "pending":
            messages.error(request, "Yangi guruhni tanlang!")
            return redirect("transfer_all_students", pk=pk)
        new_group = get_object_or_404(Group, pk=new_group_id)
        trans_info = f"{group.name} → {new_group.name}"
        full_reason = f"{reason} | {trans_info}" if reason else trans_info
        count = 0
        for student in students:
            student.groups.remove(group)
            student.groups.add(new_group)
            student.frozen_until = None
            student.status = "kutilyotgan"
            student.save(update_fields=["frozen_until", "status"])
            StudentLog.objects.create(
                student=student, group=group, action="transferred",
                reason=full_reason
            )
            count += 1
        messages.success(request, f"{count} ta o'quvchi {group.name} dan {new_group.name} ga o'tkazildi!")
        return redirect("group_detail", pk=new_group.pk)
    course_id = request.GET.get("course_id")
    teacher_id = request.GET.get("teacher_id")
    courses = Course.objects.all().order_by("name")
    teachers = Employee.objects.none()
    groups = Group.objects.none()
    if course_id:
        teachers = Employee.objects.filter(
            role__name="O'qituvchi", teacher_groups__course_id=course_id
        ).exclude(teacher_groups__isnull=True).distinct().order_by("first_name")
    if teacher_id and course_id:
        groups = Group.objects.filter(
            status__in=["aktiv", "kutilyotgan"],
            course_id=course_id, teacher_id=teacher_id,
        ).exclude(pk=group.pk).select_related("course", "room", "teacher"
        ).prefetch_related("lesson_times").annotate(
            student_count=Count("students")
        ).order_by("name")
    return render(request, "group/transfer_all.html", {
        "group": group, "students": students, "courses": courses,
        "teachers": teachers, "groups": groups,
        "selected_course_id": course_id, "selected_teacher_id": teacher_id,
    })


@login_required(login_url="login")
def graduated_students(request):
    students = Student.objects.filter(graduated_groups__isnull=False).prefetch_related(
        "graduated_groups", "groups"
    ).distinct().order_by("-created_at")
    return render(request, "student/graduated.html", {"students": students})


@login_required(login_url="login")
def student_profile(request, pk):
    student = get_object_or_404(Student.objects.prefetch_related("groups", "graduated_groups"), pk=pk)
    logs = list(student.logs.select_related("group").all())
    import re
    for log in logs:
        log.target_name = None
        if log.action == "transferred" and log.reason:
            m = re.search(r"→\s*(.+?)$", log.reason)
            if m:
                log.target_name = m.group(1).strip()
            if not log.target_name:
                m = re.search(r"\bdan\b\s+(.+?)\s+ga\s+o'tkazildi", log.reason)
                if m:
                    log.target_name = m.group(1).strip()
            if not log.target_name and re.search(r"\bkutilyotgan", log.reason, re.I):
                log.target_name = "Kutilyotganlar"
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
                student=student, group=student.groups.first(), action="frozen",
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
        student=student, group=student.groups.first(), action="unfrozen",
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
            group = student.groups.first()
            student.groups.clear()
            student.frozen_until = None
            student.status = "chiqarilgan"
            student.save(update_fields=["frozen_until", "status"])
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
            if group in student.groups.all():
                messages.warning(request, f"{student.first_name} {student.last_name} allaqachon {group.name} guruhiga qo'shilgan!")
                return redirect("student_profile", pk=student.pk)
            reason = form.cleaned_data["reason"]
            student.groups.add(group)
            student.frozen_until = None
            student.status = "kutilyotgan"
            student.save(update_fields=["frozen_until", "status"])
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
def group_archive(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        students = group.students.all()
        for student in students:
            student.groups.remove(group)
            student.graduated_groups.add(group)
            student.frozen_until = None
            student.status = "bitirilgan"
            student.save(update_fields=["frozen_until", "status"])
            StudentLog.objects.create(
                student=student, group=group, action="graduated",
                reason=f"{group.name} guruhi arxivlandi"
            )
        group.status = "arxivlangan"
        group.save()
        messages.success(request, f"Guruh arxivlandi va {students.count()} ta o'quvchi bitirildi")
        return redirect("group_list")
    return render(request, "group/archive.html", {"group": group})


@login_required(login_url="login")
def group_settings(request, pk):
    group = get_object_or_404(Group, pk=pk)
    group_form = GroupForm(instance=group)
    lesson_form = LessonTimeForm(group=group)
    lesson_times = group.lesson_times.all()

    if request.method == "POST":
        if "update_group" in request.POST:
            group_form = GroupForm(request.POST, instance=group)
            if group_form.is_valid():
                group_form.save()
                messages.success(request, "Guruh sozlamalari saqlandi")
                return redirect("group_settings", pk=group.pk)
        elif "add_lesson" in request.POST:
            lesson_form = LessonTimeForm(request.POST, group=group)
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
def employee_list(request):
    employees = Employee.objects.select_related("position", "role").all().order_by("-created_at")
    return render(request, "employee/list.html", {"employees": employees})


@login_required(login_url="login")
def employee_create(request):
    form = EmployeeForm()
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            password = form.cleaned_data.get("password")
            if password:
                user = User.objects.create_user(
                    username=employee.phone,
                    password=password,
                    first_name=employee.first_name,
                    last_name=employee.last_name,
                )
                employee.user = user
            employee.save()
            form.save_m2m()
            messages.success(request, "Xodim muvaffaqiyatli qo'shildi")
            return redirect("employee_list")
    return render(request, "employee/create.html", {"form": form})


@login_required(login_url="login")
def branch_list(request):
    branches = Branch.objects.all().order_by("-created_at")
    return render(request, "branch/list.html", {"branches": branches})


@login_required(login_url="login")
def branch_create(request):
    form = BranchForm()
    if request.method == "POST":
        form = BranchForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Filial muvaffaqiyatli qo'shildi")
            return redirect("branch_list")
    return render(request, "branch/form.html", {"form": form, "title": "Filial qo'shish"})


@login_required(login_url="login")
def branch_update(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    form = BranchForm(instance=branch)
    if request.method == "POST":
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            messages.success(request, "Filial muvaffaqiyatli yangilandi")
            return redirect("branch_list")
    return render(request, "branch/form.html", {"form": form, "title": "Filialni tahrirlash"})


@login_required(login_url="login")
def branch_delete(request, pk):
    branch = get_object_or_404(Branch, pk=pk)
    if request.method == "POST":
        branch.delete()
        messages.success(request, "Filial muvaffaqiyatli o'chirildi")
        return redirect("branch_list")
    return render(request, "branch/delete.html", {"object": branch, "title": "Filialni o'chirish"})


@login_required(login_url="login")
def room_list(request):
    rooms = Room.objects.all().order_by("-created_at")
    return render(request, "room/list.html", {"rooms": rooms})


@login_required(login_url="login")
def room_create(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Xona muvaffaqiyatli qo'shildi")
            return redirect("room_list")
    return render(request, "room/form.html", {"form": form, "title": "Xona qo'shish"})


@login_required(login_url="login")
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(instance=room)
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Xona muvaffaqiyatli yangilandi")
            return redirect("room_list")
    return render(request, "room/form.html", {"form": form, "title": "Xonani tahrirlash"})


@login_required(login_url="login")
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == "POST":
        room.delete()
        messages.success(request, "Xona muvaffaqiyatli o'chirildi")
        return redirect("room_list")
    return render(request, "room/delete.html", {"object": room, "title": "Xonani o'chirish"})


@login_required(login_url="login")
def role_list(request):
    roles = Role.objects.all().order_by("-created_at")
    return render(request, "role/list.html", {"roles": roles})


@login_required(login_url="login")
def role_create(request):
    form = RoleForm()
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol muvaffaqiyatli qo'shildi")
            return redirect("role_list")
    return render(request, "role/form.html", {"form": form, "title": "Rol qo'shish"})


@login_required(login_url="login")
def role_update(request, pk):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(instance=role)
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, "Rol muvaffaqiyatli yangilandi")
            return redirect("role_list")
    return render(request, "role/form.html", {"form": form, "title": "Rolni tahrirlash"})


@login_required(login_url="login")
def role_delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    if request.method == "POST":
        role.delete()
        messages.success(request, "Rol muvaffaqiyatli o'chirildi")
        return redirect("role_list")
    return render(request, "role/delete.html", {"object": role, "title": "Rolni o'chirish"})


@login_required(login_url="login")
def position_list(request):
    positions = Position.objects.all().order_by("-created_at")
    return render(request, "position/list.html", {"positions": positions})


@login_required(login_url="login")
def position_create(request):
    form = PositionForm()
    if request.method == "POST":
        form = PositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vazifa muvaffaqiyatli qo'shildi")
            return redirect("position_list")
    return render(request, "position/form.html", {"form": form, "title": "Vazifa qo'shish"})


@login_required(login_url="login")
def position_update(request, pk):
    position = get_object_or_404(Position, pk=pk)
    form = PositionForm(instance=position)
    if request.method == "POST":
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            form.save()
            messages.success(request, "Vazifa muvaffaqiyatli yangilandi")
            return redirect("position_list")
    return render(request, "position/form.html", {"form": form, "title": "Vazifani tahrirlash"})


@login_required(login_url="login")
def position_delete(request, pk):
    position = get_object_or_404(Position, pk=pk)
    if request.method == "POST":
        position.delete()
        messages.success(request, "Vazifa muvaffaqiyatli o'chirildi")
        return redirect("position_list")
    return render(request, "position/delete.html", {"object": position, "title": "Vazifani o'chirish"})


@login_required(login_url="login")
def statistics(request):
    total_courses = Course.objects.count()
    total_groups = Group.objects.count()
    total_students = Student.objects.count()
    total_surveys = MarketingSurvey.objects.count()
    pending_students = Student.objects.filter(groups__isnull=True, status="kutilyotgan").count()
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

    recent_students = Student.objects.prefetch_related("groups", "marketing_survey").order_by("-created_at")[:10]

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
