from django.shortcuts import render
from django.http import HttpResponse
import os
from django.core.paginator import Paginator
# Create your views here.
from .forms import *
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def index(request):
    return HttpResponse("<h1>Welcome to Django World!</h1>")


@login_required()
def home(request):
    ls1 = ['A', 'B', 'C', 'D', 'E']
    return render(request, 'home.html', {'message': "This is Template Language Example",
                                         'message1': "Welcome To Jinja2",
                                         'ls1': ls1})


def demo(request, a, b):
    return HttpResponse("<h1>" + str(a) + ' ' + str(b) + "</h1>")


def formdemo(request):
    if request.method == 'POST':
        vdf = ValidationDemoForm(request.POST)
        if vdf.is_valid():
            # print(vdf.cleaned_data)
            fys = FirstYearStudent()
            fys.name = vdf.cleaned_data['name']
            fys.gender = vdf.cleaned_data['gender']
            fys.email = vdf.cleaned_data['email']
            fys.password = vdf.cleaned_data['password']
            fys.address = vdf.cleaned_data['address']
            fys.state = vdf.cleaned_data['state']
            fys.xii_percentage = vdf.cleaned_data['percentage']
            fys.admission_date = vdf.cleaned_data['admission_date']
            fys.save()
            vdf = ValidationDemoForm()
            return render(request, 'formdemo.html', {"vdf": vdf, "message": 'Student added Successfully'})
        else:
            return render(request, 'formdemo.html', {"vdf": vdf})
    else:
        vdf = ValidationDemoForm()
        return render(request, 'formdemo.html', {"vdf": vdf})


@login_required()
def addLocation(request):
    if request.method == 'POST':
        loc = LocationForm(request.POST)
        if loc.is_valid():
            loc.save()
            return HttpResponse("<h1>Form Submitted Success</h1>")
        else:
            return render(request, 'addlocation.html', {'locForm': loc})

    loc = LocationForm()
    return render(request, 'addlocation.html', {'locForm': loc})


def showlocations(request):
    loc_list = Location.objects.all()
    return render(request, 'showlocations.html', {'loc_list': loc_list})


def updateLocation(request, id):
    location = Location.objects.get(pk=id)
    if request.method == 'POST':
        loc = LocationForm(request.POST)
        if loc.is_valid():
            locMod = Location()
            locMod.id = location.id
            locMod.state = loc.cleaned_data['state']
            # print(loc.state)
            locMod.save()
            return HttpResponse("<h1>Form Submitted Success</h1>")
        else:
            return render(request, 'addlocation.html', {'locForm': loc})
    loc = LocationForm(instance=location)
    return render(request, 'addlocation.html', {'locForm': loc})


def deletelocation(request, id):
    loc = Location.objects.get(pk=id)
    emp_list = loc.employee_set.all()
    for emp in emp_list:
        emp.delete()
    loc.delete()
    return redirect("showlocations")


def addemployee(request):
    if request.method == "POST":
        emp_form = EmployeeForm(request.POST, request.FILES)
        if emp_form.is_valid():
            emp_form.save()
            emp_form = EmployeeForm()
            return render(request, 'addemployee.html', {'emp_form': emp_form,
                                                        'message': "Employee Added Successfully"})
        else:
            return render(request, 'addemployee.html', {'emp_form': emp_form})
    emp_form = EmployeeForm()
    return render(request, 'addemployee.html', {'emp_form': emp_form})


def showemployees(request):
    empployees = Employee.objects.all()
    p = Paginator(empployees, 2, orphans=1)
    page = request.GET.get('page')
    emp_list = p.get_page(page)
    return render(request, 'showemployees.html', {'emp_list': emp_list})


def updateemployee(request, id):
    emp = Employee.objects.get(pk=id)
    if request.method == 'POST':
        emp_form = EmployeeForm(request.POST, request.FILES)
        if emp_form.is_valid():
            if request.POST.get('photo-clear', False):
                # we don't remove old photo
                if os.path.isfile(emp.photo.path) and emp.photo.name != 'no_photo.jpg':
                    os.remove(emp.photo.path)
                emp.photo = 'no_photo.jpg'
            elif type(request.POST.get('photo', 0)) is int:
                # print(emp.photo)
                # exit()
                if os.path.isfile(emp.photo.path) and emp.photo.name != 'no_photo.jpg':
                    os.remove(emp.photo.path)
                emp.photo = emp_form.cleaned_data['photo']
            else:
                emp_form.photo = emp.photo.name
            emp.name = emp_form.cleaned_data['name']
            emp.gender = emp_form.cleaned_data['gender']
            emp.package = emp_form.cleaned_data['package']
            emp.address = emp_form.cleaned_data['address']
            emp.location = emp_form.cleaned_data['location']
            emp.save()
            emp_form = EmployeeForm()
            return render(request, 'addemployee.html', {'emp_form': emp_form, 'message': "Employee Updated Successfully"})
        else:
            return render(request, 'addemployee.html', {'emp_form': emp_form})
    emp_form = EmployeeForm(instance=emp)
    return render(request, 'addemployee.html', {'emp_form': emp_form})


def deleteemployee(request, id):
    emp_id = Employee.objects.get(pk=id)
    emp_id.delete()
    return redirect('showemployees')


def register(request):
    if request.method == 'POST':
        # check if date is validated
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            User.objects.create_user(reg_form.cleaned_data['email'], email=reg_form.cleaned_data['email'],
                                     password=reg_form.cleaned_data['password'],
                                     first_name=reg_form.cleaned_data['first_name'],
                                     last_name=reg_form.cleaned_data['last_name'])
            reg_form = RegistrationForm()
            return render(request, 'registration.html', {'reg_form': reg_form, 'message': "Registered Successfully"})
        else:
            return render(request, 'registration.html', {'reg_form': reg_form})
    reg_form = RegistrationForm()
    return render(request, 'registration.html', {'reg_form': reg_form})
