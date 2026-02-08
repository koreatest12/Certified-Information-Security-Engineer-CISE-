import json
import os
import random
import uuid
import datetime

# ==========================================
# 📚 정보보안기사 문제은행 데이터베이스 (DB)
# ==========================================
KNOWLEDGE_DB = {
    "SYSTEM": {
        "Linux_Commands": ["chmod", "chown", "umask", "passwd", "ls -al", "ps -ef", "netstat", "tcpdump"],
        "Log_Files": ["/var/log/messages", "/var/log/secure", "/var/log/auth.log", "wtmp", "btmp", "lastlog"],
        "Concepts": ["SetUID", "Sticky Bit", "Inode", "Race Condition", "Buffer Overflow"]
    },
    "NETWORK": {
        "Attacks": ["Syn Flooding", "UDP Flooding", "Smurf", "Land Attack", "TearDrop", "ARP Spoofing", "Session Hijacking"],
        "Protocols": ["HTTP/HTTPS", "FTP", "SMTP", "SNMP", "DNS", "SSH", "Telnet", "ICMP"],
        "Devices": ["Firewall", "IDS", "IPS", "WAF", "VPN", "NAC", "Router"]
    },
    "APP": {
        "OWASP": ["SQL Injection", "XSS", "CSRF", "Broken Auth", "Security Misconfiguration", "Sensitive Data Exposure"],
        "DB": ["Confidentiality", "Integrity", "Availability", "Trigger", "View", "Encryption"]
    },
    "GENERAL": {
        "Crypto": ["Symmetric Key", "Public Key", "Hash Function", "Digital Signature", "PKI", "Access Control"],
        "Model": ["Bell-LaPadula", "Biba", "Clark-Wilson", "RBAC", "DAC", "MAC"]
    },
    "LAW": {
        "Acts": ["정보통신망법", "개인정보보호법", "정보통신기반보호법", "전자서명법", "클라우드컴퓨팅법"],
        "Terms": ["CISO", "CPO", "ISMS-P", "PIA", "CC인증"]
    }
}

def generate_question(idx):
    """문제은행 알고리즘을 통한 퀴즈 생성"""
    q_type = random.choice(["SYSTEM", "NETWORK", "APP", "GENERAL", "LAW"])
    
    if q_type == "SYSTEM":
        item = random.choice(KNOWLEDGE_DB["SYSTEM"]["Linux_Commands"])
        question = f"[시스템보안] 리눅스 환경에서 '{item}' 명령어에 대한 설명으로 가장 적절한 것은?"
        answer = f"{item} 기능에 대한 정확한 설명입니다."
        options = [answer, "파일의 무결성을 검증한다.", "네트워크 연결 상태를 확인한다.", "사용자 계정을 삭제한다."]

    elif q_type == "NETWORK":
        item = random.choice(KNOWLEDGE_DB["NETWORK"]["Attacks"])
        question = f"[네트워크보안] 다음 중 '{item}' 공격의 특징과 대응 방안으로 올바른 것은?"
        answer = "출발지 IP 변조 여부를 확인한다."
        options = [answer, "입력값 검증을 수행한다.", "DB 암호화를 적용한다.", "물리적 접근을 통제한다."]

    elif q_type == "APP":
        item = random.choice(KNOWLEDGE_DB["APP"]["OWASP"])
        question = f"[어플리케이션보안] OWASP Top 10 중 '{item}' 취약점을 예방하기 위한 보안 대책은?"
        answer = "입력값에 대한 검증 및 필터링을 수행한다." if "Injection" in item else "보안 설정을 최신 상태로 유지한다."
        options = [answer, "네트워크 대역폭을 확장한다.", "백신 소프트웨어를 설치한다.", "불필요한 서비스를 비활성화한다."]

    elif q_type == "GENERAL":
        item = random.choice(KNOWLEDGE_DB["GENERAL"]["Model"])
        question = f"[정보보안일반] 접근통제 모델 중 '{item}'의 주요 특징은 무엇인가?"
        answer = "기밀성 보장을 최우선으로 한다." if "Bell" in item else "무결성 보장을 최우선으로 한다."
        options = [answer, "가용성을 최우선으로 한다.", "사용자의 편의성을 강조한다.", "비용 절감을 목표로 한다."]

    else: # LAW
        item = random.choice(KNOWLEDGE_DB["LAW"]["Acts"])
        question = f"[정보보안법규] '{item}'에 의거하여 침해사고 발생 시 신고해야 할 기관은?"
        answer = "한국인터넷진흥원(KISA) 또는 과학기술정보통신부"
        options = [answer, "경찰청 사이버수사대", "행정안전부", "국가정보원"]

    random.shuffle(options)

    return {
        "id": str(uuid.uuid4())[:8],
        "question": f"[문제 {idx}] {question}",
        "answer": answer,
        "category": q_type,
        "options": options,
        "explanation": f"정답은 '{answer}'입니다. {item} 관련 내용은 기출 빈도가 높으므로 반드시 숙지해야 합니다.",
        "correct_count": 0,
        "wrong_count": 0
    }

def main():
    # 데이터 저장 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    print(f"🏭 Starting Problem Bank Generation in {data_dir}...")

    # 1. 퀴즈 10,000문제 생성
    quizzes = [generate_question(i) for i in range(1, 10001)]
    
    with open(os.path.join(data_dir, 'quiz.json'), 'w', encoding='utf-8') as f:
        json.dump(quizzes, f, indent=2, ensure_ascii=False)

    # 2. 노트 1,000개 생성
    notes = []
    for i in range(1, 1001):
        subj = random.choice(list(KNOWLEDGE_DB.keys()))
        notes.append({
            "id": str(uuid.uuid4())[:8],
            "title": f"[{subj}] 기출 요약 노트 #{i}",
            "category": subj,
            "content": f"{subj} 과목의 핵심 요약입니다. 시험 직전 필독.",
            "importance": random.randint(3, 5),
            "created_at": datetime.datetime.now().isoformat(),
            "is_completed": False
        })

    with open(os.path.join(data_dir, 'notes.json'), 'w', encoding='utf-8') as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)

    print(f"✅ Generated {len(quizzes)} Quizzes and {len(notes)} Notes.")

if __name__ == "__main__":
    main()
