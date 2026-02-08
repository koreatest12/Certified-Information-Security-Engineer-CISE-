import datetime
import uuid
# from typing import Optional  <-- 이 부분이 에러 원인이므로 삭제했습니다.
from typing import List, Dict

# ==========================================
# 1. 학습 노트 모델 (StudyNote)
# ==========================================
class StudyNote:
    def __init__(self, title: str, category: str, content: str, importance: int = 1, tags: List[str] = None):
        self.id = str(uuid.uuid4())[:8]  # 짧은 ID 생성
        self.title = title
        self.category = category
        self.content = content
        self.importance = importance  # 1~5
        self.tags = tags if tags else []
        self.created_at = datetime.datetime.now().isoformat()
        self.review_count = 0
        self.is_completed = False

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "importance": self.importance,
            "tags": self.tags,
            "created_at": self.created_at,
            "review_count": self.review_count,
            "is_completed": self.is_completed
        }

    @classmethod
    def from_dict(cls, data: Dict):
        note = cls(
            title=data["title"],
            category=data["category"],
            content=data["content"],
            importance=data.get("importance", 1),
            tags=data.get("tags", [])
        )
        note.id = data["id"]
        note.created_at = data["created_at"]
        note.review_count = data.get("review_count", 0)
        note.is_completed = data.get("is_completed", False)
        return note

    def summary(self) -> str:
        status = "[완료]" if self.is_completed else "[학습중]"
        star = "*" * self.importance
        return f"[{self.id}] {status} {self.title} | {self.category} | 중요도: {star} | 복습: {self.review_count}회"

# ==========================================
# 2. 퀴즈 문제 모델 (QuizQuestion)
# ==========================================
class QuizQuestion:
    def __init__(self, question: str, answer: str, category: str, options: List[str] = None, explanation: str = ""):
        self.id = str(uuid.uuid4())[:8]
        self.question = question
        self.answer = answer
        self.category = category
        self.options = options if options else []  # 객관식 보기
        self.explanation = explanation
        self.correct_count = 0
        self.wrong_count = 0

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "question": self.question,
            "answer": self.answer,
            "category": self.category,
            "options": self.options,
            "explanation": self.explanation,
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count
        }

    @classmethod
    def from_dict(cls, data: Dict):
        quiz = cls(
            question=data["question"],
            answer=data["answer"],
            category=data["category"],
            options=data.get("options", []),
            explanation=data.get("explanation", "")
        )
        quiz.id = data["id"]
        quiz.correct_count = data.get("correct_count", 0)
        quiz.wrong_count = data.get("wrong_count", 0)
        return quiz

# ==========================================
# 3. 과목 및 카테고리 상수
# ==========================================
CATEGORIES = [
    "시스템 보안",
    "네트워크 보안",
    "어플리케이션 보안",
    "정보보안 일반",
    "정보보안 법규"
]

SUBCATEGORIES = {
    "시스템 보안": ["운영체제", "클라이언트 보안", "서버 보안"],
    "네트워크 보안": ["네트워크 일반", "네트워크 위협", "네트워크 장비"],
    "어플리케이션 보안": ["웹 보안", "SW 개발 보안", "이메일/DB 보안"],
    "정보보안 일반": ["접근통제", "암호학", "보안운영"],
    "정보보안 법규": ["정보통신망법", "개인정보보호법", "정보통신기반보호법"]
}
