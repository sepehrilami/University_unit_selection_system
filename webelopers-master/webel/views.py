from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
# Imaginary function to handle an uploaded file.

from webel.forms import ContactForm, MyCourse
# Create your views here.
from webel.forms import SignUpForm, LoginForm, EditProfile, MakeCourse, SearchCourse

# import requests
from .models import Course, UserAvatar


def index(request):
    return render(request, 'base.html')


def signup(request):
    message = []

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            # profile = form.cleaned_data.get('profile')
            # UserProfile.objects.create(user, profile)
            login(request, user)
            return redirect('/')
        else:

            if 'password2' in form.errors:
                message.append('password')

            if 'username' in form.errors:
                message.append('username')

            print(form.errors)
            print(message)
    else:
        form = SignUpForm()
    return render(request, 'b_register.html', {'form': form, 'message': message})


def login_view(request):
    message = 'nothing'

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                message = 'invalid'
        else:
            message = 'notvalid'
    else:
        form = LoginForm()

    return render(request, 'b_login.html', {'form': form, 'message': message})


@login_required(login_url='/login')
def logout_view(request):
    logout(request)
    return redirect('/')


def contact(request):
    sent = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()

            subject = form.cleaned_data['title']
            email = form.cleaned_data['email']
            message = form.cleaned_data['text'] + '\n' + email
            recipient_list = ['marofidaniyal@gmail.com', 'webe19lopers@gmail.com']

            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

            # daniurl = "https://azmabepors.com/action/webel"
            #
            # postdata = {
            #     'title': subject,
            #     'text': message,
            #     'email': email
            # }
            #
            # r = requests.post(daniurl, data=postdata)

            sent = True

            # return HttpResponseRedirect('/thanks/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form, 'sent': sent})


@login_required(login_url='/login')
def profile(request):
    username = request.user.username
    user = User.objects.get(username=username)

    try:
        daniavatar = UserAvatar.objects.filter(username=username).last()
        urlfile = daniavatar.avatar
    except:
        urlfile = 'http://danihost.ir/da512.png'
    # print(daniavatar)
    # print(daniavatar.avatar)
    profile = {'username': user.username,
               'first_name': user.first_name,
               'last_name': user.last_name,
               'avatarurl': urlfile}

    return render(request, 'profile.html', {'profile': profile})


@login_required(login_url='/login')
def panel(request):
    return render(request, 'panel.html')


@login_required(login_url='/login')
def setting(request):
    if request.method == "POST":
        form = EditProfile(request.POST, instance=request.user)
        if form.is_valid():
            if request.FILES:
                uploaded_file = request.FILES['document']
                fs = FileSystemStorage()
                filename = fs.save(uploaded_file.name, uploaded_file)
                fileurl = fs.url(filename)
                username = request.user.username
                UserAvatar(username=username, avatar=fileurl).save()

            form.save()
            return redirect('/profile')
    else:
        form = EditProfile(instance=request.user)

    return render(request, 'setting.html', {'form': form})


@login_required(login_url='/login')
def make_course(request):
    if request.method == 'POST':
        form = MakeCourse(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('form is not vaild')
    else:
        form = MakeCourse()

    return render(request, 'makecourse.html', {'form': form})


@login_required(login_url='/login')
def courses(request):
    courses_data = []
    searchedcourses = []
    search = False

    if request.method == 'POST':
        # do sth
        search = True
        form = SearchCourse(request.POST)
        if form.is_valid():

            # dept=True
            search_query = form.cleaned_data['search_query']
            # if form.cleaned_data['department']:
            #     asdept=Course.objects.all().filter(department=search_query)
            # elif form.cleaned_data['teacher']:
            #     asteacher=Course.objects.all().filter(teacher=search_query)
            # elif form.cleaned_data['course']:
            #     ascourse=Course.objects.all().filter(name=search_query)
            # else:
            searchcourse = Course.objects.all().filter(department=search_query)

            for crs in searchcourse:
                searchedcourses.append({'course_number': crs.course_number,
                                        'group_number': crs.group_number,
                                        'course_name': crs.name,
                                        'department': crs.department,
                                        'times': {'start': crs.start_time, 'end': crs.end_time},
                                        'teacher': crs.teacher})


        else:
            print('not vaild')

    else:
        form = SearchCourse()

        allCourses = Course.objects.all()

        for course in allCourses:
            days = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه']

            course_data = {'course_number': course.course_number,
                           'group_number': course.group_number,
                           'course_name': course.name,
                           'department': course.department,
                           'days': {'first': days[course.first_day], 'second': days[course.second_day]},
                           'times': {'start': course.start_time, 'end': course.end_time},
                           'teacher': course.teacher,
                           'course_id': course.id
                           }
            courses_data.append(course_data)

    return render(request, 'courses.html',
                  {'courses': courses_data, 'form': form, 'search': search, 'seachedcourses': searchedcourses})


@login_required(login_url='/login')
def addToMyCourses(request):
    courses_data = []

    form = MakeCourse(request.GET)
    if form.is_valid():
        courses_data.append()
    return render(request, 'courses.html',
                  {'my_courses': courses_data, 'form': form})
