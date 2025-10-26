#!/bin/sh

# alembic upgrade head 명령을 실행하여 DB 스키마를 최신 상태로 마이그레이션
alembic upgrade head

# 그 다음, Dockerfile의 CMD로 전달된 원래 명령(예: uvicorn main:app ...)을 실행
exec "$@"