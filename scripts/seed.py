#!/usr/bin/env python3
"""
MEGA SEED – Mental Gym
- Creates faculties automatically (extendable list)
- Generates 120 questions per faculty (adjustable)
- Preserves all other data (users, progress)
- Safe to run multiple times
- Open-ended questions marked with answer = "open"

Run: python scripts/seed_questions.py
"""

import sys
import random
import string
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.models.faculty import Faculty
from app.models.question import Question

# ------------------------------------------------------------------
# FACULTY DEFINITIONS – Add or remove freely
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
    # New faculties – will be created automatically
    {"name": "Emotional Intelligence", "description": "Understanding and managing emotions"},
    {"name": "Spatial Reasoning", "description": "Visualising and manipulating objects in space"},
    {"name": "Decision Making", "description": "Evaluating choices and making sound judgments"},
]

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def shuffle_options(correct: str, wrongs: List[str]) -> List[str]:
    opts = [correct] + wrongs
    random.shuffle(opts)
    return opts

# ------------------------------------------------------------------
# GENERATORS – one per faculty, each returns list of question dicts
# ------------------------------------------------------------------

def generate_logic_questions(count: int) -> List[Dict]:
    questions = []
    categories = ["dogs", "cats", "birds", "fish", "mammals", "reptiles", "insects", "trees"]
    properties = ["fast", "smart", "tall", "small", "furry", "scaly", "colorful", "quiet"]
    templates = [
        {
            "template": "All {} are {}. Some {} are {}. Can we conclude some {} are {}?",
            "options": ["Yes", "No"],
            "answer": "No",
            "explanation": "No logical guarantee exists between these groups."
        },
        {
            "template": "All {} are {}. All {} are {}. Therefore, some {} are {}?",
            "options": ["Yes", "No", "Cannot be determined"],
            "answer": "Cannot be determined",
            "explanation": "We cannot assume overlap between two different groups."
        },
        {
            "template": "If A > B and B > C, then:",
            "options": ["C > A", "A > C", "A = C", "No relation"],
            "answer": "A > C",
            "explanation": "Transitive property of inequality."
        },
        {
            "template": "If all X are Y, and no Y are Z, then:",
            "options": ["Some X are Z", "No X are Z", "All X are Z", "Cannot be determined"],
            "answer": "No X are Z",
            "explanation": "If X is subset of Y and Y is disjoint from Z, X cannot intersect Z."
        },
        {
            "template": "Some {} are {}. All {} are {}. Therefore, some {} are {}?",
            "options": ["Yes", "No", "Cannot be determined"],
            "answer": "Cannot be determined",
            "explanation": "We cannot confirm overlap without more information."
        },
        {
            "template": "If A and B are both greater than C, which must be true?",
            "options": ["A > B", "B > A", "A = B", "Cannot be determined"],
            "answer": "Cannot be determined",
            "explanation": "We cannot determine the relationship between A and B."
        },
    ]
    for _ in range(count):
        t = random.choice(templates)
        if "{}" in t["template"]:
            c1 = random.choice(categories)
            c2 = random.choice(categories)
            p1 = random.choice(properties)
            p2 = random.choice(properties)
            q_text = t["template"].format(c1, c2, c1, p1, c1, p2)
        else:
            q_text = t["template"]
        questions.append({
            "type": "mcq",
            "difficulty": random.choice(["easy", "medium", "hard"]),
            "question": q_text,
            "options": t["options"],
            "answer": t["answer"],
            "explanation": t["explanation"]
        })
    return questions


