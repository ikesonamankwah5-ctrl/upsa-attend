from django.core.management.base import BaseCommand
from django.utils.text import slugify

from career.models import (
    Career,
    CareerSkill,
    AcademicProgramme,
    CareerAcademicProgramme,
)


class Command(BaseCommand):

    help = 'Seed the UPSA career catalogue.'

    CAREERS = [

        # =================================================
        # ACCOUNTING AND AUDIT
        # =================================================

        {
            'title': 'Accountant',
            'area': 'Accounting and Finance',
            'short': 'Manage financial records, prepare reports and support financial decision-making.',
            'description': 'Accountants prepare financial statements, maintain accounting records, analyse transactions and help organisations understand their financial position.',
            'education': 'Accounting, Accounting and Finance, Finance or a related qualification.',
            'progression': 'Accounts Assistant → Accountant → Senior Accountant → Finance Manager → Financial Controller → CFO.',
            'industries': 'Banking, insurance, manufacturing, consulting, government and private businesses.',
            'programmes': [
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Financial Accounting', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Financial Reporting', 'TECHNICAL'),
                ('Attention to Detail', 'PROFESSIONAL'),
                ('Analytical Thinking', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'External Auditor',
            'area': 'Accounting and Audit',
            'short': 'Independently examine financial statements and organisational records.',
            'description': 'External auditors assess whether an organisation presents its financial information fairly and complies with relevant accounting standards and regulations.',
            'education': 'Accounting or Accounting and Finance, followed by relevant professional qualifications.',
            'progression': 'Audit Associate → Audit Senior → Audit Manager → Audit Partner.',
            'industries': 'Audit firms, consulting, financial services and public institutions.',
            'programmes': [
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
            ],
            'skills': [
                ('Auditing', 'TECHNICAL'),
                ('Financial Reporting', 'TECHNICAL'),
                ('Risk Assessment', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
                ('Professional Ethics', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Internal Auditor',
            'area': 'Accounting and Audit',
            'short': 'Evaluate internal controls, operational processes and organisational risks.',
            'description': 'Internal auditors examine business processes and controls to identify weaknesses, improve accountability and reduce organisational risks.',
            'education': 'Accounting, Finance, Business Administration or a related programme.',
            'progression': 'Internal Audit Assistant → Internal Auditor → Audit Manager → Chief Audit Executive.',
            'industries': 'Banks, insurance companies, government, manufacturing and multinational organisations.',
            'programmes': [
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Internal Controls', 'TECHNICAL'),
                ('Risk Management', 'TECHNICAL'),
                ('Auditing', 'TECHNICAL'),
                ('Problem Solving', 'PROFESSIONAL'),
                ('Integrity', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Tax Consultant',
            'area': 'Taxation',
            'short': 'Help individuals and organisations understand and manage their tax obligations.',
            'description': 'Tax consultants advise clients on taxation, tax compliance, tax planning and the interpretation of applicable tax rules.',
            'education': 'Accounting, Finance or a related business qualification, with relevant tax training.',
            'progression': 'Tax Assistant → Tax Consultant → Senior Tax Manager → Tax Director.',
            'industries': 'Accounting firms, consulting, government and corporate organisations.',
            'programmes': [
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
            ],
            'skills': [
                ('Taxation', 'TECHNICAL'),
                ('Financial Analysis', 'TECHNICAL'),
                ('Research', 'PROFESSIONAL'),
                ('Attention to Detail', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # BANKING, FINANCE AND INVESTMENT
        # =================================================

        {
            'title': 'Financial Analyst',
            'area': 'Finance and Investment',
            'short': 'Analyse financial information to support investment and business decisions.',
            'description': 'Financial analysts examine financial statements, business performance, budgets and market information to help organisations make informed decisions.',
            'education': 'Finance, Accounting, Banking and Finance, Business Economics or Business Administration.',
            'progression': 'Finance Assistant → Financial Analyst → Senior Analyst → Finance Manager → Finance Director.',
            'industries': 'Banks, insurance, investment firms, consulting, energy and multinational companies.',
            'programmes': [
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
                'Bachelor of Science in Agribusiness and Finance',
            ],
            'skills': [
                ('Financial Modelling', 'TECHNICAL'),
                ('Advanced Excel', 'TECHNICAL'),
                ('Financial Statement Analysis', 'TECHNICAL'),
                ('Power BI', 'TECHNICAL'),
                ('Analytical Thinking', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Investment Analyst',
            'area': 'Finance and Investment',
            'short': 'Research financial markets, companies and investment opportunities.',
            'description': 'Investment analysts evaluate companies, securities and financial markets to support investment recommendations and portfolio decisions.',
            'education': 'Finance, Accounting, Economics, Actuarial Science or a related qualification.',
            'progression': 'Research Assistant → Investment Analyst → Senior Analyst → Portfolio Manager → Investment Director.',
            'industries': 'Investment banking, asset management, pension funds and financial institutions.',
            'programmes': [
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Actuarial Science',
            ],
            'skills': [
                ('Investment Analysis', 'TECHNICAL'),
                ('Financial Modelling', 'TECHNICAL'),
                ('Valuation', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Research', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Credit Analyst',
            'area': 'Banking and Finance',
            'short': 'Evaluate borrowers and assess their ability to repay loans.',
            'description': 'Credit analysts assess the financial position, credit history and repayment capacity of individuals and businesses before lending decisions are made.',
            'education': 'Banking and Finance, Accounting, Business Economics or Business Administration.',
            'progression': 'Credit Assistant → Credit Analyst → Senior Credit Analyst → Credit Manager → Risk Director.',
            'industries': 'Commercial banks, microfinance institutions, fintech companies and lending organisations.',
            'programmes': [
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
            ],
            'skills': [
                ('Credit Risk Analysis', 'TECHNICAL'),
                ('Financial Statement Analysis', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Risk Assessment', 'TECHNICAL'),
                ('Decision Making', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Banking Officer',
            'area': 'Banking and Finance',
            'short': 'Support banking operations, customer accounts and financial services.',
            'description': 'Banking officers work in banking operations, customer services, account management, lending and other financial services.',
            'education': 'Banking and Finance, Accounting, Business Administration or Management.',
            'progression': 'Banking Assistant → Banking Officer → Branch Operations Manager → Branch Manager.',
            'industries': 'Commercial banks, rural banks, microfinance institutions and fintech companies.',
            'programmes': [
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Accounting',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Banking Operations', 'TECHNICAL'),
                ('Financial Analysis', 'TECHNICAL'),
                ('Customer Service', 'COMMUNICATION'),
                ('Problem Solving', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Risk Analyst',
            'area': 'Risk Management',
            'short': 'Identify, measure and monitor financial and operational risks.',
            'description': 'Risk analysts examine potential threats to an organisation and develop methods to measure, monitor and reduce their impact.',
            'education': 'Finance, Accounting, Actuarial Science, Business Economics or Business Administration.',
            'progression': 'Risk Assistant → Risk Analyst → Risk Manager → Chief Risk Officer.',
            'industries': 'Banking, insurance, energy, consulting and investment management.',
            'programmes': [
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
            ],
            'skills': [
                ('Risk Management', 'TECHNICAL'),
                ('Data Analysis', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Statistical Analysis', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Insurance Analyst',
            'area': 'Insurance and Risk',
            'short': 'Analyse insurance performance, policies, claims and business risks.',
            'description': 'Insurance analysts support insurance operations through financial analysis, underwriting information, claims analysis and risk reporting.',
            'education': 'Actuarial Science, Banking and Finance, Accounting or Business Administration.',
            'progression': 'Insurance Assistant → Insurance Analyst → Senior Analyst → Insurance Manager.',
            'industries': 'Life insurance, general insurance, reinsurance, brokerage and consulting.',
            'programmes': [
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Business Administration',
            ],
            'skills': [
                ('Insurance Principles', 'TECHNICAL'),
                ('Risk Analysis', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Data Analysis', 'TECHNICAL'),
                ('Analytical Thinking', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # ACTUARIAL SCIENCE AND ECONOMICS
        # =================================================

        {
            'title': 'Actuarial Analyst',
            'area': 'Actuarial Science',
            'short': 'Use mathematics and statistics to measure financial uncertainty.',
            'description': 'Actuarial analysts use mathematical models, probability and statistics to evaluate financial risks, insurance liabilities and future uncertainties.',
            'education': 'Actuarial Science, Mathematics, Statistics or a closely related quantitative qualification.',
            'progression': 'Actuarial Assistant → Actuarial Analyst → Senior Actuary → Actuarial Manager → Chief Actuary.',
            'industries': 'Insurance, reinsurance, pensions, banking and consulting.',
            'programmes': [
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Business Economics',
            ],
            'skills': [
                ('Probability and Statistics', 'TECHNICAL'),
                ('Financial Mathematics', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Python', 'TECHNICAL'),
                ('Analytical Thinking', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Economist',
            'area': 'Economics and Research',
            'short': 'Study economic trends, markets and policies.',
            'description': 'Economists research how individuals, businesses and governments make economic decisions and analyse the effects of economic policies and market changes.',
            'education': 'Business Economics, Economics, Statistics or a related quantitative programme.',
            'progression': 'Research Assistant → Economist → Senior Economist → Economic Adviser → Director.',
            'industries': 'Government, central banking, financial institutions, research organisations and international development.',
            'programmes': [
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Accounting and Finance',
            ],
            'skills': [
                ('Economic Analysis', 'TECHNICAL'),
                ('Econometrics', 'TECHNICAL'),
                ('Statistics', 'TECHNICAL'),
                ('Research', 'PROFESSIONAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # DATA, TECHNOLOGY AND ANALYTICS
        # =================================================

        {
            'title': 'Data Analyst',
            'area': 'Data and Analytics',
            'short': 'Turn raw data into useful information for business decisions.',
            'description': 'Data analysts collect, clean, organise and analyse information to identify patterns, answer business questions and communicate insights.',
            'education': 'Data Science and Analytics, Applied Statistics, Information Technology, Business Economics or Business Administration with additional analytics training.',
            'progression': 'Junior Data Analyst → Data Analyst → Senior Data Analyst → Analytics Manager → Head of Analytics.',
            'industries': 'Banking, insurance, telecommunications, retail, healthcare, government and energy.',
            'programmes': [
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Business Administration',
                'Bachelor of Science in Agribusiness and Finance',
            ],
            'skills': [
                ('Microsoft Excel', 'TECHNICAL'),
                ('SQL', 'TECHNICAL'),
                ('Power BI', 'TECHNICAL'),
                ('Python', 'TECHNICAL'),
                ('Data Visualisation', 'TECHNICAL'),
                ('Problem Solving', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Business Intelligence Analyst',
            'area': 'Business Intelligence',
            'short': 'Build dashboards and reporting systems that help businesses make better decisions.',
            'description': 'Business Intelligence Analysts transform organisational data into dashboards, reports and insights that support management and strategic decision-making.',
            'education': 'Data Science and Analytics, Information Technology, Business Administration, Accounting, Finance, Statistics or a related programme, supported by analytics skills.',
            'progression': 'Reporting Analyst → BI Analyst → Senior BI Analyst → BI Manager → Head of Business Intelligence.',
            'industries': 'Banking, insurance, retail, telecommunications, manufacturing, consulting and energy.',
            'programmes': [
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Business Administration',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Logistics and Transport Management',
            ],
            'skills': [
                ('Advanced Excel', 'TECHNICAL'),
                ('SQL', 'TECHNICAL'),
                ('Power BI', 'TECHNICAL'),
                ('Data Modelling', 'TECHNICAL'),
                ('Data Visualisation', 'TECHNICAL'),
                ('Business Analysis', 'TECHNICAL'),
            ],
        },

        {
            'title': 'Data Scientist',
            'area': 'Data Science and Artificial Intelligence',
            'short': 'Use programming, statistics and machine learning to solve complex problems.',
            'description': 'Data scientists develop analytical models, use machine learning and examine large datasets to predict outcomes and solve complex organisational problems.',
            'education': 'Data Science and Analytics, Applied Statistics, Actuarial Science or Information Technology with strong mathematical and programming skills.',
            'progression': 'Junior Data Scientist → Data Scientist → Senior Data Scientist → Data Science Manager → Chief Data Officer.',
            'industries': 'Technology, banking, insurance, telecommunications, healthcare and research.',
            'programmes': [
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Information Technology',
            ],
            'skills': [
                ('Python', 'TECHNICAL'),
                ('Statistics', 'TECHNICAL'),
                ('Machine Learning', 'TECHNICAL'),
                ('SQL', 'TECHNICAL'),
                ('Data Visualisation', 'TECHNICAL'),
                ('Mathematical Modelling', 'TECHNICAL'),
            ],
        },

        {
            'title': 'Database Administrator',
            'area': 'Information Technology',
            'short': 'Manage, secure and maintain organisational databases.',
            'description': 'Database administrators maintain databases, manage access, monitor performance and protect organisational information.',
            'education': 'Information Technology, Data Science and Analytics or a related computing qualification.',
            'progression': 'IT Support Assistant → Database Administrator → Senior Database Administrator → Database Architect.',
            'industries': 'Banking, government, telecommunications, technology and healthcare.',
            'programmes': [
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Data Science and Analytics',
                'Diploma in Information Technology Management',
            ],
            'skills': [
                ('SQL', 'TECHNICAL'),
                ('Database Management', 'TECHNICAL'),
                ('Database Security', 'TECHNICAL'),
                ('Data Backup and Recovery', 'TECHNICAL'),
                ('Problem Solving', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'IT Business Analyst',
            'area': 'Technology and Business Analysis',
            'short': 'Connect business needs with technology solutions.',
            'description': 'IT business analysts work with stakeholders to understand business requirements, document processes and help design technology solutions.',
            'education': 'Information Technology, Data Science and Analytics, Business Administration or a related programme.',
            'progression': 'Business Analyst Assistant → Business Analyst → Senior Business Analyst → Business Analysis Manager.',
            'industries': 'Technology, banking, insurance, telecommunications, consulting and government.',
            'programmes': [
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Business Administration',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Logistics and Transport Management',
                'Diploma in Information Technology Management',
                'Diploma in Management',
            ],
            'skills': [
                ('Business Process Modelling', 'TECHNICAL'),
                ('Requirements Analysis', 'TECHNICAL'),
                ('SQL', 'TECHNICAL'),
                ('Documentation', 'COMMUNICATION'),
                ('Problem Solving', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Cybersecurity Analyst',
            'area': 'Information Technology',
            'short': 'Protect computer systems, networks and organisational information.',
            'description': 'Cybersecurity analysts monitor systems, investigate security incidents and help organisations prevent unauthorised access and cyberattacks.',
            'education': 'Information Technology or a related computing programme, supported by cybersecurity training and practical experience.',
            'progression': 'IT Support Technician → Security Analyst → Security Engineer → Security Manager → Chief Information Security Officer.',
            'industries': 'Banking, telecommunications, government, technology and consulting.',
            'programmes': [
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Data Science and Analytics',
                'Diploma in Information Technology Management',
            ],
            'skills': [
                ('Network Security', 'TECHNICAL'),
                ('Cybersecurity Fundamentals', 'TECHNICAL'),
                ('Linux', 'TECHNICAL'),
                ('Incident Response', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # BUSINESS ADMINISTRATION AND MANAGEMENT
        # =================================================

        {
            'title': 'Business Analyst',
            'area': 'Business Management',
            'short': 'Examine business problems and recommend practical improvements.',
            'description': 'Business analysts study organisational performance, processes and requirements to identify problems and recommend improvements.',
            'education': 'Business Administration, Management, Finance, Economics, Information Technology or a related programme.',
            'progression': 'Business Analyst Assistant → Business Analyst → Senior Business Analyst → Strategy Manager → Business Director.',
            'industries': 'Consulting, banking, insurance, technology, manufacturing and government.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Logistics and Transport Management',
                'Diploma in Management',
            ],
            'skills': [
                ('Business Analysis', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Power BI', 'TECHNICAL'),
                ('Process Improvement', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
                ('Communication', 'COMMUNICATION'),
            ],
        },

        {
            'title': 'Operations Manager',
            'area': 'Operations and Management',
            'short': 'Coordinate people, resources and processes to improve organisational performance.',
            'description': 'Operations managers oversee daily business activities, monitor performance, manage resources and improve organisational efficiency.',
            'education': 'Business Administration, Management, Logistics, Accounting or a related programme.',
            'progression': 'Operations Assistant → Operations Supervisor → Operations Manager → General Manager → Chief Operating Officer.',
            'industries': 'Manufacturing, banking, logistics, retail, telecommunications and energy.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Applied Marketing',
                'Diploma in Management',
                'Diploma in Accounting',
            ],
            'skills': [
                ('Operations Management', 'TECHNICAL'),
                ('Project Management', 'TECHNICAL'),
                ('Process Improvement', 'TECHNICAL'),
                ('Leadership', 'LEADERSHIP'),
                ('Decision Making', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Human Resource Officer',
            'area': 'Human Resources',
            'short': 'Support recruitment, employee relations and workforce administration.',
            'description': 'Human resource officers support recruitment, staff records, employee development, performance management and workplace relations.',
            'education': 'Business Administration, Management or another relevant programme, supported by HR training.',
            'progression': 'HR Assistant → HR Officer → HR Manager → HR Director → Chief Human Resources Officer.',
            'industries': 'Government, banking, insurance, consulting and private organisations.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Public Relations Management',
                'Diploma in Management',
                'Diploma in Public Relations',
            ],
            'skills': [
                ('Recruitment', 'TECHNICAL'),
                ('Human Resource Management', 'TECHNICAL'),
                ('Conflict Resolution', 'PROFESSIONAL'),
                ('Communication', 'COMMUNICATION'),
                ('Leadership', 'LEADERSHIP'),
            ],
        },

        {
            'title': 'Project Manager',
            'area': 'Project Management',
            'short': 'Plan and coordinate projects to achieve defined objectives.',
            'description': 'Project managers plan activities, coordinate teams, manage budgets and monitor project delivery against agreed objectives.',
            'education': 'Business Administration, Management, IT, Logistics, Finance or a related programme, supported by project management experience.',
            'progression': 'Project Assistant → Project Coordinator → Project Manager → Programme Manager → Portfolio Director.',
            'industries': 'Construction, technology, banking, consulting, government and development organisations.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Public Relations Management',
                'Diploma in Management',
                'Diploma in Information Technology Management',
            ],
            'skills': [
                ('Project Planning', 'TECHNICAL'),
                ('Budget Management', 'TECHNICAL'),
                ('Risk Management', 'TECHNICAL'),
                ('Leadership', 'LEADERSHIP'),
                ('Time Management', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Management Consultant',
            'area': 'Strategy and Consulting',
            'short': 'Help organisations solve problems and improve performance.',
            'description': 'Management consultants analyse organisational challenges and recommend strategies to improve efficiency, profitability and competitiveness.',
            'education': 'Business Administration, Economics, Finance, Accounting, Statistics or another relevant programme.',
            'progression': 'Consulting Analyst → Consultant → Senior Consultant → Manager → Partner.',
            'industries': 'Management consulting, financial services, government and multinational organisations.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Applied Marketing',
                'Diploma in Management',
            ],
            'skills': [
                ('Business Strategy', 'TECHNICAL'),
                ('Data Analysis', 'TECHNICAL'),
                ('Problem Solving', 'PROFESSIONAL'),
                ('Research', 'PROFESSIONAL'),
                ('Presentation Skills', 'COMMUNICATION'),
            ],
        },

        # =================================================
        # MARKETING, COMMUNICATION AND PUBLIC RELATIONS
        # =================================================

        {
            'title': 'Marketing Manager',
            'area': 'Marketing',
            'short': 'Develop strategies to promote products, services and brands.',
            'description': 'Marketing managers plan campaigns, analyse customers and markets, manage marketing teams and evaluate promotional performance.',
            'education': 'Applied Marketing, Business Administration, Communication Studies or a related programme.',
            'progression': 'Marketing Assistant → Marketing Executive → Marketing Manager → Marketing Director → Chief Marketing Officer.',
            'industries': 'Retail, banking, telecommunications, media, manufacturing and technology.',
            'programmes': [
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Business Administration',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Public Relations Management',
                'Diploma in Marketing',
                'Diploma in Public Relations',
                'Diploma in Management',
            ],
            'skills': [
                ('Marketing Strategy', 'TECHNICAL'),
                ('Market Research', 'TECHNICAL'),
                ('Digital Marketing', 'TECHNICAL'),
                ('Data Analysis', 'TECHNICAL'),
                ('Creativity', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Digital Marketing Specialist',
            'area': 'Digital Marketing',
            'short': 'Use digital channels to attract customers and grow brands.',
            'description': 'Digital marketing specialists manage online campaigns, social media, search marketing, digital content and online customer engagement.',
            'education': 'Applied Marketing, Communication Studies, Public Relations or Business Administration.',
            'progression': 'Digital Marketing Assistant → Specialist → Digital Marketing Manager → Head of Digital Marketing.',
            'industries': 'Advertising, retail, technology, banking, media and e-commerce.',
            'programmes': [
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Business Administration',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Public Relations Management',
                'Bachelor of Arts in Applied French and Communications',
                'Diploma in Marketing',
                'Diploma in Public Relations',
            ],
            'skills': [
                ('Social Media Marketing', 'TECHNICAL'),
                ('SEO', 'TECHNICAL'),
                ('Content Marketing', 'TECHNICAL'),
                ('Google Analytics', 'TECHNICAL'),
                ('Creativity', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Public Relations Officer',
            'area': 'Public Relations and Communication',
            'short': 'Manage an organisation’s public image and stakeholder relationships.',
            'description': 'Public relations officers communicate organisational messages, coordinate media relations and help maintain positive relationships with stakeholders.',
            'education': 'Public Relations Management, Communication Studies, Applied French and Communications or Business Administration.',
            'progression': 'PR Assistant → PR Officer → PR Manager → Communications Director.',
            'industries': 'Government, media, banking, telecommunications, NGOs and corporate organisations.',
            'programmes': [
                'Bachelor of Arts in Public Relations Management',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Applied French and Communications',
                'Bachelor of Business Administration',
                'Diploma in Public Relations',
            ],
            'skills': [
                ('Public Relations', 'TECHNICAL'),
                ('Media Relations', 'COMMUNICATION'),
                ('Writing', 'COMMUNICATION'),
                ('Crisis Communication', 'COMMUNICATION'),
                ('Relationship Management', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Corporate Communications Specialist',
            'area': 'Communication',
            'short': 'Manage internal and external organisational communication.',
            'description': 'Corporate communications specialists develop communication strategies, prepare corporate messages and coordinate communication with employees, customers and stakeholders.',
            'education': 'Communication Studies, Public Relations Management, Applied French and Communications or Business Administration.',
            'progression': 'Communications Assistant → Communications Specialist → Communications Manager → Corporate Affairs Director.',
            'industries': 'Banking, insurance, government, telecommunications and multinational organisations.',
            'programmes': [
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Public Relations Management',
                'Bachelor of Arts in Applied French and Communications',
                'Bachelor of Business Administration',
                'Diploma in Public Relations',
            ],
            'skills': [
                ('Corporate Communication', 'COMMUNICATION'),
                ('Professional Writing', 'COMMUNICATION'),
                ('Stakeholder Management', 'PROFESSIONAL'),
                ('Public Relations', 'TECHNICAL'),
                ('Presentation Skills', 'COMMUNICATION'),
            ],
        },

        {
            'title': 'Market Research Analyst',
            'area': 'Marketing Analytics',
            'short': 'Study customer behaviour, market trends and competitive activity.',
            'description': 'Market research analysts collect and interpret customer and market information to help organisations make marketing and product decisions.',
            'education': 'Applied Marketing, Data Science and Analytics, Applied Statistics, Business Economics or Business Administration.',
            'progression': 'Research Assistant → Market Research Analyst → Senior Analyst → Research Manager.',
            'industries': 'Advertising, banking, telecommunications, retail and consulting.',
            'programmes': [
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
                'Diploma in Marketing',
            ],
            'skills': [
                ('Market Research', 'TECHNICAL'),
                ('Statistical Analysis', 'TECHNICAL'),
                ('Survey Design', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Data Visualisation', 'TECHNICAL'),
            ],
        },

        # =================================================
        # LOGISTICS AND SUPPLY CHAIN
        # =================================================

        {
            'title': 'Supply Chain Analyst',
            'area': 'Supply Chain Management',
            'short': 'Analyse supply chain performance and identify operational improvements.',
            'description': 'Supply chain analysts examine purchasing, inventory, transportation and supplier performance to improve efficiency and reduce costs.',
            'education': 'Logistics and Transport Management, Business Administration, Accounting, Data Science or a related programme.',
            'progression': 'Supply Chain Assistant → Supply Chain Analyst → Supply Chain Manager → Supply Chain Director.',
            'industries': 'Manufacturing, retail, logistics, energy, mining and distribution.',
            'programmes': [
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Business Administration',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Supply Chain Management', 'TECHNICAL'),
                ('Inventory Analysis', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Power BI', 'TECHNICAL'),
                ('SQL', 'TECHNICAL'),
            ],
        },

        {
            'title': 'Procurement Officer',
            'area': 'Procurement and Purchasing',
            'short': 'Manage purchasing activities and supplier relationships.',
            'description': 'Procurement officers source goods and services, evaluate suppliers, manage purchasing documentation and support cost-effective procurement.',
            'education': 'Logistics and Transport Management, Business Administration, Accounting or Management.',
            'progression': 'Procurement Assistant → Procurement Officer → Procurement Manager → Head of Procurement.',
            'industries': 'Government, manufacturing, construction, energy, healthcare and retail.',
            'programmes': [
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Business Administration',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Diploma in Management',
                'Diploma in Accounting',
            ],
            'skills': [
                ('Procurement Management', 'TECHNICAL'),
                ('Contract Management', 'TECHNICAL'),
                ('Supplier Evaluation', 'TECHNICAL'),
                ('Negotiation', 'COMMUNICATION'),
                ('Integrity', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'Logistics Manager',
            'area': 'Logistics and Transport',
            'short': 'Coordinate transportation, warehousing and distribution operations.',
            'description': 'Logistics managers oversee the movement, storage and distribution of goods and services while monitoring cost, delivery and operational performance.',
            'education': 'Logistics and Transport Management, Business Administration or Management.',
            'progression': 'Logistics Assistant → Logistics Officer → Logistics Manager → Operations Director.',
            'industries': 'Transport, shipping, manufacturing, retail, mining and energy.',
            'programmes': [
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Business Administration',
                'Diploma in Management',
            ],
            'skills': [
                ('Logistics Management', 'TECHNICAL'),
                ('Transportation Planning', 'TECHNICAL'),
                ('Inventory Management', 'TECHNICAL'),
                ('Leadership', 'LEADERSHIP'),
                ('Problem Solving', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # LAW AND LEGAL SERVICES
        # =================================================

        {
            'title': 'Legal Practitioner',
            'area': 'Law and Legal Services',
            'short': 'Provide legal advice and represent clients within the legal system.',
            'description': 'Legal practitioners advise clients, interpret laws, prepare legal documents and represent clients in legal proceedings. Practising as a lawyer requires the relevant professional legal education and qualification.',
            'education': 'Bachelor of Laws (LLB), followed by the required professional legal training and qualification in the relevant jurisdiction.',
            'progression': 'Legal Trainee → Associate → Senior Associate → Partner or Independent Practitioner.',
            'industries': 'Law firms, government, courts, corporate legal departments and NGOs.',
            'programmes': [
                'Bachelor of Laws (LLB)',
            ],
            'skills': [
                ('Legal Research', 'TECHNICAL'),
                ('Legal Writing', 'COMMUNICATION'),
                ('Contract Law', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
                ('Advocacy', 'COMMUNICATION'),
            ],
        },

        {
            'title': 'Compliance Officer',
            'area': 'Legal Compliance and Governance',
            'short': 'Help organisations comply with laws, regulations and internal policies.',
            'description': 'Compliance officers monitor regulatory requirements, review organisational procedures and help prevent legal and regulatory violations.',
            'education': 'Law, Accounting, Banking and Finance or Business Administration, with relevant compliance training.',
            'progression': 'Compliance Assistant → Compliance Officer → Compliance Manager → Chief Compliance Officer.',
            'industries': 'Banking, insurance, telecommunications, government and corporate organisations.',
            'programmes': [
                'Bachelor of Laws (LLB)',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Accounting',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Business Administration',
                'Diploma in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Regulatory Compliance', 'TECHNICAL'),
                ('Risk Assessment', 'TECHNICAL'),
                ('Legal Research', 'TECHNICAL'),
                ('Documentation', 'COMMUNICATION'),
                ('Integrity', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # REAL ESTATE
        # =================================================

        {
            'title': 'Real Estate Analyst',
            'area': 'Real Estate and Property',
            'short': 'Analyse property markets, investments and real estate performance.',
            'description': 'Real estate analysts evaluate property markets, rental income, investment opportunities and financial performance to support property decisions.',
            'education': 'Real Estate Management and Finance, Finance, Accounting or Business Economics.',
            'progression': 'Property Analyst Assistant → Real Estate Analyst → Senior Analyst → Investment Manager.',
            'industries': 'Property development, real estate investment, banking, valuation and consulting.',
            'programmes': [
                'Bachelor of Science in Real Estate Management and Finance',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Banking and Finance',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
            ],
            'skills': [
                ('Property Valuation', 'TECHNICAL'),
                ('Financial Modelling', 'TECHNICAL'),
                ('Market Research', 'TECHNICAL'),
                ('Excel', 'TECHNICAL'),
                ('Investment Analysis', 'TECHNICAL'),
            ],
        },

        {
            'title': 'Property Manager',
            'area': 'Real Estate and Property',
            'short': 'Manage properties, tenants, maintenance and property operations.',
            'description': 'Property managers oversee residential and commercial properties, coordinate maintenance, manage tenants and monitor property performance.',
            'education': 'Real Estate Management and Finance, Business Administration or Management.',
            'progression': 'Property Assistant → Property Officer → Property Manager → Head of Property Management.',
            'industries': 'Real estate, property development, facilities management and investment companies.',
            'programmes': [
                'Bachelor of Science in Real Estate Management and Finance',
                'Bachelor of Business Administration',
                'Bachelor of Science in Accounting',
                'Diploma in Management',
            ],
            'skills': [
                ('Property Management', 'TECHNICAL'),
                ('Facilities Management', 'TECHNICAL'),
                ('Financial Administration', 'TECHNICAL'),
                ('Customer Service', 'COMMUNICATION'),
                ('Negotiation', 'COMMUNICATION'),
            ],
        },

        # =================================================
        # AGRIBUSINESS
        # =================================================

        {
            'title': 'Agribusiness Manager',
            'area': 'Agribusiness',
            'short': 'Manage the commercial and financial operations of agricultural businesses.',
            'description': 'Agribusiness managers oversee agricultural enterprises, supply chains, financial planning, production and market development.',
            'education': 'Agribusiness and Finance, Business Administration, Accounting or Finance.',
            'progression': 'Agribusiness Assistant → Operations Officer → Agribusiness Manager → Managing Director.',
            'industries': 'Agriculture, food processing, agricultural finance, commodity trading and distribution.',
            'programmes': [
                'Bachelor of Science in Agribusiness and Finance',
                'Bachelor of Business Administration',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Logistics and Transport Management',
            ],
            'skills': [
                ('Agribusiness Management', 'TECHNICAL'),
                ('Financial Planning', 'TECHNICAL'),
                ('Supply Chain Management', 'TECHNICAL'),
                ('Market Analysis', 'TECHNICAL'),
                ('Entrepreneurship', 'PROFESSIONAL'),
            ],
        },

        # =================================================
        # ENTREPRENEURSHIP
        # =================================================

        {
            'title': 'Entrepreneur',
            'area': 'Entrepreneurship',
            'short': 'Create and grow a business by identifying and pursuing opportunities.',
            'description': 'Entrepreneurs identify market needs, develop business models, mobilise resources and build ventures that create economic and social value.',
            'education': 'Business Administration, Marketing, Finance, IT, Agribusiness or any relevant programme. Practical business skills and experience are important.',
            'progression': 'Business Founder → Business Owner → Managing Director → Business Group Leader.',
            'industries': 'Technology, agriculture, retail, consulting, finance, education and creative industries.',
            'programmes': [
                'Bachelor of Business Administration',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Accounting and Finance',
                'Bachelor of Science in Information Technology',
                'Bachelor of Science in Agribusiness and Finance',
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Arts in Communication Studies',
                'Bachelor of Arts in Applied French and Communications',
                'Diploma in Management',
                'Diploma in Marketing',
            ],
            'skills': [
                ('Business Planning', 'TECHNICAL'),
                ('Financial Management', 'TECHNICAL'),
                ('Marketing', 'TECHNICAL'),
                ('Leadership', 'LEADERSHIP'),
                ('Problem Solving', 'PROFESSIONAL'),
                ('Negotiation', 'COMMUNICATION'),
            ],
        },

        # =================================================
        # FRENCH AND INTERNATIONAL COMMUNICATION
        # =================================================

        {
            'title': 'French Language Specialist',
            'area': 'Languages and International Communication',
            'short': 'Use French language expertise in business, communication and international settings.',
            'description': 'French language specialists support translation, interpretation, international communication and multilingual business activities.',
            'education': 'Applied French and Communications or another relevant language qualification.',
            'progression': 'Language Assistant → French Specialist → Senior Language Professional → International Communications Manager.',
            'industries': 'International organisations, diplomacy, tourism, education, trade and multinational companies.',
            'programmes': [
                'Bachelor of Arts in Applied French and Communications',
                'Bachelor of Arts in Communication Studies',
            ],
            'skills': [
                ('French Language', 'COMMUNICATION'),
                ('Translation', 'COMMUNICATION'),
                ('Interpretation', 'COMMUNICATION'),
                ('Cross-Cultural Communication', 'COMMUNICATION'),
                ('Research', 'PROFESSIONAL'),
            ],
        },

        {
            'title': 'International Business Development Officer',
            'area': 'International Business',
            'short': 'Identify international markets and develop cross-border business relationships.',
            'description': 'International business development officers research foreign markets, identify business opportunities and build relationships with international partners.',
            'education': 'Business Administration, Applied French and Communications, Marketing, Economics or Logistics.',
            'progression': 'Business Development Assistant → International Business Officer → Regional Manager → International Business Director.',
            'industries': 'International trade, logistics, manufacturing, consulting and multinational companies.',
            'programmes': [
                'Bachelor of Arts in Applied French and Communications',
                'Bachelor of Business Administration',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Science in Logistics and Transport Management',
                'Bachelor of Science in Business Economics',
                'Bachelor of Science in Agribusiness and Finance',
            ],
            'skills': [
                ('International Business', 'TECHNICAL'),
                ('Market Research', 'TECHNICAL'),
                ('Negotiation', 'COMMUNICATION'),
                ('Cross-Cultural Communication', 'COMMUNICATION'),
                ('Business Strategy', 'TECHNICAL'),
            ],
        },

        # =================================================
        # STATISTICS AND QUANTITATIVE RESEARCH
        # =================================================

        {
            'title': 'Statistician',
            'area': 'Statistics and Research',
            'short': 'Collect, analyse and interpret numerical information.',
            'description': 'Statisticians design studies, analyse datasets and apply statistical methods to help organisations understand trends and make evidence-based decisions.',
            'education': 'Applied Statistics, Data Science and Analytics, Actuarial Science or another quantitative programme.',
            'progression': 'Statistical Assistant → Statistician → Senior Statistician → Research or Analytics Manager.',
            'industries': 'Government, research, healthcare, banking, insurance and consulting.',
            'programmes': [
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Actuarial Science',
                'Bachelor of Science in Business Economics',
            ],
            'skills': [
                ('Statistical Analysis', 'TECHNICAL'),
                ('Probability', 'TECHNICAL'),
                ('R or Python', 'TECHNICAL'),
                ('Data Visualisation', 'TECHNICAL'),
                ('Research Methods', 'TECHNICAL'),
            ],
        },

        {
            'title': 'Research Analyst',
            'area': 'Research and Analytics',
            'short': 'Conduct research and turn findings into useful recommendations.',
            'description': 'Research analysts gather information, design research activities, analyse findings and prepare reports for organisations and decision-makers.',
            'education': 'Business Economics, Applied Statistics, Data Science, Business Administration, Marketing or Communication Studies.',
            'progression': 'Research Assistant → Research Analyst → Senior Research Analyst → Research Manager.',
            'industries': 'Consulting, government, banking, NGOs, education and market research.',
            'programmes': [
                'Bachelor of Science in Applied Statistics',
                'Bachelor of Science in Data Science and Analytics',
                'Bachelor of Science in Business Economics',
                'Bachelor of Business Administration',
                'Bachelor of Science in Applied Marketing',
                'Bachelor of Arts in Communication Studies',
            ],
            'skills': [
                ('Research Methods', 'TECHNICAL'),
                ('Data Analysis', 'TECHNICAL'),
                ('Report Writing', 'COMMUNICATION'),
                ('Excel', 'TECHNICAL'),
                ('Critical Thinking', 'PROFESSIONAL'),
            ],
        },

    ]

    def handle(self, *args, **options):

        created_careers = 0
        updated_careers = 0
        created_skills = 0
        created_connections = 0

        programmes = {
            programme.name: programme
            for programme in AcademicProgramme.objects.filter(
                is_active=True
            )
        }

        for item in self.CAREERS:

            career, created = Career.objects.update_or_create(
                slug=slugify(item['title']),
                defaults={
                    'title': item['title'],
                    'career_area': item['area'],
                    'short_description': item['short'],
                    'description': item['description'],
                    'education_requirements': item['education'],
                    'career_progression': item['progression'],
                    'industries': item['industries'],
                    'recommended_skills': ', '.join(
                        skill[0] for skill in item['skills']
                    ),
                    'is_active': True,
                }
            )

            if created:
                created_careers += 1
            else:
                updated_careers += 1

            for skill_name, skill_type in item['skills']:

                skill, skill_created = CareerSkill.objects.get_or_create(
                    career=career,
                    name=skill_name,
                    defaults={
                        'skill_type': skill_type,
                        'importance': 4,
                    }
                )

                if skill_created:
                    created_skills += 1

            for programme_name in item['programmes']:

                academic_programme = programmes.get(programme_name)

                if academic_programme is None:
                    self.stdout.write(
                        self.style.WARNING(
                            f'Programme not found: {programme_name}'
                        )
                    )
                    continue

                connection, connection_created = (
                    CareerAcademicProgramme.objects.get_or_create(
                        career=career,
                        academic_programme=academic_programme,
                        defaults={
                            'relevance': 'DIRECT',
                            'relevance_note': (
                                f'This career is a potential career path '
                                f'for graduates of {programme_name}. '
                                f'Additional professional training, '
                                f'experience or certifications may be required.'
                            ),
                        }
                    )
                )

                if connection_created:
                    created_connections += 1

        self.stdout.write('')

        self.stdout.write(
            self.style.SUCCESS(
                f'Careers created: {created_careers}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Careers updated: {updated_careers}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'New skills created: {created_skills}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Career-programme connections created: '
                f'{created_connections}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Total active careers: '
                f'{Career.objects.filter(is_active=True).count()}'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Total career-programme connections: '
                f'{CareerAcademicProgramme.objects.count()}'
            )
        )