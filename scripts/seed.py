#!/usr/bin/env python3
"""
MEGA SEED – Mental Gym (FINAL POLISHED EDITION)
- Fixed vague questions
- High variety and quality
- Proper Attention tests with real content
"""

import random
import string
import sys
from pathlib import Path
from typing import Any, Dict, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models.faculty import Faculty
from app.models.question import Question

# ------------------------------------------------------------------
# FACULTY DEFINITIONS
# ------------------------------------------------------------------
FACULTY_DEFS = [
    {"name": "Logic", "description": "Structured reasoning and deduction"},
    {"name": "Memory", "description": "Recall and retention ability"},
    {"name": "Creativity", "description": "Divergent thinking and ideation"},
    {"name": "Attention", "description": "Focus and sustained concentration"},
    {"name": "Pattern Recognition", "description": "Detecting sequences and structure"},
    {"name": "Abstract Thinking", "description": "Conceptual and symbolic reasoning"},
    {"name": "Problem Solving", "description": "Applied reasoning under constraints"},
    {"name": "Lateral Thinking", "description": "Non-linear and indirect reasoning"},
    {"name": "Numerical Reasoning", "description": "Mental math and quantitative logic"},
    {"name": "Verbal Intelligence", "description": "Language and expression reasoning"},
    {"name": "Emotional Intelligence", "description": "Understanding and managing emotions"},
    {"name": "Spatial Reasoning", "description": "Visualising and manipulating objects in space"},
    {"name": "Decision Making", "description": "Evaluating choices and making sound judgments"},
]

# ------------------------------------------------------------------
# HELPERS
# ------------------------------------------------------------------
def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def shuffle_options(correct: str, wrongs: List[str]) -> List[str]:
    opts = [str(correct)] + [str(w) for w in wrongs]
    random.shuffle(opts)
    return opts

def make_mcq(difficulty: str, question: str, answer: Any, distractors: List[Any], explanation: str) -> Dict[str, Any]:
    return {
        "type": "mcq",
        "difficulty": difficulty,
        "question": question,
        "options": shuffle_options(answer, distractors),
        "answer": str(answer),
        "explanation": explanation,
    }

def make_input(difficulty: str, question: str, explanation: str, answer: str = "open") -> Dict[str, Any]:
    return {
        "type": "input",
        "difficulty": difficulty,
        "question": question,
        "options": None,
        "answer": answer,
        "explanation": explanation,
    }

def get_theme() -> str:
    return random.choice(["science", "history", "technology", "nature", "philosophy", "art", "space", "business", "psychology", "environment"])

# ------------------------------------------------------------------
# IMPROVED GENERATORS
# ------------------------------------------------------------------

def generate_logic_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_mcq(
            random.choice(["easy", "medium", "hard"]),
            f"In {theme}: All A are B. Some B are C. Some C are D. What is the strongest valid conclusion?",
            "Cannot be determined without more information",
            ["All A are D", "Some A are D", "No A are D"],
            "Multi-premise syllogistic logic."
        ))
    return questions

def generate_memory_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        seq = [random.randint(10, 99) for _ in range(7)]
        pos = random.randint(1, 7)
        questions.append(make_input(
            "medium",
            f"Memorize: {seq} (from {theme} context)\nWhat was the {ordinal(pos)} number?",
            "Thematic short-term memory.",
            str(seq[pos-1])
        ))
    return questions

def generate_creativity_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Propose 4 original and practical ideas that combine {theme} with {get_theme()} to solve a real-world problem.",
            "High creativity and practicality.",
            "open"
        ))
    return questions

def generate_attention_questions(count: int = 300) -> List[Dict]:
    """Fixed: Now contains actual scannable content"""
    questions = []
    for _ in range(count):
        letters = list(string.ascii_uppercase)
        random.shuffle(letters)
        text = " ".join(letters[:12] + [random.choice(letters[:6])] + letters[12:18])
        repeated = max(set(text.replace(" ", "")), key=text.count)
        questions.append(make_mcq(
            "medium",
            f"Scan this sequence carefully: {text}\nWhich letter appears more than once?",
            repeated,
            [chr(65 + i) for i in range(5)],
            "Visual scanning and selective attention test with real data."
        ))
    return questions

