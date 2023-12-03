from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, QuestionsForm, AnswerForm, VoteQuestionForm
from .models import User, Question, Answer, QuestionCategory, Person, VoteQuestion

# Create your views here.


@require_http_methods(["GET"])
def index(request):
    context = {'name': 'questhub'}
    return render(request, "quest/index.html", context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username, password=password)
            if user:
                url = reverse('quest:main', args=[user.person.id, user.person.name])
                return redirect(url)
        except User.DoesNotExist:
            messages.error(
                request, 'Credenciales incorrectas. Intenta de nuevo')
            return render(request, 'quest/index.html')
    else:
        messages.error(request, 'Credenciales incorrectas. Intenta de nuevo')
        return render(request, 'quest/index.html')


@require_http_methods(['GET'])
def mian_page(request, id, name):
    questions = Question.objects.annotate(
        count_answers=Count('answer', distinct=True), 
        count_votes=Count('votequestion__id', distinct=True))[::-1][:10]
    context = {'questions': questions, 'user': name, 'id': id}
    return render(request, 'quest/main.html', context)


@require_http_methods(['GET'])
def create_question(request, pk):
    category = QuestionCategory.objects.all()
    user = User.objects.get(pk=pk)
    context = {'categories': category, 'id': pk, 'name':user.person.name}
    return render(request, 'quest/create_question.html', context)


@require_http_methods(['POST'])
def procesing_question(request, pk):
    user = User.objects.get(pk=pk)
    
    post_data = request.POST.copy()
    post_data['author'] = pk
    
    form_question = QuestionsForm(post_data)
    if form_question.is_valid():
        form_question.save()
        messages.success(request, 'Pregunta creada exitosamente')
        url = reverse('quest:main', args=[user.id, user.person.name])
        return redirect(url)
    else:
        url = reverse('quest:main', args=[user.id, user.person.name])
        return redirect(url)
    
def answer(request, id_question, pk_user):
    question = Question.objects.get(pk=id_question)
    person = User.objects.get(pk=pk_user)
    answers_question = Answer.objects.filter(question=question)
    context = {'question': question, 'answers': answers_question, 'id': pk_user, 'name': person.person.name}
    return render(request, 'quest/answers.html', context)

def create_answer(request, pk_question, pk_user):
    question = Question.objects.get(pk=pk_question)
    user = User.objects.get(pk=pk_user)
    context = {'question': question, 'id':pk_user,'name':user.person.name}
    return render(request, 'quest/create_answers.html', context)

def save_answer(request, pk_question, pk_user):
    user = User.objects.get(pk=pk_user)
    post_data = request.POST.copy()
    post_data['question'] = pk_question
    post_data['author'] = pk_user
    form_answer = AnswerForm(post_data)
    
    if (form_answer.is_valid()):
        form_answer.save()
        messages.success(request, 'Respuesta creada exitosamente')
        return redirect(reverse('quest:main', args=[user.id, user.person.name]))
    else:
        messages.error(request, 'Error al crear la respuesta')
        return redirect(reverse('quest:main', args=[user.id, user.person.name]))
    
def vote_question(request, pk_question, pk_user):
    post_data = request.POST.copy()
    user = User.objects.get(pk=pk_user)
    post_data['question']=pk_question
    post_data['author']=pk_user
    post_data['vote']="upvote"
    
    verify_vote = VoteQuestion.objects.filter(question=pk_question, author=pk_user)
    
    form_vote = VoteQuestionForm(post_data)
    if(form_vote.is_valid() and not verify_vote):
        form_vote.save()
        messages.success(request, 'Voto exitoso')
        return redirect(reverse('quest:main', args=[user.person.id, user.person.name]))
    else:
        messages.error(request, 'Error al votar, ya has votado')
        return redirect(reverse('quest:main', args=[user.person.id, user.person.name]))

def about(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'id': user_id, 'name': user.person.name}
    return render(request, 'quest/about.html', context )

def contact(request, user_id):
    user = User.objects.get(pk=user_id)
    context = {'id': user_id, 'name': user.person.name}
    return render(request, 'quest/contact.html', context)