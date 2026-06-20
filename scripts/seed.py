"""
Mental Gym Seed Script (Unified - High Population Version)
Combines all possible SQLAlchemy DB operations using the full question set:
- Targeted Purges (DELETE)
- Existence Verifications (SELECT)
- Explicit Instances (INSERT)
- Batch Processing (BULK INSERT / add_all)
- Atomic Increments (UPDATE)

Run:
python scripts/seed.py
"""

import sys
from pathlib import Path

# Fix path navigation to app root
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.user_progress import UserProgress
from app.models.faculty import Faculty
from app.models.faculty_progress import FacultyProgress
from app.models.question import Question
from app.core.security import hash_password


# -----------------------------
# HIGH POPULATION SEED DATA
# -----------------------------
FACULTIES = [
    ("Logic", "Structured reasoning and deduction"),
    ("Memory", "Recall and retention ability"),
    ("Creativity", "Divergent thinking and ideation"),
    ("Attention", "Focus and sustained concentration"),
    ("Pattern Recognition", "Detecting sequences and structure"),
    ("Abstract Thinking", "Conceptual and symbolic reasoning"),
    ("Problem Solving", "Applied reasoning under constraints"),
    ("Lateral Thinking", "Non-linear and indirect reasoning"),
    ("Numerical Reasoning", "Mental math and quantitative logic"),
    ("Verbal Intelligence", "Language and expression reasoning"),
]

