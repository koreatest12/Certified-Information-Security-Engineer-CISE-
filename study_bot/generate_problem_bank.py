import json, os, random, uuid
def generate():
    os.makedirs('study_bot/data', exist_ok=True)
    quizzes = []
    cats = ["시스템 보안", "네트워크 보안", "어플리케이션 보안", "정보보안 일반", "정보보안 법규"]
    for i in range(1, 10001):
        c = random.choice(cats)
        quizzes.append({
            "id": str(uuid.uuid4())[:8],
            "question": f"[{c}] AI 테스트용 문제 #{i}",
            "answer": "정답",
            "category": c,
            "options": ["정답", "오답1", "오답2"]
        })
    with open('study_bot/data/quiz.json', 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(quizzes)} quizzes.")
if __name__ == "__main__": generate()
