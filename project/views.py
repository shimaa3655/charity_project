from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from project.forms import *
from project.models import *
from django.contrib import messages

def home(request):
    user_country = None
    nearby_projects = None
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            user_profile = UserProfile.objects.get(user__pk=user_id)
            user_country = user_profile.country

        except UserProfile.DoesNotExist:
            pass
   
    if user_country:
        nearby_projects = Project.objects.filter(country=user_country) 
    
    top_projects = Project.top_rated_projects()
    featured_projects = FeaturedProject.objects.filter(is_featured=True)
    newest_featured_projects = FeaturedProject.newest_featured_projects()

    categories = Category.objects.all() 
    
    if nearby_projects is not None:
        nearby_projects = [project for project in nearby_projects if not project.is_cancelled and project.progress_percentage != 100 and project.end_time > timezone.now()][:5]
    
    if top_projects is not None:
        top_projects = [project for project in top_projects if not project.is_cancelled and project.progress_percentage != 100 and project.end_time > timezone.now()][:5]
    
   

    for project in top_projects:
     project.average_rating = Rating.average_rating(project)

    for project in nearby_projects:
     project.average_rating = Rating.average_rating(project)

    for featured_project in featured_projects:
        featured_project.project.average_rating = Rating.average_rating(featured_project.project)



    return render(request, 'homepage/home.html', {'projects': top_projects, 'nearby_projects': nearby_projects, 'categories': categories,'newest_featured_projects': newest_featured_projects})








def category_detail(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    try:
        projects_query = Project.objects.filter(category=category)
        projects = [project for project in projects_query if not project.is_cancelled and project.progress_percentage != 100 and project.end_time > timezone.now()]
    except Exception as e:
        projects = []

    for project in projects:
     project.average_rating = Rating.average_rating(project)


    return render(request, 'homepage/category_detail.html', {'category': category, 'projects': projects})




def search_projects(request):
    query = request.GET.get('query')

    projects_query = Project.objects.filter(title__icontains=query) | Project.objects.filter(tags__name__icontains=query)
    projects = [project for project in projects_query if not project.is_cancelled and project.progress_percentage != 100 and project.end_time > timezone.now()]
     
    for project in projects:
        project.average_rating = Rating.average_rating(project)

    return render(request, 'homepage/search_results.html', {'projects': projects})




def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(creator=request.user)
            return redirect('project:home')  
    else:
        form = ProjectForm()
    return render(request, 'createproject/create_project.html', {'form': form})





def view_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    comments = Comment.objects.filter(project_id=project_id)
    
    project_tags = project.tags.all()
    projects_query = Project.objects
    for tag in project_tags:
        projects_query = projects_query.filter(tags__name__icontains=tag.name)

   
    projects_query = projects_query.exclude(id=project_id).distinct()
    
    projects_tag = [project for project in projects_query if not project.is_cancelled and project.progress_percentage != 100 and project.end_time > timezone.now()][:4]

    for related_project in projects_tag:
        related_project.average_rating = Rating.average_rating(related_project)
        print("Related project tags:", related_project.tags.all())
  
    return render(request, 'viewPage/viewProject.html', {'project': project, 'comments': comments , 'projects_tag': projects_tag})




def submit_comment(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        comment_text = request.POST.get('comment')
        
       
        comment = Comment.objects.create(
            user=request.user, 
            project_id=project_id,
            text=comment_text
        )
        
       
        return redirect('project:view_project', project_id=project_id)
   





def add_rate(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        rating = request.POST.get('rating')
        user = request.user

        existing_rate = Rating.objects.filter(user=user, project_id=project_id).exists()
        if existing_rate:
            messages.error(request, "You have already rated this project.")
            return redirect('project:view_project', project_id=project_id)
            
        new_rating = Rating.objects.create(user=user, project_id=project_id, rating=rating)

        messages.success(request, "Thank you for rating this project!")

        return redirect('project:view_project', project_id=project_id)
    
    else:
       return redirect('project:view_project', project_id=project_id)
    




def report_comment(request):
    if request.method == 'POST':
        project_id = request.POST.get('project')
        comment_id = request.POST.get('comment')
        reason = request.POST.get('reason')
        user_id = request.POST.get('user')
        
        report = Report.objects.create(
            project_id=project_id,
             user_id=user_id,
            comment_id=comment_id,
            reason=reason,
           
        )
        
        return redirect('project:view_project', project_id=project_id)
    


def report_project(request):
     if request.method == 'POST':
        project_id = request.POST.get('project')
        reason = request.POST.get('reason')
        user_id = request.POST.get('user')
        
        report = Report.objects.create(
            project_id=project_id,
             user_id=user_id,
            reason=reason,
           
        )
        
       
        return redirect('project:view_project', project_id=project_id)
        
    