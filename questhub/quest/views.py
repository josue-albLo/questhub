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
    print('login view')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('Validando credenciales')
        try:
            user = User.objects.get(username=username, password=password)
            if user:
                print('Credenciales correctas')
                url = reverse(
                    'quest:main')+f'?user_id={user.person.id}&user_name={user.person.name}'
                return redirect(url)
        except User.DoesNotExist:
            messages.error(
                request, 'Credenciales incorrectas. Intenta de nuevo')
            return render(request, 'quest/index.html')
    else:
        messages.error(request, 'Credenciales incorrectas. Intenta de nuevo')
        return render(request, 'quest/index.html')


@require_http_methods(['GET'])
def mian_page(request):
    print(request.user)
    user_id = request.GET['user_id']
    user_name = request.GET['user_name']
    print(f'Informacion del usuario {user_id} {user_name}')
    questions = Question.objects.annotate(
        count_answers=Count('answer', distinct=True), 
        count_votes=Count('votequestion__id', distinct=True))[::-1][:10]
    context = {'questions': questions, 'user': user_name, 'id': user_id}
    print(questions)
    return render(request, 'quest/main.html', context)


@require_http_methods(['GET'])
def create_question(request, pk):
    category = QuestionCategory.objects.all()
    context = {'categories': category, 'user_id': pk}
    return render(request, 'quest/create_question.html', context)


@require_http_methods(['POST'])
def procesing_question(request, pk):
    user = Person.objects.get(pk=pk)
    
    post_data = request.POST.copy()
    post_data['author'] = pk
    
    form_question = QuestionsForm(post_data)
    if form_question.is_valid():
        form_question.save()
        messages.success(request, 'Pregunta creada exitosamente')
        url = reverse('quest:main') + \
            f'?user_id={user.id}&user_name={user.name}'
        return redirect(url)
    else:
        print('Formulario invalido')
        url = reverse('quest:main') + \
            f'?user_id={user.id}&user_name={user.name}'
        return redirect(url)
    
def answer(request, id_question, pk_user):
    question = Question.objects.get(pk=id_question)
    answers_question = Answer.objects.filter(question=question)
    context = {'question': question, 'answers': answers_question, 'user_id': pk_user}
    return render(request, 'quest/answers.html', context)

def create_answer(request, pk_question, pk_user):
    question = Question.objects.get(pk=pk_question)
    context = {'question': question, 'user_id':pk_user}
    return render(request, 'quest/create_answers.html', context)

def save_answer(request, pk_question, pk_user):
    user = Person.objects.get(pk=pk_user)
    post_data = request.POST.copy()
    post_data['question'] = pk_question
    post_data['author'] = pk_user
    form_answer = AnswerForm(post_data)
    
    if (form_answer.is_valid()):
        form_answer.save()
        messages.success(request, 'Respuesta creada exitosamente')
        return redirect(reverse('quest:main')+f'?user_id={user.id}&user_name={user.name}')
    else:
        messages.error(request, 'Error al crear la respuesta')
        return redirect(reverse('quest:main')+f'?user_id={user.id}&user_name={user.name}')
    
def vote_question(request, pk_question, pk_user):
    post_data = request.POST.copy()
    user = User.objects.get(pk=pk_user)
    post_data['question']=pk_question
    post_data['author']=pk_user
    post_data['vote']="upvote"
    form_vote = VoteQuestionForm(post_data)
    print(request.GET)
    if(form_vote.is_valid()):
        form_vote.save()
        messages.success(request, 'Voto exitoso')
        return redirect(reverse('quest:main')+f'?user_id={pk_user}&user_name={user.person.name}')
    return redirect(reverse('quest:main')+f'?user_id={pk_user}&user_name={user.person.name}')