import json
import random
import os
import datetime

# ==========================================
# 🤖 AI 수험생 설정 (AI Persona)
# ==========================================
AI_PROFILE = {
    "name": "CISE_Alpha_Bot",
    "version": "v2.0",
    "strengths": ["네트워크 보안", "어플리케이션 보안"], # 강점 과목 (정답률 높음)
    "weaknesses": ["정보보안 법규"],                   # 약점 과목 (정답률 낮음)
}

def load_data():
    """문제은행 데이터 로드"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'quiz.json')
    
    if not os.path.exists(data_path):
        print(f"❌ Error: Data file not found at {data_path}")
        return []
        
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def solve_question(question):
    """AI가 문제를 푸는 로직 (확률 기반 시뮬레이션)"""
    category = question.get('category', 'General')
    
    # 기본 정답률 75%
    accuracy = 0.75
    
    # 강점 과목은 95%, 약점 과목은 50% 확률로 정답
    if category in AI_PROFILE["strengths"]:
        accuracy = 0.95
    elif category in AI_PROFILE["weaknesses"]:
        accuracy = 0.50
        
    # 시뮬레이션 실행
    is_correct = random.random() < accuracy
    
    # AI의 답변 도출
    if is_correct:
        selected_answer = question['answer']
        reasoning = f"✅ [AI 분석] '{category}' 분야 지식에 기반하여 정답을 확신합니다."
    else:
        # 오답 중 하나를 랜덤 선택
        options = question.get('options', [])
        wrong_options = [o for o in options if o != question['answer']]
        selected_answer = random.choice(wrong_options) if wrong_options else "모름"
        reasoning = f"❌ [AI 혼란] 이 문제는 '{category}' 분야의 심화 내용이라 헷갈립니다."

    return {
        "id": question['id'],
        "question": question['question'],
        "category": category,
        "ai_answer": selected_answer,
        "correct_answer": question['answer'],
        "is_correct": is_correct,
        "reasoning": reasoning
    }

def generate_report(results):
    """AI 분석 리포트 생성 (Markdown)"""
    total = len(results)
    correct = sum(1 for r in results if r['is_correct'])
    score = (correct / total) * 100
    
    # 과목별 분석
    cat_stats = {}
    for r in results:
        cat = r['category']
        if cat not in cat_stats:
            cat_stats[cat] = {"total": 0, "correct": 0}
        cat_stats[cat]["total"] += 1
        if r['is_correct']:
            cat_stats[cat]["correct"] += 1

    # 리포트 작성
    report = f"""# 🤖 AI 모의고사 분석 리포트
**실행 일시:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**응시 모델:** {AI_PROFILE['name']} ({AI_PROFILE['version']})

## 📊 종합 결과
- **총 문제 수:** {total}문항
- **정답 수:** {correct}문항
- **최종 점수:** **{score:.1f}점**
- **판정:** {'🎉 **합격 (PASS)**' if score >= 60 else '⚠️ **불합격 (FAIL)**'}

## 📈 과목별 성취도
| 과목명 | 문제 수 | 정답 수 | 정답률 | 상태 |
| :--- | :---: | :---: | :---: | :---: |
"""
    
    for cat, stat in cat_stats.items():
        rate = (stat['correct'] / stat['total']) * 100
        status = "🟢 우수" if rate >= 80 else ("🔴 위험" if rate < 60 else "🟡 보통")
        report += f"| {cat} | {stat['total']} | {stat['correct']} | {rate:.1f}% | {status} |\n"

    report += "\n## 📝 AI 오답 노트 (일부 발췌)\n"
    wrong_answers = [r for r in results if not r['is_correct']][:5] # 5개만 표시
    
    if not wrong_answers:
        report += "- 오답이 없습니다! 완벽합니다. 🎉\n"
    else:
        for w in wrong_answers:
            report += f"- **[Q]** {w['question']}\n"
            report += f"  - 🤖 AI 답: {w['ai_answer']}\n"
            report += f"  - ✅ 정답: {w['correct_answer']}\n"
            report += f"  - 💡 원인: {w['reasoning']}\n\n"

    return report

def main():
    print("🤖 Starting AI Quiz Solver...")
    
    # 1. 데이터 로드
    quizzes = load_data()
    if not quizzes:
        return

    # 2. 모의고사 구성 (랜덤 100문제)
    exam_questions = random.sample(quizzes, 100)
    
    # 3. AI 풀이 실행
    results = [solve_question(q) for q in exam_questions]
    
    # 4. 리포트 생성 및 저장
    report_content = generate_report(results)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(base_dir, 'ai_exam_report.md')
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"✅ AI Exam Finished. Report saved to: {report_path}")

if __name__ == "__main__":
    main()
