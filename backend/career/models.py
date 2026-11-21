from django.db import models
from django.db.models import Q
from django.conf import settings
from django.utils import timezone


# =========================================================
# OPPORTUNITY SOURCES
# =========================================================

class OpportunitySource(models.Model):

    RSS = 'RSS'
    API = 'API'
    WEBSITE = 'WEBSITE'
    MANUAL = 'MANUAL'

    SOURCE_TYPES = [
        (RSS, 'RSS Feed'),
        (API, 'API'),
        (WEBSITE, 'Website'),
        (MANUAL, 'Manual Source'),
    ]

    name = models.CharField(max_length=150, unique=True)
    website_url = models.URLField()
    feed_url = models.URLField(blank=True)

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_TYPES,
        default=WEBSITE
    )

    is_active = models.BooleanField(default=True)
    check_interval_hours = models.PositiveIntegerField(default=24)

    last_checked_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================================================
# CAREER OPPORTUNITIES
# =========================================================

class Opportunity(models.Model):

    JOB = 'JOB'
    INTERNSHIP = 'INTERNSHIP'
    SCHOLARSHIP = 'SCHOLARSHIP'
    GRANT = 'GRANT'
    COMPETITION = 'COMPETITION'
    FELLOWSHIP = 'FELLOWSHIP'
    VOLUNTEERING = 'VOLUNTEERING'
    SKILLS = 'SKILLS'
    EVENT = 'EVENT'
    OTHER = 'OTHER'

    CATEGORY_CHOICES = [
        (JOB, 'Jobs & Graduate Programmes'),
        (INTERNSHIP, 'Internships & Attachments'),
        (SCHOLARSHIP, 'Scholarships & Study Abroad'),
        (GRANT, 'Entrepreneurship & Grants'),
        (COMPETITION, 'Competitions'),
        (FELLOWSHIP, 'Fellowships'),
        (VOLUNTEERING, 'Volunteering & Leadership'),
        (SKILLS, 'Skills & Certifications'),
        (EVENT, 'Career Events'),
        (OTHER, 'Other Opportunities'),
    ]

    DRAFT = 'DRAFT'
    PENDING_REVIEW = 'PENDING_REVIEW'
    PUBLISHED = 'PUBLISHED'
    CLOSED = 'CLOSED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PENDING_REVIEW, 'Pending Review'),
        (PUBLISHED, 'Published'),
        (CLOSED, 'Closed'),
        (REJECTED, 'Rejected'),
    ]

    title = models.CharField(max_length=250)
    organisation = models.CharField(max_length=200)

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()
    eligibility = models.TextField(blank=True)
    requirements = models.TextField(blank=True)

    location = models.CharField(max_length=200, blank=True)
    work_mode = models.CharField(max_length=50, blank=True)

    application_url = models.URLField()
    source_url = models.URLField(blank=True)

    source = models.ForeignKey(
        OpportunitySource,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='opportunities'
    )

    application_deadline = models.DateTimeField(null=True, blank=True)
    date_posted = models.DateField(null=True, blank=True)

    is_featured = models.BooleanField(default=False)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING_REVIEW
    )

    discovered_at = models.DateTimeField(default=timezone.now)
    last_verified_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    external_id = models.CharField(max_length=255, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_opportunities'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['category', 'status']),
            models.Index(fields=['application_deadline']),
            models.Index(fields=['status', 'is_featured']),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=['source', 'external_id'],
                condition=Q(source__isnull=False) & ~Q(external_id=''),
                name='unique_source_external_opportunity'
            )
        ]

    def __str__(self):
        return f'{self.title} - {self.organisation}'

    @property
    def is_expired(self):
        return (
            self.application_deadline is not None
            and self.application_deadline < timezone.now()
        )


# =========================================================
# SAVED OPPORTUNITIES
# =========================================================

class SavedOpportunity(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_opportunities'
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_saved_opportunity'
            )
        ]

    def __str__(self):
        return f'{self.user} saved {self.opportunity}'


# =========================================================
# OPPORTUNITY APPLICATION TRACKING
# =========================================================

