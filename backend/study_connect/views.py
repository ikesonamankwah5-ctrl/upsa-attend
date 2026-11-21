from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import (
    StudyGroup,
    StudyGroupMembership,
    StudySession,
    GroupMessage,
)

from .forms import (
    StudyGroupForm,
    StudySessionForm,
    GroupMessageForm,
)


@login_required
def study_group_list(request):
    search_query = request.GET.get('q', '').strip()

    groups = StudyGroup.objects.filter(
        is_active=True,
        visibility='PUBLIC'
    ).select_related('created_by').order_by('-created_at')

    if search_query:
        groups = groups.filter(
            Q(title__icontains=search_query)
            | Q(course__icontains=search_query)
            | Q(programme__icontains=search_query)
            | Q(academic_level__icontains=search_query)
        )

    my_memberships = StudyGroupMembership.objects.filter(
        student=request.user,
        status='ACTIVE'
    ).select_related('group')

    my_groups = StudyGroup.objects.filter(
        memberships__student=request.user,
        memberships__status='ACTIVE',
        is_active=True
    ).distinct()

    pending_requests = StudyGroupMembership.objects.filter(
        student=request.user,
        status='PENDING'
    ).select_related('group')

    return render(
        request,
        'study_connect/group_list.html',
        {
            'groups': groups,
            'my_groups': my_groups,
            'my_memberships': my_memberships,
            'pending_requests': pending_requests,
            'search_query': search_query,
        }
    )


@login_required
def create_study_group(request):
    if request.method == 'POST':
        form = StudyGroupForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                group = form.save(commit=False)
                group.created_by = request.user
                group.save()

                StudyGroupMembership.objects.create(
                    group=group,
                    student=request.user,
                    role='ADMIN',
                    status='ACTIVE'
                )

            messages.success(
                request,
                'Your study group has been created successfully!'
            )

            return redirect(
                'study_group_detail',
                group_id=group.id
            )
    else:
        form = StudyGroupForm()

    return render(
        request,
        'study_connect/create_group.html',
        {'form': form}
    )


@login_required
def study_group_detail(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id,
        is_active=True
    )

    membership = StudyGroupMembership.objects.filter(
        group=group,
        student=request.user
    ).first()

    is_member = (
        membership is not None
        and membership.status == 'ACTIVE'
    )

    is_pending = (
        membership is not None
        and membership.status == 'PENDING'
    )

    is_creator = group.created_by_id == request.user.id

    if group.visibility == 'PRIVATE':
        if not is_member and not is_pending and not is_creator:
            messages.warning(
                request,
                'This is a private group. You must request to join first.'
            )
            return redirect('study_group_list')

    members = StudyGroupMembership.objects.filter(
        group=group,
        status='ACTIVE'
    ).select_related('student')

    sessions = StudySession.objects.none()
    pending_memberships = StudyGroupMembership.objects.none()
    group_messages = GroupMessage.objects.none()

    if is_member:
        sessions = group.study_sessions.order_by('scheduled_at')

        group_messages = group.messages.select_related(
            'sender'
        ).order_by('-created_at')[:100]

    if is_member and membership.role == 'ADMIN':
        pending_memberships = StudyGroupMembership.objects.filter(
            group=group,
            status='PENDING'
        ).select_related('student')

    context = {
        'group': group,
        'membership': membership,
        'is_member': is_member,
        'is_pending': is_pending,
        'members': members,
        'sessions': sessions,
        'pending_memberships': pending_memberships,
        'group_messages': reversed(group_messages),
        'is_creator': is_creator,
        'message_form': GroupMessageForm(),
    }

    return render(
        request,
        'study_connect/group_detail.html',
        context
    )


@login_required
@require_POST
def join_study_group(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id,
        is_active=True
    )

    membership, created = StudyGroupMembership.objects.get_or_create(
        group=group,
        student=request.user,
        defaults={
            'role': 'MEMBER',
            'status': (
                'ACTIVE'
                if group.visibility == 'PUBLIC'
                else 'PENDING'
            )
        }
    )

    if not created:
        if membership.status == 'ACTIVE':
            messages.info(
                request,
                'You are already a member of this group.'
            )
        else:
            messages.info(
                request,
                'Your membership request is already pending.'
            )

    elif group.visibility == 'PUBLIC':
        messages.success(
            request,
            'You have successfully joined the study group!'
        )
    else:
        messages.success(
            request,
            'Your request to join this private group has been submitted.'
        )

    return redirect(
        'study_group_detail',
        group_id=group.id
    )


