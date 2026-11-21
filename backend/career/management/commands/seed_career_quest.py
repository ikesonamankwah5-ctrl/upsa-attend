from django.core.management.base import BaseCommand

from career.models import (
    Career,
    CareerQuestion,
    CareerAnswerOption,
    CareerAnswerWeight,
)


class Command(BaseCommand):

    help = 'Seed Career Quest questions, options and career scoring weights.'

    QUESTIONS = [

        # =================================================
        # STAGE 1: DISCOVER ME
        # =================================================

        {
            'stage': 'DISCOVER_ME',
            'order': 1,
            'xp': 15,
            'type': 'SINGLE',
            'text': 'Which activity would genuinely excite you?',
            'scenario': 'Imagine you have a free day to explore something new.',
            'options': [
                {
                    'text': 'Analysing information and discovering hidden patterns.',
                    'careers': [
                        'Data Analyst', 'Business Intelligence Analyst',
                        'Data Scientist', 'Statistician',
                        'Financial Analyst', 'Research Analyst',
                    ],
                },
                {
                    'text': 'Building a business or developing a new idea.',
                    'careers': [
                        'Entrepreneur', 'Business Analyst',
                        'Management Consultant', 'Agribusiness Manager',
                    ],
                },
                {
                    'text': 'Working with people and communicating ideas.',
                    'careers': [
                        'Public Relations Officer',
                        'Corporate Communications Specialist',
                        'Human Resource Officer',
                        'Marketing Manager',
                    ],
                },
                {
                    'text': 'Solving technical problems using technology.',
                    'careers': [
                        'Cybersecurity Analyst',
                        'Database Administrator',
                        'IT Business Analyst',
                        'Data Scientist',
                    ],
                },
            ],
        },

        {
            'stage': 'DISCOVER_ME',
            'order': 2,
            'xp': 15,
            'type': 'SINGLE',
            'text': 'What kind of problems do you enjoy solving?',
            'scenario': 'You are given a difficult challenge. Which one would you choose?',
            'options': [
                {
                    'text': 'Financial problems, budgets and investment decisions.',
                    'careers': [
                        'Accountant', 'Financial Analyst',
                        'Investment Analyst', 'Credit Analyst',
                        'Actuarial Analyst', 'Tax Consultant',
                    ],
                },
                {
                    'text': 'Business inefficiencies and organisational challenges.',
                    'careers': [
                        'Business Analyst', 'Operations Manager',
                        'Management Consultant', 'Project Manager',
                        'Supply Chain Analyst',
                    ],
                },
                {
                    'text': 'Technology, computer systems and security problems.',
                    'careers': [
                        'Database Administrator',
                        'Cybersecurity Analyst',
                        'IT Business Analyst', 'Data Scientist',
                    ],
                },
                {
                    'text': 'Communication, customer and relationship problems.',
                    'careers': [
                        'Public Relations Officer',
                        'Marketing Manager',
                        'Human Resource Officer',
                        'Corporate Communications Specialist',
                    ],
                },
            ],
        },

        {
            'stage': 'DISCOVER_ME',
            'order': 3,
            'xp': 15,
            'type': 'SINGLE',
            'text': 'Which subject area naturally attracts your attention?',
            'scenario': '',
            'options': [
                {
                    'text': 'Numbers, mathematics and statistics.',
                    'careers': [
                        'Actuarial Analyst', 'Statistician',
                        'Data Scientist', 'Data Analyst',
                        'Financial Analyst',
                    ],
                },
                {
                    'text': 'Business, markets and entrepreneurship.',
                    'careers': [
                        'Entrepreneur', 'Business Analyst',
                        'Marketing Manager', 'Management Consultant',
                        'International Business Development Officer',
                    ],
                },
                {
                    'text': 'Technology, computers and digital innovation.',
                    'careers': [
                        'Cybersecurity Analyst',
                        'Database Administrator',
                        'IT Business Analyst',
                        'Data Scientist',
                    ],
                },
                {
                    'text': 'Law, communication and international affairs.',
                    'careers': [
                        'Legal Practitioner',
                        'Public Relations Officer',
                        'French Language Specialist',
                        'International Business Development Officer',
                    ],
                },
            ],
        },

        # =================================================
        # STAGE 2: MY SUPERPOWERS
        # =================================================

        {
            'stage': 'SUPERPOWERS',
            'order': 4,
            'xp': 20,
            'type': 'MULTIPLE',
            'text': 'Which of these describe your strongest abilities?',
            'scenario': 'Select all the abilities that genuinely describe you.',
            'options': [
                {
                    'text': 'I am good with numbers and calculations.',
                    'careers': [
                        'Accountant', 'Financial Analyst',
                        'Actuarial Analyst', 'Statistician',
                        'Investment Analyst',
                    ],
                },
                {
                    'text': 'I notice patterns and understand information quickly.',
                    'careers': [
                        'Data Analyst', 'Business Intelligence Analyst',
                        'Data Scientist', 'Research Analyst',
                    ],
                },
                {
                    'text': 'I can organise people, activities and resources.',
                    'careers': [
                        'Operations Manager', 'Project Manager',
                        'Logistics Manager', 'Human Resource Officer',
                    ],
                },
                {
                    'text': 'I am creative and good at generating ideas.',
                    'careers': [
                        'Entrepreneur', 'Marketing Manager',
                        'Digital Marketing Specialist',
                        'Public Relations Officer',
                    ],
                },
                {
                    'text': 'I am good at investigating and finding solutions.',
                    'careers': [
                        'Business Analyst', 'Management Consultant',
                        'External Auditor', 'Internal Auditor',
                        'Compliance Officer',
                    ],
                },
            ],
        },

        {
            'stage': 'SUPERPOWERS',
            'order': 5,
            'xp': 20,
            'type': 'MULTIPLE',
            'text': 'What do people usually come to you for?',
            'scenario': '',
            'options': [
                {
                    'text': 'Help with calculations, budgets or financial matters.',
                    'careers': [
                        'Accountant', 'Financial Analyst',
                        'Banking Officer', 'Credit Analyst',
                    ],
                },
                {
                    'text': 'Advice, planning and problem-solving.',
                    'careers': [
                        'Business Analyst', 'Management Consultant',
                        'Project Manager', 'Risk Analyst',
                    ],
                },
                {
                    'text': 'Technology and computer-related assistance.',
                    'careers': [
                        'Database Administrator',
                        'Cybersecurity Analyst',
                        'IT Business Analyst',
                    ],
                },
                {
                    'text': 'Communication, writing and explaining things.',
                    'careers': [
                        'Public Relations Officer',
                        'Corporate Communications Specialist',
                        'French Language Specialist',
                    ],
                },
                {
                    'text': 'Organising activities and bringing people together.',
                    'careers': [
                        'Human Resource Officer',
                        'Project Manager',
                        'Operations Manager',
                        'Entrepreneur',
                    ],
                },
            ],
        },

        {
            'stage': 'SUPERPOWERS',
            'order': 6,
            'xp': 20,
            'type': 'SINGLE',
            'text': 'Which statement sounds most like you?',
            'scenario': '',
            'options': [
                {
                    'text': 'I prefer accuracy, structure and attention to detail.',
                    'careers': [
                        'Accountant', 'External Auditor',
                        'Internal Auditor', 'Tax Consultant',
                        'Compliance Officer',
                    ],
                },
                {
                    'text': 'I enjoy discovering new ideas and possibilities.',
                    'careers': [
                        'Entrepreneur', 'Data Scientist',
                        'Management Consultant', 'Research Analyst',
                    ],
                },
                {
                    'text': 'I enjoy influencing, motivating and connecting people.',
                    'careers': [
                        'Marketing Manager', 'Human Resource Officer',
                        'Public Relations Officer',
                        'International Business Development Officer',
                    ],
                },
                {
                    'text': 'I enjoy logical thinking and technical challenges.',
                    'careers': [
                        'Data Analyst', 'Actuarial Analyst',
                        'Cybersecurity Analyst', 'Statistician',
                    ],
                },
            ],
        },

        # =================================================
        # STAGE 3: MY WORK STYLE
        # =================================================

        {
            'stage': 'WORK_STYLE',
            'order': 7,
            'xp': 20,
            'type': 'SINGLE',
            'text': 'What type of working environment would you prefer?',
            'scenario': 'Imagine your first full-time professional job.',
            'options': [
                {
                    'text': 'An office where I analyse reports and information.',
                    'careers': [
                        'Data Analyst', 'Business Intelligence Analyst',
                        'Financial Analyst', 'Accountant',
                        'Statistician', 'Research Analyst',
                    ],
                },
                {
                    'text': 'A technology environment solving digital problems.',
                    'careers': [
                        'Cybersecurity Analyst',
                        'Database Administrator',
                        'Data Scientist', 'IT Business Analyst',
                    ],
                },
                {
                    'text': 'A business environment involving people and decisions.',
                    'careers': [
                        'Business Analyst', 'Management Consultant',
                        'Human Resource Officer', 'Operations Manager',
                    ],
                },
                {
                    'text': 'A dynamic environment involving customers and markets.',
                    'careers': [
                        'Marketing Manager', 'Entrepreneur',
                        'Digital Marketing Specialist',
                        'Market Research Analyst',
                    ],
                },
            ],
        },

        {
            'stage': 'WORK_STYLE',
            'order': 8,
            'xp': 20,
            'type': 'SINGLE',
            'text': 'How would you prefer to complete an important assignment?',
            'scenario': '',
            'options': [
                {
                    'text': 'Independently, with time to concentrate deeply.',
                    'careers': [
                        'Data Analyst', 'Accountant',
                        'Actuarial Analyst', 'Statistician',
                        'Investment Analyst',
                    ],
                },
                {
                    'text': 'With a team where everyone contributes different ideas.',
                    'careers': [
                        'Project Manager', 'Management Consultant',
                        'Business Analyst', 'Operations Manager',
                    ],
                },
                {
                    'text': 'By interacting with clients and stakeholders.',
                    'careers': [
                        'Public Relations Officer',
                        'Marketing Manager', 'Banking Officer',
                        'International Business Development Officer',
                    ],
                },
                {
                    'text': 'By using technology and practical tools.',
                    'careers': [
                        'Database Administrator',
                        'Cybersecurity Analyst',
                        'Data Scientist', 'IT Business Analyst',
                    ],
                },
            ],
        },

        {
            'stage': 'WORK_STYLE',
            'order': 9,
            'xp': 20,
            'type': 'SINGLE',
            'text': 'Which responsibility would you enjoy most?',
            'scenario': '',
            'options': [
                {
                    'text': 'Monitoring performance and preparing reports.',
                    'careers': [
                        'Business Intelligence Analyst', 'Data Analyst',
                        'Financial Analyst', 'Accountant',
                    ],
                },
                {
                    'text': 'Leading people and managing operations.',
                    'careers': [
                        'Operations Manager', 'Project Manager',
                        'Human Resource Officer', 'Logistics Manager',
                    ],
                },
                {
                    'text': 'Developing strategies and identifying opportunities.',
                    'careers': [
                        'Management Consultant', 'Entrepreneur',
                        'Business Analyst', 'Investment Analyst',
                    ],
                },
                {
                    'text': 'Protecting systems, information and organisations.',
                    'careers': [
                        'Cybersecurity Analyst', 'Risk Analyst',
                        'Compliance Officer', 'Internal Auditor',
                    ],
                },
            ],
        },

        # =================================================
        # STAGE 4: MY AMBITIONS
        # =================================================

        {
            'stage': 'AMBITIONS',
            'order': 10,
            'xp': 25,
            'type': 'SINGLE',
            'text': 'What would you most like to achieve in your career?',
            'scenario': '',
            'options': [
                {
                    'text': 'Become a highly skilled technical expert.',
                    'careers': [
                        'Data Scientist', 'Actuarial Analyst',
                        'Cybersecurity Analyst',
                        'Database Administrator', 'Statistician',
                    ],
                },
                {
                    'text': 'Become a senior manager or executive.',
                    'careers': [
                        'Operations Manager', 'Financial Analyst',
                        'Marketing Manager', 'Project Manager',
                        'Management Consultant',
                    ],
                },
                {
                    'text': 'Build and own a successful business.',
                    'careers': [
                        'Entrepreneur', 'Agribusiness Manager',
                        'International Business Development Officer',
                    ],
                },
                {
                    'text': 'Become a respected professional in my field.',
                    'careers': [
                        'Legal Practitioner', 'External Auditor',
                        'Investment Analyst', 'Accountant',
                        'French Language Specialist',
                    ],
                },
            ],
        },

        {
            'stage': 'AMBITIONS',
            'order': 11,
            'xp': 25,
            'type': 'SINGLE',
            'text': 'Which achievement would make you feel most fulfilled?',
            'scenario': '',
            'options': [
                {
                    'text': 'Using information to influence important decisions.',
                    'careers': [
                        'Business Intelligence Analyst', 'Data Analyst',
                        'Financial Analyst', 'Economist',
                    ],
                },
                {
                    'text': 'Managing a successful team or organisation.',
                    'careers': [
                        'Operations Manager', 'Human Resource Officer',
                        'Project Manager', 'Logistics Manager',
                    ],
                },
                {
                    'text': 'Creating something valuable from an original idea.',
                    'careers': [
                        'Entrepreneur', 'Data Scientist',
                        'Digital Marketing Specialist',
                    ],
                },
                {
                    'text': 'Helping people and organisations make informed decisions.',
                    'careers': [
                        'Management Consultant', 'Legal Practitioner',
                        'Financial Analyst', 'Risk Analyst',
                        'Research Analyst',
                    ],
                },
            ],
        },

        {
            'stage': 'AMBITIONS',
            'order': 12,
            'xp': 25,
            'type': 'SINGLE',
            'text': 'Which industry would you be most excited to work in?',
            'scenario': '',
            'options': [
                {
                    'text': 'Banking, insurance and financial services.',
                    'careers': [
                        'Financial Analyst', 'Banking Officer',
                        'Insurance Analyst', 'Actuarial Analyst',
                        'Credit Analyst', 'Investment Analyst',
                    ],
                },
                {
                    'text': 'Technology, data and innovation.',
                    'careers': [
                        'Data Analyst', 'Data Scientist',
                        'Business Intelligence Analyst',
                        'Cybersecurity Analyst',
                    ],
                },
                {
                    'text': 'Business, consulting and entrepreneurship.',
                    'careers': [
                        'Business Analyst', 'Entrepreneur',
                        'Management Consultant', 'Project Manager',
                    ],
                },
                {
                    'text': 'Media, communication and international organisations.',
                    'careers': [
                        'Public Relations Officer',
                        'Corporate Communications Specialist',
                        'French Language Specialist',
                        'Digital Marketing Specialist',
                    ],
                },
                {
                    'text': 'Logistics, agriculture and real estate.',
                    'careers': [
                        'Supply Chain Analyst', 'Logistics Manager',
                        'Agribusiness Manager', 'Real Estate Analyst',
                        'Property Manager',
                    ],
                },
            ],
        },

        # =================================================
        # STAGE 5: CAREER CHALLENGES
        # =================================================

        {
            'stage': 'CHALLENGE',
            'order': 13,
            'xp': 30,
            'type': 'SINGLE',
            'text': 'Your organisation is losing money. What would you do first?',
            'scenario': 'You have been asked to help management understand the problem.',
            'options': [
                {
                    'text': 'Examine financial statements and identify unusual expenses.',
                    'careers': [
                        'Accountant', 'Financial Analyst',
                        'Internal Auditor', 'External Auditor',
                    ],
                },
                {
                    'text': 'Analyse business data to discover the cause.',
                    'careers': [
                        'Data Analyst', 'Business Intelligence Analyst',
                        'Business Analyst', 'Management Consultant',
                    ],
                },
                {
                    'text': 'Review operations and identify inefficiencies.',
                    'careers': [
                        'Operations Manager', 'Supply Chain Analyst',
                        'Logistics Manager', 'Project Manager',
                    ],
                },
                {
                    'text': 'Investigate financial risks and possible fraud.',
                    'careers': [
                        'Risk Analyst', 'Internal Auditor',
                        'Compliance Officer', 'Credit Analyst',
                    ],
                },
            ],
        },

        {
            'stage': 'CHALLENGE',
            'order': 14,
            'xp': 30,
            'type': 'SINGLE',
            'text': 'A company wants to grow its customer base. What would you recommend?',
            'scenario': '',
            'options': [
                {
                    'text': 'Conduct market research and understand customer behaviour.',
                    'careers': [
                        'Market Research Analyst', 'Marketing Manager',
                        'Data Analyst', 'Business Intelligence Analyst',
                    ],
                },
                {
                    'text': 'Develop creative advertising and digital campaigns.',
                    'careers': [
                        'Digital Marketing Specialist',
                        'Marketing Manager',
                        'Public Relations Officer',
                    ],
                },
                {
                    'text': 'Improve operations and customer service.',
                    'careers': [
                        'Operations Manager', 'Business Analyst',
                        'Project Manager',
                    ],
                },
                {
                    'text': 'Explore new markets and business partnerships.',
                    'careers': [
                        'Entrepreneur',
                        'International Business Development Officer',
                        'Management Consultant',
                    ],
                },
            ],
        },

        {
            'stage': 'CHALLENGE',
            'order': 15,
            'xp': 30,
            'type': 'SINGLE',
            'text': 'You are given a large dataset and asked to make a recommendation. What interests you most?',
            'scenario': '',
            'options': [
                {
                    'text': 'Clean the data, analyse it and build a dashboard.',
                    'careers': [
                        'Data Analyst', 'Business Intelligence Analyst',
                        'Data Scientist',
                    ],
                },
                {
                    'text': 'Use statistical methods to identify trends and patterns.',
                    'careers': [
                        'Statistician', 'Actuarial Analyst',
                        'Data Scientist', 'Research Analyst',
                    ],
                },
                {
                    'text': 'Use the information to make financial recommendations.',
                    'careers': [
                        'Financial Analyst', 'Investment Analyst',
                        'Credit Analyst', 'Economist',
                    ],
                },
                {
                    'text': 'Use the findings to improve business strategy.',
                    'careers': [
                        'Business Analyst', 'Management Consultant',
                        'Operations Manager', 'Entrepreneur',
                    ],
                },
            ],
        },

    ]

    def handle(self, *args, **options):

        created_questions = 0
        updated_questions = 0
        created_options = 0
        created_weights = 0

        careers = {
            career.title: career
            for career in Career.objects.filter(is_active=True)
        }

        for item in self.QUESTIONS:

            question, created = CareerQuestion.objects.update_or_create(
                stage=item['stage'],
                order=item['order'],
                defaults={
                    'question_text': item['text'],
                    'scenario': item['scenario'],
                    'question_type': item['type'],
                    'xp_reward': item['xp'],
                    'is_active': True,
                }
            )

            if created:
                created_questions += 1
            else:
                updated_questions += 1

            for option_index, option_data in enumerate(item['options'], start=1):

                option, option_created = CareerAnswerOption.objects.get_or_create(
                    question=question,
                    option_text=option_data['text'],
                    defaults={
                        'order': option_index,
                    }
                )

                if option_created:
                    created_options += 1
                else:
                    option.order = option_index
                    option.save(update_fields=['order'])

                for career_title in option_data['careers']:

                    career = careers.get(career_title)

                    if career is None:
                        self.stdout.write(
                            self.style.WARNING(
                                f'Career not found: {career_title}'
                            )
                        )
                        continue

                    weight, weight_created = CareerAnswerWeight.objects.update_or_create(
                        answer_option=option,
                        career=career,
                        defaults={
                            'weight': 3,
                        }
                    )

                    if weight_created:
                        created_weights += 1

        self.stdout.write('')

        self.stdout.write(
            self.style.SUCCESS(
                f'Questions created: {created_questions}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Questions updated: {updated_questions}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Answer options created: {created_options}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Career scoring weights created: {created_weights}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Total active questions: '
                f'{CareerQuestion.objects.filter(is_active=True).count()}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Total answer options: {CareerAnswerOption.objects.count()}'
            )
        )