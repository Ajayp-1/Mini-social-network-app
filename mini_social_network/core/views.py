from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from .models import Post, Like, Comment
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from django.core.paginator import Paginator
from django.db import connection

# Import numpy and pandas with error handling
try:
    import numpy as np
    import pandas as pd
    ANALYTICS_DEPS_AVAILABLE = True
except ImportError:
    ANALYTICS_DEPS_AVAILABLE = False


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('feed')


def feed_view(request):
    posts = Post.objects.all().select_related('author').prefetch_related('likes', 'comments')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get liked posts for current user
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    return render(request, 'core/feed.html', {
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'user_likes': liked_posts
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if content:
            post = Post.objects.create(
                author=request.user,
                content=content,
                image=image
            )
            messages.success(request, 'Post created successfully!')
            return redirect('feed')
        else:
            messages.error(request, 'Content is required!')
    
    return render(request, 'core/create_post.html')


@login_required
def edit_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if content:
            post.content = content
            if image:
                post.image = image
            post.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('feed')
        else:
            messages.error(request, 'Content is required!')
    
    return render(request, 'core/edit_post.html', {'post': post})


@login_required
def delete_post_view(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('feed')
    
    return render(request, 'core/delete_post.html', {'post': post})


@login_required
@require_POST
def toggle_like_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        messages.success(request, 'Post unliked!')
    else:
        messages.success(request, 'Post liked!')
    
    return redirect('feed')


@login_required
@require_POST
def add_comment_view(request, pk):
    post = get_object_or_404(Post, pk=pk)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            author=request.user,
            post=post,
            content=content
        )
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Comment content is required!')
    
    return redirect('feed')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).select_related('author').prefetch_related('likes', 'comments')
    
    # Calculate user stats
    total_posts = posts.count()
    total_likes = Like.objects.filter(post__author=user).count()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get liked posts for current user
    liked_posts = []
    if request.user.is_authenticated:
        liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)
    
    return render(request, 'core/profile.html', {
        'profile_user': user,
        'posts': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'total_posts': total_posts,
        'total_likes': total_likes,
        'user_likes': liked_posts
    })


