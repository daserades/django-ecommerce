from django.core.mail import BadHeaderError,EmailMultiAlternatives
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message'] + "  from_email: " + from_email
            try:
                msg = EmailMultiAlternatives(subject, message, from_email, [settings.DEFAULT_EMAIL_FROM])
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "sendemail/contact.html", {'form': form})


def successView(request):
    return render(request, "sendemail/success.html")