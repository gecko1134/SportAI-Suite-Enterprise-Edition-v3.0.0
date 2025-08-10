# SportAI Suite Environment Configuration
# Copy this file to .env and update with your values

# ====================
# Application Settings
# ====================
APP_NAME="SportAI Suite Enterprise"
APP_ENV=production
DEBUG=false
SECRET_KEY=your-very-secure-secret-key-here-change-this
FACILITY_ID=auto  # Set to 'auto' to generate UUID or specify custom ID

# ====================
# Server Configuration
# ====================
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
MAX_UPLOAD_SIZE=200  # MB

# ====================
# Database Configuration
# ====================
DATABASE_TYPE=postgresql  # Options: sqlite, postgresql, mysql
DATABASE_URL=postgresql://sportai_user:sportai_pass@localhost:5432/sportai
# For SQLite: DATABASE_URL=sqlite:///database/sportai.db

# ====================
# Redis Cache
# ====================
REDIS_ENABLED=true
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=sportai2025
REDIS_DB=0

# ====================
# Security Settings
# ====================
SESSION_TIMEOUT=3600  # seconds (1 hour)
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900  # seconds (15 minutes)
PASSWORD_MIN_LENGTH=8
PASSWORD_REQUIRE_UPPERCASE=true
PASSWORD_REQUIRE_LOWERCASE=true
PASSWORD_REQUIRE_DIGIT=true
PASSWORD_REQUIRE_SPECIAL=true
ENABLE_TWO_FACTOR=false
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400  # seconds (24 hours)

# ====================
# Email Configuration (SMTP)
# ====================
EMAIL_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_USE_TLS=true
EMAIL_FROM="SportAI Suite <noreply@sportai.com>"
EMAIL_ADMIN=admin@sportai.com

# ====================
# SMS Configuration (Twilio)
# ====================
SMS_ENABLED=false
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# ====================
# Payment Processing
# ====================
PAYMENT_ENABLED=false
STRIPE_ENABLED=false
STRIPE_PUBLIC_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# ====================
# License Configuration
# ====================
LICENSE_SERVER_URL=https://license.sportai.com/api/v1
LICENSE_KEY=your-license-key-here
LICENSE_CHECK_INTERVAL=86400  # seconds (24 hours)
SUBSCRIPTION_TIER=professional  # Options: starter, professional, enterprise

# ====================
# AI/ML Configuration
# ====================
ENABLE_AI_MODULES=true
OPENAI_API_KEY=sk-xxx  # For advanced AI features
AI_MODEL_PATH=./models
MAX_AI_REQUESTS_PER_DAY=1000

# ====================
# Storage Configuration
# ====================
STORAGE_TYPE=local  # Options: local, s3, azure, gcs
STORAGE_PATH=./uploads
MAX_STORAGE_GB=100

# AWS S3 (if STORAGE_TYPE=s3)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_S3_BUCKET=sportai-uploads
AWS_REGION=us-east-1

# ====================
# Monitoring & Logging
# ====================
LOG_LEVEL=INFO  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE_PATH=./logs
LOG_ROTATION=daily
LOG_RETENTION_DAYS=30
ENABLE_AUDIT_LOG=true
AUDIT_LOG_PATH=./audit_logs

# Sentry Error Tracking
SENTRY_ENABLED=false
SENTRY_DSN=https://xxx@xxx.ingest.sentry