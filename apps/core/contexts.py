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

    