from django.shortcuts import render
from django.http import HttpResponse

#views for groups

def groups_list(request):
    groups = (
        {'id': 1, 'name': 'МтМ-21', 'leader': {'id': 1, 'name': 'Дмитрий Литвинов'} },
        {'id': 2, 'name': 'МтМ-22', 'leader': {'id': 2, 'name': 'Виталий Подоба'} },
    )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
    return HttpResponse('<h1>Group add form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete group %s</h1>' % gid)
