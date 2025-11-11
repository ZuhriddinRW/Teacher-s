from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import Group
from django.urls import reverse
from django.views.generic import View

from .decorators import unauthenticated_user, admin_only
from .forms import UserLoginForm, InfoTeacherForm, GroupForm, StudentForm, RateForm, CourseForm, PayStudentForm, \
    RatingStudentForm, ContactForm
from django.contrib import messages
from django.http import HttpResponse

from .forms import UserRegisterForm
from .models import Teacher, GroupStudent, Student, Months, RateStudent, Course, PayStudent, RatingStudent, \
    VisitStudent, GroupDay, Status, Advertising, Sms
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render(request, 'temp/index.html')


def contact(request):
    return render(request, 'temp/contact.html')


def course(request):
    return render(request, 'temp/course.html')


# @unauthenticated_user
def adminUser(request):
    return render(request, 'admin/adminUser.html')


def logoutPage(request):
    logout(request)
    return redirect('login')



def loginPage(request):
    if request.method == 'POST':
        # print("salom ================================")
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('adminUser')
            messages.success(request, 'ok')
        else:
            messages.error(request, 'Username yoki parol xato qaytadan kiriting')
    form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def teacher(request):
    return render(request, 'teacher/teacher.html')


def createTeacher(request):
    if request.method == 'POST':
        profile_form = UserRegisterForm(data=request.POST)
        info_form = InfoTeacherForm(data=request.POST)
        if profile_form.is_valid() and info_form.is_valid():
            user = profile_form.save()
            code = profile_form.cleaned_data.get('password1')
            profile = info_form.save(commit=False)
            profile.code = code
            profile.user = user
            profile.save()
            group = Group.objects.get(name='teacher')
            user.groups.add(group)
            return redirect('deleteTeacher')
            messages.success(request, 'ok')
        else:
            messages.error(request, 'Bulmadi')
    else:
        profile_form = UserRegisterForm()
    info_form = InfoTeacherForm()
    context = {
        'profile_form': profile_form,
        'info_form': info_form}
    return render(request, 'teacher/createTeacher.html', context)


