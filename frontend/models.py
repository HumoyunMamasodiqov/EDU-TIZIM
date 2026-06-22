from django.db import models
from datetime import date, timedelta


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kurs nomi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"


class MarketingSurvey(models.Model):
    name = models.CharField(max_length=255, verbose_name="So'rovnoma turi")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Marketing so'rovnoma"
        verbose_name_plural = "Marketing so'rovnomalar"


class Group(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "aktiv", "Aktiv"
        PENDING = "kutilyotgan", "Kutilyotgan"
        CLOSED = "yopilgan", "Yopilgan"
        ARCHIVED = "arxivlangan", "Arxivlangan"

    class EducationType(models.TextChoices):
        ONLINE = "onlayn", "Onlayn"
        OFFLINE = "oflayn", "Oflayn"

    class DayType(models.TextChoices):
        ODD = "toq", "Toq kunlar"
        EVEN = "juft", "Juft kunlar"
        EVERYDAY = "har_kun", "Har kunlik"

    name = models.CharField(max_length=255, verbose_name="Guruh nomi")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Guruh holati",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="groups", verbose_name="Kurs"
    )
    education_type = models.CharField(
        max_length=20,
        choices=EducationType.choices,
        default=EducationType.OFFLINE,
        verbose_name="Ta'lim turi",
    )
    day_type = models.CharField(
        max_length=20,
        choices=DayType.choices,
        default=DayType.EVERYDAY,
        verbose_name="Dars kunlari turi",
    )
    days = models.CharField(max_length=255, blank=True, null=True, verbose_name="Kunlarni yozing")
    telegram_link = models.URLField(blank=True, null=True, verbose_name="Telegram guruh havolasi")
    start_date = models.DateField(verbose_name="Boshlanish sanasi")
    end_date = models.DateField(verbose_name="Tugash sanasi")
    created_at = models.DateTimeField(auto_now_add=True)

    def is_ending_soon(self):
        if not self.end_date:
            return False
        remaining = (self.end_date - date.today()).days
        return 0 <= remaining <= 7

    def remaining_days(self):
        if not self.end_date:
            return None
        return (self.end_date - date.today()).days

    @property
    def frozen_students_count(self):
        return self.students.filter(frozen_until__gte=date.today()).count()

    def __str__(self):
        return f"{self.name} ({self.course.name})"

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"


class Student(models.Model):
    class Status(models.TextChoices):
        PENDING = "kutilyotgan", "Kutilyotgan"
        REMOVED = "chiqarilgan", "Chiqarilgan"

    first_name = models.CharField(max_length=255, verbose_name="Ism")
    last_name = models.CharField(max_length=255, verbose_name="Familya")
    phone = models.CharField(max_length=20, verbose_name="Telefon raqam")
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, related_name="students", verbose_name="Guruh"
    )
    frozen_until = models.DateField(null=True, blank=True, verbose_name="Muzlatish tugash sanasi")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Holati",
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="Tug'ilgan sana")
    marketing_survey = models.ForeignKey(
        MarketingSurvey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="Marketing so'rovnoma",
    )
    additional_info = models.TextField(blank=True, null=True, verbose_name="Qo'shimcha ma'lumotlar")
    father_full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Otasining ism familya")
    father_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Otasining nomeri")
    mother_full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Onasining ism familya")
    mother_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Onasining nomeri")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_frozen(self):
        if not self.frozen_until:
            return False
        return self.frozen_until >= date.today()

    @property
    def frozen_remaining_days(self):
        if not self.frozen_until:
            return 0
        remaining = (self.frozen_until - date.today()).days
        return max(remaining, 0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"


class LessonTime(models.Model):
    DAY_CHOICES = [
        ("dushanba", "Dushanba"),
        ("seshanba", "Seshanba"),
        ("chorshanba", "Chorshanba"),
        ("payshanba", "Payshanba"),
        ("juma", "Juma"),
        ("shanba", "Shanba"),
        ("yakshanba", "Yakshanba"),
    ]

    DAY_ORDER = {d[0]: i for i, d in enumerate(DAY_CHOICES)}

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="lesson_times", verbose_name="Guruh"
    )
    days = models.CharField(max_length=255, verbose_name="Hafta kunlari")
    start_time = models.TimeField(verbose_name="Boshlanish vaqti")
    end_time = models.TimeField(verbose_name="Tugash vaqti")

    def get_days_display(self):
        day_map = dict(self.DAY_CHOICES)
        selected = [d.strip() for d in self.days.split(",") if d.strip()]
        return ", ".join(day_map.get(d, d) for d in selected)

    def __str__(self):
        return f"{self.get_days_display()} {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"

    class Meta:
        verbose_name = "Dars vaqti"
        verbose_name_plural = "Dars vaqtlari"
        ordering = ["start_time"]


class StudentLog(models.Model):
    class Action(models.TextChoices):
        JOINED = "joined", "Guruhga qo'shildi"
        REMOVED = "removed", "Guruhdan chiqarildi"
        FROZEN = "frozen", "Muzlatildi"
        UNFROZEN = "unfrozen", "Muzlatish bekor qilindi"

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="logs", verbose_name="O'quvchi"
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Guruh"
    )
    action = models.CharField(max_length=20, choices=Action.choices, verbose_name="Harakat")
    reason = models.TextField(blank=True, null=True, verbose_name="Sabab")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.get_action_display()}"

    class Meta:
        verbose_name = "O'quvchi harakati"
        verbose_name_plural = "O'quvchi harakatlari"
        ordering = ["-created_at"]
