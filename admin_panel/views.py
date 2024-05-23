from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import *
from .models import *

def admin_panel(request):
    tables = [
        ('User Profile', UserProfile.count_objects()),
        ('Category', Category.count_objects()),
        ('Project', Project.count_objects()),
        ('Tag', Tag.count_objects()),
        ('Donation', Donation.count_objects()),
        ('Comment', Comment.count_objects()),
        ('Reply', Reply.count_objects()),
        ('Project Cancellation', ProjectCancellation.count_objects()),
        ('Rating', Rating.count_objects()),
        ('Report', Report.count_objects()),
        ('Project Picture', ProjectPicture.count_objects()),
        ('Featured Project', FeaturedProject.count_objects()),
    ]
    return render(request, 'home/home_admin.html', {'tables': tables})


def user_profile_view(request):
    user_profiles = UserProfile.objects.all()
    return render(request, 'user_profile/user_profile.html', {'user_profiles': user_profiles})

def delete_profile(request, profile_id):
    if request.method == 'POST':
        try:
            profile = UserProfile.objects.get(id=profile_id)
            user_id = profile.user.id
            User.objects.filter(id=user_id).delete()
            profile.delete()
        except UserProfile.DoesNotExist:
            pass  
    return redirect('admin_panel:user_profile')

def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.exclude(pk=user_id).filter(email=email).exists():
                user_form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                user_form.save()
                profile_form.save()
                return redirect('admin_panel:user_profile') 
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        
    return render(request, 'user_profile/user_update_form.html', {'user_form': user_form, 'profile_form': profile_form})

def add_user(request):
    if request.method == 'POST':
        user_form = AddUserForm(request.POST)
        profile_form = AddUserProfileForm(request.POST, request.FILES)  

        if user_form.is_valid() and profile_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                user_form.add_error('email', 'This email is already in use. Please choose another one.')
            else:
                user_instance = user_form.save(commit=False)
                user_instance.set_password(user_form.cleaned_data["password"])
                user_instance.save()

                profile_instance = profile_form.save(commit=False)
                profile_instance.user = user_instance
                
                if 'image' in request.FILES:
                    profile_instance.image = request.FILES['image']
                    
                profile_instance.save()
                
                return redirect('admin_panel:user_profile')
    else:
        user_form = AddUserForm()
        profile_form = AddUserProfileForm()
        
    return render(request, 'user_profile/add_user_form.html', {'user_form': user_form, 'profile_form': profile_form})

###################################category################################

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category.html', {'categories': categories})

def delete_category(request, category_id):
    if request.method == 'POST':
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
        except Category.DoesNotExist:
            pass 
    return redirect('admin_panel:category_list')

def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryUpdateForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:category_list')
    else:
        form = CategoryUpdateForm(instance=category)
    return render(request, 'category/update_category.html', {'form': form})

