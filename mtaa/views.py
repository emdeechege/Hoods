from django.shortcuts import render,redirect,get_object_or_404
from django.http  import HttpResponse,Http404,HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib import messages
# from django.views.generic.edit import UpdateView

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            current_user = form.save(commit=False)
            current_user.is_active = False
            current_user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your MtaaHood Account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': current_user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(current_user.pk)),
                'token':account_activation_token.make_token(current_user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        current_user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        current_user = None
    if current_user is not None and account_activation_token.check_token(current_user, token):
        current_user.is_active = True
        current_user.save()
        login(request, current_user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. <a href="https://mtaanihoods.herokuapp.com"> Login </a> Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def home(request):

	if request.user.is_authenticated:
		if Join.objects.filter(user_id = request.user).exists():
			hood = Hood.objects.get(pk = request.user.join.hood_id.id)
			posts =" Posts.objects.filter(hood = request.user.join.hood_id.id)"
			businesses = Business.objects.filter(hood = request.user.join.hood_id.id)

			return render(request,'hoods/hood.html',{"hood":hood,"businesses":businesses,"posts":posts})
		else:
			neighbourhoods = Hood.objects.all()
			return render(request,'index.html',{"neighbourhoods":neighbourhoods})
	else:
		neighbourhoods = Hood.objects.all()
		return render(request,'index.html',{"neighbourhoods":neighbourhoods})

def new_business(request):
    current_user = request.user

    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.save()
            return redirect('home')

    else:
        form = BusinessForm()
    return render(request, 'business.html', {"form": form})

@login_required(login_url='/accounts/login/')
def profile(request):
	'''
	This view function will fetch a user's profile
	'''
	profile = Profile.objects.get(user = request.user)
	return render(request,'profiles/profile.html',{"profile":profile})

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user = request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES,instance = profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.email = current_user.email
            profile.save()
        return redirect('profile')

    else:
        form = EditProfileForm(instance = profile)
    return render(request, 'profiles/edit_profile.html', {"form": form})

def hoods(request):

	hood = Hood.objects.filter(user = request.user)

	return render(request,'hoods/hood.html',{"hood":hood})

@login_required(login_url='/accounts/login/')
def join(request,hoodId):

	neighbourhood = Hood.objects.get(pk = hoodId)
	if Join.objects.filter(user_id = request.user).exists():

		Join.objects.filter(user_id = request.user).update(hood_id = neighbourhood)
	else:

		Join(user_id=request.user,hood_id = neighbourhood).save()

	messages.success(request, 'Success! You have succesfully joined this Neighbourhood ')
	return redirect('home')

@login_required(login_url='/accounts/login/')
def exitHood(request,hoodId):

	if Join.objects.filter(user_id = request.user).exists():
		Join.objects.get(user_id = request.user).delete()
		messages.error(request, 'You have succesfully exited this Neighbourhood.')
		return redirect('home')

@login_required(login_url='/accounts/login/')
def create_post(request):

	if Join.objects.filter(user_id = request.user).exists():
		if request.method == 'POST':
			form = PostForm(request.POST)
			if form.is_valid():
				post = form.save(commit = False)
				post.user = request.user
				post.hood = request.user.join.hood_id
				post.save()
				messages.success(request,'You have succesfully created a Forum Post')
				return redirect('home')
		else:
			form = PostForm()
		return render(request,'posts/createpost.html',{"form":form})
