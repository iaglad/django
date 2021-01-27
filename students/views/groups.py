from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..models import Group
from django.forms import ModelForm
from django.views.generic import UpdateView, CreateView, DeleteView
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.urls import reverse
from django.contrib import messages

# views for groups

def groups_list(request):
    groups = Group.objects.all()
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    paginator = Paginator(groups, 6)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        groups = paginator.page(1)
    except EmptyPage:
        groups = paginator.page(paginator.num_pages)
    return render(request, 'students/groups_list.html', {'groups': groups})

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('groups_add')
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

class GroupCreateView(CreateView):
    model = Group
    template_name = 'students/universal.html'
    form_class = GroupCreateForm

    def get_success_url(self):
        messages.success(self.request, 'Сохранено успешно')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Добавление отменено')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить группу'
        return context


class GroupUpdateForm(ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse('groups_edit', kwargs={'pk': kwargs['instance'].id})
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

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/universal.html'
    form_class = GroupUpdateForm

    def get_success_url(self):
        messages.success(self.request, 'Сохранено успешно')
        return reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            messages.warning(request, 'Редактирование отменено')
            return HttpResponseRedirect(reverse('groups'))
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактировать группу'
        return context

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удалить группу'
        context['myurl'] = 'groups_delete'
        return context

    def get_success_url(self):
        messages.success(self.request, 'Удалено успешно')
        return reverse('groups')
