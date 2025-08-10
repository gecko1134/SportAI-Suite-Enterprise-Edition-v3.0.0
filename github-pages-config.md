# SportAI Suite Documentation

Welcome to the official documentation for SportAI Suite Enterprise Edition.

## Quick Links

- [Installation Guide](#installation)
- [User Guide](#user-guide)
- [API Documentation](#api-documentation)
- [Deployment Guide](#deployment)
- [Security Best Practices](#security)

## Installation

### Requirements
- Python 3.8+
- 2GB RAM minimum
- 10GB storage

### Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/sportai-suite.git
cd sportai-suite

# Run setup wizard
python setup.py

# Start application
streamlit run sportai_main_app_file.py
```

## User Guide

### First Login
1. Navigate to `http://localhost:8501`
2. Use the admin credentials created during setup
3. Configure your facility settings

### Managing Users
Navigate to Settings → Users to:
- Add new users
- Assign roles (Admin, Manager, Staff, User)
- Manage permissions
- Reset passwords

### Facility Configuration
Settings → Configuration allows you to:
- Set facility name and type
- Configure features
- Customize branding
- Manage integrations

## API Documentation

### Authentication
```python
import requests

# Get token
response = requests.post('http://localhost:8501/api/auth/login', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['token']

# Use token
headers = {'Authorization': f'Bearer {token}'}
```

### Endpoints

#### Facilities
- `GET /api/facilities` - List facilities
- `GET /api/facilities/{id}` - Get facility details
- `POST /api/facilities` - Create facility
- `PUT /api/facilities/{id}` - Update facility
- `DELETE /api/facilities/{id}` - Delete facility

#### Members
- `GET /api/members` - List members
- `POST /api/members` - Add member
- `GET /api/members/{id}` - Get member details
- `PUT /api/members/{id}` - Update member

#### Events
- `GET /api/events` - List events
- `POST /api/events` - Create event
- `GET /api/events/{id}` - Get event details

## Deployment

### Docker Deployment
```bash
# Production deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f

# Backup database
docker-compose exec backup /scripts/backup.sh
```

### Cloud Deployment

#### AWS
1. Launch EC2 instance (t3.medium or larger)
2. Install Docker and Docker Compose
3. Clone repository
4. Configure environment variables
5. Run Docker Compose

#### Azure
1. Create Azure Container Instance
2. Configure with docker-compose.yml
3. Set environment variables
4. Deploy

#### Google Cloud
1. Use Cloud Run or GKE
2. Build and push image to GCR
3. Deploy with environment variables

## Security

### Best Practices
1. **Always use HTTPS** in production
2. **Change default passwords** immediately
3. **Enable 2FA** for admin accounts
4. **Regular backups** (automated via cron)
5. **Monitor audit logs** regularly
6. **Keep dependencies updated**

### Password Policy
- Minimum 8 characters
- Must include uppercase, lowercase, digit, and special character
- Account lockout after 5 failed attempts
- Session timeout after 1 hour

### Data Protection
- All passwords hashed with PBKDF2-HMAC-SHA256
- Session tokens are cryptographically secure
- Database encryption at rest (optional)
- SSL/TLS for all communications

## Troubleshooting

### Common Issues

**Application won't start**
```bash
# Check logs
tail -f logs/sportai_*.log

# Verify dependencies
pip list | grep streamlit

# Check database
python -c "import sqlite3; conn = sqlite3.connect('database/sportai.db'); print('DB OK')"
```

**Login issues**
```bash
# Reset admin password
python scripts/reset_password.py admin@sportai.com

# Check account status
sqlite3 database/sportai.db "SELECT email, locked_until FROM users WHERE email='admin@sportai.com'"
```

**Performance issues**
- Enable Redis caching
- Increase worker processes
- Use PostgreSQL instead of SQLite
- Enable CDN for static assets

## Support

- **GitHub Issues**: [Report bugs](https://github.com/yourusername/sportai-suite/issues)
- **Discussions**: [Community forum](https://github.com/yourusername/sportai-suite/discussions)
- **Email**: support@sportai.com
- **Documentation**: [Full docs](https://docs.sportai.com)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) for details.