def generate_memory_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: short sequences (input)
    for _ in range(count // 3):
        seq = random.sample(range(1, 10), 4)
        pos = random.randint(1, 4)
        questions.append({
            "type": "input",
            "difficulty": "easy",
            "question": f"Remember this sequence: {'-'.join(map(str, seq))}. What was the {ordinal(pos)} number?",
            "options": None,
            "answer": str(seq[pos-1]),
            "explanation": "Tests short-term recall."
        })
    # Medium: recognition (MCQ)
    items_pool = ["apple", "banana", "orange", "mango", "grape", "peach", "pear", "cherry", "kiwi", "plum"]
    for _ in range(count // 3):
        missing = random.choice(items_pool)
        present = random.sample([x for x in items_pool if x != missing], 4)
        opts = present + [missing]
        random.shuffle(opts)
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": f"Which word was NOT in the list: {', '.join(present)}?",
            "options": opts,
            "answer": missing,
            "explanation": "Tests recognition memory."
        })
    # Hard: longer sequences (input)
    for _ in range(count - len(questions)):
        seq = random.sample(range(1, 20), 6)
        pos = random.randint(1, 6)
        questions.append({
            "type": "input",
            "difficulty": "hard",
            "question": f"Memorise this sequence: {'-'.join(map(str, seq))}. What was the {ordinal(pos)} number?",
            "options": None,
            "answer": str(seq[pos-1]),
            "explanation": "Tests medium-term recall."
        })
    return questions[:count]


def generate_creativity_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: choose most creative (MCQ)
    scenarios = [
        ("plastic bottle", ["Turn into a vase", "Throw away", "Cut into strips", "Use as a paperweight"], "Turn into a vase"),
        ("old t-shirt", ["Make a rag", "Donate", "Turn into a bag", "Use as a pillowcase"], "Turn into a bag"),
        ("cardboard box", ["Storage", "Recycle", "Build a fort", "Flatten it"], "Build a fort"),
        ("broken chair", ["Throw it away", "Repair with glue", "Turn into a plant stand", "Use as firewood"], "Turn into a plant stand"),
        ("glass jar", ["Recycle", "Store buttons", "Make a lantern", "Use as a cup"], "Make a lantern"),
        ("wooden pallet", ["Burn", "Recycle", "Build a bookshelf", "Throw away"], "Build a bookshelf"),
        ("empty tin can", ["Recycle", "Make a pencil holder", "Use as a flower pot", "Throw away"], "Make a pencil holder"),
        ("old newspapers", ["Recycle", "Paper mache", "Wrap gifts", "Throw away"], "Paper mache"),
    ]
    for item in scenarios:
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": f"Which is the most creative way to reuse a {item[0]}?",
            "options": item[1],
            "answer": item[2],
            "explanation": "Assesses creative thinking."
        })
    # Medium: open-ended unusual uses (input) – answer = "open"
    objects = [
        "spoon", "paperclip", "rubber band", "brick", "string", "coin",
        "bottle cap", "old book", "fork", "pencil", "straw", "egg carton",
        "blanket", "hanger", "toothbrush", "candle"
    ]
    for obj in objects:
        questions.append({
            "type": "input",
            "difficulty": "medium",
            "question": f"List 5 unusual uses for a {obj}.",
            "options": None,
            "answer": "open",   # Community answers will be shown
            "explanation": "Divergent thinking test."
        })
    # Hard: design challenges (input) – open-ended
    challenges = [
        "Design a completely new way to water plants using only recycled materials.",
        "Propose a new method to teach children math using everyday objects.",
        "Imagine a device that helps people wake up more gently. Describe it.",
        "Create a novel game that can be played with only a piece of paper and a pen.",
        "Design an eco-friendly packaging solution for a fragile item.",
        "Invent a new tool to help elderly people open jars effortlessly.",
        "Propose a way to make queueing in lines more enjoyable."
    ]
    for c in challenges:
        questions.append({
            "type": "input",
            "difficulty": "hard",
            "question": c,
            "options": None,
            "answer": "open",
            "explanation": "Evaluates innovative problem solving."
        })
    # Fill remaining with variations of unusual uses
    while len(questions) < count:
        q = random.choice([q for q in questions if q["type"] == "input" and "unusual uses" in q["question"]])
        q = q.copy()
        obj = random.choice(objects)
        q["question"] = f"List 5 unusual uses for a {obj}."
        questions.append(q)
    return questions[:count]


