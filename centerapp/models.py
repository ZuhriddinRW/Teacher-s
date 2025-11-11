from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lastname = models.CharField(max_length=25)
    middleName = models.CharField(max_length=25)
    year = models.DateField(null=True)
    code = models.CharField(null=True, max_length=50)
    phone = models.CharField(null=True, blank=True, max_length=17)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('teacherView', 'viewTeacher', kwargs={"pk": self.pk})


class Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('teacherView', 'viewTeacher', kwargs={"pk": self.pk})


class GroupDay(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('courseUpdate, groupDelete, groupView', 'groupStudents',
                       kwargs={"pk": self.pk})


class GroupStudent(models.Model):
    groupName = models.CharField(max_length=25)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    startTime = models.DateField()
    finishTime = models.DateField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    day = models.ForeignKey(GroupDay, on_delete=models.CASCADE, null=True)
    time = models.TimeField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    inProgress = models.BooleanField(default=None, null=True)

    def __str__(self):
        return self.groupName

    def get_absolute_url(self):
        return reverse('groupUpdate, groupDelete, groupView', 'groupStudents',
                       kwargs={"pk": self.pk})


class Student(models.Model):
    username = models.CharField(max_length=40)
    lastname = models.CharField(max_length=40)
    middleName = models.CharField(max_length=40)
    year = models.DateField()
    phone = models.CharField(null=True, blank=True, max_length=17)
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class Months(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class RateStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    group = models.ForeignKey(GroupStudent, on_delete=models.CASCADE, null=True)
    bool = models.BooleanField(default=False)
    month = models.ForeignKey(Months, on_delete=models.CASCADE)
    text = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.student.username

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class PayStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    text = models.CharField(max_length=200, null=True)
    money = models.CharField(max_length=9, null=True)

    def __str__(self):
        return self.student.username

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class RatingStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    rating = models.CharField(max_length=3, null=True)

    def __str__(self):
        return self.student.username

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class VisitStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    visit = models.BooleanField(default=True)

    def __str__(self):
        return self.student.username

    def get_absolute_url(self):
        return reverse('studentUpdate, studentDelete, studentView', kwargs={"pk": self.pk})


class Advertising(models.Model):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    name = models.CharField(max_length=60)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Sms(models.Model):
    subject = models.CharField(max_length=100)
    content = models.CharField(max_length=5000)
    bool = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
