from django.contrib import admin
from django.utils import timezone

from .models import (
    OpportunitySource,
    Opportunity,
    SavedOpportunity,
    OpportunityApplication,
    AcademicProgramme,
    Career,
    CareerAcademicProgramme,
    CareerSkill,
    CareerQuestion,
    CareerAnswerOption,
    CareerAnswerWeight,
    CareerAssessment,
    CareerResponse,
    CareerRecommendation,
    TrainingProvider,
    LearningProgramme,
    CareerProgramme,
    SavedLearningProgramme,
    LearningProgrammeProgress,
)


# =====================================================
# OPPORTUNITIES HUB
# =====================================================

@admin.register(OpportunitySource)
class OpportunitySourceAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'source_type',
        'is_active',
        'check_interval_hours',
        'last_checked_at',
    )

    list_filter = ('source_type', 'is_active')

    search_fields = ('name', 'website_url', 'notes')

    readonly_fields = ('last_checked_at', 'created_at')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'organisation',
        'category',
        'status',
        'application_deadline',
        'is_featured',
    )

    list_filter = ('category', 'status', 'is_featured')

    search_fields = ('title', 'organisation', 'description')

    readonly_fields = (
        'discovered_at',
        'created_at',
        'updated_at',
    )

    list_editable = ('status', 'is_featured')

    date_hierarchy = 'created_at'

    actions = (
        'publish_opportunities',
        'reject_opportunities',
        'close_opportunities',
    )

    @admin.action(description='Publish selected opportunities')
    def publish_opportunities(self, request, queryset):
        updated = queryset.update(
            status=Opportunity.PUBLISHED,
            published_at=timezone.now(),
        )
        self.message_user(
            request,
            f'{updated} opportunities successfully published.'
        )

    @admin.action(description='Reject selected opportunities')
    def reject_opportunities(self, request, queryset):
        updated = queryset.update(status=Opportunity.REJECTED)
        self.message_user(
            request,
            f'{updated} opportunities rejected.'
        )

    @admin.action(description='Close selected opportunities')
    def close_opportunities(self, request, queryset):
        updated = queryset.update(status=Opportunity.CLOSED)
        self.message_user(
            request,
            f'{updated} opportunities closed.'
        )


@admin.register(SavedOpportunity)
class SavedOpportunityAdmin(admin.ModelAdmin):

    list_display = ('user', 'opportunity', 'saved_at')

    search_fields = (
        'user__username',
        'opportunity__title',
    )


@admin.register(OpportunityApplication)
class OpportunityApplicationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'opportunity',
        'status',
        'updated_at',
    )

    list_filter = ('status',)

    search_fields = (
        'user__username',
        'opportunity__title',
    )


# =====================================================
# ACADEMIC PROGRAMMES
# =====================================================

@admin.register(AcademicProgramme)
class AcademicProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'programme_type',
        'is_active',
        'created_at',
    )

    list_filter = (
        'programme_type',
        'is_active',
    )

    search_fields = (
        'name',
        'description',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    readonly_fields = ('created_at',)


class CareerAcademicProgrammeInline(admin.TabularInline):

    model = CareerAcademicProgramme

    extra = 1

    autocomplete_fields = ('career',)

    fields = (
        'career',
        'relevance',
        'relevance_note',
    )


@admin.register(CareerAcademicProgramme)
class CareerAcademicProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'academic_programme',
        'career',
        'relevance',
    )

    list_filter = (
        'academic_programme__programme_type',
        'relevance',
    )

    search_fields = (
        'academic_programme__name',
        'career__title',
        'relevance_note',
    )

    autocomplete_fields = (
        'academic_programme',
        'career',
    )


# =====================================================
# CAREER QUEST AND CAREER PATHWAYS
# =====================================================

