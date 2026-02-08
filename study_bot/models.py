"""
정보보안기사(CISE) 공부자료 정리 봇 - 데이터 모델
"""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


# 정보보안기사 시험 과목 분류
CATEGORIES = {
    "1": "시스템 보안",
    "2": "네트워크 보안",
    "3": "어플리케이션 보안",
    "4": "정보보안 일반",
    "5": "정보보안 관리 및 법규",
}

# 각 과목별 세부 주제
SUBCATEGORIES = {
    "시스템 보안": [
        "운영체제 보안",
        "클라이언트 보안",
        "서버 보안",
        "리눅스/유닉스 보안",
        "윈도우 보안",
        "악성코드 분석",
    ],
    "네트워크 보안": [
        "네트워크 기초",
        "네트워크 공격/방어",
        "방화벽",
        "IDS/IPS",
        "VPN",
        "무선 네트워크 보안",
        "프로토콜 보안",
    ],
    "어플리케이션 보안": [
        "웹 보안",
        "데이터베이스 보안",
        "전자상거래 보안",
        "소프트웨어 개발 보안",
        "OWASP Top 10",
    ],
    "정보보안 일반": [
        "암호학",
        "접근통제",
        "인증 기술",
        "보안 모델",
        "해시 함수",
        "공개키 기반구조(PKI)",
    ],
    "정보보안 관리 및 법규": [
        "정보보호 관리체계(ISMS)",
        "개인정보보호법",
        "정보통신망법",
        "전자서명법",
        "위험관리",
        "BCP/DRP",
    ],
}


@dataclass
class StudyNote:
    """공부 노트 데이터 모델"""
    title: str
    category: str
    content: str
    keywords: List[str] = field(default_factory=list)
    subcategory: str = ""
    note_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    importance: int = 3  # 1~5 (5가 가장 중요)
    review_count: int = 0
    mastered: bool = False

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StudyNote":
        return cls(**data)

    def summary(self) -> str:
        stars = "*" * self.importance
        status = "[완료]" if self.mastered else "[학습중]"
        return (
            f"[{self.note_id}] {status} {self.title} "
            f"| {self.category} > {self.subcategory} "
            f"| 중요도: {stars} | 복습: {self.review_count}회"
        )


@dataclass
class QuizQuestion:
    """퀴즈 문제 데이터 모델"""
    question: str
    answer: str
    category: str
    choices: List[str] = field(default_factory=list)
    explanation: str = ""
    question_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    correct_count: int = 0
    wrong_count: int = 0

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "QuizQuestion":
        return cls(**data)

    @property
    def accuracy(self) -> float:
        total = self.correct_count + self.wrong_count
        if total == 0:
            return 0.0
        return (self.correct_count / total) * 100
