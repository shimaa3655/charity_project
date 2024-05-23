from django.urls import path
from . import views

app_name = 'project'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('create/', views.create_project, name='create_project'),
    path('search/', views.search_projects, name='search_projects'),
    path('report/project',views.report_project, name='report_project'),
    path('project/<int:project_id>/', views.view_project, name='view_project'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    path('add_rate/', views.add_rate, name='add_rate'),
    path('report/',views.report_comment, name='report_comment'),
    path('report/project',views.report_project, name='report_project'),
]
