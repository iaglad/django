from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Student, Group
from django.contrib import messages
from .include.utils import err
from datetime import datetime

# views for students

def students_list(request):
    students = Student.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket', 'student_group'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    # paginator
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        students = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        students = paginator.page(page)
    #
    messages.success(request, 'Page= ' + str(page))
    #
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    if request.method == "POST":
        if request.POST.get('add_button') is not None:
            errors = {}
            data = {'middle_name': request.POST.get('middle_name'),
                    'notes': request.POST.get('notes')}
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = "Имя - обязательное поле!"
            else:
                data['first_name'] = first_name
            last_name = request.POST.get('last_name', '').strip()
            if not last_name:
                errors['last_name'] = "Фамилия - обязательное поле!"
            else:
                data['last_name'] = last_name
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = "Дата рождения - обязательное поле!"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = "Формат: 1984-12-30"
                data['birthday'] = birthday
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = "Номер билета - обязательное поле!"
            else:
                data['ticket'] = ticket
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = "Выберите группу для студента"
            else:
                group = Group.objects.filter(pk=student_group).first()
                if group:
                    data['student_group'] = group
                else:
                    errors['student_group'] = "Выберите корректную группу для студента"
            photo = request.FILES.get('photo')
            try:
                if photo.size > 2097152:
                    errors['photo'] = photo.name + "- too big size - " + str(photo.size)
            except AttributeError:
                pass
            if photo:
                data['photo'] = photo
            #
            if not errors:
                student = Student(**data)
                student.save()
                status_str = '%s?status_message=Студент успешно добавлен: ' + data['first_name'] + ' ' + data['last_name']
                return HttpResponseRedirect(status_str % reverse('home'))
            else:
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            return HttpResponseRedirect('%s?status_message=Добавление студента отменено' % reverse('home'))
    else:
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})


def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
