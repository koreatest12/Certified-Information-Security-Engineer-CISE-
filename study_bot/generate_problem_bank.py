import json
import os
import random
import uuid
from datetime import datetime

# 데이터 저장 경로
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

# === 정보보안기사 지식 베이스 (Knowledge Base) ===
DB = {
    "SYSTEM": {
        "Topics": ["Linux 권한", "Windows 인증", "로그 분석", "RAID", "Inode", "SetUID"],
        "Attacks": ["Buffer Overflow", "Race Condition", "Format String", "Rootkit"]
    },
    "NETWORK": {
        "Topics": ["OSI 7 Layer", "TCP/IP", "VPN", "Firewall", "IDS/IPS", "NAC"],
        "Attacks": ["Syn Flooding", "Spoofing", "Sniffing", "Session Hijacking", "DDoS"]
    },
    "APP": {
        "Topics": ["SDLC", "DB 보안", "암호화 알고리즘", "전자서명", "PKI"],
        "Attacks": ["SQL Injection", "XSS", "CSRF", "Web Shell", "File Upload"]
    },
    "GENERAL": {
        "Topics": ["접근통제 모델(MAC/DAC/RBAC)", "보안 3요소", "재해복구(DRS)", "BCP"],
        "Attacks": ["Social Engineering", "APT", "Ransomware"]
    },
    "LAW": {
        "Topics": ["정보통신망법", "개인정보보호법", "기반보호법", "ISMS-P 인증", "CISO 지정"],
        "Attacks": ["Compliance 위반", "개인정보 유출"]
    }
}

def generate_10k_bank():
    print(f"🏭 Generating 10,000 Problem Bank Items in {DATA_DIR}...")
    
    quizzes = []
    # 10,000 문제 생성
    for i in range(1, 10001):
        cat = random.choice(list(DB.keys()))
        topic = random.choice(DB[cat]["Topics"])
        attack = random.choice(DB[cat]["Attacks"])
        
        q = {
            "id": str(uuid.uuid4())[:8],
            "question": f"[{cat}] {topic} 환경에서 발생하는 '{attack}' 공격의 대응 방안으로 적절한 것은? (문제은행 #{i})",
            "answer": "보안 설정 강화 및 최신 패치 적용",
            "category": cat,
            "options": ["보안 설정 강화", "시스템 재부팅", "로그 삭제", "네트워크 차단"],
            "explanation": f"{attack} 공격은 {topic}의 취약점을 이용하므로 근본적인 패치가 필요합니다.",
            "correct_count": 0,
            "wrong_count": 0
        }
        quizzes.append(q)

    # 퀴즈 파일 저장
    with open(os.path.join(DATA_DIR, 'quiz.json'), 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)

    # 노트 1,000개 생성
    notes = []
    for i in range(1, 1001):
        cat = random.choice(list(DB.keys()))
        notes.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"[{cat}] 기출 핵심 요약 #{i}",
            "category": cat,
            "content": f"{cat} 과목 필수 암기 사항입니다.",
            "importance": random.randint(3, 5),
            "created_at": datetime.now().isoformat(),
            "is_completed": False
        })

    # 노트 파일 저장
    with open(os.path.join(DATA_DIR, 'notes.json'), 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {len(quizzes)} Quizzes and {len(notes)} Notes.")

if __name__ == "__main__":
    generate_10k_bank()