# Populated dictionary format preserved from your comprehensive first script
QUESTION_SEED = [
    # LOGIC
    {
        "faculty": "Logic",
        "type": "mcq",
        "difficulty": "easy",
        "question": "All dogs are animals. Some animals are fast. Can we conclude some dogs are fast?",
        "options": ["Yes", "No"],
        "answer": "No",
        "explanation": "No logical guarantee exists."
    },
    {
        "faculty": "Logic",
        "type": "mcq",
        "difficulty": "medium",
        "question": "If A > B and B > C, then:",
        "options": ["C > A", "A > C", "A = C", "No relation"],
        "answer": "A > C",
        "explanation": "Transitive property of inequality."
    },
    # MEMORY
    {
        "faculty": "Memory",
        "type": "input",
        "difficulty": "easy",
        "question": "Remember this sequence: 7 - 2 - 9 - 4. What was the 3rd number?",
        "options": None,
        "answer": "9",
        "explanation": "Tests short-term recall."
    },
    {
        "faculty": "Memory",
        "type": "mcq",
        "difficulty": "medium",
        "question": "Which word was NOT in the list: apple, banana, orange, mango?",
        "options": ["apple", "grape", "orange", "banana"],
        "answer": "grape",
        "explanation": "Tests recognition memory."
    },
    # CREATIVITY
    {
        "faculty": "Creativity",
        "type": "input",
        "difficulty": "medium",
        "question": "List 5 unusual uses for a spoon.",
        "options": None,
        "answer": "open",
        "explanation": "Divergent thinking test."
    },
    {
        "faculty": "Creativity",
        "type": "mcq",
        "difficulty": "easy",
        "question": "Which is the most creative solution?",
        "options": ["Reuse bottle as lamp", "Throw bottle away", "Break bottle", "Ignore bottle"],
        "answer": "Reuse bottle as lamp",
        "explanation": "Value-added repurposing."
    },
    # ATTENTION
    {
        "faculty": "Attention",
        "type": "mcq",
        "difficulty": "easy",
        "question": "Which letter appears twice: A B C D A E?",
        "options": ["A", "B", "C", "D"],
        "answer": "A",
        "explanation": "Selective attention test."
    },
    {
        "faculty": "Attention",
        "type": "input",
        "difficulty": "medium",
        "question": "Count how many times '7' appears: 7, 17, 27, 7, 70",
        "options": None,
        "answer": "3",
        "explanation": "Focus and scanning ability."
    },
    # PATTERN RECOGNITION
    {
        "faculty": "Pattern Recognition",
        "type": "mcq",
        "difficulty": "easy",
        "question": "2, 4, 6, 8, ?",
        "options": ["9", "10", "12", "14"],
        "answer": "10",
        "explanation": "Add 2 sequence."
    },
    {
        "faculty": "Pattern Recognition",
        "type": "mcq",
        "difficulty": "medium",
        "question": "1, 4, 9, 16, ?",
        "options": ["20", "25", "30", "36"],
        "answer": "25",
        "explanation": "Perfect squares."
    },
    # ABSTRACT THINKING
    {
        "faculty": "Abstract Thinking",
        "type": "mcq",
        "difficulty": "easy",
        "question": "Idea is to mind as paint is to ____",
        "options": ["brush", "canvas", "color", "art"],
        "answer": "canvas",
        "explanation": "Analogy mapping."
    },
    {
        "faculty": "Abstract Thinking",
        "type": "mcq",
        "difficulty": "medium",
        "question": "Truth is to fact as belief is to ____",
        "options": ["opinion", "lie", "proof", "logic"],
        "answer": "opinion",
        "explanation": "Concept mapping."
    },
    # PROBLEM SOLVING
    {
        "faculty": "Problem Solving",
        "type": "mcq",
        "difficulty": "easy",
        "question": "What is 3 × 3?",
        "options": ["6", "9", "12", "15"],
        "answer": "9",
        "explanation": "Basic multiplication."
    },
    {
        "faculty": "Problem Solving",
        "type": "mcq",
        "difficulty": "medium",
        "question": "20 - 7 = ?",
        "options": ["12", "13", "14", "15"],
        "answer": "13",
        "explanation": "Arithmetic reasoning."
    },
    # LATERAL THINKING
    {
        "faculty": "Lateral Thinking",
        "type": "mcq",
        "difficulty": "easy",
        "question": "A man pushes his car to a hotel and loses all his money. Why?",
        "options": ["He is rich", "He is playing Monopoly", "Car broke", "He sold it"],
        "answer": "He is playing Monopoly",
        "explanation": "Non-literal interpretation."
    },
    {
        "faculty": "Lateral Thinking",
        "type": "mcq",
        "difficulty": "medium",
        "question": "What gets wetter as it dries?",
        "options": ["Towel", "Water", "Air", "Sponge"],
        "answer": "Towel",
        "explanation": "Lateral reasoning."
    },
    # NUMERICAL REASONING
    {
        "faculty": "Numerical Reasoning",
        "type": "mcq",
        "difficulty": "easy",
        "question": "10 + 15 = ?",
        "options": ["20", "25", "30", "35"],
        "answer": "25",
        "explanation": "Basic addition."
    },
    {
        "faculty": "Numerical Reasoning",
        "type": "mcq",
        "difficulty": "medium",
        "question": "5 × 12 = ?",
        "options": ["50", "55", "60", "65"],
        "answer": "60",
        "explanation": "Multiplication."
    },
    # VERBAL INTELLIGENCE
    {
        "faculty": "Verbal Intelligence",
        "type": "mcq",
        "difficulty": "easy",
        "question": "Synonym of 'fast'?",
        "options": ["slow", "quick", "late", "weak"],
        "answer": "quick",
        "explanation": "Vocabulary test."
    },
    {
        "faculty": "Verbal Intelligence",
        "type": "input",
        "difficulty": "medium",
        "question": "Explain what 'clarity of thought' means in your own words.",
        "options": None,
        "answer": "open",
        "explanation": "Expression ability."
    },
]