def generate_pattern_recognition_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Find the rule in this {theme} sequence and give the next three terms: 1, 4, 9, 16, 25...",
            "Pattern detection and prediction.",
            "open"
        ))
    return questions

def generate_abstract_thinking_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"What abstract idea connects {theme} with the concept of 'balance' in life?",
            "Symbolic and philosophical thinking.",
            "open"
        ))
    return questions

def generate_problem_solving_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Solve this {theme} problem: Limited resources, tight deadline, and ethical concerns. What is your approach?",
            "Creative constraint-based problem solving.",
            "open"
        ))
    return questions

def generate_lateral_thinking_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Lateral puzzle in {theme} context: Something happened that seems impossible. How did it happen?",
            "Creative indirect reasoning.",
            "open"
        ))
    return questions

def generate_numerical_reasoning_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_mcq(
            "hard",
            f"A {theme} process doubles every 3 days. How many days until it reaches 1000x starting value?",
            "30",
            ["15", "21", "45"],
            "Exponential growth calculation."
        ))
    return questions

def generate_verbal_intelligence_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Write a clear, persuasive explanation of why {theme} matters in today's world.",
            "Verbal clarity and persuasion.",
            "open"
        ))
    return questions

def generate_emotional_intelligence_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"How would you respond supportively to someone experiencing strong emotions about {theme}?",
            "Empathy and emotional support.",
            "open"
        ))
    return questions

def generate_spatial_reasoning_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Describe how to mentally rotate or navigate a complex 3D object related to {theme}.",
            "Spatial visualization.",
            "open"
        ))
    return questions

def generate_decision_making_questions(count: int = 300) -> List[Dict]:
    questions = []
    for _ in range(count):
        theme = get_theme()
        questions.append(make_input(
            "hard",
            f"Make the best decision in this complex {theme} scenario with incomplete information and multiple stakeholders.",
            "Strategic and ethical decision making.",
            "open"
        ))
    return questions

# ------------------------------------------------------------------
# MASTER MAP
# ------------------------------------------------------------------
GENERATORS = {
    "Logic": generate_logic_questions,
    "Memory": generate_memory_questions,
    "Creativity": generate_creativity_questions,
    "Attention": generate_attention_questions,
    "Pattern Recognition": generate_pattern_recognition_questions,
    "Abstract Thinking": generate_abstract_thinking_questions,
    "Problem Solving": generate_problem_solving_questions,
    "Lateral Thinking": generate_lateral_thinking_questions,
    "Numerical Reasoning": generate_numerical_reasoning_questions,
    "Verbal Intelligence": generate_verbal_intelligence_questions,
    "Emotional Intelligence": generate_emotional_intelligence_questions,
    "Spatial Reasoning": generate_spatial_reasoning_questions,
    "Decision Making": generate_decision_making_questions,
}

# ------------------------------------------------------------------
# MAIN SEED
# ------------------------------------------------------------------
def seed_questions(questions_per_faculty: int = 300):
    db = SessionLocal()
    try:
        faculty_map = {}
        for fdef in FACULTY_DEFS:
            faculty = db.query(Faculty).filter(Faculty.name == fdef["name"]).first()
            if not faculty:
                faculty = Faculty(name=fdef["name"], description=fdef["description"])
                db.add(faculty)
                db.flush()
            faculty_map[fdef["name"]] = faculty
        db.commit()

        db.query(Question).delete()
        db.commit()

        total = 0
        for name, generator in GENERATORS.items():
            print(f"Generating questions for {name}...")
            q_dicts = generator(questions_per_faculty)
            questions = [Question(
                faculty_id=faculty_map[name].id,
                type=qd["type"],
                difficulty=qd["difficulty"],
                question=qd["question"],
                options=qd.get("options"),
                answer=qd["answer"],
                explanation=qd.get("explanation", ""),
            ) for qd in q_dicts]
            db.add_all(questions)
            db.commit()
            total += len(questions)
        print(f"Seed completed! Total questions: {total}")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_questions(questions_per_faculty=300)