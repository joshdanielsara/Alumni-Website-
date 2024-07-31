from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q

from .forms import UserProfileForm

from .forms import ProfileForm, ProfilePictureForm

from .forms import (
    PostForm, 
    CustomRegistrationForm, 
    CommentForm, 
    MessageForm, 
    ProfileForm
)
from .models import (
    UserProfile, 
    Post, 
    Comment, 
    Message, 
    Group, 
    Profile
)



def home(request):
    return render(request, 'home.html')




@login_required(login_url='login')
def jobs(request):
    all_posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'jobs.html', {'posts': all_posts, 'comment_form': comment_form, 'current_user': request.user})

@login_required(login_url='login')
def news(request):
    all_posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'news.html', {'posts': all_posts, 'comment_form': comment_form, 'current_user': request.user})

@login_required(login_url='login')
def events(request):
    all_posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'events.html', {'posts': all_posts, 'comment_form': comment_form, 'current_user': request.user})




def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_post')
            else:
                return redirect('home')
        else:
            response = HttpResponse(
                """
                <script>
                    alert("Invalid login credentials.");
                    window.location.href = '/login';
                </script>
                """
            )
            return response

    return render(request, 'login.html')


class CustomRegistrationForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30)
   
    last_name = forms.CharField(max_length=30)
   

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validate input
        if not username or not first_name or not last_name or not email or not password1 or not password2:
            response = HttpResponse(
                """
                <script>
                    alert("All fields are required.");
                    window.location.href = '/register';
                </script>
                """
            )
            return response

        if password1 != password2:
            response = HttpResponse(
                """
                <script>
                    alert("Passwords do not match.");
                    window.location.href = '/register';
                </script>
                """
            )
            return response

        if User.objects.filter(username=username).exists():
            response = HttpResponse(
                """
                <script>
                    alert("This username is already taken.");
                    window.location.href = '/register';
                </script>
                """
            )
            return response

        # Create a new user
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create a user profile
        user_profile = UserProfile(user=user)
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.save()

        response = HttpResponse(
            """
            <script>
                alert("Your account has been successfully created.");
                window.location.href = '/login';
            </script>
            """
        )
        return response
    else:
        return render(request, "register.html")








@login_required(login_url='login')
def admin_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post successfully created.')
            return redirect('admin_post')
    else:
        form = PostForm()

    posts = Post.objects.all()
    return render(request, 'admin.html', {'form': form, 'posts': posts})



@login_required(login_url='login')
def post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Post successfully created.')
            return redirect('admin_post')
    else:
        form = PostForm()

    return render(request, 'admin.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    # Check if the user has already liked the post
    if user in post.likes.all():
        # If yes, unlike the post
        post.likes.remove(user)
    else:
        # If not, like the post
        post.likes.add(user)

    # Get the updated like count
    likes_count = post.likes.count()

    return JsonResponse({'likes': likes_count, 'liked': user in post.likes.all()})


@login_required(login_url='login')
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()

            # Prepare response data
            response_data = {
                'comment': {
                    'id': comment.id,
                    'user': {
                        'username': comment.user.username,
                        'first_name': comment.user.first_name
                    },
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
                }
            }

            # Return JSON response with comment data
            return JsonResponse(response_data)
        else:
            # Return an error response if form is invalid
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    # For non-POST requests or when the form is invalid
    return JsonResponse({'error': 'Method not allowed'}, status=405)



def get_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().values(
        'id', 'content', 'created_at', 'user__username', 'user__first_name'
    )
    # Format created_at to a human-readable format
    formatted_comments = [
        {
            'id': comment['id'],
            'content': comment['content'],
            'created_at': comment['created_at'].strftime('%B %d, %Y, %I:%M %p'),
            'user': {
                'username': comment['user__username'],
                'first_name': comment['user__first_name']
            }
        } for comment in comments
    ]
    return JsonResponse({'comments': formatted_comments})



@login_required(login_url='login')
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)









@login_required(login_url='login')
def send_message(request, receiver_id=None):
    if receiver_id is not None:
        recipient = get_object_or_404(User, pk=receiver_id)
    else:
        recipient = None

    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            message = Message(sender=request.user, content=content)
            if recipient:
                message.receiver = recipient
            message.save()
            return redirect('send_message', receiver_id=recipient.id) if recipient else redirect('send_message')

    # Handle search query
    query = request.GET.get('query')
    if query:
        group_messages = Message.objects.filter(
            Q(content__icontains=query),
            receiver=None
        ).order_by('-timestamp')[::-1]
    else:
        group_messages = Message.objects.filter(receiver=None).order_by('-timestamp')[::-1]

    return render(request, 'send_message.html', {'group_messages': group_messages, 'recipient': recipient})







@login_required(login_url='login')
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    if request.method == 'POST':
        message.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required(login_url='login')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=user_profile)
        profile_picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)

        if profile_form.is_valid() and profile_picture_form.is_valid():
            profile_form.save()
            profile_picture_form.save()

            # Update the User model fields
            user = request.user
            user.first_name = profile_form.cleaned_data['first_name']
            user.last_name = profile_form.cleaned_data['last_name']
            user.save()

            return redirect('profile')
    else:
        profile_form = ProfileForm(instance=user_profile)
        profile_picture_form = ProfilePictureForm(instance=user_profile)

    profile_picture_url = user_profile.profile_picture.url if user_profile.profile_picture else None

    return render(request, 'profile.html', {'profile': user_profile, 'profile_form': profile_form, 'profile_picture_url': profile_picture_url})








@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'user_profile.html'

    def get(self, request, username):
        viewed_user = get_object_or_404(User, username=username)
        logged_in_user = request.user

        viewed_user_profile, created = UserProfile.objects.get_or_create(user=viewed_user)
        viewed_user_profile_form = UserProfileForm(instance=viewed_user_profile)

        # Ensure that the profile picture URL is available
        profile_picture_url = viewed_user_profile.profile_picture.url if viewed_user_profile.profile_picture else None

        return render(request, self.template_name, {
            'viewed_user': viewed_user,
            'logged_in_user': logged_in_user,
            'viewed_user_profile': viewed_user_profile,
            'profile_picture_url': profile_picture_url,
        })



class SearchUserView(View):
    template_name = 'search_user.html'

    def get(self, request):
        query = request.GET.get('q', '')  # Default to an empty string if 'q' is None

        if query:
            results = User.objects.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query) |
                Q(userprofile__year_graduated__icontains=query) |
                Q(userprofile__strand__icontains=query)
            ).distinct()
        else:
            results = []

        return render(request, self.template_name, {'results': results, 'query': query})