def generate_attention_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: find repeated letter (MCQ)
    for _ in range(count // 3):
        letters = random.sample(string.ascii_uppercase, 5)
        repeated = random.choice(letters)
        text = " ".join(letters + [repeated])
        unique = list(set(text.replace(" ", "")))
        random.shuffle(unique)
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": f"Which letter appears twice: {text}?",
            "options": unique,
            "answer": repeated,
            "explanation": "Selective attention test."
        })
    # Medium: count target (input)
    for _ in range(count // 3):
        target = random.randint(1, 9)
        parts = [str(random.randint(1, 9)) for _ in range(8)]
        # Ensure target appears at least twice
        for i in random.sample(range(8), 2):
            parts[i] = str(target)
        text = ", ".join(parts)
        count_ans = str(parts.count(str(target)))
        questions.append({
            "type": "input",
            "difficulty": "medium",
            "question": f"Count how many times '{target}' appears: {text}",
            "options": None,
            "answer": count_ans,
            "explanation": "Focus and scanning ability."
        })
    # Hard: odd one out (MCQ)
    categories = {
        "animals": ["dog", "cat", "bird", "fish", "horse", "cow", "sheep", "pig"],
        "fruits": ["apple", "banana", "orange", "mango", "grape", "peach", "pear"],
        "colors": ["red", "blue", "green", "yellow", "purple", "orange", "black"],
        "furniture": ["chair", "table", "desk", "sofa", "bed", "cabinet"],
        "vehicles": ["car", "bus", "train", "plane", "ship", "bicycle"],
        "tools": ["hammer", "screwdriver", "wrench", "drill", "saw", "pliers"],
    }
    for _ in range(count - len(questions)):
        cat = random.choice(list(categories.keys()))
        items = categories[cat]
        chosen = random.sample(items, 4)
        other_cat = random.choice([c for c in categories if c != cat])
        intruder = random.choice(categories[other_cat])
        while intruder in chosen:
            intruder = random.choice(categories[other_cat])
        full_list = chosen + [intruder]
        random.shuffle(full_list)
        questions.append({
            "type": "mcq",
            "difficulty": "hard",
            "question": f"Which item does not belong: {', '.join(full_list)}?",
            "options": full_list,
            "answer": intruder,
            "explanation": "Tests sustained attention and discrimination."
        })
    return questions[:count]


def generate_pattern_recognition_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: arithmetic progression (MCQ)
    for _ in range(count // 3):
        step = random.randint(1, 5)
        start = random.randint(1, 10)
        seq = [start + i*step for i in range(4)]
        next_val = seq[-1] + step
        options = [str(next_val + d) for d in [-2, -1, 1, 2]] + [str(next_val)]
        random.shuffle(options)
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": f"{', '.join(map(str, seq))}, ?",
            "options": options,
            "answer": str(next_val),
            "explanation": f"Add {step} sequence."
        })
    # Medium: squares, cubes, multiply (MCQ)
    for _ in range(count // 3):
        pattern_type = random.choice(["square", "cube", "multiply"])
        if pattern_type == "square":
            n = random.randint(2, 8)
            seq = [i**2 for i in range(1, 5)]
            next_val = (n+1)**2
            expl = "Perfect squares."
        elif pattern_type == "cube":
            n = random.randint(2, 5)
            seq = [i**3 for i in range(1, 5)]
            next_val = (n+1)**3
            expl = "Perfect cubes."
        else:
            factor = random.randint(2, 5)
            seq = [factor * i for i in range(1, 5)]
            next_val = factor * 5
            expl = f"Multiply by {factor}."
        options = [str(next_val + d) for d in [-5, -3, 3, 5]] + [str(next_val)]
        random.shuffle(options)
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": f"{', '.join(map(str, seq))}, ?",
            "options": options,
            "answer": str(next_val),
            "explanation": expl
        })
    # Hard: alternating increments / complex (MCQ)
    for _ in range(count - len(questions)):
        # e.g., 1, 2, 4, 7, 11, ? (increments +1,+2,+3,+4,+5)
        base = random.randint(0, 3)
        seq = [base]
        inc = 1
        for _ in range(4):
            seq.append(seq[-1] + inc)
            inc += 1
        next_val = seq[-1] + inc
        options = [str(next_val + d) for d in [-3, -1, 1, 3]] + [str(next_val)]
        random.shuffle(options)
        questions.append({
            "type": "mcq",
            "difficulty": "hard",
            "question": f"{', '.join(map(str, seq))}, ?",
            "options": options,
            "answer": str(next_val),
            "explanation": "Increments increase by 1 each step."
        })
    return questions[:count]


