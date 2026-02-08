import json
import os
import random
import uuid
import datetime

# ==========================================
# 🛡️ CISE 정보보안기사 대용량 지식 베이스
# ==========================================
KNOWLEDGE_DB = {
    "ATTACKS": {
        "DDoS": "서비스 가용성을 침해하는 분산 서비스 거부 공격",
        "SQL Injection": "입력값 검증 미흡을 이용한 DB 조작 공격",
        "XSS": "사용자 브라우저에서 실행되는 악성 스크립트 공격",
        "CSRF": "사용자 권한을 도용하여 비정상 요청을 실행하는 공격",
        "Ransomware": "파일 암호화 후 금전을 요구하는 악성코드",
        "APT": "지능적이고 지속적인 타겟형 위협 공격",
        "Phishing": "신뢰할 수 있는 기관을 사칭한 이메일 사기",
        "Sniffing": "네트워크 트래픽을 도청하는 수동적 공격",
        "Spoofing": "IP나 MAC 주소를 위변조하는 공격"
    },
    "PROTOCOLS": {
        "HTTP": 80, "HTTPS": 443, "FTP": 21, "SSH": 22, "Telnet": 23,
        "DNS": 53, "SMTP": 25, "SNMP": 161, "RDP": 3389, "POP3": 110,
        "IMAP": 143, "MySQL": 3306, "PostgreSQL": 5432
    },
    "LAWS": [
        "정보통신망법", "개인정보보호법", "정보통신기반보호법", "전자서명법", "클라우드컴퓨팅법"
    ],
    "CONCEPTS": {
        "기밀성(Confidentiality)": "인가된 사용자만 정보 접근 허용",
        "무결성(Integrity)": "정보의 무단 변조 방지",
        "가용성(Availability)": "필요 시 언제든 서비스 사용 가능",
        "인증(Authentication)": "사용자 신원 확인",
        "부인방지(Non-Repudiation)": "행위 사실을 부인할 수 없음"
    }
}

CATEGORIES = ["시스템 보안", "네트워크 보안", "어플리케이션 보안", "정보보안 일반", "정보보안 법규"]

def generate_quiz(idx):
    """랜덤 퀴즈 1개 생성"""
    q_type = random.randint(1, 4)
    quiz_id = str(uuid.uuid4())[:8]
    
    if q_type == 1: # 공격 유형
        atk, desc = random.choice(list(KNOWLEDGE_DB["ATTACKS"].items()))
        cat = "어플리케이션 보안" if atk in ["SQL Injection", "XSS"] else "네트워크 보안"
        question = f"다음 중 '{atk}' 공격의 특징으로 올바른 것은?"
        answer = desc
        options = [desc, "암호화 키를 탈취한다.", "물리적 장비를 파괴한다.", "DB 스키마를 삭제한다."]

    elif q_type == 2: # 포트
        proto, port = random.choice(list(KNOWLEDGE_DB["PROTOCOLS"].items()))
        cat = "네트워크 보안"
        question = f"프로토콜 {proto}의 기본 포트 번호는?"
        answer = str(port)
        options = [str(port), str(port+1), str(random.randint(1000,9000)), "8080"]

    elif q_type == 3: # 보안 요소
        con, desc = random.choice(list(KNOWLEDGE_DB["CONCEPTS"].items()))
        cat = "정보보안 일반"
        question = f"정보보안의 목표 중 '{con}'에 대한 설명은?"
        answer = desc
        options = [desc, "시스템 속도 향상", "하드웨어 비용 절감", "네트워크 대역폭 확장"]

    else: # 법규
        law = random.choice(KNOWLEDGE_DB["LAWS"])
        cat = "정보보안 법규"
        question = f"다음 중 정보보안 관련 법령에 해당하는 것은?"
        answer = law
        options = [law, "도로교통법", "건축법", "식품위생법"]

    random.shuffle(options)
    
    return {
        "id": quiz_id,
        "question": f"[문제 {idx}] {question}",
        "answer": answer,
        "category": cat,
        "options": options,
        "explanation": f"정답은 '{answer}' 입니다.",
        "correct_count": 0,
        "wrong_count": 0
    }

def initialize_data():
    """10,000개 데이터 생성 및 파일 저장"""
    # 저장 경로 설정 (절대 경로 사용)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    print(f"🚀 Generating 10,000 Knowledge Items in {data_dir}...")
    
    # 1. 퀴즈 10,000개 생성
    quizzes = [generate_quiz(i) for i in range(1, 10001)]
    quiz_path = os.path.join(data_dir, 'quiz.json')
    
    with open(quiz_path, 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)
    
    # 2. 노트 1,000개 생성
    notes = []
    for i in range(1, 1001):
        cat = random.choice(CATEGORIES)
        notes.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"[{cat}] 핵심요약 #{i}",
            "category": cat,
            "content": f"{cat} 과목 필수 암기 노트입니다.",
            "importance": random.randint(1,5),
            "tags": ["기출"],
            "created_at": datetime.datetime.now().isoformat(),
            "is_completed": False
        })
    
    note_path = os.path.join(data_dir, 'notes.json')
    with open(note_path, 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)
        
    print(f"✅ SUCCESS: Generated {len(quizzes)} Quizzes and {len(notes)} Notes.")

if __name__ == "__main__":
    initialize_data()
