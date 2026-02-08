#!/usr/bin/env python3
"""
정보보안기사(CISE) 공부자료 정리 봇
====================================
정보보안기사 시험 준비를 위한 CLI 기반 공부자료 관리 도구입니다.

기능:
- 과목별 공부 노트 추가/조회/수정/삭제
- 키워드 기반 노트 검색
- 객관식/주관식 퀴즈 기능
- 학습 진도 및 통계 관리

사용법:
    python main.py
"""

import sys
import os

# 모듈 경로 설정
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot import run_bot


def main():
    try:
        run_bot()
    except KeyboardInterrupt:
        print("\n\n  프로그램을 종료합니다.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