class OpportunityApplication(models.Model):

    INTERESTED = 'INTERESTED'
    APPLYING = 'APPLYING'
    APPLIED = 'APPLIED'
    INTERVIEW = 'INTERVIEW'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    WITHDRAWN = 'WITHDRAWN'

    APPLICATION_STATUS_CHOICES = [
        (INTERESTED, 'Interested'),
        (APPLYING, 'Preparing Application'),
        (APPLIED, 'Application Submitted'),
        (INTERVIEW, 'Interview'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (WITHDRAWN, 'Withdrawn'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='opportunity_applications'
    )

    opportunity = models.ForeignKey(
        Opportunity,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    status = models.CharField(
        max_length=20,
        choices=APPLICATION_STATUS_CHOICES,
        default=INTERESTED
    )

    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'opportunity'],
                name='unique_opportunity_application'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.opportunity}'


# =========================================================
# ACADEMIC PROGRAMMES
# =========================================================

class AcademicProgramme(models.Model):

    DIPLOMA = 'DIPLOMA'
    UNDERGRADUATE = 'UNDERGRADUATE'

    PROGRAMME_TYPE_CHOICES = [
        (DIPLOMA, 'Diploma'),
        (UNDERGRADUATE, 'Undergraduate'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True)

    programme_type = models.CharField(
        max_length=20,
        choices=PROGRAMME_TYPE_CHOICES
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# =========================================================
# CAREER DISCOVERY
# =========================================================

class Career(models.Model):

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)

    career_area = models.CharField(max_length=150)

    short_description = models.CharField(max_length=300)
    description = models.TextField()

    education_requirements = models.TextField(blank=True)
    career_progression = models.TextField(blank=True)

    industries = models.TextField(blank=True)
    recommended_skills = models.TextField(blank=True)

    # GHANA SALARY INSIGHTS

    entry_salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    entry_salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    mid_salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    mid_salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    senior_salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    senior_salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_currency = models.CharField(
        max_length=10,
        default='GHS'
    )

    MONTHLY = 'MONTHLY'
    ANNUAL = 'ANNUAL'

    SALARY_PERIOD_CHOICES = [
        (MONTHLY, 'Monthly'),
        (ANNUAL, 'Annual'),
    ]

    salary_period = models.CharField(
        max_length=10,
        choices=SALARY_PERIOD_CHOICES,
        default=MONTHLY
    )

    GROSS = 'GROSS'
    NET = 'NET'
    NOT_SPECIFIED = 'NOT_SPECIFIED'

    SALARY_BASIS_CHOICES = [
        (GROSS, 'Gross Salary'),
        (NET, 'Net Salary'),
        (NOT_SPECIFIED, 'Not Specified'),
    ]

    salary_basis = models.CharField(
        max_length=20,
        choices=SALARY_BASIS_CHOICES,
        default=NOT_SPECIFIED
    )

    salary_source = models.CharField(
        max_length=200,
        blank=True
    )

    salary_source_url = models.URLField(
        blank=True
    )

    salary_last_verified = models.DateField(
        null=True,
        blank=True
    )

    salary_notes = models.TextField(
        blank=True
    )

    academic_programmes = models.ManyToManyField(
        AcademicProgramme,
        through='CareerAcademicProgramme',
        related_name='careers',
        blank=True
    )

    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Careers'

    def __str__(self):
        return self.title


# =========================================================
# CAREER AND ACADEMIC PROGRAMME MAPPING
# =========================================================

class CareerAcademicProgramme(models.Model):

    DIRECT = 'DIRECT'
    RELATED = 'RELATED'
    TRANSFERABLE = 'TRANSFERABLE'

    RELEVANCE_CHOICES = [
        (DIRECT, 'Directly Related'),
        (RELATED, 'Related Career'),
        (TRANSFERABLE, 'Transferable Career'),
    ]

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='programme_connections'
    )

    academic_programme = models.ForeignKey(
        AcademicProgramme,
        on_delete=models.CASCADE,
        related_name='career_connections'
    )

    relevance = models.CharField(
        max_length=20,
        choices=RELEVANCE_CHOICES,
        default=DIRECT
    )

    relevance_note = models.TextField(blank=True)

    class Meta:
        ordering = ['academic_programme__name', 'career__title']

        constraints = [
            models.UniqueConstraint(
                fields=['career', 'academic_programme'],
                name='unique_career_academic_programme'
            )
        ]

    def __str__(self):
        return f'{self.career} - {self.academic_programme}'


# =========================================================
# CAREER SKILLS
# =========================================================

class CareerSkill(models.Model):

    TECHNICAL = 'TECHNICAL'
    PROFESSIONAL = 'PROFESSIONAL'
    COMMUNICATION = 'COMMUNICATION'
    LEADERSHIP = 'LEADERSHIP'

    SKILL_TYPES = [
        (TECHNICAL, 'Technical Skill'),
        (PROFESSIONAL, 'Professional Skill'),
        (COMMUNICATION, 'Communication Skill'),
        (LEADERSHIP, 'Leadership Skill'),
    ]

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='skills'
    )

    name = models.CharField(max_length=150)

    skill_type = models.CharField(
        max_length=20,
        choices=SKILL_TYPES,
        default=TECHNICAL
    )

    importance = models.PositiveSmallIntegerField(default=3)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-importance', 'name']

    def __str__(self):
        return f'{self.name} - {self.career.title}'


