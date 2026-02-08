import json, random, os, datetime

# (위 Python 코드 전체 내용이 여기에 들어갑니다. 편의상 핵심 로직만 삽입)
def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'quiz.json')
    if not os.path.exists(data_path): return
    
    with open(data_path, 'r', encoding='utf-8') as f: quizzes = json.load(f)
    
    # 100문제 풀이 시뮬레이션
    score = 0
    results = []
    for q in random.sample(quizzes, 100):
        is_correct = random.random() < 0.8 # 80% 정답률
        if is_correct: score += 1
        results.append(f"- {q['question']} -> {'✅' if is_correct else '❌'}")
    
    report = f"# 🤖 AI Exam Report\n**Score:** {score}/100\n\n## Details\n" + "\n".join(results[:10])
    
    with open(os.path.join(base_dir, 'ai_exam_report.md'), 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"AI Report Generated. Score: {score}")

if __name__ == "__main__": main()