def analytics_view(request):
    # Basic statistics
    total_posts = Post.objects.count()
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()
    # Simple averages for template (avoid unsupported template filters)
    avg_comments_per_post = float(total_comments) / float(total_posts) if total_posts > 0 else 0.0
    avg_posts_per_user = float(total_posts) / float(total_users) if total_users > 0 else 0.0
    
    # Top 3 most liked posts
    # Avoid clashing with Post.like_count @property by using a different annotation name
    top_posts = Post.objects.annotate(
        likes_count=Count('likes')
    ).order_by('-likes_count')[:3]
    
    # Top 5 users by number of posts for chart
    top_users = User.objects.annotate(
        post_count=Count('posts')
    ).order_by('-post_count')[:5]
    
    # Create matplotlib chart
    graphic = None
    try:
        if top_users:
            usernames = [user.username for user in top_users]
            post_counts = [user.post_count for user in top_users]
            
            plt.figure(figsize=(10, 6))
            plt.bar(usernames, post_counts, color='skyblue')
            plt.title('Top 5 Users by Number of Posts')
            plt.xlabel('Users')
            plt.ylabel('Number of Posts')
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            # Save plot to base64 string
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            graphic = base64.b64encode(image_png)
            graphic = graphic.decode('utf-8')
            plt.close()
    except Exception as e:
        messages.error(request, f"Error generating chart: {str(e)}")
    
    # Default values for analytics data
    avg_likes_per_post = 0.0
    std_likes_per_post = 0.0
    posts_by_day = []
    
    # Use pandas and numpy for additional metrics if available
    if ANALYTICS_DEPS_AVAILABLE:
        try:
            # Likes per post distribution
            likes_per_post = list(
                Like.objects.values('post_id').annotate(cnt=Count('id')).values_list('cnt', flat=True)
            )
            avg_likes_per_post = float(np.mean(likes_per_post)) if likes_per_post else 0.0
            std_likes_per_post = float(np.std(likes_per_post)) if likes_per_post else 0.0

            # Posts by day using raw SQL + pandas
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT strftime('%Y-%m-%d', created_at) AS day, COUNT(*) AS count
                    FROM core_post
                    GROUP BY day
                    ORDER BY day
                    """
                )
                rows = cursor.fetchall()
            posts_by_day_df = pd.DataFrame(rows, columns=['day', 'count'])
            posts_by_day = posts_by_day_df.to_dict(orient='records')
        except Exception as e:
            messages.error(request, f"Error processing analytics data: {str(e)}")
    else:
        messages.warning(request, "Advanced analytics features are disabled. Install numpy and pandas to enable them.")
        # Fallback for posts by day using Django ORM
        from django.db.models.functions import TruncDate
        posts_by_day_qs = Post.objects.annotate(
            day=TruncDate('created_at')
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        posts_by_day = [{'day': item['day'].strftime('%Y-%m-%d'), 'count': item['count']} for item in posts_by_day_qs]

    return render(request, 'core/analytics.html', {
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_users': total_users,
        'top_posts': top_posts,
        'chart_url': graphic,
        'avg_likes_per_post': avg_likes_per_post,
        'std_likes_per_post': std_likes_per_post,
        'avg_comments_per_post': avg_comments_per_post,
        'avg_posts_per_user': avg_posts_per_user,
        'posts_by_day': posts_by_day,
        'analytics_deps_available': ANALYTICS_DEPS_AVAILABLE,
    })


def analytics_data_view(request):
    """Return analytics data as JSON using raw SQL, pandas, and numpy."""
    total_posts = Post.objects.count()
    total_likes = Like.objects.count()
    total_comments = Comment.objects.count()
    total_users = User.objects.count()

    # Default values
    labels = []
    data = []
    avg_likes = 0.0
    std_likes = 0.0

    if ANALYTICS_DEPS_AVAILABLE:
        try:
            # Posts by day via raw SQL
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT strftime('%Y-%m-%d', created_at) AS day, COUNT(*) AS count
                    FROM core_post
                    GROUP BY day
                    ORDER BY day
                    """
                )
                rows = cursor.fetchall()
            posts_by_day_df = pd.DataFrame(rows, columns=['day', 'count'])
            labels = posts_by_day_df['day'].tolist() if not posts_by_day_df.empty else []
            data = posts_by_day_df['count'].tolist() if not posts_by_day_df.empty else []

            # Likes per post stats via numpy
            likes_per_post = list(
                Like.objects.values('post_id').annotate(cnt=Count('id')).values_list('cnt', flat=True)
            )
            avg_likes = float(np.mean(likes_per_post)) if likes_per_post else 0.0
            std_likes = float(np.std(likes_per_post)) if likes_per_post else 0.0
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error',
                'message': 'Error processing analytics data'
            }, status=500)
    else:
        # Fallback for posts by day using Django ORM
        from django.db.models.functions import TruncDate
        posts_by_day_qs = Post.objects.annotate(
            day=TruncDate('created_at')
        ).values('day').annotate(
            count=Count('id')
        ).order_by('day')
        
        labels = [item['day'].strftime('%Y-%m-%d') for item in posts_by_day_qs]
        data = [item['count'] for item in posts_by_day_qs]
        
        # Basic stats without numpy
        likes_per_post = list(
            Like.objects.values('post_id').annotate(cnt=Count('id')).values_list('cnt', flat=True)
        )
        avg_likes = sum(likes_per_post) / len(likes_per_post) if likes_per_post else 0.0
        # Standard deviation without numpy (simplified)
        if likes_per_post and len(likes_per_post) > 1:
            variance = sum((x - avg_likes) ** 2 for x in likes_per_post) / (len(likes_per_post) - 1)
            std_likes = variance ** 0.5
        else:
            std_likes = 0.0

    return JsonResponse({
        'posts_by_day': {
            'labels': labels,
            'data': data,
        },
        'likes_stats': {
            'avg': avg_likes,
            'std': std_likes,
        },
        'summary': {
            'total_posts': total_posts,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_users': total_users,
        },
        'analytics_deps_available': ANALYTICS_DEPS_AVAILABLE,
    })
