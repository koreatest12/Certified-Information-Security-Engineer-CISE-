import json, random, os, datetime

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_dir, 'data', 'quiz.json')
    if not os.path.exists(data_path): return
    
    with open(data_path, 'r', encoding='utf-8') as f: quizzes = json.load(f)
    
    # 100문제 풀이 시뮬레이션
    score = 0
    results = []
    # 매번 다른 문제를 풀도록 랜덤 샘플링
    for q in random.sample(quizzes, 100):
        is_correct = random.random() < 0.8 # 80% 정답률 시뮬레이션
        if is_correct: score += 1
        results.append(f"- {q['question']} -> {'✅' if is_correct else '❌'}")
    
    # 리포트 생성 (시간 포함)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    report = f"# 🤖 AI Exam Report\n**Run Time:** {now}\n**Score:** {score}/100\n\n## Details\n" + "\n".join(results[:10])
    
    with open(os.path.join(base_dir, 'ai_exam_report.md'), 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"AI Report Generated. Score: {score}")

if __name__ == "__main__": main()
