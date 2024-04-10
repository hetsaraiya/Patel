from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signUp, name="signup"), # Done
    path("userProfile/", createUserProfile, name="userProfile"), # Done
    path("familyDetails/", createFamilyDetails, name="familyDetails"), # Done
    path("createPost/", createPost, name="createPost"), # Done
    path("addComment/", addComment, name="addComment"), # Done
    path("likePost/", likePost, name="likePost"), # Done
    path("makeMatrimonialProfile/", makeMatrimonialProfile, name="makeMatrimonialProfile"), # Done
    path("getCount/", getCount, name="getCount"), # Done
    path("login/", login, name="login"), # Done
    path("getUserDetails/", getUserDetails, name="getUserDetails"), # Done
]