def add_category(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:category_list') 
    else:
        form = AddCategoryForm()
    return render(request, 'category/add_category_form.html', {'form': form})


###################################featured project################################

def featured_projects(request):
    featured_projects = FeaturedProject.objects.all()
    return render(request, 'featured_project/featured_project.html', {'featured_projects': featured_projects})

def delete_featured_project(request, project_id):
    featured_project = FeaturedProject.objects.get(project_id=project_id)
    if request.method == 'POST':
        featured_project.delete()
        return redirect('admin_panel:featured_projects')
    return render(request, 'featured_project/featured_project.html', {'featured_projects': FeaturedProject.objects.all()})

def update_featured_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    featured_project = get_object_or_404(FeaturedProject, project=project)
    if request.method == 'POST':
        form = FeaturedProjectForm(request.POST, instance=featured_project)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:featured_projects')
    else:
        form = FeaturedProjectForm(instance=featured_project)
    return render(request, 'featured_project/featured_project_update_form.html', {'form': form})

def add_featured_project(request):
    if request.method == 'POST':
        form = FeaturedProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:featured_projects') 
    else:
        form = FeaturedProjectForm()
    return render(request, 'featured_project/add_featured_project.html', {'form': form})


###################################comment################################

def comment_list(request):
    comments = Comment.objects.all()
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        return redirect('admin_panel:comment')
    return render(request, 'comment/comment.html', {'comments': comments})

def add_comment(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:comment')
    else:
        form = CommentForm()
    return render(request, 'comment/addcomment.html', {'form': form})

def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_panel:comment'))
    else:
        form = CommentForm(instance=comment)
    return render(request, 'comment/updatecomment.html', {'form': form, 'comment': comment})



###################################donations################################

def add_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:donations')
    else:
        form = DonationForm()
    return render(request, 'donation/addDonations.html', {'form': form})

def update_donation(request, donation_id):
    donation = get_object_or_404(Donation, pk=donation_id)
    
    if request.method == 'POST':
        form = DonationForm(request.POST, instance=donation)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:donations')
    else:
        form = DonationForm(instance=donation)
    
    return render(request, 'donation/updateDonations.html', {'form': form, 'donation': donation})

def list_donations(request):
    donations = Donation.objects.all()
    if request.method == 'POST':
        donation_id = request.POST.get('donation_id')
        donation = get_object_or_404(Donation , pk=donation_id)
        donation.delete()
        return redirect('admin_panel:donations')
    return render(request, 'donation/donations.html', {'donations': donations})



###################################reply################################

def add_reply(request):
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:replies')
    else:
        form = ReplyForm()
    return render(request, 'reply/addReply.html', {'form': form})

def update_reply(request, reply_id):
    reply = get_object_or_404(Reply, pk=reply_id)
    
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:replies')
    else:
        form = ReplyForm(instance=reply)
    
    return render(request, 'reply/updateReply.html', {'form': form, 'reply': reply})

def list_replies(request):
    replies = Reply.objects.all()
    
    if request.method == 'POST':
        reply_id = request.POST.get('reply_id')
        reply = get_object_or_404(Reply, pk=reply_id)
        reply.delete()
        return redirect('admin_panel:replies')
    
    return render(request, 'reply/reply.html', {'replies': replies})



###################################tags################################

def show_added_tags(request):
    tags = Tag.objects.all()
    return render(request, 'tag/show_addTag.html', {'tags': tags})

def add_tag(request):
    if request.method == 'POST':
        form = TagSelectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            projects = form.cleaned_data['projects']
            tag = Tag.objects.create(name=name)
            tag.projects.set(projects)
            tag.save()
            return redirect('admin_panel:show_added_tags')
    else:
        form = TagSelectionForm()
    return render(request, 'tag/add_tag.html', {'form': form})

def update_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    if request.method == 'POST':
        form = TagSelectionForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:show_added_tags')
    else:
        form = TagSelectionForm(instance=tag)
    return render(request, 'tag/update_tag.html', {'form': form})

def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tag.delete()
    return redirect('admin_panel:show_added_tags')



###################################rate################################

def show_rate(request):
    ratings = Rating.objects.all()
    return render(request, 'rate/show_rate.html', {'ratings': ratings})

def rate_project(request):
    if request.method == 'POST':
        form = RateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:show_rate')  
    else:
        form = RateProjectForm()
    return render(request, 'rate/adding_rate.html', {'form': form})

def update_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    if request.method == 'POST':
        form = RateProjectForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:show_rate')
    else:
        form = RateProjectForm(instance=rating)
    return render(request, 'rate/update_rate.html', {'form': form})

def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    rating.delete()
    return redirect('admin_panel:show_rate')



###################################report################################

def add_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:show_reports')
    else:
        form = ReportForm()
    return render(request, 'report/addReport.html', {'form': form})

def show_reports(request):
    reports = Report.objects.all()
    return render(request, 'report/showReports.html', {'reports': reports})

def update_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:show_reports')
    else:
        form = ReportForm(instance=report)
    return render(request, 'report/updateReport.html', {'form': form})

def delete_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.delete()
    return redirect('admin_panel:show_reports')



###################################project################################

def project_list_view(request):
    projects = Project.objects.all() 
    return render(request, 'project/project.html', {'projects': projects})

def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=project_id)
        project.delete()
        return redirect('admin_panel:project')  

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:project')  
    else:
        form = ProjectForm(instance=project)
    return render(request, 'project/project_update_form.html', {'project_form': form})

def add_project(request):
    if request.method == 'POST':
        project_form = AddProjectForm(request.POST, request.FILES)
        if project_form.is_valid():
            project_instance = project_form.save(commit=False)
            project_instance.save()
            return redirect('admin_panel:project')  
    else:
        project_form = AddProjectForm()
        
    return render(request, 'project/add_project_form.html', {'project_form': project_form})



###################################cancellation################################

def cancellation_list(request):
    cancellations = ProjectCancellation.objects.all()
    return render(request, 'cancel_project/cancellation_list.html', {'cancellations': cancellations})

def create_cancellation(request):
    if request.method == 'POST':
        form = ProjectCancellationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:cancellation_list')
    else:
        form = ProjectCancellationForm()
    return render(request, 'cancel_project/create_cancellation.html', {'form': form})

def delete_cancellation(request, cancellation_id):
    cancellation = get_object_or_404(ProjectCancellation, pk=cancellation_id)
    if request.method == 'POST':
        cancellation.delete()
        return redirect('admin_panel:cancellation_list')
    return render(request, 'cancel_project/cancellation_detail.html', {'cancellation': cancellation})

def update_cancellation(request, cancellation_id):
    cancellation = get_object_or_404(ProjectCancellation, pk=cancellation_id)
    if request.method == 'POST':
        form = ProjectCancellationForm(request.POST, instance=cancellation)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:cancellation_list')
    else:
        form = ProjectCancellationForm(instance=cancellation)
    return render(request, 'cancel_project/update_cancellation.html', {'form': form})


###################################project pictures################################

def project_picture_list(request):
    project_pictures = ProjectPicture.objects.all()
    return render(request, 'picture/project_picture_list.html', {'project_pictures': project_pictures})

def add_project_picture(request):
    if request.method == 'POST':
        form = ProjectPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:project_picture_list')
    else:
        form = ProjectPictureForm()
    return render(request, 'picture/add_project_picture.html', {'form': form})

def update_project_picture(request, picture_id):
    picture = get_object_or_404(ProjectPicture, pk=picture_id)
    if request.method == 'POST':
        form = ProjectPictureForm(request.POST, request.FILES, instance=picture)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:project_picture_list')
    else:
        form = ProjectPictureForm(instance=picture)
    return render(request, 'picture/update_project_picture.html', {'form': form})

def delete_project_picture(request, picture_id):
    picture = get_object_or_404(ProjectPicture, pk=picture_id)
    if request.method == 'POST':
        picture.delete()
        return redirect('admin_panel:project_picture_list')
    project_pictures = ProjectPicture.objects.all()
    return render(request, 'picture/project_picture_list.html', {'project_pictures': project_pictures})
