#!/bin/bash

echo "🚀 [INIT] Starting Massive Server Environment Setup..."

# 1. 프로젝트 루트 설정
PROJECT_ROOT=$(pwd)
echo "📍 Project Root: $PROJECT_ROOT"

# 2. 대량 디렉토리 구조 생성 (Server Standard)
echo "📂 Creating Directory Structure..."
mkdir -p $PROJECT_ROOT/config/environments
mkdir -p $PROJECT_ROOT/logs/app
mkdir -p $PROJECT_ROOT/logs/audit
mkdir -p $PROJECT_ROOT/logs/error
mkdir -p $PROJECT_ROOT/scripts/maintenance
mkdir -p $PROJECT_ROOT/docker/nginx
mkdir -p $PROJECT_ROOT/docker/app
mkdir -p $PROJECT_ROOT/docs/api
mkdir -p $PROJECT_ROOT/tests/integration
mkdir -p $PROJECT_ROOT/tests/unit

# 3. 환경 설정 파일 대량 생성 (Config)
echo "⚙️ Generating Configuration Files..."

# 3-1. App Config (JSON)
cat <<EOF > $PROJECT_ROOT/config/app_config.json
{
  "app_name": "CISE-Study-Bot",
  "version": "1.0.0",
  "env": "production",
  "logging": {
    "level": "INFO",
    "path": "/logs/app"
  },
  "database": {
    "type": "json_storage",
    "path": "./data"
  }
}
EOF

# 3-2. Logging Config (CONF)
cat <<EOF > $PROJECT_ROOT/config/logging.conf
[loggers]
keys=root,studyBot

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_studyBot]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=studyBot
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('logs/app/bot.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
EOF

# 4. Docker 환경 대량 생성
echo "🐳 Generating Docker Environment..."

# 4-1. Python App Dockerfile
cat <<EOF > $PROJECT_ROOT/docker/app/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "study_bot/main.py"]
EOF

# 4-2. Docker Compose
cat <<EOF > $PROJECT_ROOT/docker-compose.yml
version: '3.8'

services:
  study-bot:
    build:
      context: .
      dockerfile: docker/app/Dockerfile
    volumes:
      - ./study_bot/data:/app/study_bot/data
      - ./logs:/app/logs
    restart: always
EOF

# 5. 유지보수 스크립트 생성
echo "🛠️ Creating Maintenance Scripts..."

# 5-1. Clean logs script
cat <<EOF > $PROJECT_ROOT/scripts/maintenance/clean_logs.sh
#!/bin/bash
echo "Cleaning old logs..."
find $PROJECT_ROOT/logs -name "*.log" -mtime +7 -delete
echo "Done."
EOF
chmod +x $PROJECT_ROOT/scripts/maintenance/clean_logs.sh

echo "✅ [SUCCESS] Server Environment Setup Complete!"
tree $PROJECT_ROOT 2>/dev/null || find $PROJECT_ROOT -maxdepth 2 -not -path '*/.*'
