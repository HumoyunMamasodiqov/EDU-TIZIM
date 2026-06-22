from django import forms
from .models import Course, Group, Student, MarketingSurvey, LessonTime


class LoginForm(forms.Form):
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "placeholder": "XX XXX XX XX",
            "class": "form-control phone-input",
        }),
        label="Telefon raqam",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Parol", "class": "form-control"}),
        label="Parol",
    )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Kurs nomini kiriting"}),
        }


class GroupForm(forms.ModelForm):
    start_date = forms.DateField(
        input_formats=["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"],
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Sana: 22.06.2026", "autocomplete": "off"}, format="%d.%m.%Y"),
        label="Boshlanish sanasi",
    )
    end_date = forms.DateField(
        input_formats=["%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"],
        widget=forms.DateInput(attrs={"class": "form-control", "placeholder": "Sana: 22.06.2026", "autocomplete": "off"}, format="%d.%m.%Y"),
        label="Tugash sanasi",
    )

    class Meta:
        model = Group
        fields = ["name", "status", "course", "education_type", "day_type", "days", "telegram_link", "start_date", "end_date"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Guruh nomini kiriting"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "course": forms.Select(attrs={"class": "form-control"}),
            "education_type": forms.Select(attrs={"class": "form-control"}),
            "day_type": forms.Select(attrs={"class": "form-control"}),
            "days": forms.TextInput(attrs={"class": "form-control", "placeholder": "Misol: Dushanba, Chorshanba, Juma"}),
            "telegram_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://t.me/..."}),
        }


class StudentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["group"].required = False
        self.fields["group"].empty_label = "--- Kutilyotgan (guruhsiz) ---"

    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "phone", "group", "birth_date",
            "marketing_survey", "additional_info",
            "father_full_name", "father_phone",
            "mother_full_name", "mother_phone",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismini kiriting"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Familyasini kiriting"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
            "group": forms.Select(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "marketing_survey": forms.Select(attrs={"class": "form-control"}),
            "additional_info": forms.Textarea(attrs={"class": "form-control", "placeholder": "Qo'shimcha ma'lumotlar", "rows": 3}),
            "father_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Otasining ism familyasi"}),
            "father_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
            "mother_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Onasining ism familyasi"}),
            "mother_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
        }


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "first_name", "last_name", "phone", "group", "birth_date",
            "marketing_survey", "additional_info",
            "father_full_name", "father_phone",
            "mother_full_name", "mother_phone",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ismini kiriting"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Familyasini kiriting"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
            "group": forms.Select(attrs={"class": "form-control"}),
            "birth_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "marketing_survey": forms.Select(attrs={"class": "form-control"}),
            "additional_info": forms.Textarea(attrs={"class": "form-control", "placeholder": "Qo'shimcha ma'lumotlar", "rows": 3}),
            "father_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Otasining ism familyasi"}),
            "father_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
            "mother_full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Onasining ism familyasi"}),
            "mother_phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+998 XX XXX XX XX"}),
        }


class MarketingSurveyForm(forms.ModelForm):
    class Meta:
        model = MarketingSurvey
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "So'rovnoma turini kiriting (masalan: Banner orqali, Do'st taklif qildi)"}),
        }


class FreezeForm(forms.Form):
    days = forms.IntegerField(
        min_value=1, max_value=365,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Necha kun?", "min": 1, "max": 365}),
        label="Muzlatish muddati (kun)",
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Muzlatish sababi (ixtiyoriy)", "rows": 3}),
        label="Sabab",
    )


class RemoveFromGroupForm(forms.Form):
    reason = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Chiqarish sababini yozing", "rows": 3}),
        label="Chiqarish sababi",
    )


class LessonTimeForm(forms.ModelForm):
    days = forms.MultipleChoiceField(
        choices=LessonTime.DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={"class": "checkbox-group"}),
        label="Hafta kunlari",
    )

    class Meta:
        model = LessonTime
        fields = ["days", "start_time", "end_time"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}, format="%H:%M"),
            "end_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}, format="%H:%M"),
        }
        labels = {
            "start_time": "Boshlanish vaqti",
            "end_time": "Tugash vaqti",
        }

    def clean_days(self):
        days = self.cleaned_data["days"]
        return ",".join(days)


class AddToGroupForm(forms.Form):
    group = forms.ModelChoiceField(
        queryset=Group.objects.filter(status="aktiv"),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Guruhni tanlang",
        empty_label="--- Guruh tanlang ---",
    )
    reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Qo'shimcha izoh (ixtiyoriy)", "rows": 2}),
        label="Izoh",
    )
