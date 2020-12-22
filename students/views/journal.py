from django.shortcuts import render
from django.http import HttpResponse

# views for journal

def journal(request):
    students = (
        {'id': 1, 'first_name': 'Дмитрий', 'last_name': 'Литвинов'},
        {'id': 2, 'first_name': 'Виталий', 'last_name': 'Подоба'},
        {'id': 3, 'first_name': 'Андрей', 'last_name': 'Какойто'},
    )
    return render(request, 'students/journal.html', {'students': students})
