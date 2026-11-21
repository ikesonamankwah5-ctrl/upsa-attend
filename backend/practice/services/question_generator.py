import re
import random


def clean_text(text):
    """Clean extracted lecture-note text."""

    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_sentences(text):
    """Break lecture notes into meaningful sentences."""

    text = clean_text(text)

    sentences = re.split(r'(?<=[.!?])\s+', text)

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) >= 8
    ]


def extract_definitions(text):
    """Identify simple definitions from lecture notes."""

    patterns = [
        r'([A-Z][A-Za-z\s]{2,50}?)\s+is\s+([^.!?]{10,200})',
        r'([A-Z][A-Za-z\s]{2,50}?)\s+refers to\s+([^.!?]{10,200})',
        r'([A-Z][A-Za-z\s]{2,50}?)\s+means\s+([^.!?]{10,200})',
        r'([A-Z][A-Za-z\s]{2,50}?)\s+can be defined as\s+([^.!?]{10,200})',
    ]

    definitions = []

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for term, meaning in matches:

            term = term.strip()
            meaning = meaning.strip()

            if len(term.split()) <= 6:

                definitions.append({
                    'term': term,
                    'meaning': meaning
                })

    unique_definitions = []
    seen = set()

    for definition in definitions:

        key = definition['term'].lower()

        if key not in seen:
            seen.add(key)
            unique_definitions.append(definition)

    return unique_definitions


def generate_theory_questions(sentences, number_of_questions):

    questions = []

    question_templates = [
        "Explain the following statement from your lecture notes: {}",
        "Discuss the meaning and importance of the following: {}",
        "Describe what your lecture notes explain about: {}",
        "Explain the concept presented in the following statement: {}",
    ]

    random.shuffle(sentences)

    for sentence in sentences:

        if len(questions) >= number_of_questions:
            break

        question_text = random.choice(question_templates).format(
            sentence
        )

        questions.append({
            'question_text': question_text,
            'question_type': 'THEORY',
            'options': [],
            'correct_answer': '',
            'explanation': (
                'Use your uploaded lecture notes to construct '
                'a complete answer.'
            ),
            'model_answer': sentence,
            'marks': 5,
        })

    return questions


def generate_objective_questions(definitions, number_of_questions):

    questions = []

    if len(definitions) < 4:
        return questions

    random.shuffle(definitions)

    for definition in definitions:

        if len(questions) >= number_of_questions:
            break

        correct_meaning = definition['meaning']

        other_meanings = [
            item['meaning']
            for item in definitions
            if item['meaning'] != correct_meaning
        ]

        if len(other_meanings) < 3:
            continue

        options = random.sample(other_meanings, 3)

        options.append(correct_meaning)

        random.shuffle(options)

        questions.append({
            'question_text': (
                f"According to your lecture notes, "
                f"which statement best describes "
                f"{definition['term']}?"
            ),
            'question_type': 'OBJECTIVE',
            'options': options,
            'correct_answer': correct_meaning,
            'explanation': (
                f"{definition['term']} is described in your "
                f"lecture notes as: {correct_meaning}"
            ),
            'model_answer': '',
            'marks': 1,
        })

    return questions


def generate_practice_questions(
    source_text,
    question_format,
    number_of_questions
):
    """
    Generate practice questions using extracted lecture notes.

    This is a temporary mock generator.
    It does not use an external AI API.
    """

    if not source_text or not source_text.strip():
        raise ValueError(
            "No readable lecture-note content was provided."
        )

    if number_of_questions < 1:
        raise ValueError(
            "The number of questions must be at least 1."
        )

    sentences = extract_sentences(source_text)

    definitions = extract_definitions(source_text)

    if question_format == 'OBJECTIVE':

        questions = generate_objective_questions(
            definitions,
            number_of_questions
        )

    elif question_format == 'THEORY':

        questions = generate_theory_questions(
            sentences,
            number_of_questions
        )

    elif question_format == 'MIXED':

        objective_count = number_of_questions // 2

        theory_count = number_of_questions - objective_count

        objective_questions = generate_objective_questions(
            definitions,
            objective_count
        )

        theory_questions = generate_theory_questions(
            sentences,
            theory_count
        )

        questions = objective_questions + theory_questions

        random.shuffle(questions)

    else:
        raise ValueError(
            "Invalid question format selected."
        )

    if not questions:
        raise ValueError(
            "The uploaded lecture notes do not contain enough "
            "recognisable content to generate questions. "
            "Try uploading more detailed lecture notes."
        )

    for number, question in enumerate(questions, start=1):
        question['question_number'] = number

    return questions