@login_required
@require_POST
def approve_membership(request, membership_id):
    membership = get_object_or_404(
        StudyGroupMembership,
        id=membership_id,
        status='PENDING'
    )

    is_admin = StudyGroupMembership.objects.filter(
        group=membership.group,
        student=request.user,
        role='ADMIN',
        status='ACTIVE'
    ).exists()

    if not is_admin:
        messages.error(
            request,
            'Only the group administrator can approve membership requests.'
        )
        return redirect('study_group_list')

    membership.status = 'ACTIVE'
    membership.save(update_fields=['status'])

    messages.success(
        request,
        f'{membership.student} has been approved to join the group.'
    )

    return redirect(
        'study_group_detail',
        group_id=membership.group_id
    )


@login_required
@require_POST
def reject_membership(request, membership_id):
    membership = get_object_or_404(
        StudyGroupMembership,
        id=membership_id,
        status='PENDING'
    )

    is_admin = StudyGroupMembership.objects.filter(
        group=membership.group,
        student=request.user,
        role='ADMIN',
        status='ACTIVE'
    ).exists()

    if not is_admin:
        messages.error(
            request,
            'Only the group administrator can reject membership requests.'
        )
        return redirect('study_group_list')

    group_id = membership.group_id
    membership.delete()

    messages.success(
        request,
        'The membership request has been rejected.'
    )

    return redirect(
        'study_group_detail',
        group_id=group_id
    )


@login_required
@require_POST
def leave_study_group(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id
    )

    membership = get_object_or_404(
        StudyGroupMembership,
        group=group,
        student=request.user,
        status='ACTIVE'
    )

    if membership.role == 'ADMIN':
        messages.error(
            request,
            'The group administrator cannot leave the group. '
            'Transfer administration or deactivate the group first.'
        )
    else:
        membership.delete()

        messages.success(
            request,
            'You have left the study group.'
        )

    return redirect('study_group_list')


@login_required
def create_study_session(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id,
        is_active=True
    )

    membership = StudyGroupMembership.objects.filter(
        group=group,
        student=request.user,
        status='ACTIVE'
    ).first()

    if not membership or membership.role != 'ADMIN':
        messages.error(
            request,
            'Only the group administrator can organise study sessions.'
        )
        return redirect(
            'study_group_detail',
            group_id=group.id
        )

    if request.method == 'POST':
        form = StudySessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)
            session.group = group
            session.created_by = request.user
            session.save()

            messages.success(
                request,
                'Your study session has been scheduled successfully!'
            )

            return redirect(
                'study_group_detail',
                group_id=group.id
            )
    else:
        form = StudySessionForm()

    return render(
        request,
        'study_connect/create_session.html',
        {
            'form': form,
            'group': group,
        }
    )


@login_required
@require_POST
def delete_study_group(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id
    )

    is_admin = StudyGroupMembership.objects.filter(
        group=group,
        student=request.user,
        role='ADMIN',
        status='ACTIVE'
    ).exists()

    if not is_admin or group.created_by_id != request.user.id:
        messages.error(
            request,
            'You are not authorised to delete this study group.'
        )
        return redirect('study_group_list')

    group_title = group.title
    group.delete()

    messages.success(
        request,
        f'"{group_title}" has been deleted successfully.'
    )

    return redirect('study_group_list')


@login_required
@require_POST
def send_group_message(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id,
        is_active=True
    )

    is_member = StudyGroupMembership.objects.filter(
        group=group,
        student=request.user,
        status='ACTIVE'
    ).exists()

    if not is_member:
        messages.error(
            request,
            'Only approved group members can send messages.'
        )
        return redirect('study_group_list')

    form = GroupMessageForm(request.POST)

    if form.is_valid():
        group_message = form.save(commit=False)
        group_message.group = group
        group_message.sender = request.user
        group_message.save()

        messages.success(
            request,
            'Message sent successfully!'
        )
    else:
        messages.error(
            request,
            'Please enter a valid message.'
        )

    return redirect(
        'study_group_detail',
        group_id=group.id
    )
@login_required
def get_group_messages(request, group_id):
    group = get_object_or_404(
        StudyGroup,
        id=group_id,
        is_active=True
    )

    is_member = StudyGroupMembership.objects.filter(
        group=group,
        student=request.user,
        status='ACTIVE'
    ).exists()

    if not is_member:
        return JsonResponse(
            {'error': 'You are not authorised to view these messages.'},
            status=403
        )

    messages_list = group.messages.select_related(
        'sender'
    ).order_by('-created_at')[:100]

    messages_list = reversed(messages_list)

    data = [
        {
            'sender': str(message.sender),
            'message': message.message,
            'created_at': message.created_at.strftime(
                '%d %b %Y - %H:%M'
            ),
        }
        for message in messages_list
    ]

    return JsonResponse({'messages': data})