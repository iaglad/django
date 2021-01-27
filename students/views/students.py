from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Student, Group
from django.contrib import messages
from .include.utils import err
from datetime import datetime
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

# views for students

def students_list(request):
    students = Student.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket', 'student_group'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    # paginator
    paginator = Paginator(students, 8)
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
    #messages.success(request, 'Page= ' + str(page))
    #
    return render(request, 'students/students_list.html', {'students': students})

class StudentCreateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('students_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout.append(FormActions(
            Submit('add_button', 'Сохранить'),
            Submit('cancel_button', 'Отменить', css_class='btn-danger', formnovalidate='formnovalidate',),
        ))

class StudentCreateView(CreateView):
    model = Student
    template_name = 'students/universal.html'
    form_class = StudentCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Сохранено успешно')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Добавление отменено')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить студента'
        return context

class StudentUpdateForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.layout.append(FormActions(
            Submit('add_button', 'Сохранить'),
            Submit('cancel_button', 'Отменить', css_class='btn-danger', formnovalidate='formnovalidate',),
        ))

class StudentUpdateView(UpdateView):
    model = Student
    template_name = 'students/universal.html'
    form_class = StudentUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Сохранено успешно')
        return reverse('home')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Редактирование отменено')
            return HttpResponseRedirect(reverse('home'))
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать студента'
        return context

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить студента'
        context['myurl'] = 'students_delete'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Удалено успешно')
        return reverse('home')

# ----------------------------------------------------------------------------
def students_add1(request):
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
                messages.success(request, 'Студент успешно добавлен: ' + data['first_name'] + ' ' + data['last_name'])
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title'), 'errors': errors})
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, 'Добавление студента отменено')
            return HttpResponseRedirect(reverse('home'))
    else:
        return render(request, 'students/students_add.html', {'groups': Group.objects.all().order_by('title')})
