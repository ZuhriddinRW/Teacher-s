from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import DateInput


from .models import Teacher, GroupStudent, Student, RateStudent, Course, PayStudent, RatingStudent, Sms


class ContentForm(forms.Form):
    subject = forms.CharField(label='Mavzu:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class ExampleForm(forms.Form):
    my_date_field = forms.DateField(widget=DateInput)


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control  '}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='login', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=' Add password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class InfoTeacherForm(forms.ModelForm):
    lastname = forms.CharField(label='Familya:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    middleName = forms.CharField(label='Otasining ismi', widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.DateField(label='Yili', widget=DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=13, label='Phone', widget=DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Teacher
        fields = ('lastname', 'middleName', 'year', 'phone')


class GroupForm(forms.ModelForm):
    groupName = forms.CharField(label='Guruh nomi:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    startTime = forms.DateField(label='Ochilgan vaqti', widget=DateInput(attrs={'class': 'form-control'}))
    finishTime = forms.DateField(label='Tugash vaqti', widget=DateInput(attrs={'class': 'form-control'}))
    time = forms.TimeField(widget=TimeInput, )

    class Meta:
        model = GroupStudent
        fields = ('groupName', 'startTime', 'finishTime', 'time', 'teacher', 'status', 'day', 'course')


class StudentForm(forms.ModelForm):
    username = forms.CharField(label='Ismi:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(label='Familyasi:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    middleName = forms.CharField(label='Otasining ismi:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.DateField(label='To"g"ilgan Yili', widget=DateInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=13, label='Phone', widget=DateInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Student
        fields = ('username', 'lastname', 'middleName', 'year', 'phone', 'group')


class RateForm(forms.ModelForm):
    class Meta:
        model = RateStudent
        fields = ('student', 'month',)


class CourseForm(forms.ModelForm):
    name = forms.CharField(label='Kurs nomi:', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Course
        fields = ('name',)


class PayStudentForm(forms.ModelForm):
    text = forms.CharField(label='Izoh', widget=forms.TextInput(attrs={'class': 'form-control'}))
    money = forms.IntegerField(label='Pul miqdori', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PayStudent
        fields = ('money', 'text',)


class RatingStudentForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=100, min_value=0)

    class Meta:
        model = RatingStudent
        fields = ('rating',)


class ContactForm(forms.ModelForm):
    subject = forms.CharField(label='Mavzu:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Text', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))

    class Meta:
        model = Sms
        fields = ('subject', 'content')
