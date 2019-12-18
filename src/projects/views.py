from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from .forms import ProjectForm, CommentForm, MemberJoinForm
from django.utils import timezone
from .models import Project, Comment, Member, Category
from django.contrib.auth import get_user_model
import json
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.utils import formats
from django.contrib import messages


def new_project(request):
    form = ProjectForm()
    user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST) 
        if form.is_valid():
            form.save(request)
            messages.success(request, "Project added with success!")
            return redirect('/projects')

    return render(request, 'projects/new_project.html', {'form': form, 'user':user})

def editProject(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = request.user
    if user != project.creator:
        return redirect('../projects', {})
    
    start_datetime = formats.date_format(project.start_date, 'Y-m-d')
    end_datetime = formats.date_format(project.end_date, 'Y-m-d')
    
    form = ProjectForm(initial={'project_name':project.name,'url': project.url,
     'start_date': start_datetime, 'end_date':end_datetime})
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save(request)
            return redirect('/project/'+ str(pk))
    return render(request, 'projects/editProject.html', {'form': form, 'project':project, 'user':user})

def projects(request):
    projects = Project.objects.all()
    if request.GET.get('keywords'):
        projects = projects.filter(name__icontains = request.GET['keywords'])
    
    if request.GET.get('category'):
        projects = projects.filter(category__icontains = request.GET['category'])

    return render(request, 'projects/projects.html', {'projects':projects})

def personal_projects(request):   
    projects = Project.objects.all()
    projects = projects.filter(creator = request.user)

    return render(request, 'projects/projects.html', {'projects':projects})    

def testing(request):
    projects_list = Project.objects.all()
    paginator = Paginator(projects_list, 3) # Show 5  per page
    page = request.GET.get('page')
    projects = paginator.get_page(page)

    return render(request, 'projects/testing.html', {'projects':projects})


def project(request, pk):
    project = get_object_or_404(Project, id=pk)
    proj_categories = project.category.split('#')
    categories = ''
    if proj_categories[0] != '':
        categories = Category.objects.filter(id__in=proj_categories)
    if request.method == 'POST':
        if request.POST.get('comment', ''):
            form = CommentForm(request.POST)
        else:
            form = MemberJoinForm(request.POST)
        form.save(request)
      
    try:
        if not request.user.is_anonymous:
            Member.objects.get(idProject_id=pk, idUser_id=request.user)
            member = True
        else:
            member = False
    except Member.DoesNotExist:
        member = False
    try: 
        comments = Comment.objects.filter(idProject_id=pk)
    except Comment.DoesNotExist:
        comments = None  

    return render(request, 'projects/project.html', {'project':project, 'comments':comments, 
        'member': member, 'categories': categories})
    #return render(request, 'projects/project.html', {'project':project})
    


def overview(request):
    projects_list = Project.objects.get_queryset().order_by('id')
    comments = Comment.objects.all()
    users = get_user_model().objects.all()
    paginator = Paginator(projects_list, 3) 
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'projects/overview.html',
         {'projects':projects, 'projects_list': projects_list, 'comments': comments, 'users': users})


def dashboard(request):
    projects_list = Project.objects.get_queryset().order_by('id')
    projects_list = projects_list.filter(creator = request.user)

    comments = Comment.objects.filter(author_id = request.user)
    joined = Member.objects.filter(idUser_id = request.user)

    paginator = Paginator(projects_list, 3) 
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'projects/dashboard.html',
         {'projects':projects, 'projects_list': projects_list, 'comments': comments, 'joined': joined})

def deleteProject(request, pk):
    obj = get_object_or_404(Project, id=pk)
    obj.delete()
    projects = Project.objects.all()            
    
    return redirect('../overview', {'projects':projects})
    #return render(request, 'projects/projects.html', {'projects':projects}) 


def text_autocomplete(request):    
    if request.GET.get('q'):
        text = request.GET['q']
        data = Project.objects.filter(name__icontains=text).values_list('name',flat=True)
        json = list(data)
        return JsonResponse(json, safe=False)
    else:
        return HttpResponse("No cookies")