class CareerSkillInline(admin.TabularInline):

    model = CareerSkill

    extra = 1


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'career_area',
        'is_featured',
        'is_active',
    )

    list_filter = (
        'career_area',
        'is_featured',
        'is_active',
    )

    search_fields = (
        'title',
        'short_description',
        'description',
    )

    prepopulated_fields = {
        'slug': ('title',),
    }

    inlines = (
        CareerSkillInline,
        CareerAcademicProgrammeInline,
    )


class CareerAnswerOptionInline(admin.TabularInline):

    model = CareerAnswerOption

    extra = 2


@admin.register(CareerQuestion)
class CareerQuestionAdmin(admin.ModelAdmin):

    list_display = (
        'question_text',
        'stage',
        'question_type',
        'order',
        'is_active',
        'xp_reward',
    )

    list_filter = (
        'stage',
        'question_type',
        'is_active',
    )

    search_fields = (
        'question_text',
        'scenario',
    )

    ordering = ('stage', 'order')

    inlines = (CareerAnswerOptionInline,)


@admin.register(CareerAnswerOption)
class CareerAnswerOptionAdmin(admin.ModelAdmin):

    list_display = (
        'option_text',
        'question',
        'order',
    )

    search_fields = (
        'option_text',
        'question__question_text',
    )


@admin.register(CareerAnswerWeight)
class CareerAnswerWeightAdmin(admin.ModelAdmin):

    list_display = (
        'answer_option',
        'career',
        'weight',
    )

    list_filter = ('career',)

    search_fields = (
        'answer_option__option_text',
        'career__title',
    )


# =====================================================
# CAREER ASSESSMENTS AND RECOMMENDATIONS
# =====================================================

@admin.register(CareerAssessment)
class CareerAssessmentAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'status',
        'total_xp',
        'started_at',
        'completed_at',
    )

    list_filter = ('status',)

    search_fields = (
        'user__username',
        'user__email',
    )

    readonly_fields = (
        'started_at',
        'completed_at',
    )


@admin.register(CareerResponse)
class CareerResponseAdmin(admin.ModelAdmin):

    list_display = (
        'assessment',
        'question',
        'answered_at',
    )

    search_fields = (
        'assessment__user__username',
        'question__question_text',
    )

    filter_horizontal = ('selected_options',)


@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):

    list_display = (
        'assessment',
        'career',
        'score',
        'rank',
    )

    list_filter = ('career',)

    search_fields = (
        'assessment__user__username',
        'career__title',
        'explanation',
    )


# =====================================================
# TRAINING PROVIDERS AND PROGRAMME FINDER
# =====================================================

class LearningProgrammeInline(admin.TabularInline):

    model = LearningProgramme

    extra = 0

    show_change_link = True


@admin.register(TrainingProvider)
class TrainingProviderAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'country',
        'is_verified',
        'is_active',
    )

    list_filter = (
        'country',
        'is_verified',
        'is_active',
    )

    search_fields = (
        'name',
        'description',
        'website_url',
    )

    prepopulated_fields = {
        'slug': ('name',),
    }

    inlines = (LearningProgrammeInline,)


@admin.register(LearningProgramme)
class LearningProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'provider',
        'programme_type',
        'cost_type',
        'delivery_mode',
        'status',
        'is_featured',
    )

    list_filter = (
        'programme_type',
        'cost_type',
        'delivery_mode',
        'status',
        'is_featured',
    )

    search_fields = (
        'title',
        'provider__name',
        'description',
        'skills_taught',
    )

    date_hierarchy = 'application_deadline'


@admin.register(CareerProgramme)
class CareerProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'career',
        'programme',
    )

    search_fields = (
        'career__title',
        'programme__title',
        'programme__provider__name',
    )


@admin.register(SavedLearningProgramme)
class SavedLearningProgrammeAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'programme',
    )

    search_fields = (
        'user__username',
        'programme__title',
    )


@admin.register(LearningProgrammeProgress)
class LearningProgrammeProgressAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'programme',
        'status',
        'started_at',
        'completed_at',
        'updated_at',
    )

    list_filter = ('status',)

    search_fields = (
        'user__username',
        'programme__title',
    )

    readonly_fields = ('updated_at',)