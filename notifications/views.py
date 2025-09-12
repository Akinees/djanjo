from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Notification, NotificationPreference

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user)
    
    # Mark all as read if requested
    if request.GET.get('mark_all_read'):
        notifications.filter(read=False).update(read=True)
        return redirect('notifications:list')
    
    # Pagination
    paginator = Paginator(notifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Unread count
    unread_count = notifications.filter(read=False).count()
    
    context = {
        'page_obj': page_obj,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)

@login_required
def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    
    # Redirect to action URL if available, otherwise back to notifications
    if notification.action_url:
        return redirect(notification.action_url)
    return redirect('notifications:list')

@login_required
def unread_count(request):
    count = Notification.objects.filter(user=request.user, read=False).count()
    return JsonResponse({'count': count})

@login_required
def preferences(request):
    preference, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        preference.email_notifications = request.POST.get('email_notifications') == 'on'
        preference.push_notifications = request.POST.get('push_notifications') == 'on'
        preference.lesson_reminders = request.POST.get('lesson_reminders') == 'on'
        preference.achievement_alerts = request.POST.get('achievement_alerts') == 'on'
        preference.weekly_progress = request.POST.get('weekly_progress') == 'on'
        preference.save()
        
        return redirect('notifications:preferences')
    
    context = {
        'preference': preference,
    }
    return render(request, 'notifications/preferences.html', context)

def create_notification(user, title, message, notification_type, action_url=None):
    """Helper function to create notifications"""
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        action_url=action_url
    )