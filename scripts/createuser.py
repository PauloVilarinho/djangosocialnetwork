from socialnetwork.models import *

def run():

    profiles = Profile.objects.all()

    for profile in profiles:
        name = profile.name.split(" ")[0] + str(profile.id)
        user = User.objects.create_user(username=name, email=profile.email, password=name)
        profile.user = user
        profile.save()

    print("users created")