def generate_abstract_thinking_questions(count: int) -> List[Dict]:
    questions = []
    word_pairs = [
        ("Idea", "mind", "paint", ["brush", "canvas", "color", "art"], "canvas"),
        ("Bird", "feather", "fish", ["water", "scale", "fin", "ocean"], "scale"),
        ("Doctor", "hospital", "teacher", ["school", "student", "classroom", "book"], "school"),
        ("Truth", "fact", "belief", ["opinion", "lie", "proof", "logic"], "opinion"),
        ("Heat", "fire", "cold", ["ice", "snow", "winter", "freeze"], "ice"),
        ("Light", "bright", "dark", ["dim", "night", "shadow", "gloom"], "dim"),
        ("Pessimism", "optimism", "cynicism", ["idealism", "realism", "skepticism", "trust"], "idealism"),
        ("Book", "author", "painting", ["artist", "canvas", "museum", "color"], "artist"),
        ("Tree", "forest", "star", ["constellation", "sky", "galaxy", "universe"], "constellation"),
        ("Shoe", "foot", "glove", ["hand", "finger", "wrist", "arm"], "hand"),
        ("Clock", "time", "thermometer", ["temperature", "weather", "heat", "mercury"], "temperature"),
        ("Key", "lock", "password", ["account", "security", "access", "encryption"], "access"),
        ("Seed", "plant", "egg", ["bird", "animal", "hatch", "shell"], "bird"),
        ("Music", "ear", "painting", ["eye", "color", "canvas", "artist"], "eye"),
    ]
    for i, (a, b, c, opts, ans) in enumerate(word_pairs):
        diff = "easy" if i < 5 else ("medium" if i < 10 else "hard")
        q_text = f"{a} is to {b} as {c} is to ____"
        questions.append({
            "type": "mcq",
            "difficulty": diff,
            "question": q_text,
            "options": opts,
            "answer": ans,
            "explanation": "Analogy mapping."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        q["question"] = q["question"].replace("Idea", "Concept").replace("mind", "brain")
        questions.append(q)
    return questions[:count]


def generate_problem_solving_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: arithmetic (MCQ)
    for _ in range(count // 3):
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        op = random.choice(['+', '-', '×'])
        if op == '+':
            ans = a + b
            q = f"{a} + {b} = ?"
        elif op == '-':
            a = max(a, b)
            ans = a - b
            q = f"{a} - {b} = ?"
        else:
            ans = a * b
            q = f"{a} × {b} = ?"
        wrongs = [ans + d for d in [-2, -1, 1, 2] if ans + d >= 0]
        if len(wrongs) > 3:
            wrongs = random.sample(wrongs, 3)
        else:
            wrongs = [ans+1, ans+2, ans+3]
        opts = shuffle_options(str(ans), list(map(str, wrongs)))
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": q,
            "options": opts,
            "answer": str(ans),
            "explanation": "Basic arithmetic."
        })
    # Medium: multi-step (MCQ)
    for _ in range(count // 3):
        a = random.randint(2, 12)
        b = random.randint(2, 10)
        c = random.randint(1, 5)
        ans = a * b + c
        q = f"({a} × {b}) + {c} = ?"
        wrongs = [ans + d for d in [-5, -3, 3, 5]]
        opts = shuffle_options(str(ans), list(map(str, wrongs)))
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": q,
            "options": opts,
            "answer": str(ans),
            "explanation": "Arithmetic reasoning."
        })
    # Hard: word problems (MCQ)
    problems = [
        ("A train travels 60 km in 1 hour. How far in 2.5 hours?", "150", ["120", "150", "180", "200"]),
        ("If 3 apples cost $2, how much do 9 apples cost?", "6", ["4", "5", "6", "8"]),
        ("A rectangle has length 8 and width 5. What is its area?", "40", ["30", "35", "40", "45"]),
        ("If a pizza is cut into 8 slices and you eat 3, what fraction is left?", "5/8", ["3/8", "5/8", "1/2", "3/4"]),
        ("A car travels 120 km in 2 hours. What is its average speed?", "60", ["50", "60", "70", "80"]),
        ("If you buy 4 pens for $2 each, how much change from $10?", "2", ["1", "2", "3", "4"]),
        ("A box contains 24 chocolates. You eat 1/4 of them. How many are left?", "18", ["12", "16", "18", "20"]),
        ("What is 15% of 200?", "30", ["25", "30", "35", "40"]),
    ]
    for q, ans, opts in problems:
        questions.append({
            "type": "mcq",
            "difficulty": "hard",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Applied problem solving."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        q["question"] = q["question"].replace("60", "70").replace("2.5", "3")
        if q["answer"].isdigit():
            q["answer"] = str(int(q["answer"]) + 10)
        questions.append(q)
    return questions[:count]


def generate_lateral_thinking_questions(count: int) -> List[Dict]:
    riddles = [
        ("A man pushes his car to a hotel and loses all his money. Why?", ["He is rich", "He is playing Monopoly", "Car broke", "He sold it"], "He is playing Monopoly", "Non-literal interpretation."),
        ("What gets wetter as it dries?", ["Towel", "Water", "Air", "Sponge"], "Towel", "Lateral reasoning."),
        ("The more you take, the more you leave behind. What am I?", ["Footsteps", "Breath", "Time", "Memory"], "Footsteps", "Riddle solving."),
        ("What can travel around the world while staying in a corner?", ["A stamp", "A person", "A letter", "A cloud"], "A stamp", "Lateral thinking puzzle."),
        ("What has keys but can't open locks?", ["Piano", "Keyboard", "Map", "Door"], "Piano", "Wordplay lateral thinking."),
        ("I have cities, but no houses; forests, but no trees; and water, but no fish. What am I?", ["Map", "Globe", "Book", "Painting"], "Map", "Lateral riddle."),
        ("What has a head, a tail, but no body?", ["Coin", "Snake", "Fish", "Arrow"], "Coin", "Lateral thinking."),
        ("What goes up but never comes down?", ["Age", "Temperature", "Balloon", "Smoke"], "Age", "Abstract riddle."),
        ("What can be broken without being held?", ["A promise", "A record", "A glass", "A heart"], "A promise", "Lateral wordplay."),
        ("What is always in front of you but can't be seen?", ["Future", "Your nose", "Air", "Light"], "Future", "Philosophical lateral."),
        ("What has a neck but no head?", ["A bottle", "A shirt", "A guitar", "A giraffe"], "A bottle", "Lateral riddle."),
        ("What begins with T, ends with T, and has T in it?", ["Teapot", "Tent", "Table", "Turtle"], "Teapot", "Word riddle."),
    ]
    questions = []
    for q, opts, ans, expl in riddles:
        diff = "easy" if "Monopoly" in q or "dries" in q else ("hard" if "corner" in q or "broken" in q else "medium")
        questions.append({
            "type": "mcq",
            "difficulty": diff,
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": expl
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        q["question"] = q["question"].replace("car", "bike").replace("hotel", "gas station")
        questions.append(q)
    return questions[:count]


def generate_numerical_reasoning_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: basic operations
    for _ in range(count // 3):
        a = random.randint(10, 50)
        b = random.randint(5, 20)
        op = random.choice(['+', '-', '×'])
        if op == '+': ans = a+b; q = f"{a} + {b} = ?"
        elif op == '-': ans = a-b; q = f"{a} - {b} = ?"
        else: ans = a*b; q = f"{a} × {b} = ?"
        wrongs = [ans + d for d in [-4, -2, 2, 4]]
        opts = shuffle_options(str(ans), list(map(str, wrongs)))
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": q,
            "options": opts,
            "answer": str(ans),
            "explanation": "Numerical operation."
        })
    # Medium: percentages / primes
    for _ in range(count // 3):
        q_type = random.choice(["percent", "prime"])
        if q_type == "percent":
            val = random.randint(50, 200)
            percent = random.choice([10, 20, 25, 50])
            ans = int(val * percent / 100)
            q = f"What is {percent}% of {val}?"
            wrongs = [ans + d for d in [-5, -3, 3, 5]]
            opts = shuffle_options(str(ans), list(map(str, wrongs)))
        else:
            candidates = [11, 13, 17, 19, 23, 29, 31, 37]
            prime = random.choice(candidates)
            compos = [x for x in candidates if x != prime and x % 2 != 0 and x % 3 != 0]
            opts = [str(prime)] + [str(c) for c in random.sample(compos, 3)]
            random.shuffle(opts)
            q = "Which number is prime?"
            ans = str(prime)
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Numerical reasoning."
        })
    # Hard: algebra
    for _ in range(count - len(questions)):
        x = random.randint(2, 9)
        coeff = random.randint(2, 5)
        constant = random.randint(1, 10)
        ans = x
        lhs = coeff * x + constant
        q = f"{coeff}x + {constant} = {lhs}. What is x?"
        wrongs = [x + d for d in [-3, -1, 1, 3] if x + d > 0]
        opts = shuffle_options(str(ans), list(map(str, wrongs)))
        questions.append({
            "type": "mcq",
            "difficulty": "hard",
            "question": q,
            "options": opts,
            "answer": str(ans),
            "explanation": "Algebraic reasoning."
        })
    return questions[:count]


def generate_verbal_intelligence_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: synonyms
    syn_pairs = [
        ("fast", "quick", ["slow", "quick", "late", "weak"]),
        ("big", "large", ["small", "large", "tall", "wide"]),
        ("happy", "joyful", ["sad", "joyful", "angry", "calm"]),
        ("cold", "chilly", ["hot", "chilly", "freezing", "warm"]),
        ("brave", "courageous", ["cowardly", "courageous", "fearless", "reckless"]),
        ("bright", "luminous", ["dark", "luminous", "glowing", "dull"]),
        ("quick", "swift", ["slow", "swift", "rapid", "hasty"]),
        ("ancient", "old", ["new", "old", "modern", "young"]),
    ]
    for word, syn, opts in syn_pairs:
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": f"Synonym of '{word}'?",
            "options": opts,
            "answer": syn,
            "explanation": "Vocabulary test."
        })
    # Medium: antonyms
    ant_pairs = [
        ("hot", "cold", ["warm", "cold", "cool", "freezing"]),
        ("light", "dark", ["bright", "dim", "dark", "heavy"]),
        ("strong", "weak", ["powerful", "weak", "fragile", "tough"]),
        ("create", "destroy", ["build", "destroy", "make", "construct"]),
        ("love", "hate", ["like", "hate", "adore", "despise"]),
        ("victory", "defeat", ["win", "defeat", "success", "triumph"]),
    ]
    for word, ant, opts in ant_pairs:
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": f"Antonym of '{word}'?",
            "options": opts,
            "answer": ant,
            "explanation": "Vocabulary test."
        })
    # Hard: analogies (MCQ)
    analogies = [
        ("Doctor is to patient as teacher is to ____", ["student", "class", "school", "book"], "student"),
        ("Book is to author as painting is to ____", ["artist", "canvas", "museum", "color"], "artist"),
        ("Car is to road as train is to ____", ["track", "station", "engine", "commute"], "track"),
        ("Knife is to cut as pen is to ____", ["write", "draw", "ink", "paper"], "write"),
        ("Wheel is to car as wing is to ____", ["airplane", "bird", "feather", "fly"], "airplane"),
        ("Chair is to sit as bed is to ____", ["sleep", "lie", "rest", "comfort"], "sleep"),
        ("Hammer is to nail as screwdriver is to ____", ["screw", "bolt", "drill", "wrench"], "screw"),
        ("Fish is to water as bird is to ____", ["air", "nest", "sky", "fly"], "air"),
    ]
    for stem, opts, ans in analogies:
        questions.append({
            "type": "mcq",
            "difficulty": "hard",
            "question": stem,
            "options": opts,
            "answer": ans,
            "explanation": "Verbal analogy."
        })
    # Open-ended (input) – answer = "open"
    concepts = [
        "clarity of thought", "empathy", "sustainability", "critical thinking",
        "resilience", "innovation", "integrity", "compassion", "wisdom"
    ]
    for c in concepts:
        questions.append({
            "type": "input",
            "difficulty": "medium",
            "question": f"Explain what '{c}' means in your own words.",
            "options": None,
            "answer": "open",
            "explanation": "Expression ability."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        if q["type"] == "mcq" and "Synonym" in q["question"]:
            q["question"] = q["question"].replace("Synonym", "Word similar to")
        elif q["type"] == "input":
            q["question"] = q["question"].replace("clarity of thought", "creativity")
        questions.append(q)
    return questions[:count]


# NEW FACULTY GENERATORS – you can add more as needed

def generate_emotional_intelligence_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: identify emotions from scenarios (MCQ)
    scenarios = [
        ("You just received a gift you didn't expect. How do you feel?", ["Happy", "Sad", "Angry", "Surprised"], "Surprised"),
        ("A friend cancels plans at the last minute. How might you feel?", ["Disappointed", "Relieved", "Excited", "Curious"], "Disappointed"),
        ("You helped someone and they thanked you warmly. How do you feel?", ["Proud", "Jealous", "Indifferent", "Anxious"], "Proud"),
        ("You see someone being bullied. What emotion might you feel?", ["Empathy", "Joy", "Envy", "Boredom"], "Empathy"),
        ("You've been working hard and finally achieve your goal. How do you feel?", ["Satisfied", "Frustrated", "Worried", "Alone"], "Satisfied"),
    ]
    for q, opts, ans in scenarios:
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Emotion recognition."
        })
    # Medium: reading facial expressions (MCQ) – simplified with text
    expressions = [
        ("Which emotion is often shown by a smile?", ["Happiness", "Anger", "Fear", "Sadness"], "Happiness"),
        ("Which emotion is typically shown by frowning and tears?", ["Sadness", "Joy", "Surprise", "Disgust"], "Sadness"),
        ("Wide eyes and open mouth usually indicate what?", ["Surprise", "Fear", "Anger", "Happiness"], "Surprise"),
        ("What emotion is associated with raised eyebrows and a tight mouth?", ["Disgust", "Joy", "Sadness", "Fear"], "Disgust"),
    ]
    for q, opts, ans in expressions:
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Facial expression recognition."
        })
    # Hard: open-ended empathy scenarios (input) – answer = "open"
    scenarios_open = [
        "Describe how you would comfort a friend who just lost a pet.",
        "How would you respond to a colleague who is visibly stressed?",
        "Imagine a situation where you have to give constructive criticism. How would you do it empathetically?",
        "Describe a time you felt deeply understood by someone. What did they do?",
    ]
    for s in scenarios_open:
        questions.append({
            "type": "input",
            "difficulty": "hard",
            "question": s,
            "options": None,
            "answer": "open",
            "explanation": "Measures empathy and emotional response."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        q["question"] = q["question"].replace("friend", "family member")
        questions.append(q)
    return questions[:count]


def generate_spatial_reasoning_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: identify shapes (MCQ)
    shape_descs = [
        ("Which shape has three sides?", ["Square", "Triangle", "Circle", "Pentagon"], "Triangle"),
        ("Which shape has four equal sides?", ["Rectangle", "Square", "Oval", "Trapezoid"], "Square"),
        ("Which shape has no corners?", ["Circle", "Square", "Rectangle", "Pentagon"], "Circle"),
        ("Which shape has five sides?", ["Pentagon", "Hexagon", "Octagon", "Triangle"], "Pentagon"),
    ]
    for q, opts, ans in shape_descs:
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Basic shape recognition."
        })
    # Medium: mental rotation (describe)
    rotations = [
        ("If you rotate a square 45°, what shape do you get?", ["Square", "Rhombus", "Rectangle", "Circle"], "Square"),
        ("A cube has how many faces?", ["4", "6", "8", "12"], "6"),
        ("What is the 2D net of a cube?", ["6 squares", "4 squares", "3 squares", "8 squares"], "6 squares"),
    ]
    for q, opts, ans in rotations:
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Spatial visualization."
        })
    # Hard: open-ended spatial description (input) – answer = "open"
    spatial_tasks = [
        "Describe how to get from your bedroom to the kitchen in your home.",
        "Imagine you are looking at a map. How would you explain the route from point A to point B?",
        "Draw a mental picture of a bird's-eye view of your house. Describe it.",
    ]
    for s in spatial_tasks:
        questions.append({
            "type": "input",
            "difficulty": "hard",
            "question": s,
            "options": None,
            "answer": "open",
            "explanation": "Spatial orientation and description."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        questions.append(q)
    return questions[:count]


def generate_decision_making_questions(count: int) -> List[Dict]:
    questions = []
    # Easy: simple trade-offs (MCQ)
    trades = [
        ("You have $10 to spend. Which option is the best use of money?", ["Buy a snack", "Save it", "Buy a toy", "Donate"], "Save it"),
        ("You have one hour free. What is the most productive use?", ["Watch TV", "Exercise", "Nap", "Scroll social media"], "Exercise"),
        ("Which choice is likely to lead to better health in the long run?", ["Eat fast food", "Cook a meal at home", "Skip dinner", "Eat dessert"], "Cook a meal at home"),
    ]
    for q, opts, ans in trades:
        questions.append({
            "type": "mcq",
            "difficulty": "easy",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Evaluates basic decision making."
        })
    # Medium: risk vs reward (MCQ)
    risks = [
        ("You can invest $100 with 50% chance to double or lose it all. What is the expected value?", ["$100", "$50", "$0", "$200"], "$100"),
        ("Which is a safer investment?", ["Stocks", "Bonds", "Real estate", "Cryptocurrency"], "Bonds"),
    ]
    for q, opts, ans in risks:
        questions.append({
            "type": "mcq",
            "difficulty": "medium",
            "question": q,
            "options": opts,
            "answer": ans,
            "explanation": "Risk evaluation."
        })
    # Hard: ethical dilemma open-ended (input)
    dilemmas = [
        "You see a colleague taking credit for your work. How do you handle it?",
        "You find a wallet with $500 and no ID. What do you do?",
        "You are offered a promotion that requires moving to a new city, but your family is settled. What factors do you consider?",
    ]
    for s in dilemmas:
        questions.append({
            "type": "input",
            "difficulty": "hard",
            "question": s,
            "options": None,
            "answer": "open",
            "explanation": "Complex decision making and ethics."
        })
    while len(questions) < count:
        q = random.choice(questions).copy()
        q["question"] = q["question"].replace("colleague", "classmate")
        questions.append(q)
    return questions[:count]


# ------------------------------------------------------------------
# MASTER MAP: faculty name -> generator function
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
    # New faculties
    "Emotional Intelligence": generate_emotional_intelligence_questions,
    "Spatial Reasoning": generate_spatial_reasoning_questions,
    "Decision Making": generate_decision_making_questions,
}

# ------------------------------------------------------------------
# MAIN SEED FUNCTION
# ------------------------------------------------------------------
def seed_questions(questions_per_faculty: int = 120):
    db = SessionLocal()
    try:
        # 1. Ensure all faculties exist
        print("🔍 Checking faculties...")
        faculty_map = {}
        for fdef in FACULTY_DEFS:
            faculty = db.query(Faculty).filter(Faculty.name == fdef["name"]).first()
            if not faculty:
                faculty = Faculty(name=fdef["name"], description=fdef["description"])
                db.add(faculty)
                db.flush()
                print(f"✅ Created faculty: {fdef['name']}")
            else:
                print(f"ℹ️ Faculty exists: {fdef['name']}")
            faculty_map[fdef["name"]] = faculty
        db.commit()

        # 2. Delete all existing questions
        print("🗑️  Clearing all questions...")
        deleted = db.query(Question).delete()
        db.commit()
        print(f"✅ Deleted {deleted} questions.")

        # 3. Generate and insert questions per faculty
        total_inserted = 0
        for name, generator in GENERATORS.items():
            faculty = faculty_map.get(name)
            if not faculty:
                print(f"⚠️ Faculty '{name}' not found in map, skipping.")
                continue
            print(f"🔄 Generating {questions_per_faculty} questions for {name}...")
            q_dicts = generator(questions_per_faculty)
            questions = []
            for qd in q_dicts:
                q = Question(
                    faculty_id=faculty.id,
                    type=qd["type"],
                    difficulty=qd["difficulty"],
                    question=qd["question"],
                    options=qd.get("options"),  # list or None
                    answer=qd["answer"],
                    explanation=qd.get("explanation", "")
                )
                questions.append(q)
            db.add_all(questions)
            db.commit()
            total_inserted += len(questions)
            print(f"✅ Inserted {len(questions)} questions for {name}.")

        print(f"\n🎉 Seed completed! Total questions inserted: {total_inserted}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Adjust the number to scale up or down
    seed_questions(questions_per_faculty=130)