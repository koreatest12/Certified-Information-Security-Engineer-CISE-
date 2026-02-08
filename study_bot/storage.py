"""
정보보안기사(CISE) 공부자료 정리 봇 - 데이터 저장소
JSON 파일 기반 영속 저장소
"""

import json
import os
from typing import List, Optional

from models import StudyNote, QuizQuestion


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
NOTES_FILE = os.path.join(DATA_DIR, "notes.json")
QUIZ_FILE = os.path.join(DATA_DIR, "quiz.json")
STATS_FILE = os.path.join(DATA_DIR, "stats.json")


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_json(filepath: str) -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filepath: str, data: list):
    _ensure_data_dir()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── 노트 관련 ──

def save_note(note: StudyNote):
    """노트 저장 (추가 또는 업데이트)"""
    notes = _load_json(NOTES_FILE)
    for i, n in enumerate(notes):
        if n["note_id"] == note.note_id:
            notes[i] = note.to_dict()
            _save_json(NOTES_FILE, notes)
            return
    notes.append(note.to_dict())
    _save_json(NOTES_FILE, notes)


def get_all_notes() -> List[StudyNote]:
    """전체 노트 조회"""
    data = _load_json(NOTES_FILE)
    return [StudyNote.from_dict(d) for d in data]


def get_notes_by_category(category: str) -> List[StudyNote]:
    """과목별 노트 조회"""
    all_notes = get_all_notes()
    return [n for n in all_notes if n.category == category]


def search_notes(keyword: str) -> List[StudyNote]:
    """키워드로 노트 검색 (제목, 내용, 키워드 필드)"""
    keyword_lower = keyword.lower()
    all_notes = get_all_notes()
    results = []
    for note in all_notes:
        if (keyword_lower in note.title.lower()
                or keyword_lower in note.content.lower()
                or any(keyword_lower in kw.lower() for kw in note.keywords)):
            results.append(note)
    return results


def get_note_by_id(note_id: str) -> Optional[StudyNote]:
    """ID로 노트 조회"""
    all_notes = get_all_notes()
    for note in all_notes:
        if note.note_id == note_id:
            return note
    return None


def delete_note(note_id: str) -> bool:
    """노트 삭제"""
    notes = _load_json(NOTES_FILE)
    new_notes = [n for n in notes if n["note_id"] != note_id]
    if len(new_notes) == len(notes):
        return False
    _save_json(NOTES_FILE, new_notes)
    return True


# ── 퀴즈 관련 ──

def save_quiz(quiz: QuizQuestion):
    """퀴즈 저장"""
    quizzes = _load_json(QUIZ_FILE)
    for i, q in enumerate(quizzes):
        if q["question_id"] == quiz.question_id:
            quizzes[i] = quiz.to_dict()
            _save_json(QUIZ_FILE, quizzes)
            return
    quizzes.append(quiz.to_dict())
    _save_json(QUIZ_FILE, quizzes)


def get_all_quizzes() -> List[QuizQuestion]:
    """전체 퀴즈 조회"""
    data = _load_json(QUIZ_FILE)
    return [QuizQuestion.from_dict(d) for d in data]


def get_quizzes_by_category(category: str) -> List[QuizQuestion]:
    """과목별 퀴즈 조회"""
    all_quizzes = get_all_quizzes()
    return [q for q in all_quizzes if q.category == category]


# ── 통계 관련 ──

def get_stats() -> dict:
    """학습 통계 조회"""
    notes = get_all_notes()
    quizzes = get_all_quizzes()

    category_stats = {}
    for note in notes:
        cat = note.category
        if cat not in category_stats:
            category_stats[cat] = {"total": 0, "mastered": 0, "review_total": 0}
        category_stats[cat]["total"] += 1
        if note.mastered:
            category_stats[cat]["mastered"] += 1
        category_stats[cat]["review_total"] += note.review_count

    quiz_stats = {"total": 0, "correct": 0, "wrong": 0}
    for q in quizzes:
        quiz_stats["total"] += q.correct_count + q.wrong_count
        quiz_stats["correct"] += q.correct_count
        quiz_stats["wrong"] += q.wrong_count

    return {
        "total_notes": len(notes),
        "mastered_notes": sum(1 for n in notes if n.mastered),
        "total_quizzes": len(quizzes),
        "category_stats": category_stats,
        "quiz_stats": quiz_stats,
    }
