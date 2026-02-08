"""
정보보안기사(CISE) 공부자료 정리 봇 - 핵심 로직
CLI 기반 인터랙티브 봇
"""

from datetime import datetime
from typing import Optional

from models import StudyNote, QuizQuestion, CATEGORIES, SUBCATEGORIES
import storage
from quiz import run_quiz


def clear_screen():
    print("\n" * 2)


def print_header(title: str):
    width = 60
    print("=" * width)
    print(f"  {title}")
    print("=" * width)


def print_separator():
    print("-" * 60)


def show_main_menu():
    print_header("정보보안기사(CISE) 공부자료 정리 봇")
    print()
    print("  [1] 공부 노트 추가")
    print("  [2] 노트 목록 보기")
    print("  [3] 과목별 노트 보기")
    print("  [4] 노트 검색")
    print("  [5] 노트 상세 보기")
    print("  [6] 노트 수정")
    print("  [7] 노트 삭제")
    print("  [8] 퀴즈 풀기")
    print("  [9] 퀴즈 추가")
    print("  [10] 학습 통계")
    print("  [11] 과목 구조 보기")
    print("  [0] 종료")
    print()


def select_category() -> Optional[str]:
    """과목 선택"""
    print("\n  과목을 선택하세요:")
    for key, value in CATEGORIES.items():
        print(f"    [{key}] {value}")
    print("    [0] 취소")
    choice = input("\n  선택 > ").strip()
    if choice == "0":
        return None
    return CATEGORIES.get(choice)


