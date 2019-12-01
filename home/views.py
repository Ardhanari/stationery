from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from .forms import ContactForm

# Create your views here.

def about(request):
    """Renders about page"""
    return render(request, 'about.html')

def faq(request):
    """Renders FAQ page"""
    return render(request, 'faq.html')

def contact(request):
    """
    Renders contact page
    With POST - sends an email to shop inbox
    """

    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['from_email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            msg_mail = str(from_email) + '\n\n' + str(message)
            
            try:
                send_mail(subject, msg_mail, from_email, ['stationerycuriousshop@gmail.com', ])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent! Thank you")
            return redirect('userprofile')
    return render(request, "contact.html", {'form': form})