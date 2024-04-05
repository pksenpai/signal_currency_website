from apps.users.models import Profile


def profile_image(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        
        context = {
            "image": profile.image,
            "alt": profile.alt,
        }
        
        return context
    return {}

# def background_image(request):
#     context = {
#         "background_image": f"/static/core/pics/{request.path}.jpg"
#     }
#     return context
    
    