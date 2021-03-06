from django.shortcuts import render
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ContactForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('contact_admin')
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 col-form-label'
        self.helper.field_class = 'col-sm-10'
        self.helper.add_input(Submit('send_button', 'Послать'))

    from_email = forms.EmailField(
        label="Ваш e-mail:")
    subject = forms.CharField(
        label="Тема письма:",
        max_length=128)
    message = forms.CharField(
        label="Текст:",
        max_length=2560,
        widget=forms.Textarea)

def contact_admin(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['from_email']
            try:
                send_mail(subject, message, from_email, [settings.ADMIN_EMAIL])
            except Exception:
                messages.error(request, 'Error send email to admin')
            else:
                messages.success(request, 'Email sent')
            return HttpResponseRedirect(reverse('contact_admin'))
    else:
        form = ContactForm()
    return render(request, 'contact_admin/form.html', {'form': form})