# =========================================================
# CAREER QUEST QUESTIONS
# =========================================================

class CareerQuestion(models.Model):

    DISCOVER_ME = 'DISCOVER_ME'
    SUPERPOWERS = 'SUPERPOWERS'
    WORK_STYLE = 'WORK_STYLE'
    AMBITIONS = 'AMBITIONS'
    CHALLENGE = 'CHALLENGE'

    STAGE_CHOICES = [
        (DISCOVER_ME, 'Discover Me'),
        (SUPERPOWERS, 'My Superpowers'),
        (WORK_STYLE, 'My Work Style'),
        (AMBITIONS, 'My Ambitions'),
        (CHALLENGE, 'Career Challenges'),
    ]

    SINGLE = 'SINGLE'
    MULTIPLE = 'MULTIPLE'

    QUESTION_TYPES = [
        (SINGLE, 'Single Choice'),
        (MULTIPLE, 'Multiple Choice'),
    ]

    stage = models.CharField(
        max_length=20,
        choices=STAGE_CHOICES
    )

    question_text = models.TextField()
    scenario = models.TextField(blank=True)

    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default=SINGLE
    )

    explanation = models.TextField(blank=True)
    xp_reward = models.PositiveIntegerField(default=10)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['stage', 'order']

    def __str__(self):
        return self.question_text[:100]


class CareerAnswerOption(models.Model):

    question = models.ForeignKey(
        CareerQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )

    option_text = models.CharField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.option_text


class CareerAnswerWeight(models.Model):

    answer_option = models.ForeignKey(
        CareerAnswerOption,
        on_delete=models.CASCADE,
        related_name='career_weights'
    )

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='answer_weights'
    )

    weight = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['answer_option', 'career'],
                name='unique_answer_career_weight'
            )
        ]

    def __str__(self):
        return f'{self.answer_option} → {self.career}'


# =========================================================
# CAREER ASSESSMENTS
# =========================================================

class CareerAssessment(models.Model):

    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    STATUS_CHOICES = [
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='career_assessments'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=IN_PROGRESS
    )

    total_xp = models.PositiveIntegerField(default=0)

    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-started_at']

    def __str__(self):
        return f'Career Quest - {self.user}'


class CareerResponse(models.Model):

    assessment = models.ForeignKey(
        CareerAssessment,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    question = models.ForeignKey(
        CareerQuestion,
        on_delete=models.CASCADE,
        related_name='responses'
    )

    selected_options = models.ManyToManyField(
        CareerAnswerOption,
        related_name='responses'
    )

    answered_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['assessment', 'question'],
                name='unique_assessment_question'
            )
        ]

    def __str__(self):
        return f'{self.assessment} - {self.question}'


class CareerRecommendation(models.Model):

    assessment = models.ForeignKey(
        CareerAssessment,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='recommendations'
    )

    score = models.PositiveIntegerField(default=0)
    explanation = models.TextField(blank=True)
    rank = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']

        constraints = [
            models.UniqueConstraint(
                fields=['assessment', 'career'],
                name='unique_assessment_career'
            )
        ]

    def __str__(self):
        return f'{self.career} - {self.score}'


# =========================================================
# TRAINING PROVIDERS
# =========================================================

class TrainingProvider(models.Model):

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True)
    website_url = models.URLField()
    description = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================================================
# LEARNING PROGRAMMES
# =========================================================