def select_subcategory(category: str) -> str:
    """세부 주제 선택"""
    subs = SUBCATEGORIES.get(category, [])
    if not subs:
        return ""
    print(f"\n  [{category}] 세부 주제를 선택하세요:")
    for i, sub in enumerate(subs, 1):
        print(f"    [{i}] {sub}")
    print(f"    [0] 직접 입력")
    choice = input("\n  선택 > ").strip()
    if choice == "0":
        return input("  세부 주제 입력 > ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(subs):
            return subs[idx]
    except ValueError:
        pass
    return ""


def add_note():
    """새 공부 노트 추가"""
    print_header("공부 노트 추가")

    category = select_category()
    if not category:
        return

    subcategory = select_subcategory(category)

    title = input("\n  제목 > ").strip()
    if not title:
        print("  [!] 제목을 입력해주세요.")
        return

    print("  내용을 입력하세요 (빈 줄에서 Enter로 완료):")
    lines = []
    while True:
        line = input("  ")
        if line == "":
            break
        lines.append(line)
    content = "\n".join(lines)

    if not content:
        print("  [!] 내용을 입력해주세요.")
        return

    keywords_input = input("  키워드 (쉼표로 구분) > ").strip()
    keywords = [kw.strip() for kw in keywords_input.split(",") if kw.strip()]

    importance_input = input("  중요도 (1~5, 기본값 3) > ").strip()
    try:
        importance = int(importance_input)
        importance = max(1, min(5, importance))
    except ValueError:
        importance = 3

    note = StudyNote(
        title=title,
        category=category,
        subcategory=subcategory,
        content=content,
        keywords=keywords,
        importance=importance,
    )
    storage.save_note(note)
    print(f"\n  [OK] 노트가 저장되었습니다. (ID: {note.note_id})")


def list_notes():
    """전체 노트 목록"""
    print_header("전체 노트 목록")
    notes = storage.get_all_notes()
    if not notes:
        print("\n  등록된 노트가 없습니다.")
        return

    # 과목별로 그룹핑
    by_category = {}
    for note in notes:
        by_category.setdefault(note.category, []).append(note)

    for category, cat_notes in by_category.items():
        print(f"\n  [{category}] ({len(cat_notes)}개)")
        for note in cat_notes:
            print(f"    {note.summary()}")
    print(f"\n  총 {len(notes)}개의 노트")


def notes_by_category():
    """과목별 노트 보기"""
    print_header("과목별 노트 보기")
    category = select_category()
    if not category:
        return

    notes = storage.get_notes_by_category(category)
    if not notes:
        print(f"\n  [{category}]에 등록된 노트가 없습니다.")
        return

    print(f"\n  [{category}] 노트 목록 ({len(notes)}개)")
    print_separator()
    for note in notes:
        print(f"  {note.summary()}")


def search_notes():
    """노트 검색"""
    print_header("노트 검색")
    keyword = input("\n  검색어 > ").strip()
    if not keyword:
        return

    results = storage.search_notes(keyword)
    if not results:
        print(f"\n  '{keyword}'에 대한 검색 결과가 없습니다.")
        return

    print(f"\n  '{keyword}' 검색 결과 ({len(results)}개)")
    print_separator()
    for note in results:
        print(f"  {note.summary()}")


def view_note():
    """노트 상세 보기"""
    print_header("노트 상세 보기")
    note_id = input("\n  노트 ID > ").strip()
    note = storage.get_note_by_id(note_id)
    if not note:
        print(f"\n  [!] ID '{note_id}'에 해당하는 노트를 찾을 수 없습니다.")
        return

    # 복습 횟수 증가
    note.review_count += 1
    note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    storage.save_note(note)

    print()
    print_separator()
    print(f"  제목: {note.title}")
    print(f"  과목: {note.category} > {note.subcategory}")
    print(f"  중요도: {'*' * note.importance} ({note.importance}/5)")
    print(f"  키워드: {', '.join(note.keywords) if note.keywords else '없음'}")
    print(f"  상태: {'완료' if note.mastered else '학습중'}")
    print(f"  복습 횟수: {note.review_count}회")
    print(f"  생성일: {note.created_at}")
    print(f"  수정일: {note.updated_at}")
    print_separator()
    print(f"\n{note.content}\n")
    print_separator()

    # 학습 완료 토글
    toggle = input("  학습 완료 상태 변경? (y/n) > ").strip().lower()
    if toggle == "y":
        note.mastered = not note.mastered
        storage.save_note(note)
        status = "완료" if note.mastered else "학습중"
        print(f"  [OK] 상태가 '{status}'(으)로 변경되었습니다.")


def edit_note():
    """노트 수정"""
    print_header("노트 수정")
    note_id = input("\n  수정할 노트 ID > ").strip()
    note = storage.get_note_by_id(note_id)
    if not note:
        print(f"\n  [!] ID '{note_id}'에 해당하는 노트를 찾을 수 없습니다.")
        return

    print(f"\n  현재 제목: {note.title}")
    new_title = input("  새 제목 (Enter로 유지) > ").strip()
    if new_title:
        note.title = new_title

    print(f"\n  현재 내용:\n{note.content}")
    print("\n  새 내용 입력 (빈 줄에서 Enter로 완료, 바로 Enter로 유지):")
    first_line = input("  ")
    if first_line:
        lines = [first_line]
        while True:
            line = input("  ")
            if line == "":
                break
            lines.append(line)
        note.content = "\n".join(lines)

    print(f"\n  현재 키워드: {', '.join(note.keywords)}")
    new_keywords = input("  새 키워드 (쉼표 구분, Enter로 유지) > ").strip()
    if new_keywords:
        note.keywords = [kw.strip() for kw in new_keywords.split(",") if kw.strip()]

    new_importance = input(f"  새 중요도 (현재: {note.importance}, Enter로 유지) > ").strip()
    if new_importance:
        try:
            note.importance = max(1, min(5, int(new_importance)))
        except ValueError:
            pass

    note.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    storage.save_note(note)
    print("\n  [OK] 노트가 수정되었습니다.")


def delete_note():
    """노트 삭제"""
    print_header("노트 삭제")
    note_id = input("\n  삭제할 노트 ID > ").strip()
    note = storage.get_note_by_id(note_id)
    if not note:
        print(f"\n  [!] ID '{note_id}'에 해당하는 노트를 찾을 수 없습니다.")
        return

    print(f"\n  삭제할 노트: {note.title} ({note.category})")
    confirm = input("  정말 삭제하시겠습니까? (y/n) > ").strip().lower()
    if confirm == "y":
        storage.delete_note(note_id)
        print("  [OK] 노트가 삭제되었습니다.")
    else:
        print("  삭제가 취소되었습니다.")


def add_quiz():
    """퀴즈 문제 추가"""
    print_header("퀴즈 문제 추가")

    category = select_category()
    if not category:
        return

    question = input("\n  문제 > ").strip()
    if not question:
        print("  [!] 문제를 입력해주세요.")
        return

    print("  보기를 입력하세요 (최소 2개, 빈 줄에서 Enter로 완료):")
    choices = []
    idx = 1
    while True:
        choice = input(f"    {idx}. ").strip()
        if choice == "":
            if len(choices) < 2:
                print("  [!] 최소 2개의 보기가 필요합니다.")
                continue
            break
        choices.append(choice)
        idx += 1

    answer = input("  정답 (번호) > ").strip()
    try:
        answer_idx = int(answer) - 1
        if 0 <= answer_idx < len(choices):
            answer_text = choices[answer_idx]
        else:
            print("  [!] 올바른 번호를 입력해주세요.")
            return
    except ValueError:
        answer_text = answer

    explanation = input("  해설 (선택사항) > ").strip()

    quiz = QuizQuestion(
        question=question,
        answer=answer_text,
        category=category,
        choices=choices,
        explanation=explanation,
    )
    storage.save_quiz(quiz)
    print(f"\n  [OK] 퀴즈가 저장되었습니다. (ID: {quiz.question_id})")


def show_stats():
    """학습 통계 표시"""
    print_header("학습 통계")
    stats = storage.get_stats()

    print(f"\n  전체 노트: {stats['total_notes']}개")
    print(f"  학습 완료: {stats['mastered_notes']}개")
    if stats['total_notes'] > 0:
        pct = (stats['mastered_notes'] / stats['total_notes']) * 100
        print(f"  완료율: {pct:.1f}%")

    print(f"\n  등록된 퀴즈: {stats['total_quizzes']}개")

    qs = stats['quiz_stats']
    if qs['total'] > 0:
        acc = (qs['correct'] / qs['total']) * 100
        print(f"  퀴즈 정답률: {acc:.1f}% ({qs['correct']}/{qs['total']})")

    cat_stats = stats['category_stats']
    if cat_stats:
        print("\n  과목별 현황:")
        print_separator()
        for cat, cs in cat_stats.items():
            mastered_pct = (cs['mastered'] / cs['total'] * 100) if cs['total'] > 0 else 0
            print(
                f"  {cat}: {cs['total']}개 | "
                f"완료: {cs['mastered']}개 ({mastered_pct:.0f}%) | "
                f"총 복습: {cs['review_total']}회"
            )


def show_category_structure():
    """과목 구조 보기"""
    print_header("정보보안기사 시험 과목 구조")
    for key, category in CATEGORIES.items():
        subs = SUBCATEGORIES.get(category, [])
        print(f"\n  [{key}] {category}")
        for sub in subs:
            print(f"      - {sub}")


def run_bot():
    """메인 봇 루프"""
    print("\n  정보보안기사(CISE) 공부자료 정리 봇을 시작합니다!")
    print("  공부 노트를 체계적으로 관리하고 퀴즈로 복습하세요.\n")

    handlers = {
        "1": add_note,
        "2": list_notes,
        "3": notes_by_category,
        "4": search_notes,
        "5": view_note,
        "6": edit_note,
        "7": delete_note,
        "8": lambda: run_quiz(select_category),
        "9": add_quiz,
        "10": show_stats,
        "11": show_category_structure,
    }

    while True:
        show_main_menu()
        choice = input("  선택 > ").strip()

        if choice == "0":
            print("\n  공부 화이팅! 다음에 또 만나요!\n")
            break

        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except KeyboardInterrupt:
                print("\n  [!] 작업이 취소되었습니다.")
            except Exception as e:
                print(f"\n  [!] 오류가 발생했습니다: {e}")
        else:
            print("\n  [!] 올바른 메뉴를 선택해주세요.")

        input("\n  Enter를 눌러 계속...")
