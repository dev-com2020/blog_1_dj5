from django.shortcuts import render

from .services import generate_questions


def home(request):
    if request.method == 'POST':
        text = request.POST['text']
        questions = generate_questions(text)
        context = {'questions': questions}
    return render(request,'base.html',context)