class LearningProgramme(models.Model):

    COURSE = 'COURSE'
    CERTIFICATION = 'CERTIFICATION'
    BOOTCAMP = 'BOOTCAMP'
    WORKSHOP = 'WORKSHOP'
    PROFESSIONAL_TRAINING = 'PROFESSIONAL_TRAINING'
    UNIVERSITY_PROGRAMME = 'UNIVERSITY_PROGRAMME'
    GRADUATE_PROGRAMME = 'GRADUATE_PROGRAMME'

    PROGRAMME_TYPES = [
        (COURSE, 'Short Course'),
        (CERTIFICATION, 'Professional Certification'),
        (BOOTCAMP, 'Bootcamp'),
        (WORKSHOP, 'Workshop'),
        (PROFESSIONAL_TRAINING, 'Professional Training'),
        (UNIVERSITY_PROGRAMME, 'University Programme'),
        (GRADUATE_PROGRAMME, 'Graduate Programme'),
    ]

    FREE = 'FREE'
    PAID = 'PAID'
    FUNDED = 'FUNDED'
    SCHOLARSHIP = 'SCHOLARSHIP'

    COST_TYPES = [
        (FREE, 'Free'),
        (PAID, 'Paid'),
        (FUNDED, 'Fully Funded'),
        (SCHOLARSHIP, 'Scholarship Available'),
    ]

    ONLINE = 'ONLINE'
    PHYSICAL = 'PHYSICAL'
    HYBRID = 'HYBRID'

    DELIVERY_MODES = [
        (ONLINE, 'Online'),
        (PHYSICAL, 'Physical'),
        (HYBRID, 'Hybrid'),
    ]

    DRAFT = 'DRAFT'
    PENDING_REVIEW = 'PENDING_REVIEW'
    PUBLISHED = 'PUBLISHED'
    CLOSED = 'CLOSED'

    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PENDING_REVIEW, 'Pending Review'),
        (PUBLISHED, 'Published'),
        (CLOSED, 'Closed'),
    ]

    title = models.CharField(max_length=250)

    provider = models.ForeignKey(
        TrainingProvider,
        on_delete=models.PROTECT,
        related_name='programmes'
    )

    programme_type = models.CharField(
        max_length=30,
        choices=PROGRAMME_TYPES
    )

    description = models.TextField()
    skills_taught = models.TextField(blank=True)
    eligibility = models.TextField(blank=True)
    duration = models.CharField(max_length=150, blank=True)

    cost_type = models.CharField(
        max_length=20,
        choices=COST_TYPES,
        default=FREE
    )

    cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(max_length=10, default='USD')

    delivery_mode = models.CharField(
        max_length=15,
        choices=DELIVERY_MODES,
        default=ONLINE
    )

    certificate_available = models.BooleanField(default=False)
    registration_url = models.URLField()
    source_url = models.URLField(blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING_REVIEW
    )

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class CareerProgramme(models.Model):

    career = models.ForeignKey(
        Career,
        on_delete=models.CASCADE,
        related_name='learning_programmes'
    )

    programme = models.ForeignKey(
        LearningProgramme,
        on_delete=models.CASCADE,
        related_name='career_connections'
    )

    relevance_note = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['career', 'programme'],
                name='unique_career_programme'
            )
        ]

    def __str__(self):
        return f'{self.programme} → {self.career}'


# =========================================================
# STUDENT PROGRAMME TRACKING
# =========================================================

class SavedLearningProgramme(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_learning_programmes'
    )

    programme = models.ForeignKey(
        LearningProgramme,
        on_delete=models.CASCADE,
        related_name='saved_by'
    )

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'programme'],
                name='unique_saved_learning_programme'
            )
        ]

    def __str__(self):
        return f'{self.user} saved {self.programme}'


class LearningProgrammeProgress(models.Model):

    INTERESTED = 'INTERESTED'
    ENROLLED = 'ENROLLED'
    COMPLETED = 'COMPLETED'
    DROPPED = 'DROPPED'

    PROGRESS_CHOICES = [
        (INTERESTED, 'Interested'),
        (ENROLLED, 'Enrolled'),
        (COMPLETED, 'Completed'),
        (DROPPED, 'Dropped'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='learning_programme_progress'
    )

    programme = models.ForeignKey(
        LearningProgramme,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )

    status = models.CharField(
        max_length=20,
        choices=PROGRESS_CHOICES,
        default=INTERESTED
    )

    started_at = models.DateField(null=True, blank=True)
    completed_at = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'programme'],
                name='unique_learning_programme_progress'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.programme}'