# -----------------------------
# UNIFIED ENGINE PIPELINE
# -----------------------------
def seed_database(force_destructive_reset=True):
    """
    Executes an extensive seeding protocol tracking multiple ORM interaction spaces:
    - Purging strategies (DELETE/DROP)
    - Identity confirmation checks (SELECT)
    - Object structural linkage generation (INSERT/FLUSH)
    - High-density arrays handling (BULK INSERT)
    - Direct counter adjustments (UPDATE)
    """
    if force_destructive_reset:
        print("⚠️ Performing destructive database structural reset...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✓ DB Schema safely re-synchronized.")
    else:
        print("🔄 Performing programmatic session deletions...")
        db_clear = SessionLocal()
        try:
            # Operation: DELETE 
            db_clear.query(UserProgress).delete()
            db_clear.query(FacultyProgress).delete()
            db_clear.query(Question).delete()
            db_clear.query(Faculty).delete()
            db_clear.query(User).delete()
            db_clear.commit()
            print("✓ Clear operation clean execution verified.")
        except Exception as e:
            db_clear.rollback()
            print(f"✗ Selective deletion strategy aborted: {e}")
            raise
        finally:
            db_clear.close()

    # Create worker session context
    db = SessionLocal()

    try:
        # -------------------------------------------------------------
        # 1. READ & CREATE: Verify/Generate Default Target User Context
        # -------------------------------------------------------------
        target_email = "test@gym.com"
        
        # Operation: SELECT
        user_record = db.query(User).filter(User.email == target_email).first()
        
        if not user_record:
            # Operation: INSERT
            user_record = User(
                username="testuser",
                email=target_email,
                password=hash_password("1234")
            )
            db.add(user_record)
            db.flush()  # Extract autogenerated Primary Keys instantly
            print(f"✓ Created root tracking user (ID: {user_record.id})")
            
            # Link dependent relational records
            db.add(UserProgress(user_id=user_record.id, xp=0, level=1, streak=0))
        else:
            print(f"ℹ️ Core tracking user found dynamically. ID: {user_record.id}")

        # -------------------------------------------------------------
        # 2. CREATE: Base Faculty Setup Matrix
        # -------------------------------------------------------------
        faculty_map = {}
        
        for name, desc in FACULTIES:
            # Operation: SELECT (Validation lookup)
            fac = db.query(Faculty).filter(Faculty.name == name).first()
            
            if not fac:
                fac = Faculty(name=name, description=desc)
                db.add(fac)
                db.flush()
            
            faculty_map[name] = fac

            # Operation: UPSERT / Verification logic for tracking linkages
            f_prog = db.query(FacultyProgress).filter(
                FacultyProgress.user_id == user_record.id,
                FacultyProgress.faculty_id == fac.id
            ).first()

            if not f_prog:
                db.add(FacultyProgress(
                    user_id=user_record.id,
                    faculty_id=fac.id,
                    xp=0,
                    level=1,
                    streak=0,
                    attempts=0,
                    correct=0
                ))
                
        db.commit()  # Flush structural configuration maps to context memory
        print("✓ Core Faculties and progress models established.")

        # -------------------------------------------------------------
        # 3. BULK OPERATION: Core Question Bulk Implementation
        # -------------------------------------------------------------
        bulk_questions = []
        
        for q in QUESTION_SEED:
            target_fac = faculty_map.get(q["faculty"])
            if not target_fac:
                continue

            # Duplicate screening matching existing criteria
            duplicate_found = db.query(Question).filter(
                Question.faculty_id == target_fac.id,
                Question.question == q["question"]
            ).first()

            if not duplicate_found:
                bulk_questions.append(
                    Question(
                        faculty_id=target_fac.id,
                        type=q["type"],
                        difficulty=q["difficulty"],
                        question=q["question"],
                        options=q.get("options"),
                        answer=q["answer"],
                        explanation=q.get("explanation")
                    )
                )

        if bulk_questions:
            # Operation: BULK INSERT (Optimized execution block handling)
            db.add_all(bulk_questions)
            db.commit()
            print(f"✓ Bulk batch system executed. {len(bulk_questions)} Questions populated.")
        else:
            print("ℹ️ Processing complete. Question bank is already matching target parameters.")

        # -------------------------------------------------------------
        # 4. UPDATE: Modify State Analytics Post-Execution
        # -------------------------------------------------------------
        # Operation: UPDATE (Simulate awarding introductory bonus seed XP)
        db.query(UserProgress).filter(UserProgress.user_id == user_record.id).update(
            {"xp": UserProgress.xp + 100}
        )
        db.commit()
        print("✓ Incremental adjustment UPDATE verified against profile state tracking models.")

        print("\n🎮 Mental Gym high population dataset seed executed flawlessly!")

    except Exception as e:
        db.rollback()
        print(f"✗ Critical database lifecycle execution failure. Session rolling back: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing full-spectrum database generation run...\n")
    # Setting force_destructive_reset=True cleans out everything for a pristine, error-free run.
    seed_database(force_destructive_reset=True)