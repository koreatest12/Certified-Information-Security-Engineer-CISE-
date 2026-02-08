#!/usr/bin/env python3
"""
정보보안기사(CISE) 공부자료 정리 봇 - 자동화 테스트
모든 핵심 기능을 비대화형(non-interactive)으로 검증합니다.
"""

import sys
import os
import json
import tempfile
import shutil

# 모듈 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import storage
from models import StudyNote, QuizQuestion, CATEGORIES, SUBCATEGORIES


# ── 테스트 유틸리티 ──

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_true(self, condition, message):
        if condition:
            self.passed += 1
            print(f"  [PASS] {message}")
        else:
            self.failed += 1
            self.errors.append(message)
            print(f"  [FAIL] {message}")

    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.passed += 1
            print(f"  [PASS] {message}")
        else:
            self.failed += 1
            self.errors.append(f"{message} (expected={expected}, actual={actual})")
            print(f"  [FAIL] {message} (expected={expected}, actual={actual})")

    def summary(self):
        total = self.passed + self.failed
        print("\n" + "=" * 60)
        print(f"  테스트 결과: {self.passed}/{total} 통과")
        if self.errors:
            print(f"\n  실패 목록:")
            for err in self.errors:
                print(f"    - {err}")
        print("=" * 60)
        return self.failed == 0


# ── 테스트용 임시 데이터 디렉토리 설정 ──

def setup_temp_storage():
    """테스트용 임시 저장소 설정"""
    temp_dir = tempfile.mkdtemp(prefix="cise_test_")
    storage.DATA_DIR = temp_dir
    storage.NOTES_FILE = os.path.join(temp_dir, "notes.json")
    storage.QUIZ_FILE = os.path.join(temp_dir, "quiz.json")
    storage.STATS_FILE = os.path.join(temp_dir, "stats.json")
    return temp_dir


def cleanup_temp_storage(temp_dir):
    """임시 저장소 정리"""
    shutil.rmtree(temp_dir, ignore_errors=True)


# ── 테스트 케이스 ──

def test_models(runner: TestRunner):
    """데이터 모델 테스트"""
    print("\n--- 데이터 모델 테스트 ---")

    # CATEGORIES 검증
    runner.assert_equal(len(CATEGORIES), 5, "시험 과목 5개 존재")
    runner.assert_true("시스템 보안" in CATEGORIES.values(), "시스템 보안 과목 존재")
    runner.assert_true("네트워크 보안" in CATEGORIES.values(), "네트워크 보안 과목 존재")
    runner.assert_true("어플리케이션 보안" in CATEGORIES.values(), "어플리케이션 보안 과목 존재")
    runner.assert_true("정보보안 일반" in CATEGORIES.values(), "정보보안 일반 과목 존재")
    runner.assert_true("정보보안 관리 및 법규" in CATEGORIES.values(), "정보보안 관리 및 법규 과목 존재")

    # SUBCATEGORIES 검증
    for cat in CATEGORIES.values():
        runner.assert_true(cat in SUBCATEGORIES, f"'{cat}' 세부 주제 존재")
        runner.assert_true(len(SUBCATEGORIES[cat]) > 0, f"'{cat}' 세부 주제 1개 이상")

    # StudyNote 생성
    note = StudyNote(
        title="테스트 노트",
        category="시스템 보안",
        subcategory="리눅스/유닉스 보안",
        content="테스트 내용입니다.",
        keywords=["테스트", "보안"],
        importance=4,
    )
    runner.assert_equal(note.title, "테스트 노트", "노트 제목 설정")
    runner.assert_equal(note.importance, 4, "노트 중요도 설정")
    runner.assert_equal(note.mastered, False, "노트 기본 상태 학습중")
    runner.assert_true(len(note.note_id) > 0, "노트 ID 자동 생성")

    # to_dict / from_dict 변환
    note_dict = note.to_dict()
    restored = StudyNote.from_dict(note_dict)
    runner.assert_equal(restored.title, note.title, "노트 직렬화/역직렬화 - 제목")
    runner.assert_equal(restored.note_id, note.note_id, "노트 직렬화/역직렬화 - ID")
    runner.assert_equal(restored.keywords, note.keywords, "노트 직렬화/역직렬화 - 키워드")

    # summary 출력
    summary = note.summary()
    runner.assert_true("테스트 노트" in summary, "노트 요약에 제목 포함")
    runner.assert_true("시스템 보안" in summary, "노트 요약에 과목 포함")

    # QuizQuestion 생성
    quiz = QuizQuestion(
        question="테스트 문제",
        answer="정답",
        category="정보보안 일반",
        choices=["오답1", "정답", "오답2", "오답3"],
        explanation="해설입니다.",
    )
    runner.assert_equal(quiz.question, "테스트 문제", "퀴즈 문제 설정")
    runner.assert_equal(quiz.accuracy, 0.0, "퀴즈 초기 정답률 0%")

    quiz.correct_count = 3
    quiz.wrong_count = 1
    runner.assert_equal(quiz.accuracy, 75.0, "퀴즈 정답률 계산 (75%)")

    # 퀴즈 직렬화
    quiz_dict = quiz.to_dict()
    restored_quiz = QuizQuestion.from_dict(quiz_dict)
    runner.assert_equal(restored_quiz.question, quiz.question, "퀴즈 직렬화/역직렬화")


