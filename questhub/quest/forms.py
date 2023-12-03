from django.forms import ModelForm
from .models import User, Question, Answer, VoteQuestion, VoteAnswer

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        
class QuestionsForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','question','category','author']
        
class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['answer','question','author']
        
class VoteQuestionForm(ModelForm):
    class Meta:
        model = VoteQuestion
        fields = ['vote','author', 'question']

class VoteAnswerForm(ModelForm):
    class Meta:
        model = VoteAnswer
        fields = ['vote','author', 'answer']
