from project.models import UserProfile

def user_info(request):
    user_id = None
    username = None
    user_profile = None

    if 'user_id' in request.session:
        user_id = request.session['user_id']

        try:
            user_profile = UserProfile.objects.get(user_id=user_id)
            username = user_profile.user.username
        except UserProfile.DoesNotExist:
            pass
    
    return {
        'username': username,
        'user_profile': user_profile,
    }