class Teacher_view(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(teachers, 25)
        try:
            teacher = paginator.page(page)
        except PageNotAnInteger:
            teacher = paginator.page(1)
        except EmptyPage:
            teacher = paginator.page(paginator.num_pages)
        context = {
            'teachers': teacher
        }
        return render(request, 'teacher/viewTeacher.html', context)


def teacherView(request, pk):
    teacher = Teacher.objects.get(id=pk)
    context = {'teacher': teacher}

    return render(request, 'teacher/teacherView.html', context)


def teacherUpdate(request, pk):
    teacher = Teacher.objects.get(pk=pk)
    profile_form = UserRegisterForm(instance=teacher.user)
    info_form = InfoTeacherForm(instance=teacher)
    if request.method == 'POST':
        profile_form = UserRegisterForm(request.POST, instance=teacher.user)
        info_form = InfoTeacherForm(request.POST, instance=teacher)

        if profile_form.is_valid() and info_form.is_valid():
            user = profile_form.save()
            user.save()
            code = profile_form.cleaned_data.get('password')
            profile = info_form.save(commit=False)
            profile.user = user
            profile.code = code
            profile.save()
            return redirect('teachers')
            messages.success(request, 'ok')
        else:
            messages.error(request, 'Bulmadi')
    context = {'profile_form': profile_form, 'info_form': info_form}
    return render(request, 'teacher/teacherUpdate.html', context)


def groupCreate(request):
    if request.method == 'POST':
        group = GroupForm(data=request.POST)
        if group.is_valid():
            group.save()
            return redirect('deleteGroup')
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')
    else:
        group = GroupForm()
    context = {'group': group}
    return render(request, 'group/groupCreate.html', context)


def statusGroup(request):
    status = Status.objects.all()
    context = {
        'status': status
    }
    return render(request, 'group/statusGroup.html', context)


class Group_view(View):

    def get(self, request, ):
        status = Status.objects.all()
        groups = GroupStudent.objects.all().order_by('-startTime')
        page = request.GET.get('page', 1)

        paginator = Paginator(groups, 25)
        try:
            group = paginator.page(page)
        except PageNotAnInteger:
            group = paginator.page(1)
        except EmptyPage:
            group = paginator.page(paginator.num_pages)

        context = {
            'groups': group,
            'status': status
        }
        return render(request, 'group/groups.html', context)


class Groups_view(View):

    def get(self, request, pk):
        status = Status.objects.all()
        groups = GroupStudent.objects.filter(status_id=pk).order_by('-startTime')
        page = request.GET.get('page', 1)

        paginator = Paginator(groups, 25)
        try:
            group = paginator.page(page)
        except PageNotAnInteger:
            group = paginator.page(1)
        except EmptyPage:
            group = paginator.page(paginator.num_pages)

        context = {
            'groups': group,
            'status': status
        }
        return render(request, 'group/groupss.html', context)


def groupView(request, pk):
    group = GroupStudent.objects.get(id=pk)
    context = {'group': group}

    return render(request, 'group/groupView.html', context)


def groupUpdate(request, pk):
    group = GroupStudent.objects.get(pk=pk)
    if request.method == 'POST':
        info_group = GroupForm(request.POST, instance=group)
        if info_group.is_valid():
            info_group.save()
        return redirect(reverse('groupView', kwargs={"pk": pk}))
    info_group = GroupForm(instance=group)
    group = GroupStudent.objects.get(pk=pk)
    context = {'form': info_group,
               'group': group
               }
    return render(request, 'group/groupUpdate.html', context)


def studentCreate(request):
    if request.method == 'POST':
        info_form = StudentForm(data=request.POST)
        if info_form.is_valid():
            info_form.save()
            return redirect('deleteStudent')
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')
    info_form = StudentForm()
    context = {'form': info_form}
    return render(request, 'student/studentCreate.html', context)


class Student_view(View):
    def get(self, request):
        students = Student.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(students, 25)
        try:
            student = paginator.page(page)
        except PageNotAnInteger:
            student = paginator.page(1)
        except EmptyPage:
            student = paginator.page(paginator.num_pages)

        context = {
            'students': student
        }
        return render(request, 'student/students.html', context)


def studentView(request, pk):
    student = Student.objects.get(id=pk)
    context = {'student': student}
    return render(request, 'student/studentView.html', context)


def studentUpdate(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        info_group = StudentForm(request.POST, instance=student)
        if info_group.is_valid():
            info_group.save()
        return redirect(reverse('studentView', kwargs={"pk": student.pk}))
    info_group = StudentForm(instance=student)
    student = Student.objects.get(pk=pk)
    context = {'form': info_group,
               'student': student
               }
    return render(request, 'student/studentUpdate.html', context)


def rateGroup(request):
    groups = GroupStudent.objects.all()
    months = Months.objects.all()
    context = {
        'groups': groups,
        'months': months
    }
    return render(request, 'rate/rateGroup.html', context)


def createRate(request, pk):
    students = Student.objects.filter(group_id=pk)

    context = {
        'students': students,

    }
    return render(request, 'rate/rateCreate.html', context)


class Rate_view(View, ):
    def get(self, request, pk):
        students = RateStudent.objects.filter(group_id=pk)
        months = Months.objects.all()

        context = {
            'months': months,
            'students': students
        }
        return render(request, 'rate/rateCreate.html', context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            student_id = request.POST.getlist('id[]')
            month_id = request.POST.getlist('id1[]')

            rate = RateStudent()
            for id in student_id:
                student = Student.objects.get(pk=id)
                rate.student = student
                month = Months.objects.get(id=month_id)
                rate.month = month
                rate.save()
            return redirect('deleteTeacher')


def courseCreate(request):
    if request.method == 'POST':
        info_form = CourseForm(data=request.POST)
        if info_form.is_valid():
            info_form.save()
            return redirect('courses')
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')
    info_form = CourseForm()
    context = {'form': info_form}
    return render(request, 'group/courseCreate.html', context)


class Course_View(View):
    def get(selfe, request):
        course = Course.objects.all()
        context = {
            'course': course,
        }
        return render(request, 'group/courses.html', context)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            course_id = request.POST.getlist('id[]')
            for id in course_id:
                student = Course.objects.get(pk=id)
                student.delete()

            return redirect('courses')


def courseUpdate(request, pk):
    course = Course.objects.get(pk=pk)
    if request.method == 'POST':
        info_group = CourseForm(request.POST, instance=course)
        if info_group.is_valid():
            info_group.save()
        return redirect('courses')
    info_group = CourseForm(instance=course)
    context = {'form': info_group}
    return render(request, 'group/courseUpdate.html', context)


def courseGroup(request, pk):
    course = Course.objects.get(pk=pk)
    groups = GroupStudent.objects.filter(course_id=pk)
    context = {
        'groups': groups,
        'course': course
    }
    return render(request, 'group/courseGroup.html', context)


def payGroup(request):
    group = GroupStudent.objects.all()
    context = {
        # 'students': students,
        'groups': group
    }
    return render(request, 'pay/payGroup.html', context)


def payStudent(request, pk):
    students = Student.objects.filter(group_id=pk)
    group = GroupStudent.objects.get(pk=pk)
    context = {
        'students': students,
        'groups': group
    }
    return render(request, 'pay/payStudent.html', context)


def payStudentCreate(request, pk):
    if request.method == 'POST':
        pay_form = PayStudentForm(data=request.POST)
        if pay_form.is_valid():
            rating = pay_form.save(commit=False)
            student = Student.objects.get(id=pk)
            rating.student = student
            rating.save()
            return redirect(reverse('payStudent', kwargs={"pk": student.group.pk}))
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        student1 = Student.objects.get(pk=pk)
        student = PayStudentForm()
    context = {
        'form': student,
        'student': student1
    }

    return render(request, 'pay/payStudentCreate.html', context)


def payStudentView(request, pk):
    student = Student.objects.get(pk=pk)
    pay = PayStudent.objects.filter(student_id=pk)
    context = {
        'pays': pay,
        'student': student
    }
    return render(request, 'pay/payStudentView.html', context)


def payStudentUpdate(request, pk):
    indicator = PayStudent.objects.get(id=pk)
    student = indicator.student
    if request.method == 'POST':
        rating_form = PayStudentForm(request.POST, instance=indicator)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.save()

            return redirect(reverse('payStudentView', kwargs={"pk": student.pk}))
            messages.success(request, 'Bajaridi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        rating_form = PayStudentForm(instance=indicator)
        student = indicator.student
    context = {'form': rating_form,
               'student': student
               }
    return render(request, 'pay/payStudentUpdate.html', context)


def ratingGroup(request):
    group = GroupStudent.objects.all()
    context = {
        # 'students': students,
        'groups': group
    }
    return render(request, 'rating/ratingGroup.html', context)


def ratingStudent(request, pk):
    students = Student.objects.filter(group_id=pk)
    group = GroupStudent.objects.get(pk=pk)
    context = {
        'students': students,
        'groups': group
    }
    return render(request, 'rating/ratingStudent.html', context)


def ratingStudentCreate(request, pk):
    if request.method == 'POST':
        pay_form = RatingStudentForm(data=request.POST)
        if pay_form.is_valid():
            rating = pay_form.save(commit=False)
            student = Student.objects.get(id=pk)
            rating.student = student
            rating.save()
            return redirect(reverse('ratingStudent', kwargs={"pk": student.group.pk}))
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        student1 = RatingStudentForm()
        student = Student.objects.get(id=pk)
    context = {'form': student1,
               'student': student}

    return render(request, 'rating/ratingStudentCreate.html', context)


def ratingStudentView(request, pk):
    student = Student.objects.get(pk=pk)
    rating = RatingStudent.objects.filter(student_id=pk)
    context = {
        'rating': rating,
        'student': student
    }
    return render(request, 'rating/ratingStudentView.html', context)


def ratingStudentUpdate(request, pk):
    indicator = RatingStudent.objects.get(id=pk)
    student = indicator.student
    if request.method == 'POST':
        rating_form = RatingStudentForm(request.POST, instance=indicator)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.save()

            return redirect(reverse('ratingStudentView', kwargs={"pk": student.pk}))
            messages.success(request, 'Bajaridi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        rating_form = RatingStudentForm(instance=indicator)
        student = indicator.student
    context = {
        'form': rating_form,
        'student': student
    }
    return render(request, 'rating/ratingStudentCreate.html', context)


def visitGroup(request):
    group = GroupStudent.objects.all()
    context = {

        'groups': group
    }
    return render(request, 'visit/visitGroup.html', context)


class Visit_view(View, ):
    def get(self, request, pk):
        students = Student.objects.filter(group_id=pk)

        context = {

            'students': students
        }
        return render(request, 'visit/visitStudent.html', context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            student_id = request.POST.getlist('id[]')
            for id in student_id:
                visit = VisitStudent()
                visit.student = Student.objects.get(id=id)
                visit.save()
            return redirect('visitGroup')

        return redirect('deleteTeacher')


def visitStudentView(request, pk):
    student = Student.objects.get(pk=pk)
    visit = VisitStudent.objects.filter(student_id=pk)

    context = {
        'visit': visit,
        'student': student
    }
    return render(request, 'visit/visitStudentView.html', context)


def dayGroup(request):
    day = GroupDay.objects.all()
    context = {
        'day': day
    }

    return render(request, 'table/dayGroup.html', context)


def tableGroup(request, pk):
    day = GroupDay.objects.all()
    group = GroupStudent.objects.filter(day_id=pk).order_by('-startTime')
    context = {
        'group': group,
        'day': day
    }
    return render(request, 'table/tableGroup.html', context)


def advertising(request):
    adv = Advertising.objects.all()
    context = {
        'advs': adv
    }
    return render(request, 'temp/course.html', context)


def teacherGroup(request):
    group = GroupStudent.objects.filter(teacher=request.user.teacher).order_by('-startTime')
    context = {
        'groups': group
    }
    return render(request, 'teacher/teacherGroup.html', context)


def teacherVisit(request):
    group = GroupStudent.objects.filter(teacher=request.user.teacher).order_by('-startTime')
    context = {
        'groups': group
    }
    return render(request, 'teacher/teacherVisit.html', context)


class VisitStudent_view(View, ):
    def get(self, request, pk):
        students = Student.objects.filter(group_id=pk)

        context = {

            'students': students
        }
        return render(request, 'teacher/teacherStudent.html', context)

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
            student_id = request.POST.getlist('id[]')
            for id in student_id:
                visit = VisitStudent()
                visit.student = Student.objects.get(id=id)
                visit.save()

            return redirect('teacherVisit')


def teacherRatingGroup(request):
    group = GroupStudent.objects.filter(teacher=request.user.teacher).order_by('-startTime')
    context = {
        # 'students': students,
        'groups': group
    }
    return render(request, 'teacherRating/ratingGroup.html', context)


def teacherRatingStudent(request, pk):
    students = Student.objects.filter(group_id=pk)
    group = GroupStudent.objects.get(pk=pk)
    context = {
        'students': students,
        'groups': group
    }
    return render(request, 'teacherRating/ratingStudent.html', context)


def teacherRatingStudentCreate(request, pk):
    if request.method == 'POST':
        pay_form = RatingStudentForm(data=request.POST)
        if pay_form.is_valid():
            rating = pay_form.save(commit=False)
            student = Student.objects.get(id=pk)
            rating.student = student
            rating.save()
            return redirect(reverse('teacherRatingStudent', kwargs={"pk": student.group.pk}))
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        student = RatingStudentForm()

    context = {'form': student}

    return render(request, 'teacherRating/ratingStudentCreate.html', context)


def teacherRatingStudentView(request, pk):
    student = Student.objects.get(pk=pk)
    rating = RatingStudent.objects.filter(student_id=pk)
    context = {
        'rating': rating,
        'student': student
    }
    return render(request, 'teacherRating/ratingStudentView.html', context)


def teacherRatingStudentUpdate(request, pk):
    indicator = RatingStudent.objects.get(id=pk)
    if request.method == 'POST':
        rating_form = RatingStudentForm(request.POST, instance=indicator)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.save()
            student = rating.student
            return redirect(reverse('teacherRatingStudentView', kwargs={"pk": student.pk}))
            messages.success(request, 'Bajaridi')
        else:
            messages.error(request, 'Bulmadi')

    else:
        rating_form = RatingStudentForm(instance=indicator)
        student = indicator.student
    context = {'form': rating_form,
               'student': student
               }
    return render(request, 'teacherRating/ratingStudentCreate.html', context)


def teacherVisitStudentView(request, pk):
    student = Student.objects.get(pk=pk)
    visit = VisitStudent.objects.filter(student_id=pk)

    context = {
        'visit': visit,
        'student': student
    }
    return render(request, 'teacher/teacherVisitStudentView.html', context)


def courseAdd(request, pk):
    adv = Advertising.objects.get(pk=pk)
    context = {
        'item': adv
    }
    return render(request, 'temp/courseAdd.html', context)


# def test(request):
#     if request.method == 'POST':
#         form = ContentForm(request.POST)
#         if form.is_valid():
#             mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
#                              'khayitovkhumoyun000@gmail.com',
#                              ['hayitovhumoyun431@gmail.com'], fail_silently=False)
#             if mail:
#                 messages.success(request, 'Bajarildi')
#                 return redirect('test')
#             else:
#                 messages.error('bulmadi xato')
#
#         else:
#             messages.error(request, 'bulmadi xato')
#
#     else:
#
#         form = ContentForm()
#         context = {
#             'form': form,
#         }
#     return render(request, 'temp/contact.html', context)

def sms(request):
    if request.method == 'POST':
        info = ContactForm(data=request.POST)
        if info.is_valid():
            info.save()
            return redirect('sms')
            messages.success(request, 'Bajarildi')
        else:
            messages.error(request, 'Bulmadi')
    else:
        info = ContactForm()
    context = {
        'form': info
    }
    return render(request, 'temp/contact.html', context)


def smsView(request):
    smss = Sms.objects.all().order_by('-id')
    page = request.GET.get('page', 1)

    paginator = Paginator(smss, 25)
    try:
        sms = paginator.page(page)
    except PageNotAnInteger:
        sms = paginator.page(1)
    except EmptyPage:
        sms = paginator.page(paginator.num_pages)
    context = {
        'sms': sms
    }
    return render(request, 'temp/smsView.html', context)


def smsLook(request, pk):
    sms = Sms.objects.get(pk=pk)
    if sms.bool == True:
        sms.bool = False
        sms.save()

        sms_form = ContactForm(instance=sms)
        context = {
            'form': sms_form
        }
    else:
        sms_form = ContactForm(instance=sms)
        context = {
            'form': sms_form
        }

    return render(request, 'temp/smsLook.html', context)


def smsDelete(request, pk):
    sms = Sms.objects.get(pk=pk)
    sms.delete()
    return redirect('smsView')

    return render(request, 'temp/smsDelete.html')


def teacherDelete(request, pk):
    teacher = Teacher.objects.get(id=pk)
    teacher.user.delete()
    teacher.delete()
    return redirect('deleteTeacher')
    return render(request, 'teacher/viewTeacher.html')


def groupDelete(request, pk):
    group = GroupStudent.objects.get(id=pk)
    group.delete()
    return redirect('deleteGroup')

    return render(request, 'group/groups.html')


def studentDelete(request, pk):
    student = Student.objects.get(id=pk)
    student.delete()
    return redirect('deleteStudent')

    return render(request, 'student/students.html')
