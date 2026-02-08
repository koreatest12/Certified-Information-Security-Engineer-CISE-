"""
정보보안기사(CISE) 공부자료 정리 봇 - 퀴즈 기능
"""

import random
from typing import Callable, Optional

import storage
from models import CATEGORIES


def run_quiz(select_category_fn: Callable):
    """퀴즈 모드 실행"""
    print("\n" + "=" * 60)
    print("  퀴즈 모드")
    print("=" * 60)

    print("\n  퀴즈 범위를 선택하세요:")
    print("    [0] 전체 과목")
    for key, value in CATEGORIES.items():
        print(f"    [{key}] {value}")

    choice = input("\n  선택 > ").strip()

    if choice == "0":
        quizzes = storage.get_all_quizzes()
    elif choice in CATEGORIES:
        quizzes = storage.get_quizzes_by_category(CATEGORIES[choice])
    else:
        print("  [!] 올바른 선택이 아닙니다.")
        return

    if not quizzes:
        print("\n  등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가해주세요.")
        return

    print(f"\n  총 {len(quizzes)}개의 문제가 있습니다.")
    count_input = input("  몇 문제를 풀겠습니까? (Enter = 전체) > ").strip()
    try:
        count = int(count_input) if count_input else len(quizzes)
        count = min(count, len(quizzes))
    except ValueError:
        count = len(quizzes)

    # 문제 섞기
    selected = random.sample(quizzes, count)

    correct = 0
    wrong = 0

    for i, quiz in enumerate(selected, 1):
        print(f"\n  --- 문제 {i}/{count} [{quiz.category}] ---")
        print(f"\n  Q. {quiz.question}\n")

        if quiz.choices:
            # 객관식
            for j, choice_text in enumerate(quiz.choices, 1):
                print(f"    {j}. {choice_text}")

            user_answer = input("\n  정답 (번호) > ").strip()
            try:
                answer_idx = int(user_answer) - 1
                if 0 <= answer_idx < len(quiz.choices):
                    user_answer_text = quiz.choices[answer_idx]
                else:
                    user_answer_text = user_answer
            except ValueError:
                user_answer_text = user_answer

            is_correct = user_answer_text == quiz.answer
        else:
            # 주관식
            user_answer = input("\n  정답 > ").strip()
            is_correct = user_answer.lower() == quiz.answer.lower()

        if is_correct:
            print("\n  [O] 정답입니다!")
            correct += 1
            quiz.correct_count += 1
        else:
            print(f"\n  [X] 오답입니다. 정답: {quiz.answer}")
            wrong += 1
            quiz.wrong_count += 1

        if quiz.explanation:
            print(f"  해설: {quiz.explanation}")

        # 결과 저장
        storage.save_quiz(quiz)

    # 결과 요약
    print("\n" + "=" * 60)
    print("  퀴즈 결과")
    print("=" * 60)
    total = correct + wrong
    accuracy = (correct / total * 100) if total > 0 else 0
    print(f"\n  총 문제: {total}")
    print(f"  정답: {correct}개")
    print(f"  오답: {wrong}개")
    print(f"  정답률: {accuracy:.1f}%")

    if accuracy == 100:
        print("\n  완벽합니다!")
    elif accuracy >= 80:
        print("\n  잘하고 있습니다! 조금만 더 복습하세요.")
    elif accuracy >= 60:
        print("\n  합격 수준에 가까워지고 있습니다. 꾸준히 복습하세요.")
    else:
        print("\n  더 많은 복습이 필요합니다. 노트를 다시 확인해보세요.")
