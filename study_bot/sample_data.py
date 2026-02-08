import json
import os
import random
import uuid
import datetime

# ==========================================
# 🛡️ 정보보안기사 핵심 지식 베이스 (Knowledge Base)
# ==========================================
KNOWLEDGE_BASE = {
    "ATTACKS": {
        "DDoS": "시스템의 가용성을 침해하여 서비스를 마비시키는 공격",
        "SQL Injection": "입력값 검증 미흡을 이용해 DB를 조작하는 공격",
        "XSS": "사용자의 브라우저에서 악성 스크립트를 실행하는 공격",
        "Ransomware": "파일을 암호화하여 금전을 요구하는 악성코드",
        "APT": "지능적이고 지속적인 위협 공격",
        "CSRF": "사용자의 의지와 무관하게 공격자가 의도한 행위를 하게 만드는 공격",
        "Buffer Overflow": "메모리 경계를 벗어나 데이터를 덮어쓰는 공격",
        "Sniffing": "네트워크 트래픽을 도청하는 수동적 공격"
    },
    "PROTOCOLS": {
        "HTTP": 80, "HTTPS": 443, "FTP": 21, "SSH": 22,
        "Telnet": 23, "DNS": 53, "SMTP": 25, "SNMP": 161,
        "RDP": 3389, "POP3": 110
    },
    "LAWS": [
        "정보통신망법", "개인정보보호법", "정보통신기반보호법", "전자서명법", "클라우드발전법"
    ],
    "CONCEPTS": {
        "기밀성": "인가된 사용자만 정보에 접근 가능함",
        "무결성": "정보가 비인가된 방식으로 변경되지 않음",
        "가용성": "필요할 때 언제든지 서비스를 사용할 수 있음",
        "인증": "사용자의 신원을 검증하는 절차",
        "부인방지": "송수신 사실을 부인할 수 없게 함"
    }
}

CATEGORIES = ["시스템 보안", "네트워크 보안", "어플리케이션 보안", "정보보안 일반", "정보보안 법규"]

# ==========================================
# 🏭 데이터 생성 로직 (Data Generator)
# ==========================================
def generate_quiz_question(idx):
    """지식 베이스를 조합하여 랜덤 퀴즈 생성"""
    q_type = random.randint(1, 4)
    quiz_id = str(uuid.uuid4())[:8]
    
    # 1. 공격 유형 문제
    if q_type == 1:
        atk, desc = random.choice(list(KNOWLEDGE_BASE["ATTACKS"].items()))
        category = random.choice(["시스템 보안", "어플리케이션 보안"])
        question = f"다음 중 '{atk}' 공격에 대한 설명으로 가장 적절한 것은?"
        answer = desc
        options = [
            desc,
            "네트워크 대역폭을 고갈시키는 공격이다.",
            "암호화 키를 탈취하는 공격이다.",
            "사용자 세션을 가로채는 공격이다."
        ]
    
    # 2. 포트/프로토콜 문제
    elif q_type == 2:
        proto, port = random.choice(list(KNOWLEDGE_BASE["PROTOCOLS"].items()))
        category = "네트워크 보안"
        question = f"프로토콜 {proto}의 기본 포트 번호(Default Port)는 무엇인가?"
        answer = str(port)
        options = [str(port), str(port+1), str(port+80), str(random.randint(1000, 9000))]

    # 3. 보안 3요소 및 개념 문제
    elif q_type == 3:
        concept, desc = random.choice(list(KNOWLEDGE_BASE["CONCEPTS"].items()))
        category = "정보보안 일반"
        question = f"정보보안의 목표 중 '{concept}'에 대한 설명은?"
        answer = desc
        options = [desc, "시스템의 속도를 향상시킴", "비용을 절감함", "하드웨어를 보호함"]

    # 4. 법규 문제
    else:
        law = random.choice(KNOWLEDGE_BASE["LAWS"])
        category = "정보보안 법규"
        question = f"다음 중 대한민국 정보보안 관련 법령에 해당하지 않는 것은?" # 역설적 질문 생성
        answer = "도로교통법"
        options = [law, "정보통신망법", "개인정보보호법", "도로교통법"]

    # 보기 섞기
    random.shuffle(options)

    return {
        "id": quiz_id,
        "question": f"[Q{idx}] {question}",
        "answer": answer,
        "category": category,
        "options": options,
        "explanation": f"이 문제는 {category}의 핵심 개념인 {answer}에 대해 다룹니다.",
        "correct_count": 0,
        "wrong_count": 0
    }

def generate_study_note(idx):
    """학습 노트 생성"""
    category = random.choice(CATEGORIES)
    return {
        "id": str(uuid.uuid4())[:8],
        "title": f"[{category}] 핵심 요약 정리 #{idx}",
        "category": category,
        "content": f"제{idx}강: {category} 분야의 필수 암기 사항입니다. 보안 기사 실기 대비용.",
        "importance": random.randint(1, 5),
        "tags": ["기출", "핵심", "암기"],
        "created_at": datetime.datetime.now().isoformat(),
        "is_completed": random.choice([True, False]),
        "review_count": random.randint(0, 5)
    }

def initialize_data():
    """데이터 파일 생성 및 대량 데이터 주입"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    os.makedirs(data_dir, exist_ok=True)
    
    # 1. 퀴즈 데이터 생성 (9,999개)
    print("🚀 Generating 9,999 Knowledge Quizzes...")
    quizzes = [generate_quiz_question(i) for i in range(1, 10000)]
    
    quiz_path = os.path.join(data_dir, 'quiz.json')
    with open(quiz_path, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved to {quiz_path}")

    # 2. 학습 노트 생성 (1,000개)
    print("🚀 Generating 1,000 Study Notes...")
    notes = [generate_study_note(i) for i in range(1, 1001)]
    
    note_path = os.path.join(data_dir, 'notes.json')
    with open(note_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved to {note_path}")

if __name__ == "__main__":
    initialize_data()
