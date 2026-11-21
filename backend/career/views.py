from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import (
    Opportunity,
    Career,
    CareerQuestion,
    CareerAssessment,
    CareerResponse,
    CareerRecommendation,
    CareerAnswerOption,
)


# =========================================================
# OPPORTUNITIES HUB
# =========================================================

@login_required
def career_dashboard(request):

    opportunities = Opportunity.objects.filter(
        status=Opportunity.PUBLISHED
    ).filter(
        Q(application_deadline__isnull=True) |
        Q(application_deadline__gte=timezone.now())
    )

    featured_opportunities = opportunities.filter(
        is_featured=True
    )[:6]

    latest_opportunities = opportunities[:10]

    category_counts = []

    for category_value, category_label in Opportunity.CATEGORY_CHOICES:
        count = opportunities.filter(
            category=category_value
        ).count()

        category_counts.append({
            'value': category_value,
            'label': category_label,
            'count': count,
        })

    context = {
        'total_opportunities': opportunities.count(),
        'featured_opportunities': featured_opportunities,
        'latest_opportunities': latest_opportunities,
        'category_counts': category_counts,
    }

    return render(request, 'career/dashboard.html', context)


@login_required
def opportunity_list(request):

    opportunities = Opportunity.objects.filter(
        status=Opportunity.PUBLISHED
    ).filter(
        Q(application_deadline__isnull=True) |
        Q(application_deadline__gte=timezone.now())
    )

    search_query = request.GET.get('q', '').strip()
    selected_category = request.GET.get('category', '').strip()

    if search_query:
        opportunities = opportunities.filter(
            Q(title__icontains=search_query) |
            Q(organisation__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )

    valid_categories = [
        value for value, label in Opportunity.CATEGORY_CHOICES
    ]

    if selected_category in valid_categories:
        opportunities = opportunities.filter(
            category=selected_category
        )
    else:
        selected_category = ''

    context = {
        'opportunities': opportunities,
        'search_query': search_query,
        'selected_category': selected_category,
        'categories': Opportunity.CATEGORY_CHOICES,
    }

    return render(request, 'career/opportunity_list.html', context)


@login_required
def opportunity_detail(request, opportunity_id):

    opportunity = get_object_or_404(
        Opportunity,
        id=opportunity_id,
        status=Opportunity.PUBLISHED
    )

    if opportunity.is_expired:
        opportunity.status = Opportunity.CLOSED
        opportunity.save(update_fields=['status'])

    return render(
        request,
        'career/opportunity_detail.html',
        {'opportunity': opportunity}
    )


# =========================================================
# CAREER QUEST DASHBOARD
# =========================================================

@login_required
def career_quest(request):

    active_questions = CareerQuestion.objects.filter(
        is_active=True
    )

    latest_assessment = CareerAssessment.objects.filter(
        user=request.user
    ).order_by('-started_at').first()

    latest_completed_assessment = CareerAssessment.objects.filter(
        user=request.user,
        status=CareerAssessment.COMPLETED
    ).order_by('-completed_at').first()

    completed_assessments = CareerAssessment.objects.filter(
        user=request.user,
        status=CareerAssessment.COMPLETED
    ).count()

    context = {
        'total_questions': active_questions.count(),
        'stage_choices': CareerQuestion.STAGE_CHOICES,
        'latest_assessment': latest_assessment,
        'latest_completed_assessment': latest_completed_assessment,
        'completed_assessments': completed_assessments,
    }

    return render(request, 'career/quest.html', context)


# =========================================================
# START OR RESUME CAREER QUEST
# =========================================================

@login_required
def start_career_quest(request):

    if request.method != 'POST':
        return redirect('career:quest')

    if not CareerQuestion.objects.filter(is_active=True).exists():
        return redirect('career:quest')

    assessment = CareerAssessment.objects.filter(
        user=request.user,
        status=CareerAssessment.IN_PROGRESS
    ).order_by('-started_at').first()

    if assessment is None:
        assessment = CareerAssessment.objects.create(
            user=request.user
        )

    return redirect(
        'career:career_question',
        assessment_id=assessment.id
    )


# =========================================================
# DELETE PREVIOUS CAREER QUEST RESULT
# =========================================================

@login_required
@require_POST
def delete_career_result(request, assessment_id):

    assessment = get_object_or_404(
        CareerAssessment,
        id=assessment_id,
        user=request.user,
        status=CareerAssessment.COMPLETED
    )

    assessment.delete()

    return redirect('career:quest')


# =========================================================
# CAREER QUEST QUESTION ENGINE
# =========================================================

@login_required
def career_question(request, assessment_id):

    assessment = get_object_or_404(
        CareerAssessment,
        id=assessment_id,
        user=request.user,
        status=CareerAssessment.IN_PROGRESS
    )

    questions = list(
        CareerQuestion.objects.filter(
            is_active=True
        ).prefetch_related('options').order_by('order', 'id')
    )

    if not questions:
        return redirect('career:quest')

    total_questions = len(questions)

    question_id = request.GET.get('q')

    if question_id:
        question = next(
            (q for q in questions if str(q.id) == question_id),
            None
        )

        if question is None:
            return redirect(
                'career:career_question',
                assessment_id=assessment.id
            )
    else:
        answered_ids = set(
            assessment.responses.values_list(
                'question_id',
                flat=True
            )
        )

        question = next(
            (q for q in questions if q.id not in answered_ids),
            questions[0]
        )

    current_index = questions.index(question)

    response = CareerResponse.objects.filter(
        assessment=assessment,
        question=question
    ).first()

    selected_option_ids = (
        list(response.selected_options.values_list('id', flat=True))
        if response else []
    )

    error_message = None

    if request.method == 'POST':

        action = request.POST.get('action', 'next')
        selected_ids = list(set(request.POST.getlist('options')))

        if selected_ids:

            if (
                question.question_type == CareerQuestion.SINGLE
                and len(selected_ids) != 1
            ):
                error_message = 'Please select only one answer.'

            else:

                valid_options = CareerAnswerOption.objects.filter(
                    question=question,
                    id__in=selected_ids
                )

                if valid_options.count() != len(selected_ids):

                    error_message = 'Invalid answer selection.'

                else:

                    with transaction.atomic():

                        response, created = CareerResponse.objects.get_or_create(
                            assessment=assessment,
                            question=question
                        )

                        response.selected_options.set(valid_options)

                        if created:

                            assessment.total_xp += question.xp_reward

                            assessment.save(
                                update_fields=['total_xp']
                            )

                    selected_option_ids = [
                        option.id for option in valid_options
                    ]

        if action == 'back' and not error_message:

            if current_index > 0:

                previous_question = questions[current_index - 1]

                return redirect(
                    f'/career/quest/{assessment.id}/question/?q={previous_question.id}'
                )

        elif action == 'next' and not error_message:

            if not selected_option_ids:

                error_message = 'Please select an answer before continuing.'

            elif current_index < total_questions - 1:

                next_question = questions[current_index + 1]

                return redirect(
                    f'/career/quest/{assessment.id}/question/?q={next_question.id}'
                )

            else:

                calculate_career_recommendations(assessment)

                return redirect(
                    'career:career_results',
                    assessment_id=assessment.id
                )

    answered_count = assessment.responses.count()

    progress_percentage = round(
        (answered_count / total_questions) * 100
    ) if total_questions else 0

    context = {
        'assessment': assessment,
        'question': question,
        'options': question.options.all(),
        'total_questions': total_questions,
        'answered_count': answered_count,
        'progress_percentage': progress_percentage,
        'error_message': error_message,
        'selected_option_ids': selected_option_ids,
        'current_number': current_index + 1,
        'is_first_question': current_index == 0,
        'is_last_question': current_index == total_questions - 1,
    }

    return render(
        request,
        'career/career_question.html',
        context
    )


# =========================================================
# CAREER RECOMMENDATION SCORING ENGINE
# =========================================================

def calculate_career_recommendations(assessment):

    responses = assessment.responses.prefetch_related(
        'selected_options'
    ).all()

    career_scores = {}

    for response in responses:

        selected_options = response.selected_options.all()

        for option in selected_options:

            weights = option.career_weights.select_related(
                'career'
            ).filter(
                career__is_active=True
            )

            for answer_weight in weights:

                career_id = answer_weight.career_id

                if career_id not in career_scores:
                    career_scores[career_id] = 0

                career_scores[career_id] += answer_weight.weight

    assessment.recommendations.all().delete()

    ranked_careers = sorted(
        career_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    rank = 1

    for career_id, score in ranked_careers[:5]:

        if score <= 0:
            continue

        career = Career.objects.get(
            id=career_id,
            is_active=True
        )

        matching_answers = CareerAnswerOption.objects.filter(
            responses__assessment=assessment,
            career_weights__career=career
        ).distinct()

        answer_highlights = list(
            matching_answers.values_list(
                'option_text',
                flat=True
            )[:3]
        )

        if answer_highlights:

            explanation = (
                'Your responses showed alignment with: '
                + '; '.join(answer_highlights)
                + '.'
            )

        else:

            explanation = (
                'This career received a positive score from your responses.'
            )

        CareerRecommendation.objects.create(
            assessment=assessment,
            career=career,
            score=score,
            explanation=explanation,
            rank=rank
        )

        rank += 1

    assessment.status = CareerAssessment.COMPLETED
    assessment.completed_at = timezone.now()

    assessment.save(
        update_fields=[
            'status',
            'completed_at',
        ]
    )


# =========================================================
# CAREER QUEST RESULTS
# =========================================================

@login_required
def career_results(request, assessment_id):

    assessment = get_object_or_404(
        CareerAssessment,
        id=assessment_id,
        user=request.user,
        status=CareerAssessment.COMPLETED
    )

    recommendations = assessment.recommendations.select_related(
        'career'
    ).prefetch_related(
        'career__skills'
    ).all()

    context = {
        'assessment': assessment,
        'recommendations': recommendations,
    }

    return render(
        request,
        'career/career_results.html',
        context
    )


# =========================================================
# CAREER DETAIL / EXPLORE CAREER
# =========================================================

@login_required
def career_detail(request, slug):

    career = get_object_or_404(
        Career.objects.prefetch_related(
            'skills',
            'academic_programmes'
        ),
        slug=slug,
        is_active=True
    )

    context = {
        'career': career,
        'skills': career.skills.all(),
        'academic_programmes': career.academic_programmes.filter(
            is_active=True
        ),
    }

    return render(
        request,
        'career/career_detail.html',
        context
    )