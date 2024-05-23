from django.contrib import admin
from .models import UserProfile, Tag, Category, Project, Donation, Comment, Reply, ProjectCancellation, Rating, Report,FeaturedProject,ProjectPicture

# Register your models.
admin.site.register(UserProfile)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(ProjectCancellation)
admin.site.register(Rating)
admin.site.register(Report)
admin.site.register(FeaturedProject)
admin.site.register(ProjectPicture)
