from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .models import Classroom, Student
from .forms import ClassroomForm, SignupForm, SigninForm, StudentForm
from django.http import Http404



def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    studnets = Student.objects.filter(classroom=classroom).order_by("name", "-exam_grade")
    context = {
        "classroom": classroom,
        "students": studnets
    }
    return render(request, 'classroom_detail.html', context)

def classroom_create(request):
    if request.user.is_anonymous:
        return redirect("signin")
    form = ClassroomForm()
    if request.method == "POST":
        form = ClassroomForm(request.POST)
        if form.is_valid():
            classroom_obj = form.save(commit=False)
            classroom_obj.teacher = request.user
            classroom_obj.save()
            messages.success(request, "Successfully Created!")
            return redirect('classroom-list')
    context = {
    "form": form,
    }
    return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated!")
            return redirect('classroom-list')
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	if not request.user:
		raise Http404
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def student_delete(request, student_id):
    classroom_id = Student.objects.get(id=student_id).classroom.id
    Student.objects.get(id=student_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-detail',classroom_id)

def student_update(request, student_id):
    student = Student.objects.get(id=student_id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Updated!")
            return redirect('classroom-detail',student.classroom.id)
    context = {
    "form": form,
    "student": student,
    }
    return render(request, 'student_update.html', context)



def student_create(request, classroom_id):
	classroom=Classroom.objects.get(id=classroom_id)
	if not request.user == classroom.teacher:
		return redirect("signin")
	form = StudentForm()
	if request.method == "POST":
		form = StudentForm(request.POST)
		if form.is_valid():
			item = form.save(commit = False)
			item.classroom = classroom
			item.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-detail',classroom.id)
	context = {
		
		"form":form,
		"classroom":classroom
	}
	return render(request, 'student_create.html', context)



def signup(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)

			user.set_password(user.password)
			user.save()
			login(request, user)
			return redirect("classroom-list")
	context = {
		"form":form,
	}
	return render(request, 'signup.html', context)

def signin(request):
	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():

			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect('classroom-list')
	context = {
		"form":form
	}
	return render(request, 'signin.html', context)

def signout(request):
	logout(request)
	return redirect("signin")

