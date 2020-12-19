from django.shortcuts import render
from django.http import HttpResponse

#views for students
def students_list(request):
    students = (
        {'id': 1, 'first_name': 'Дмитрий', 'last_name': 'Литвинов', 'ticket': 235, 'image': 'img/Dmytro.jpeg'},
        {'id': 2, 'first_name': 'Виталий', 'last_name': 'Подоба', 'ticket': 2123, 'image': 'img/Vitaliy.png'},
        {'id': 3, 'first_name': 'Андрей', 'last_name': 'Какойто', 'ticket': 354, 'image': 'img/Andrew.jpg'},
    )
    return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
    return HttpResponse('<h1>Student add form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete student %s</h1>' % sid)
