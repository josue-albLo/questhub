from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=200, default='Sin direccion')
    city = models.CharField(max_length=50, default='Sin ciudad')
    
    def __str__(self):
        return f'{self.name} {self.last_name}'
    
    class Meta:
        db_table = 'person'
    
class User(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    email = models.EmailField(max_length=254)
    
    def __str__(self):
        return f'{self.username}'
    
    class Meta:
        db_table = 'user'
        
class QuestionCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        db_table = 'question_category'
        
    
    def __str__(self):
        return f'{self.vote}'
    
    class Meta:
        db_table = 'vote'
    
class Question(models.Model):
    title = models.CharField(max_length=200)
    question = models.TextField()
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    
    def __str__(self):
        return f'{self.question}'
    
    class Meta:
        db_table = 'question'
    
    

class Answer(models.Model):
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.answer}'
    
    class Meta:
        db_table = 'answer'

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.comment}'
    
    class Meta:
        db_table = 'comment'
        
class Vote(models.Model):
    # upvote = 1 and downvote = 0
    vote = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'Has been voted {self.vote}'
    
    class Meta:
        db_table = 'vote'
    