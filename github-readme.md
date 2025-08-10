# 🏟️ SportAI Suite Enterprise Edition

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)](https://streamlit.io/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

Enterprise-grade AI-powered sports facility management platform designed for modern sports complexes, recreation centers, and athletic facilities.

![SportAI Dashboard](https://img.shields.io/badge/SportAI-Suite-blue?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0ZGRkZGRiIgZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4eiIvPjwvc3ZnPg==)

## 🎯 Features

### Core Capabilities
- 🤖 **AI-Powered Optimization** - Smart scheduling, demand forecasting, and revenue maximization
- 📊 **Comprehensive Analytics** - Real-time dashboards and detailed reporting
- 💰 **Revenue Management** - Dynamic pricing, sponsorship matching, and financial tracking
- 👥 **Member Management** - CRM, loyalty programs, and engagement tracking
- 🏟️ **Facility Management** - Multi-facility support, resource allocation, and maintenance scheduling
- 📅 **Event Management** - Tournament scheduling, league coordination, and program management
- 🔐 **Enterprise Security** - PBKDF2 password hashing, session management, and audit logging
- 🎨 **White-Label Support** - Custom branding for each facility
- 📱 **Mobile Responsive** - Works seamlessly on all devices

### Subscription Tiers

| Feature | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| Price | $99/month | $299/month | Custom |
| Users | 5 | 25 | Unlimited |
| Facilities | 1 | 3 | Unlimited |
| AI Modules | ❌ | ✅ | ✅ |
| API Access | ❌ | ✅ | ✅ |
| White Label | ❌ | ✅ | ✅ |
| Support | Email | Priority | Dedicated |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 2GB RAM minimum
- 10GB storage space

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sportai-suite.git
cd sportai-suite
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Initialize the database**
```bash
python scripts/initialize_db.py
```

6. **Run the application**
```bash
streamlit run sportai_main_app_file.py
```

7. **Access the application**
- Open browser to `http://localhost:8501`
- Check `database/[facility_id]_setup.txt` for initial admin credentials
- Login and change password immediately

## 📁 Project Structure

```
sportai-suite/
├── sportai_main_app_file.py    # Main application file
├── requirements.txt             # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore file
├── LICENSE                     # MIT License
├── README.md                   # This file
├── docker-compose.yml          # Docker configuration
├── Dockerfile                  # Docker container setup
│
├── ai_modules/                 # AI-powered modules
│   ├── __init__.py
│   ├── demand_forecasting.py
│   ├── scheduling_optimizer.py
│   ├── sponsorship_matcher.py
│   ├── membership_churn.py
│   └── marketing_optimizer.py
│
├── modules/                    # Feature modules
│   ├── facility_management/
│   ├── membership_management/
│   ├── event_management/
│   ├── financial_management/
│   └── reporting/
│
├── database/                   # Database files (gitignored)
│   └── .gitkeep
│
├── logs/                       # Application logs (gitignored)
│   └── .gitkeep
│
├── audit_logs/                 # Security audit logs (gitignored)
│   └── .gitkeep
│
├── configurations/             # Facility configurations (gitignored)
│   └── .gitkeep
│
├── scripts/                    # Utility scripts
│   ├── initialize_db.py
│   ├── backup.py
│   ├── migrate.py
│   └── health_check.py
│
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_security.py
│   ├── test_modules.py
│   └── test_api.py
│
└── docs/                       # Documentation
    ├── API.md
    ├── DEPLOYMENT.md
    ├── SECURITY.md
    └── USER_GUIDE.md
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Application Settings
APP_NAME=SportAI Suite
APP_ENV=production
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///database/sportai.db

# Security
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5
PASSWORD_MIN_LENGTH=8

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password

# License Server (Optional)
LICENSE_SERVER_URL=https://license.sportai.com
LICENSE_KEY=your-license-key

# Features
ENABLE_AI_MODULES=true
ENABLE_MULTI_FACILITY=false
ENABLE_API_ACCESS=true
```

### First-Time Setup

1. **Change default admin password**
2. **Configure facility information** (Settings → Configuration)
3. **Set up branding** (colors, logo, facility name)
4. **Add users** with appropriate roles
5. **Configure integrations** (payment, email, SMS)
6. **Set up backup schedule**

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Manual Docker Build

```bash
# Build image
docker build -t sportai-suite .

# Run container
docker run -d -p 8501:8501 \
  -v $(pwd)/database:/app/database \
  -v $(pwd)/logs:/app/logs \
  --name sportai \
  sportai-suite
```

## 🔐 Security Features

- **Password Security**: PBKDF2-HMAC SHA256 with salt and pepper
- **Session Management**: Secure tokens with configurable timeout
- **Account Protection**: Lockout after failed attempts
- **Audit Logging**: Complete activity tracking
- **Data Encryption**: At-rest and in-transit encryption
- **Role-Based Access**: Granular permission system
- **API Security**: Unique keys per user with rate limiting

## 📊 API Documentation

### Authentication

```python
import requests

# Login and get token
response = requests.post('http://localhost:8501/api/auth/login', json={
    'email': 'user@example.com',
    'password': 'secure_password'
})
token = response.json()['token']

# Use token for API calls
headers = {'Authorization': f'Bearer {token}'}
```

### Example Endpoints

```python
# Get facility metrics
GET /api/facilities/metrics

# Create event
POST /api/events
{
    "name": "Basketball Tournament",
    "date": "2025-02-15",
    "facility_id": "court-1"
}

# Get member list
GET /api/members?limit=50&offset=0
```

Full API documentation available at `/api/docs` when running.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_security.py

# Run with verbose output
pytest -v
```

## 📈 Performance Optimization

- **Lazy Loading**: Modules loaded on-demand
- **Caching**: Redis support for session and data caching
- **Database Indexing**: Optimized queries
- **Async Operations**: Background task processing
- **CDN Support**: Static asset delivery

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.sportai.com](https://docs.sportai.com)
- **Email**: support@sportai.com
- **Issues**: [GitHub Issues](https://github.com/yourusername/sportai-suite/issues)
- **Discord**: [Join our community](https://discord.gg/sportai)

## 🏆 Testimonials

> "SportAI Suite transformed our facility management. We've seen a 35% increase in utilization and 25% revenue growth in just 6 months." - *John Smith, Recreation Director*

> "The AI scheduling alone saved us 20 hours per week. It's been a game-changer." - *Sarah Johnson, Facility Manager*

## 🗺️ Roadmap

- [x] Core facility management
- [x] AI-powered scheduling
- [x] Multi-tenant support
- [x] White-label capabilities
- [ ] Mobile app (Q2 2025)
- [ ] Advanced analytics dashboard (Q2 2025)
- [ ] IoT sensor integration (Q3 2025)
- [ ] Blockchain ticketing (Q4 2025)

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/sportai-suite?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/sportai-suite?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/sportai-suite)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/sportai-suite)

---

**Built with ❤️ by the SportAI Team**

*Empowering sports facilities with intelligent management solutions*