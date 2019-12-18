from django import forms
from django.db import models
from django.utils import timezone
from .models import Project, Comment, Member, Category
from datetime import datetime
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_select2.forms import Select2MultipleWidget


class ProjectForm(forms.Form):
    project_name = forms.CharField(max_length=100)
    url = forms.CharField(max_length=200)
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))    
    contact_person_phone = forms.CharField(max_length=100, required=False)
    
    #Saca el str del modelo, poniendo el name saldran los nombres en el selector
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=Select2MultipleWidget, required=False)

    def save(self, args):
        start_dateData = self.data['start_date']
        end_dateData = self.data['end_date']        
        pk = self.data.get('projectID', '')        
        categories = ''
        for c in self.data.getlist('category'):
            categories += c + "#"
        categories = categories[:len(categories) - 1]
        
        if(pk):
            project = get_object_or_404(Project, id=pk)
            project.name = self.data['project_name']
            project.url = self.data['url']
            project.start_date = start_dateData
            project.end_date = end_dateData
            project.category = categories
        else:           
            project = Project(name = self.data['project_name'], url = self.data['url'], category = categories,
                         start_date = start_dateData, end_date = end_dateData, creator=args.user)
        
        project.save()
        return 'success'


class CommentForm(forms.Form):
    text = forms.CharField(max_length=100)
    
    def save(self, args):
        text = self.data['comment']
        project = self.data['projectId']
        comment = Comment(comment = text, idProject_id = project, author_id = args.user.id)        
        comment.save()
        return 'success'


class MemberJoinForm(forms.Form):   
    
    def save(self, args):
        projectID = self.data['projectId']
        member = Member(idProject_id = projectID, idUser_id = args.user.id)        
        member.save()
        return 'success'