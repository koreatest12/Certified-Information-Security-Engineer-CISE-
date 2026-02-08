#!/usr/bin/env python3
"""
정보보안기사(CISE) 공부자료 정리 봇 - 샘플 데이터 로더
처음 사용 시 예시 노트와 퀴즈를 추가합니다.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import StudyNote, QuizQuestion
import storage


SAMPLE_NOTES = [
    StudyNote(
        title="대칭키 vs 비대칭키 암호화",
        category="정보보안 일반",
        subcategory="암호학",
        content=(
            "1. 대칭키 암호화 (Symmetric Key)\n"
            "   - 암호화/복호화에 동일한 키 사용\n"
            "   - 종류: DES, 3DES, AES, SEED, ARIA\n"
            "   - 장점: 속도가 빠름\n"
            "   - 단점: 키 분배 문제\n"
            "\n"
            "2. 비대칭키 암호화 (Asymmetric Key)\n"
            "   - 공개키와 개인키 쌍 사용\n"
            "   - 종류: RSA, ECC, ElGamal, DSA\n"
            "   - 장점: 키 분배 문제 해결\n"
            "   - 단점: 속도가 느림\n"
            "\n"
            "3. 하이브리드 암호화\n"
            "   - 대칭키로 데이터 암호화\n"
            "   - 비대칭키로 대칭키를 암호화하여 전달"
        ),
        keywords=["대칭키", "비대칭키", "AES", "RSA", "암호화"],
        importance=5,
    ),
    StudyNote(
        title="SQL Injection 공격과 방어",
        category="어플리케이션 보안",
        subcategory="웹 보안",
        content=(
            "1. SQL Injection이란?\n"
            "   - 웹 어플리케이션의 입력값에 악의적인 SQL 구문 삽입\n"
            "   - DB 데이터 유출, 변조, 삭제 가능\n"
            "\n"
            "2. 공격 유형\n"
            "   - Union Based: UNION SELECT로 추가 쿼리\n"
            "   - Blind SQL Injection: 참/거짓 응답으로 정보 추출\n"
            "   - Error Based: 에러 메시지로 정보 추출\n"
            "   - Time Based: 응답 시간 차이로 정보 추출\n"
            "\n"
            "3. 방어 방법\n"
            "   - Prepared Statement (매개변수화된 쿼리)\n"
            "   - 입력값 검증 (화이트리스트)\n"
            "   - 최소 권한 원칙 적용\n"
            "   - WAF 도입"
        ),
        keywords=["SQL Injection", "웹 공격", "OWASP", "Prepared Statement"],
        importance=5,
    ),
    StudyNote(
        title="방화벽(Firewall) 종류",
        category="네트워크 보안",
        subcategory="방화벽",
        content=(
            "1. 패킷 필터링 방화벽\n"
            "   - OSI 3~4계층에서 동작\n"
            "   - IP, 포트 기반 필터링\n"
            "   - 속도 빠르지만 세밀한 제어 어려움\n"
            "\n"
            "2. 상태기반 검사(Stateful Inspection)\n"
            "   - 연결 상태 테이블 관리\n"
            "   - 패킷 필터링보다 정교한 제어\n"
            "\n"
            "3. 어플리케이션 게이트웨이 (프록시)\n"
            "   - OSI 7계층에서 동작\n"
            "   - 콘텐츠 레벨 검사 가능\n"
            "   - 속도가 느리지만 보안성 높음\n"
            "\n"
            "4. 차세대 방화벽 (NGFW)\n"
            "   - IPS, DPI, 어플리케이션 인식 통합\n"
            "   - SSL 검사 기능"
        ),
        keywords=["방화벽", "패킷 필터링", "Stateful", "프록시", "NGFW"],
        importance=4,
    ),
    StudyNote(
        title="리눅스 파일 권한 관리",
        category="시스템 보안",
        subcategory="리눅스/유닉스 보안",
        content=(
            "1. 파일 권한 구조\n"
            "   - rwx rwx rwx (소유자/그룹/기타)\n"
            "   - r=4, w=2, x=1\n"
            "   - 예: chmod 755 -> rwxr-xr-x\n"
            "\n"
            "2. 특수 권한\n"
            "   - SetUID (4000): 실행 시 소유자 권한으로 실행\n"
            "   - SetGID (2000): 실행 시 그룹 권한으로 실행\n"
            "   - Sticky Bit (1000): 소유자만 삭제 가능\n"
            "\n"
            "3. 보안 점검 사항\n"
            "   - SetUID 파일 주기적 점검: find / -perm -4000\n"
            "   - /etc/passwd 권한: 644\n"
            "   - /etc/shadow 권한: 400 또는 600\n"
            "   - umask 설정: 022 (기본)"
        ),
        keywords=["chmod", "SetUID", "권한", "리눅스", "umask"],
        importance=4,
    ),
    StudyNote(
        title="개인정보보호법 주요 내용",
        category="정보보안 관리 및 법규",
        subcategory="개인정보보호법",
        content=(
            "1. 개인정보의 정의\n"
            "   - 살아있는 개인에 관한 정보\n"
            "   - 성명, 주민번호 등 개인 식별 가능 정보\n"
            "\n"
            "2. 개인정보 처리 원칙\n"
            "   - 목적 제한의 원칙\n"
            "   - 최소 수집의 원칙\n"
            "   - 정보 주체 동의\n"
            "\n"
            "3. 개인정보 보호 조치\n"
            "   - 기술적 조치: 접근통제, 암호화, 로그관리\n"
            "   - 관리적 조치: 내부관리계획, 교육\n"
            "   - 물리적 조치: 출입통제\n"
            "\n"
            "4. 위반 시 벌칙\n"
            "   - 5년 이하 징역 또는 5천만원 이하 벌금\n"
            "   - 과징금: 매출액의 3% 이하"
        ),
        keywords=["개인정보", "개인정보보호법", "동의", "최소수집", "벌칙"],
        importance=5,
    ),
]

SAMPLE_QUIZZES = [
    QuizQuestion(
        question="AES 암호화 알고리즘의 블록 크기는?",
        answer="128비트",
        category="정보보안 일반",
        choices=["64비트", "128비트", "192비트", "256비트"],
        explanation="AES는 블록 크기 128비트, 키 길이 128/192/256비트를 지원합니다.",
    ),
    QuizQuestion(
        question="SQL Injection을 방어하기 위한 가장 효과적인 방법은?",
        answer="Prepared Statement",
        category="어플리케이션 보안",
        choices=["입력값 길이 제한", "Prepared Statement", "에러 메시지 숨기기", "HTTPS 적용"],
        explanation="Prepared Statement(매개변수화된 쿼리)는 SQL 구문과 데이터를 분리하여 SQL Injection을 원천적으로 방지합니다.",
    ),
    QuizQuestion(
        question="방화벽 중 OSI 7계층에서 동작하며 콘텐츠 레벨 검사가 가능한 유형은?",
        answer="어플리케이션 게이트웨이",
        category="네트워크 보안",
        choices=["패킷 필터링", "상태기반 검사", "어플리케이션 게이트웨이", "하이브리드 방화벽"],
        explanation="어플리케이션 게이트웨이(프록시 방화벽)는 OSI 7계층에서 동작하며 콘텐츠 수준의 정밀 검사가 가능합니다.",
    ),
    QuizQuestion(
        question="리눅스에서 SetUID가 설정된 파일을 찾는 명령어는?",
        answer="find / -perm -4000",
        category="시스템 보안",
        choices=["find / -perm -4000", "find / -perm -2000", "ls -la /etc", "chmod 4755 file"],
        explanation="SetUID는 퍼미션 4000으로, find / -perm -4000 명령으로 시스템 전체에서 검색할 수 있습니다.",
    ),
    QuizQuestion(
        question="개인정보보호법에서 규정하는 '개인정보'의 대상은?",
        answer="살아있는 개인",
        category="정보보안 관리 및 법규",
        choices=["모든 사람", "살아있는 개인", "대한민국 국민", "성인"],
        explanation="개인정보보호법상 개인정보는 '살아있는 개인에 관한 정보'로 사망자의 정보는 해당되지 않습니다.",
    ),
    QuizQuestion(
        question="다음 중 공개키 암호화 알고리즘이 아닌 것은?",
        answer="AES",
        category="정보보안 일반",
        choices=["RSA", "ECC", "AES", "ElGamal"],
        explanation="AES(Advanced Encryption Standard)는 대칭키 암호화 알고리즘입니다. RSA, ECC, ElGamal은 공개키(비대칭키) 암호화 알고리즘입니다.",
    ),
    QuizQuestion(
        question="OWASP Top 10에서 2021년 기준 1위 취약점은?",
        answer="Broken Access Control",
        category="어플리케이션 보안",
        choices=["Injection", "Broken Access Control", "Cryptographic Failures", "XSS"],
        explanation="OWASP Top 10 2021에서는 Broken Access Control이 1위로 올라갔으며, 이전 1위였던 Injection은 3위로 내려갔습니다.",
    ),
    QuizQuestion(
        question="IDS와 IPS의 가장 큰 차이점은?",
        answer="차단 기능 유무",
        category="네트워크 보안",
        choices=["탐지 정확도", "차단 기능 유무", "설치 위치", "분석 속도"],
        explanation="IDS(침입탐지시스템)는 탐지만 하고, IPS(침입방지시스템)는 탐지와 함께 차단까지 수행합니다.",
    ),
]


def load_sample_data():
    """샘플 데이터 로드"""
    existing_notes = storage.get_all_notes()
    existing_quizzes = storage.get_all_quizzes()

    if existing_notes or existing_quizzes:
        print("  이미 데이터가 존재합니다.")
        confirm = input("  샘플 데이터를 추가하시겠습니까? (y/n) > ").strip().lower()
        if confirm != "y":
            print("  취소되었습니다.")
            return

    print("\n  샘플 노트 추가 중...")
    for note in SAMPLE_NOTES:
        storage.save_note(note)
        print(f"    + {note.title}")

    print("\n  샘플 퀴즈 추가 중...")
    for quiz in SAMPLE_QUIZZES:
        storage.save_quiz(quiz)
        print(f"    + {quiz.question[:40]}...")

    print(f"\n  [OK] 샘플 데이터 로드 완료!")
    print(f"  노트 {len(SAMPLE_NOTES)}개, 퀴즈 {len(SAMPLE_QUIZZES)}개가 추가되었습니다.")


if __name__ == "__main__":
    load_sample_data()