def test_storage_notes(runner: TestRunner):
    """노트 저장소 테스트"""
    print("\n--- 노트 저장소 테스트 ---")

    # 빈 상태 확인
    notes = storage.get_all_notes()
    runner.assert_equal(len(notes), 0, "초기 노트 0개")

    # 노트 추가
    note1 = StudyNote(
        title="암호학 기초",
        category="정보보안 일반",
        subcategory="암호학",
        content="대칭키와 비대칭키 암호화의 차이점",
        keywords=["암호학", "대칭키", "비대칭키"],
        importance=5,
    )
    storage.save_note(note1)

    note2 = StudyNote(
        title="SQL Injection",
        category="어플리케이션 보안",
        subcategory="웹 보안",
        content="SQL Injection 공격 유형과 방어 방법",
        keywords=["SQL", "웹공격", "OWASP"],
        importance=4,
    )
    storage.save_note(note2)

    note3 = StudyNote(
        title="방화벽 종류",
        category="네트워크 보안",
        subcategory="방화벽",
        content="패킷 필터링, 상태기반 검사, 어플리케이션 게이트웨이",
        keywords=["방화벽", "패킷필터링"],
        importance=3,
    )
    storage.save_note(note3)

    # 전체 조회
    all_notes = storage.get_all_notes()
    runner.assert_equal(len(all_notes), 3, "노트 3개 저장 확인")

    # 과목별 조회
    sec_notes = storage.get_notes_by_category("정보보안 일반")
    runner.assert_equal(len(sec_notes), 1, "정보보안 일반 노트 1개")

    app_notes = storage.get_notes_by_category("어플리케이션 보안")
    runner.assert_equal(len(app_notes), 1, "어플리케이션 보안 노트 1개")

    # 검색
    results = storage.search_notes("암호")
    runner.assert_equal(len(results), 1, "키워드 '암호' 검색 결과 1개")
    runner.assert_equal(results[0].title, "암호학 기초", "검색 결과 제목 일치")

    results = storage.search_notes("SQL")
    runner.assert_equal(len(results), 1, "키워드 'SQL' 검색 결과 1개")

    results = storage.search_notes("방화벽")
    runner.assert_true(len(results) >= 1, "키워드 '방화벽' 검색 결과 1개 이상")

    # ID로 조회
    found = storage.get_note_by_id(note1.note_id)
    runner.assert_true(found is not None, "ID로 노트 조회 성공")
    runner.assert_equal(found.title, "암호학 기초", "ID 조회 제목 일치")

    not_found = storage.get_note_by_id("nonexist")
    runner.assert_true(not_found is None, "존재하지 않는 ID 조회 None")

    # 노트 수정 (업데이트)
    note1.importance = 3
    note1.mastered = True
    storage.save_note(note1)
    updated = storage.get_note_by_id(note1.note_id)
    runner.assert_equal(updated.importance, 3, "노트 수정 - 중요도 변경")
    runner.assert_equal(updated.mastered, True, "노트 수정 - 학습완료 변경")

    # 노트 삭제
    deleted = storage.delete_note(note2.note_id)
    runner.assert_true(deleted, "노트 삭제 성공")
    remaining = storage.get_all_notes()
    runner.assert_equal(len(remaining), 2, "삭제 후 노트 2개")

    not_deleted = storage.delete_note("nonexist")
    runner.assert_true(not not_deleted, "존재하지 않는 노트 삭제 실패")


def test_storage_quiz(runner: TestRunner):
    """퀴즈 저장소 테스트"""
    print("\n--- 퀴즈 저장소 테스트 ---")

    quizzes = storage.get_all_quizzes()
    runner.assert_equal(len(quizzes), 0, "초기 퀴즈 0개")

    quiz1 = QuizQuestion(
        question="AES의 블록 크기는?",
        answer="128비트",
        category="정보보안 일반",
        choices=["64비트", "128비트", "256비트"],
    )
    storage.save_quiz(quiz1)

    quiz2 = QuizQuestion(
        question="IDS와 IPS의 차이점은?",
        answer="차단 기능",
        category="네트워크 보안",
        choices=["속도", "차단 기능", "위치"],
    )
    storage.save_quiz(quiz2)

    all_quizzes = storage.get_all_quizzes()
    runner.assert_equal(len(all_quizzes), 2, "퀴즈 2개 저장 확인")

    cat_quizzes = storage.get_quizzes_by_category("정보보안 일반")
    runner.assert_equal(len(cat_quizzes), 1, "정보보안 일반 퀴즈 1개")

    # 퀴즈 결과 업데이트
    quiz1.correct_count = 5
    quiz1.wrong_count = 2
    storage.save_quiz(quiz1)
    updated = storage.get_all_quizzes()
    q1 = [q for q in updated if q.question_id == quiz1.question_id][0]
    runner.assert_equal(q1.correct_count, 5, "퀴즈 정답 수 업데이트")


