from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
#########################  UserProfile  ################################

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.CharField(max_length=15)  
    profile_picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    @classmethod
    def count_objects(cls):
        return cls.objects.count()

#######################   Category  ################################

class Category(models.Model):
    name = models.CharField(max_length=100)

    @classmethod
    def count_objects(cls):
        return cls.objects.count()

##########################   Project #######################################################
class Project(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    country = models.CharField(max_length=100, null=True, blank=True) 

    def total_donations(self):
        return self.donation_set.aggregate(models.Sum('amount'))['amount__sum'] or 0

    def total_ratings(self):
        return self.rating_set.aggregate(models.Sum('rating'))['rating__sum'] or 0
    
  
    def pictures(self):
       
        picture = self.projectpicture_set.first()
        if picture:
            return picture.image.url
        else:
            return None   

    def remaining_time(self):
        now = timezone.now()
        time_left = self.end_time - now
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        months = days // 30
        remaining_days = days % 30
        remaining_time_msg = f"{months} months, {remaining_days} days, {hours} hours"
        return remaining_time_msg

    @staticmethod
    def top_rated_projects():
        top_projects = Project.objects.annotate(total_rating=models.Sum('rating__rating')).order_by('-total_rating')
        return top_projects
    

    @property
    def progress_percentage(self):
        if self.total_target > 0:
            return (self.total_donations() / self.total_target) * 100
        else:
            return 0 
        

    @classmethod
    def count_objects(cls):
        return cls.objects.count()    
        


#########################  Tag  ################################

class Tag(models.Model):
    name = models.CharField(max_length=50)
    projects = models.ManyToManyField(Project, related_name='tags')

    @classmethod
    def count_objects(cls):
        return cls.objects.count()

############################  Donation  ####################################################

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def count_objects(cls):
        return cls.objects.count() 

#################################   Comment  ################################################

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.text

    @classmethod
    def count_objects(cls):
        return cls.objects.count()

#################################   Reply   #################################################

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    @classmethod
    def count_objects(cls):
        return cls.objects.count()    

###########################    ProjectCancellation    ################################

class ProjectCancellation(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    cancellation_reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def count_objects(cls):
        return cls.objects.count()

##########################   Rating   #########################################    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def _str_(self):
        return f"{self.user.username} - {self.project.title}: {self.rating}"
    
    @classmethod
    def count_objects(cls):
        return cls.objects.count()
    
    @classmethod
    def average_rating(cls, project):
        all_ratings = cls.objects.filter(project=project)
        total_rating = sum(rating.rating for rating in all_ratings)
        
        if all_ratings.exists():
            average_rating = (total_rating / all_ratings.count()) * 20  
        else:
            average_rating = 0
        
        return average_rating

##############################  Report   ####################################    

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    REPORT_CHOICES = (
        ('spam', 'Spam or scam'),
        ('inappropriate', 'Inappropriate content'),
        ('other', 'Other'),
    )

    def _str_(self):
        return f"Report by {self.user.username} on {self.created_at}"
    
    @classmethod
    def count_objects(cls):
        return cls.objects.count()
 

########################## Project Picture ####################################

class ProjectPicture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_pictures/%Y/%m/%d')
 
    @classmethod
    def count_objects(cls):
        return cls.objects.count()

########################### featured projects#####################################

class FeaturedProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='featured_project')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    @staticmethod
    def newest_featured_projects():
        return FeaturedProject.objects.filter(is_featured=True).order_by('-created_at')[:5]

    @classmethod
    def count_objects(cls):
        return cls.objects.count()