def test_stats(runner: TestRunner):
    """학습 통계 테스트"""
    print("\n--- 학습 통계 테스트 ---")

    stats = storage.get_stats()
    runner.assert_true("total_notes" in stats, "통계에 total_notes 포함")
    runner.assert_true("mastered_notes" in stats, "통계에 mastered_notes 포함")
    runner.assert_true("total_quizzes" in stats, "통계에 total_quizzes 포함")
    runner.assert_true("category_stats" in stats, "통계에 category_stats 포함")
    runner.assert_true("quiz_stats" in stats, "통계에 quiz_stats 포함")
    runner.assert_true(stats["total_notes"] >= 0, "노트 수 0 이상")
    runner.assert_true(stats["total_quizzes"] >= 0, "퀴즈 수 0 이상")


def test_sample_data(runner: TestRunner):
    """샘플 데이터 테스트"""
    print("\n--- 샘플 데이터 테스트 ---")

    from sample_data import SAMPLE_NOTES, SAMPLE_QUIZZES

    runner.assert_true(len(SAMPLE_NOTES) >= 5, f"샘플 노트 5개 이상 ({len(SAMPLE_NOTES)}개)")
    runner.assert_true(len(SAMPLE_QUIZZES) >= 5, f"샘플 퀴즈 5개 이상 ({len(SAMPLE_QUIZZES)}개)")

    # 모든 과목이 샘플에 포함되어 있는지 확인
    note_categories = set(n.category for n in SAMPLE_NOTES)
    for cat in CATEGORIES.values():
        runner.assert_true(cat in note_categories, f"샘플 노트에 '{cat}' 과목 포함")

    # 샘플 데이터 저장 테스트
    for note in SAMPLE_NOTES:
        storage.save_note(note)
    for quiz in SAMPLE_QUIZZES:
        storage.save_quiz(quiz)

    loaded_notes = storage.get_all_notes()
    runner.assert_true(len(loaded_notes) >= len(SAMPLE_NOTES), "샘플 노트 저장 확인")

    loaded_quizzes = storage.get_all_quizzes()
    runner.assert_true(len(loaded_quizzes) >= len(SAMPLE_QUIZZES), "샘플 퀴즈 저장 확인")


def test_json_persistence(runner: TestRunner):
    """JSON 파일 영속성 테스트"""
    print("\n--- JSON 영속성 테스트 ---")

    note = StudyNote(
        title="영속성 테스트",
        category="시스템 보안",
        content="데이터가 파일에 올바르게 저장되는지 확인",
    )
    storage.save_note(note)

    # 파일이 존재하는지 확인
    runner.assert_true(os.path.exists(storage.NOTES_FILE), "notes.json 파일 존재")

    # 파일 내용이 유효한 JSON인지 확인
    with open(storage.NOTES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    runner.assert_true(isinstance(data, list), "notes.json이 JSON 배열")
    runner.assert_true(len(data) > 0, "notes.json에 데이터 존재")

    # 한글이 올바르게 저장되는지 확인
    raw = open(storage.NOTES_FILE, "r", encoding="utf-8").read()
    runner.assert_true("영속성 테스트" in raw, "한글 데이터 올바르게 저장 (ensure_ascii=False)")


# ── 메인 실행 ──

def main():
    print("=" * 60)
    print("  정보보안기사(CISE) 공부자료 정리 봇 - 자동화 테스트")
    print("=" * 60)

    runner = TestRunner()
    temp_dir = setup_temp_storage()

    try:
        test_models(runner)

        # 저장소 테스트마다 임시 디렉토리 초기화
        cleanup_temp_storage(temp_dir)
        temp_dir = setup_temp_storage()
        test_storage_notes(runner)

        cleanup_temp_storage(temp_dir)
        temp_dir = setup_temp_storage()
        test_storage_quiz(runner)

        cleanup_temp_storage(temp_dir)
        temp_dir = setup_temp_storage()
        test_stats(runner)

        cleanup_temp_storage(temp_dir)
        temp_dir = setup_temp_storage()
        test_sample_data(runner)

        cleanup_temp_storage(temp_dir)
        temp_dir = setup_temp_storage()
        test_json_persistence(runner)

    finally:
        cleanup_temp_storage(temp_dir)

    success = runner.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
