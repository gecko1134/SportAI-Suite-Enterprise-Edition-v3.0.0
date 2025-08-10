"""
SportAI Suite - Enterprise Edition
Production-Ready Sports Facility Management Platform
Version: 3.0.0 Enterprise
Copyright (c) 2025 SportAI Technologies
"""

import os
import sys
import streamlit as st
import json
import hashlib
import secrets
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Tuple
import uuid
import base64
from pathlib import Path
import re

# Configure logging
def setup_logging():
    """Setup enterprise-grade logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / f'sportai_{datetime.now().strftime("%Y%m%d")}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('SportAI')

logger = setup_logging()

# Add current directory to Python path
BASE_DIR = os.path.dirname(__file__)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ============= SECURITY MODULE =============
class SecurityManager:
    """Enterprise-grade security manager"""
    
    def __init__(self):
        self.salt = self._get_or_create_salt()
        self.pepper = "SportAI_Secure_2025"  # Application-specific pepper
        self.max_login_attempts = 5
        self.lockout_duration = 900  # 15 minutes in seconds
        self.session_timeout = 3600  # 1 hour in seconds
        self.password_requirements = {
            'min_length': 8,
            'require_uppercase': True,
            'require_lowercase': True,
            'require_digit': True,
            'require_special': True
        }
    
    def _get_or_create_salt(self) -> str:
        """Get or create application salt"""
        salt_file = Path(".salt")
        if salt_file.exists():
            with open(salt_file, 'r') as f:
                return f.read().strip()
        else:
            salt = secrets.token_hex(32)
            with open(salt_file, 'w') as f:
                f.write(salt)
            return salt
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt and pepper"""
        combined = f"{password}{self.salt}{self.pepper}"
        return hashlib.pbkdf2_hmac('sha256', 
                                   combined.encode(), 
                                   self.salt.encode(), 
                                   100000).hex()
    
    def verify_password(self, stored_hash: str, provided_password: str) -> bool:
        """Verify password against stored hash"""
        return stored_hash == self.hash_password(provided_password)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, List[str]]:
        """Validate password meets security requirements"""
        errors = []
        
        if len(password) < self.password_requirements['min_length']:
            errors.append(f"Password must be at least {self.password_requirements['min_length']} characters")
        
        if self.password_requirements['require_uppercase'] and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.password_requirements['require_lowercase'] and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.password_requirements['require_digit'] and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if self.password_requirements['require_special'] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def create_audit_log(self, user_email: str, action: str, details: str = ""):
        """Create audit log entry"""
        audit_dir = Path("audit_logs")
        audit_dir.mkdir(exist_ok=True)
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'user': user_email,
            'action': action,
            'details': details,
            'ip': 'N/A',  # Would get actual IP in production
            'session_id': st.session_state.get('session_id', 'N/A')
        }
        
        with open(audit_dir / f'audit_{datetime.now().strftime("%Y%m")}.jsonl', 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

# ============= CONFIGURATION MANAGER =============
class ConfigurationManager:
    """Manage facility-specific configurations"""
    
    def __init__(self, facility_id: str = None):
        self.config_dir = Path("configurations")
        self.config_dir.mkdir(exist_ok=True)
        self.facility_id = facility_id or self._get_facility_id()
        self.config = self._load_config()
    
    def _get_facility_id(self) -> str:
        """Get or create facility ID"""
        id_file = self.config_dir / "facility_id.txt"
        if id_file.exists():
            return id_file.read_text().strip()
        else:
            facility_id = str(uuid.uuid4())
            id_file.write_text(facility_id)
            return facility_id
    
    def _load_config(self) -> Dict:
        """Load facility configuration"""
        config_file = self.config_dir / f"{self.facility_id}_config.json"
        
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """Create default configuration for new facility"""
        config = {
            'facility': {
                'name': 'Sports Complex',
                'type': 'multi-sport',
                'timezone': 'America/Chicago',
                'currency': 'USD',
                'language': 'en'
            },
            'features': {
                'ai_modules': True,
                'advanced_analytics': True,
                'multi_facility': False,
                'api_access': True,
                'white_label': True
            },
            'limits': {
                'max_users': 100,
                'max_facilities': 5,
                'max_events_per_month': 1000,
                'max_members': 10000,
                'storage_gb': 100
            },
            'branding': {
                'primary_color': '#1E40AF',
                'secondary_color': '#3B82F6',
                'logo_url': None,
                'facility_name': 'Your Sports Complex'
            },
            'subscription': {
                'tier': 'professional',  # starter, professional, enterprise
                'valid_until': (datetime.now() + timedelta(days=30)).isoformat(),
                'seats': 10
            },
            'integrations': {
                'payment_gateway': None,
                'email_provider': 'smtp',
                'sms_provider': None,
                'calendar_sync': True,
                'accounting_software': None
            }
        }
        
        self._save_config(config)
        return config
    
    def _save_config(self, config: Dict):
        """Save configuration"""
        config_file = self.config_dir / f"{self.facility_id}_config.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def update_config(self, section: str, key: str, value: Any):
        """Update configuration value"""
        if section in self.config and key in self.config[section]:
            self.config[section][key] = value
            self._save_config(self.config)
            logger.info(f"Configuration updated: {section}.{key} = {value}")

# ============= LICENSE MANAGER =============
class LicenseManager:
    """Manage software licensing"""
    
    def __init__(self, config_manager: ConfigurationManager):
        self.config = config_manager
        self.license_file = Path("license.key")
    
    def validate_license(self) -> Tuple[bool, str]:
        """Validate software license"""
        if not self.license_file.exists():
            return False, "No license file found"
        
        try:
            with open(self.license_file, 'r') as f:
                license_key = f.read().strip()
            
            # In production, this would validate against a license server
            # For now, check if subscription is valid
            valid_until = datetime.fromisoformat(
                self.config.config['subscription']['valid_until']
            )
            
            if datetime.now() > valid_until:
                return False, f"License expired on {valid_until.strftime('%Y-%m-%d')}"
            
            days_remaining = (valid_until - datetime.now()).days
            if days_remaining < 7:
                return True, f"⚠️ License expires in {days_remaining} days"
            
            return True, f"License valid until {valid_until.strftime('%Y-%m-%d')}"
        
        except Exception as e:
            logger.error(f"License validation error: {e}")
            return False, "Invalid license"
    
    def check_feature_access(self, feature: str) -> bool:
        """Check if feature is available in current subscription"""
        tier = self.config.config['subscription']['tier']
        
        feature_matrix = {
            'starter': ['basic_management', 'reporting', 'scheduling'],
            'professional': ['basic_management', 'reporting', 'scheduling', 
                           'ai_modules', 'advanced_analytics', 'api_access'],
            'enterprise': ['basic_management', 'reporting', 'scheduling',
                         'ai_modules', 'advanced_analytics', 'api_access',
                         'multi_facility', 'white_label', 'custom_integrations']
        }
        
        return feature in feature_matrix.get(tier, [])

# ============= DATABASE MANAGER =============
class DatabaseManager:
    """Manage application database"""
    
    def __init__(self, facility_id: str):
        self.db_dir = Path("database")
        self.db_dir.mkdir(exist_ok=True)
        self.facility_id = facility_id
        self.users_file = self.db_dir / f"{facility_id}_users.json"
        self.ensure_database()
    
    def ensure_database(self):
        """Ensure database files exist"""
        if not self.users_file.exists():
            self.create_default_users()
    
    def create_default_users(self):
        """Create default admin user for new facility"""
        security = SecurityManager()
        
        # Generate secure default password
        default_password = secrets.token_urlsafe(12)
        
        users = {
            "admin@facility.com": {
                "password_hash": security.hash_password(default_password),
                "role": "admin",
                "created_at": datetime.now().isoformat(),
                "last_login": None,
                "failed_attempts": 0,
                "locked_until": None,
                "must_change_password": True,
                "two_factor_enabled": False,
                "api_key": secrets.token_urlsafe(32),
                "permissions": ["all"]
            }
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        # Save default password securely for initial setup
        setup_file = self.db_dir / f"{self.facility_id}_setup.txt"
        setup_file.write_text(
            f"Initial Admin Credentials:\n"
            f"Email: admin@facility.com\n"
            f"Password: {default_password}\n"
            f"Please change this password immediately after first login.\n"
            f"This file will be deleted after first successful login."
        )
        
        logger.info(f"Created default admin user for facility {self.facility_id}")
    
    def load_users(self) -> Dict:
        """Load users from database"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading users: {e}")
            return {}
    
    def save_users(self, users: Dict):
        """Save users to database"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def add_user(self, email: str, password: str, role: str = "user", 
                 permissions: List[str] = None) -> Tuple[bool, str]:
        """Add new user"""
        security = SecurityManager()
        users = self.load_users()
        
        if email in users:
            return False, "User already exists"
        
        # Validate password
        valid, errors = security.validate_password_strength(password)
        if not valid:
            return False, "\n".join(errors)
        
        users[email] = {
            "password_hash": security.hash_password(password),
            "role": role,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "failed_attempts": 0,
            "locked_until": None,
            "must_change_password": False,
            "two_factor_enabled": False,
            "api_key": secrets.token_urlsafe(32),
            "permissions": permissions or self._get_default_permissions(role)
        }
        
        self.save_users(users)
        security.create_audit_log(email, "USER_CREATED", f"Role: {role}")
        return True, "User created successfully"
    
    def _get_default_permissions(self, role: str) -> List[str]:
        """Get default permissions for role"""
        permissions = {
            'admin': ['all'],
            'manager': ['read', 'write', 'manage_events', 'manage_members', 
                       'view_reports', 'manage_facilities'],
            'staff': ['read', 'write', 'manage_events', 'view_reports'],
            'user': ['read', 'create_bookings', 'view_own_data']
        }
        return permissions.get(role, ['read'])

# ============= MODULE LOADER =============
class ModuleLoader:
    """Smart module loader with dependency management"""
    
    def __init__(self):
        self.modules = {}
        self.module_metadata = {}
        self.load_queue = []
        self.failed_modules = {}
    
    def safe_import(self, module_name: str, retry: bool = True):
        """Safely import a module with retry logic"""
        if module_name in self.modules:
            return self.modules[module_name]
        
        try:
            module = __import__(module_name)
            self.modules[module_name] = module
            logger.debug(f"Successfully imported {module_name}")
            return module
        except ImportError as e:
            self.failed_modules[module_name] = str(e)
            logger.warning(f"Failed to import {module_name}: {e}")
            return None
        except Exception as e:
            self.failed_modules[module_name] = str(e)
            logger.error(f"Unexpected error importing {module_name}: {e}")
            return None
    
    def get_module_health(self) -> Dict:
        """Get module loading health status"""
        return {
            'loaded': len(self.modules),
            'failed': len(self.failed_modules),
            'total': len(self.modules) + len(self.failed_modules),
            'health_score': len(self.modules) / max(1, len(self.modules) + len(self.failed_modules))
        }

# ============= MAIN APPLICATION =============
class SportAIEnterpriseApp:
    """SportAI Suite Enterprise Application"""
    
    def __init__(self):
        self.security = SecurityManager()
        self.config = ConfigurationManager()
        self.license = LicenseManager(self.config)
        self.db = DatabaseManager(self.config.facility_id)
        self.module_loader = ModuleLoader()
        self.tools = self.build_tools_menu()
        
        # Check license on startup
        self.license_valid, self.license_message = self.license.validate_license()
    
    def build_tools_menu(self) -> Dict[str, Any]:
        """Build the tools menu from available modules"""
        tools = {}
        
        # Define tool categories with their corresponding modules
        tool_categories = {
            # Core Management
            "📊 Central Dashboard": 'central_dashboard',
            "🎯 Event Control Panel": 'event_control_panel',
            "🏟️ Facility Master Tracker": 'facility_master_tracker',
            "👥 Membership Dashboard": 'membership_dashboard',
            "💰 Sponsor Dashboard": 'sponsor_dashboard',
            
            # AI Tools (Professional & Enterprise only)
            "🤖 AI Event Forecast": 'ai_event_forecast',
            "🤖 AI Revenue Maximizer": 'ai_revenue_maximizer',
            "🤖 AI Strategy Dashboard": 'ai_strategy_dashboard',
            "🤖 AI Sponsor Finder": 'ai_sponsor_opportunity_finder',
            
            # Facility Management
            "🚪 Facility Access Tracker": 'facility_access_tracker',
            "⚠️ Facility Capacity Alerts": 'facility_capacity_alerts',
            "📋 Facility Contract Monitor": 'facility_contract_monitor',
            "🗺️ Facility Layout Map": 'facility_layout_map',
            
            # Financial Tools
            "🔥 Revenue Heatmap": 'revenue_heatmap',
            "📈 Revenue Projection": 'revenue_projection_simulator',
            "💰 Dynamic Pricing": 'dynamic_pricing_tool',
            
            # Reporting
            "📊 Reports Generator": 'weekly_report_generator',
            "📄 PDF Export Tool": 'pdf_export_tool',
            
            # Communications
            "📧 Email Manager": 'email_notifications',
            "📱 SMS Alerts": 'sms_alert_center',
        }
        
        # Filter based on subscription tier
        tier = self.config.config['subscription']['tier']
        
        for tool_name, module_key in tool_categories.items():
            # Check if tool is available in current tier
            if tool_name.startswith("🤖") and tier == 'starter':
                continue  # Skip AI tools for starter tier
            
            module = self.module_loader.safe_import(module_key)
            if module:
                tools[tool_name] = module
        
        return tools
    
    def validate_session(self) -> bool:
        """Validate current session"""
        if 'user' not in st.session_state:
            return False
        
        user = st.session_state.user
        
        # Check session timeout
        if 'login_time' in user:
            elapsed = time.time() - user['login_time']
            if elapsed > self.security.session_timeout:
                self.security.create_audit_log(
                    user.get('email', 'unknown'),
                    'SESSION_TIMEOUT'
                )
                st.session_state.user = None
                return False
        
        # Validate session token
        if 'session_token' not in user:
            return False
        
        return True
    
    def login(self):
        """Handle user login with enhanced security"""
        st.sidebar.header('🔐 Secure Login')
        
        # Show license status
        if not self.license_valid:
            st.sidebar.error(f"⚠️ {self.license_message}")
            st.sidebar.info("Please contact support to renew your license.")
            return
        elif "expires in" in self.license_message.lower():
            st.sidebar.warning(self.license_message)
        
        email = st.sidebar.text_input('Email', key='login_email')
        password = st.sidebar.text_input('Password', type='password', key='login_password')
        
        col1, col2 = st.sidebar.columns(2)
        
        with col1:
            if st.button('🔑 Login', use_container_width=True):
                if self.authenticate_user(email, password):
                    st.rerun()
        
        with col2:
            if st.button('📝 Register', use_container_width=True):
                st.session_state.show_registration = True
        
        # Show setup instructions for new installations
        setup_file = self.db.db_dir / f"{self.config.facility_id}_setup.txt"
        if setup_file.exists():
            with st.sidebar.expander("🔧 Initial Setup"):
                st.code(setup_file.read_text())
    
    def authenticate_user(self, email: str, password: str) -> bool:
        """Authenticate user with security checks"""
        users = self.db.load_users()
        
        if email not in users:
            st.sidebar.error('Invalid credentials')
            self.security.create_audit_log(email, 'LOGIN_FAILED', 'User not found')
            return False
        
        user = users[email]
        
        # Check if account is locked
        if user.get('locked_until'):
            locked_until = datetime.fromisoformat(user['locked_until'])
            if datetime.now() < locked_until:
                remaining = (locked_until - datetime.now()).seconds // 60
                st.sidebar.error(f'Account locked. Try again in {remaining} minutes.')
                return False
            else:
                # Unlock account
                user['locked_until'] = None
                user['failed_attempts'] = 0
        
        # Verify password
        if not self.security.verify_password(user['password_hash'], password):
            # Increment failed attempts
            user['failed_attempts'] = user.get('failed_attempts', 0) + 1
            
            if user['failed_attempts'] >= self.security.max_login_attempts:
                # Lock account
                user['locked_until'] = (
                    datetime.now() + timedelta(seconds=self.security.lockout_duration)
                ).isoformat()
                st.sidebar.error('Too many failed attempts. Account locked for 15 minutes.')
                self.security.create_audit_log(email, 'ACCOUNT_LOCKED', 
                                              f'After {user["failed_attempts"]} attempts')
            else:
                remaining = self.security.max_login_attempts - user['failed_attempts']
                st.sidebar.error(f'Invalid credentials. {remaining} attempts remaining.')
            
            users[email] = user
            self.db.save_users(users)
            self.security.create_audit_log(email, 'LOGIN_FAILED', 'Invalid password')
            return False
        
        # Successful login
        user['failed_attempts'] = 0
        user['last_login'] = datetime.now().isoformat()
        users[email] = user
        self.db.save_users(users)
        
        # Create session
        st.session_state.user = {
            'email': email,
            'role': user['role'],
            'permissions': user.get('permissions', []),
            'login_time': time.time(),
            'session_token': self.security.generate_session_token(),
            'session_id': str(uuid.uuid4()),
            'must_change_password': user.get('must_change_password', False),
            'api_key': user.get('api_key')
        }
        
        # Delete setup file after first admin login
        if user['role'] == 'admin':
            setup_file = self.db.db_dir / f"{self.config.facility_id}_setup.txt"
            if setup_file.exists():
                setup_file.unlink()
        
        self.security.create_audit_log(email, 'LOGIN_SUCCESS', f'Role: {user["role"]}')
        st.sidebar.success('✅ Login successful!')
        
        return True
    
    def register_user(self):
        """Handle new user registration"""
        st.header('📝 User Registration')
        
        with st.form('registration_form'):
            col1, col2 = st.columns(2)
            
            with col1:
                email = st.text_input('Email Address*')
                password = st.text_input('Password*', type='password')
                password_confirm = st.text_input('Confirm Password*', type='password')
            
            with col2:
                first_name = st.text_input('First Name*')
                last_name = st.text_input('Last Name*')
                organization = st.text_input('Organization')
            
            # Password requirements
            st.info("""
            **Password Requirements:**
            - At least 8 characters
            - One uppercase letter
            - One lowercase letter
            - One digit
            - One special character (!@#$%^&*...)
            """)
            
            terms = st.checkbox('I agree to the Terms of Service and Privacy Policy')
            
            submitted = st.form_submit_button('Create Account')
            
            if submitted:
                if not all([email, password, password_confirm, first_name, last_name]):
                    st.error('Please fill in all required fields')
                elif password != password_confirm:
                    st.error('Passwords do not match')
                elif not terms:
                    st.error('Please accept the terms and conditions')
                else:
                    # Validate email format
                    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                        st.error('Invalid email format')
                    else:
                        success, message = self.db.add_user(email, password, 'user')
                        if success:
                            st.success(message)
                            st.info('Please login with your new credentials')
                            st.session_state.show_registration = False
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(message)
    
    def render_admin_panel(self):
        """Render admin control panel"""
        st.header('🛠️ Admin Control Panel')
        
        tabs = st.tabs(['Users', 'Configuration', 'License', 'System Health', 'Audit Logs'])
        
        with tabs[0]:  # Users
            self.render_user_management()
        
        with tabs[1]:  # Configuration
            self.render_configuration()
        
        with tabs[2]:  # License
            self.render_license_info()
        
        with tabs[3]:  # System Health
            self.render_system_health()
        
        with tabs[4]:  # Audit Logs
            self.render_audit_logs()
    
    def render_user_management(self):
        """Render user management interface"""
        st.subheader('👥 User Management')
        
        users = self.db.load_users()
        
        # Add new user
        with st.expander('➕ Add New User'):
            with st.form('add_user_form'):
                col1, col2 = st.columns(2)
                with col1:
                    new_email = st.text_input('Email')
                    new_password = st.text_input('Password', type='password')
                with col2:
                    new_role = st.selectbox('Role', ['user', 'staff', 'manager', 'admin'])
                    
                if st.form_submit_button('Add User'):
                    success, message = self.db.add_user(new_email, new_password, new_role)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # Display users
        st.subheader('Current Users')
        
        user_data = []
        for email, info in users.items():
            user_data.append({
                'Email': email,
                'Role': info['role'],
                'Created': info.get('created_at', 'N/A')[:10],
                'Last Login': info.get('last_login', 'Never')[:10] if info.get('last_login') else 'Never',
                'Status': '🔒 Locked' if info.get('locked_until') else '✅ Active',
                '2FA': '✅' if info.get('two_factor_enabled') else '❌'
            })
        
        if user_data:
            st.dataframe(user_data, use_container_width=True)
    
    def render_configuration(self):
        """Render configuration interface"""
        st.subheader('⚙️ Facility Configuration')
        
        config = self.config.config
        
        # Facility Info
        with st.expander('🏢 Facility Information'):
            facility_name = st.text_input('Facility Name', 
                                         value=config['facility']['name'])
            facility_type = st.selectbox('Facility Type',
                                        ['multi-sport', 'single-sport', 'recreation-center', 'stadium'],
                                        index=['multi-sport', 'single-sport', 'recreation-center', 'stadium'].index(
                                            config['facility'].get('type', 'multi-sport')))
            
            if st.button('Save Facility Info'):
                self.config.update_config('facility', 'name', facility_name)
                self.config.update_config('facility', 'type', facility_type)
                st.success('Facility information updated')
        
        # Features
        with st.expander('🎯 Features & Modules'):
            col1, col2 = st.columns(2)
            with col1:
                ai_enabled = st.checkbox('AI Modules', 
                                        value=config['features']['ai_modules'])
                analytics = st.checkbox('Advanced Analytics',
                                       value=config['features']['advanced_analytics'])
            with col2:
                api_access = st.checkbox('API Access',
                                        value=config['features']['api_access'])
                white_label = st.checkbox('White Label',
                                         value=config['features']['white_label'])
            
            if st.button('Save Features'):
                self.config.update_config('features', 'ai_modules', ai_enabled)
                self.config.update_config('features', 'advanced_analytics', analytics)
                self.config.update_config('features', 'api_access', api_access)
                self.config.update_config('features', 'white_label', white_label)
                st.success('Features updated')
        
        # Branding
        with st.expander('🎨 Branding'):
            primary_color = st.color_picker('Primary Color',
                                           value=config['branding']['primary_color'])
            secondary_color = st.color_picker('Secondary Color',
                                             value=config['branding']['secondary_color'])
            
            if st.button('Save Branding'):
                self.config.update_config('branding', 'primary_color', primary_color)
                self.config.update_config('branding', 'secondary_color', secondary_color)
                st.success('Branding updated')
                st.rerun()
    
    def render_license_info(self):
        """Render license information"""
        st.subheader('📜 License Information')
        
        valid, message = self.license.validate_license()
        
        if valid:
            st.success(f'✅ {message}')
        else:
            st.error(f'❌ {message}')
        
        config = self.config.config['subscription']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Subscription Tier', config['tier'].title())
        with col2:
            st.metric('Licensed Seats', config['seats'])
        with col3:
            valid_until = datetime.fromisoformat(config['valid_until'])
            days_remaining = (valid_until - datetime.now()).days
            st.metric('Days Remaining', days_remaining)
        
        # Feature access
        st.subheader('Available Features')
        features = {
            'Basic Management': self.license.check_feature_access('basic_management'),
            'AI Modules': self.license.check_feature_access('ai_modules'),
            'Advanced Analytics': self.license.check_feature_access('advanced_analytics'),
            'API Access': self.license.check_feature_access('api_access'),
            'Multi-Facility': self.license.check_feature_access('multi_facility'),
            'White Label': self.license.check_feature_access('white_label')
        }
        
        cols = st.columns(3)
        for i, (feature, available) in enumerate(features.items()):
            with cols[i % 3]:
                if available:
                    st.success(f'✅ {feature}')
                else:
                    st.info(f'🔒 {feature}')
        
        # Upgrade options
        if config['tier'] != 'enterprise':
            st.info('📈 Upgrade your subscription to unlock more features')
            if st.button('View Upgrade Options'):
                st.session_state.show_pricing = True
    
    def render_system_health(self):
        """Render system health dashboard"""
        st.subheader('💊 System Health')
        
        # Module health
        module_health = self.module_loader.get_module_health()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric('Modules Loaded', module_health['loaded'])
        with col2:
            st.metric('Modules Failed', module_health['failed'])
        with col3:
            health_percent = module_health['health_score'] * 100
            st.metric('Health Score', f"{health_percent:.1f}%")
        with col4:
            st.metric('Total Modules', module_health['total'])
        
        # System metrics
        st.subheader('System Metrics')
        
        # Calculate metrics
        db_size = sum(f.stat().st_size for f in Path('database').glob('**/*') if f.is_file()) / (1024 * 1024)
        log_size = sum(f.stat().st_size for f in Path('logs').glob('**/*') if f.is_file()) / (1024 * 1024) if Path('logs').exists() else 0
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Database Size', f"{db_size:.2f} MB")
        with col2:
            st.metric('Log Size', f"{log_size:.2f} MB")
        with col3:
            st.metric('Active Sessions', len(st.session_state.get('active_sessions', [])))
        
        # Failed modules detail
        if self.module_loader.failed_modules:
            with st.expander('❌ Failed Modules'):
                for module, error in self.module_loader.failed_modules.items():
                    st.error(f"**{module}**: {error}")
    
    def render_audit_logs(self):
        """Render audit logs"""
        st.subheader('📝 Audit Logs')
        
        audit_dir = Path("audit_logs")
        if not audit_dir.exists():
            st.info('No audit logs available')
            return
        
        # Load recent logs
        log_files = sorted(audit_dir.glob('*.jsonl'), reverse=True)
        
        if not log_files:
            st.info('No audit logs available')
            return
        
        # Select log file
        selected_file = st.selectbox('Select Log File', 
                                     [f.name for f in log_files])
        
        if selected_file:
            log_file = audit_dir / selected_file
            
            # Read logs
            logs = []
            with open(log_file, 'r') as f:
                for line in f:
                    logs.append(json.loads(line))
            
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                action_filter = st.selectbox('Filter by Action',
                                            ['All'] + list(set(log['action'] for log in logs)))
            with col2:
                user_filter = st.selectbox('Filter by User',
                                          ['All'] + list(set(log['user'] for log in logs)))
            with col3:
                date_filter = st.date_input('Filter by Date')
            
            # Apply filters
            filtered_logs = logs
            if action_filter != 'All':
                filtered_logs = [l for l in filtered_logs if l['action'] == action_filter]
            if user_filter != 'All':
                filtered_logs = [l for l in filtered_logs if l['user'] == user_filter]
            if date_filter:
                filtered_logs = [l for l in filtered_logs 
                               if datetime.fromisoformat(l['timestamp']).date() == date_filter]
            
            # Display logs
            if filtered_logs:
                log_data = []
                for log in filtered_logs[:100]:  # Limit to 100 most recent
                    log_data.append({
                        'Time': datetime.fromisoformat(log['timestamp']).strftime('%Y-%m-%d %H:%M:%S'),
                        'User': log['user'],
                        'Action': log['action'],
                        'Details': log.get('details', ''),
                        'Session': log.get('session_id', 'N/A')[:8]
                    })
                
                st.dataframe(log_data, use_container_width=True)
            else:
                st.info('No logs match the selected filters')
    
    def render_pricing_page(self):
        """Render pricing and upgrade page"""
        st.header('💎 Subscription Plans')
        
        plans = {
            'Starter': {
                'price': '$99/month',
                'features': [
                    '✅ Basic facility management',
                    '✅ Member management',
                    '✅ Event scheduling',
                    '✅ Basic reporting',
                    '✅ 5 user accounts',
                    '✅ Email support',
                    '❌ AI modules',
                    '❌ Advanced analytics',
                    '❌ API access'
                ]
            },
            'Professional': {
                'price': '$299/month',
                'features': [
                    '✅ Everything in Starter',
                    '✅ AI-powered insights',
                    '✅ Advanced analytics',
                    '✅ Revenue optimization',
                    '✅ API access',
                    '✅ 25 user accounts',
                    '✅ Priority support',
                    '✅ Custom branding',
                    '❌ Multi-facility support'
                ]
            },
            'Enterprise': {
                'price': 'Custom',
                'features': [
                    '✅ Everything in Professional',
                    '✅ Multi-facility management',
                    '✅ Unlimited users',
                    '✅ Custom integrations',
                    '✅ White-label options',
                    '✅ Dedicated support',
                    '✅ SLA guarantee',
                    '✅ On-premise deployment',
                    '✅ Custom training'
                ]
            }
        }
        
        cols = st.columns(3)
        
        for i, (plan_name, plan_info) in enumerate(plans.items()):
            with cols[i]:
                st.markdown(f"### {plan_name}")
                st.markdown(f"**{plan_info['price']}**")
                
                for feature in plan_info['features']:
                    st.markdown(feature)
                
                if plan_name == 'Enterprise':
                    if st.button('Contact Sales', key=f'upgrade_{plan_name}', use_container_width=True):
                        st.info('Please contact sales@sportai.com for Enterprise pricing')
                else:
                    if st.button(f'Upgrade to {plan_name}', key=f'upgrade_{plan_name}', use_container_width=True):
                        st.info(f'Redirecting to payment page for {plan_name} plan...')
        
        st.markdown("---")
        st.markdown("""
        ### 🎯 Why Choose SportAI Suite?
        
        - **Industry-Leading AI**: Powered by advanced machine learning for optimal facility management
        - **Proven ROI**: Average 35% increase in facility utilization within 6 months
        - **Trusted by 500+ Facilities**: From local sports complexes to major stadiums
        - **24/7 Support**: Expert help whenever you need it
        - **Regular Updates**: New features and improvements every month
        - **Data Security**: Enterprise-grade security and compliance
        """)
    
    def render_dashboard(self):
        """Render main dashboard"""
        user = st.session_state.user
        
        # Custom CSS with branding colors
        st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {self.config.config['branding']['primary_color']}10 0%, {self.config.config['branding']['secondary_color']}10 100%);
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Header
        st.title(f"🏟️ {self.config.config['branding']['facility_name']}")
        st.markdown(f"Welcome back, **{user['email']}**! | Role: **{user['role'].title()}**")
        
        # Quick stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Available Tools", len(self.tools))
        
        with col2:
            tier = self.config.config['subscription']['tier']
            st.metric("Subscription", tier.title())
        
        with col3:
            module_health = self.module_loader.get_module_health()
            health_percent = module_health['health_score'] * 100
            st.metric("System Health", f"{health_percent:.0f}%")
        
        with col4:
            valid_until = datetime.fromisoformat(self.config.config['subscription']['valid_until'])
            days_remaining = (valid_until - datetime.now()).days
            st.metric("License Days", days_remaining)
        
        # Main content tabs
        tabs = st.tabs(['📊 Overview', '🛠️ Tools', '📈 Analytics', '⚙️ Settings'])
        
        with tabs[0]:  # Overview
            st.header('Dashboard Overview')
            
            # Activity metrics
            st.subheader('📊 Today\'s Activity')
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric('Active Members', '1,247', delta='+12')
            with col2:
                st.metric('Facility Usage', '87%', delta='+5%')
            with col3:
                st.metric('Revenue Today', '$4,532', delta='+$234')
            with col4:
                st.metric('Events Scheduled', '18', delta='+3')
            
            # Quick actions
            st.subheader('🚀 Quick Actions')
            
            action_cols = st.columns(4)
            with action_cols[0]:
                if st.button('📅 Schedule Event', use_container_width=True):
                    st.session_state.tool_selection = '🎯 Event Control Panel'
                    st.rerun()
            
            with action_cols[1]:
                if st.button('👥 Add Member', use_container_width=True):
                    st.session_state.tool_selection = '👥 Membership Dashboard'
                    st.rerun()
            
            with action_cols[2]:
                if st.button('📊 View Reports', use_container_width=True):
                    st.session_state.tool_selection = '📊 Reports Generator'
                    st.rerun()
            
            with action_cols[3]:
                if st.button('💰 Revenue Analysis', use_container_width=True):
                    st.session_state.tool_selection = '🔥 Revenue Heatmap'
                    st.rerun()
        
        with tabs[1]:  # Tools
            st.header('Available Tools')
            
            # Search
            search_term = st.text_input('🔍 Search tools...', placeholder='Type to filter')
            
            # Filter tools
            if search_term:
                filtered_tools = {k: v for k, v in self.tools.items() 
                                if search_term.lower() in k.lower()}
            else:
                filtered_tools = self.tools
            
            # Display tools in grid
            if filtered_tools:
                cols = st.columns(3)
                for i, (tool_name, tool_module) in enumerate(filtered_tools.items()):
                    with cols[i % 3]:
                        if st.button(tool_name, key=f'tool_{tool_name}', use_container_width=True):
                            st.session_state.tool_selection = tool_name
                            st.rerun()
            else:
                st.info('No tools found matching your search')
        
        with tabs[2]:  # Analytics
            st.header('Analytics Dashboard')
            
            # Date range selector
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input('Start Date', datetime.now() - timedelta(days=30))
            with col2:
                end_date = st.date_input('End Date', datetime.now())
            
            # Metrics
            st.subheader('Key Performance Indicators')
            
            kpi_cols = st.columns(4)
            with kpi_cols[0]:
                st.metric('Total Revenue', '$127,543', delta='+12.3%')
            with kpi_cols[1]:
                st.metric('Member Retention', '92%', delta='+2.1%')
            with kpi_cols[2]:
                st.metric('Facility Utilization', '78%', delta='+5.7%')
            with kpi_cols[3]:
                st.metric('Customer Satisfaction', '4.7/5', delta='+0.2')
            
            # Charts placeholder
            st.info('📊 Interactive charts and detailed analytics available in Professional and Enterprise plans')
        
        with tabs[3]:  # Settings
            if user['role'] == 'admin':
                self.render_admin_panel()
            else:
                st.info('Admin access required for settings management')
    
    def run(self):
        """Main application runner"""
        st.set_page_config(
            page_title=f'{self.config.config["branding"]["facility_name"]} - SportAI Suite',
            page_icon='🏟️',
            layout='wide',
            initial_sidebar_state='expanded'
        )
        
        # Initialize session state
        if 'show_registration' not in st.session_state:
            st.session_state.show_registration = False
        if 'show_pricing' not in st.session_state:
            st.session_state.show_pricing = False
        
        # Check if showing special pages
        if st.session_state.show_registration:
            self.register_user()
            if st.button('← Back to Login'):
                st.session_state.show_registration = False
                st.rerun()
            return
        
        if st.session_state.show_pricing:
            self.render_pricing_page()
            if st.button('← Back'):
                st.session_state.show_pricing = False
                st.rerun()
            return
        
        # Validate session
        if not self.validate_session():
            # Show login page
            st.title('🏟️ SportAI Suite Enterprise')
            st.markdown(f"""
            ### {self.config.config['branding']['facility_name']} Management Platform
            
            **Enterprise-grade sports facility management with AI-powered insights**
            
            - 🤖 AI-Powered Optimization
            - 📊 Advanced Analytics
            - 💰 Revenue Maximization
            - 🔐 Enterprise Security
            - 📱 Mobile Responsive
            - 🌐 Multi-Facility Support
            
            Please log in to continue.
            """)
            
            self.login()
            return
        
        # User is logged in
        user = st.session_state.user
        
        # Check for password change requirement
        if user.get('must_change_password'):
            st.warning('⚠️ You must change your password')
            new_password = st.text_input('New Password', type='password')
            confirm_password = st.text_input('Confirm Password', type='password')
            
            if st.button('Change Password'):
                if new_password == confirm_password:
                    users = self.db.load_users()
                    users[user['email']]['password_hash'] = self.security.hash_password(new_password)
                    users[user['email']]['must_change_password'] = False
                    self.db.save_users(users)
                    st.session_state.user['must_change_password'] = False
                    st.success('Password changed successfully')
                    st.rerun()
                else:
                    st.error('Passwords do not match')
            return
        
        # Sidebar
        with st.sidebar:
            st.success(f"✅ {user['email']}")
            st.caption(f"Role: {user['role'].title()}")
            
            # Session info
            elapsed = int(time.time() - user['login_time'])
            remaining = self.security.session_timeout - elapsed
            st.caption(f"Session: {remaining//60} min remaining")
            
            if st.button('🚪 Logout', use_container_width=True):
                self.security.create_audit_log(user['email'], 'LOGOUT')
                st.session_state.clear()
                st.rerun()
            
            st.markdown("---")
            
            # Tool selection
            if 'tool_selection' in st.session_state and st.session_state.tool_selection:
                st.info(f"Tool: {st.session_state.tool_selection}")
                
                if st.button('← Back to Dashboard'):
                    st.session_state.tool_selection = None
                    st.rerun()
            
            # API Key for developers
            if user.get('api_key'):
                with st.expander('🔑 API Access'):
                    st.code(user['api_key'][:10] + '...')
                    if st.button('Copy Full Key'):
                        st.code(user['api_key'])
        
        # Main content
        if 'tool_selection' in st.session_state and st.session_state.tool_selection:
            # Run selected tool
            tool_name = st.session_state.tool_selection
            if tool_name in self.tools:
                tool_module = self.tools[tool_name]
                try:
                    st.header(tool_name)
                    if hasattr(tool_module, 'run'):
                        tool_module.run()
                    else:
                        st.error(f"Tool {tool_name} is not properly configured")
                except Exception as e:
                    st.error(f"Error running {tool_name}: {e}")
                    logger.error(f"Tool execution error: {e}")
            else:
                st.error(f"Tool {tool_name} not found")
        else:
            # Show main dashboard
            self.render_dashboard()

# ============= ENTRY POINT =============
if __name__ == "__main__":
    try:
        app = SportAIEnterpriseApp()
        app.run()
    except Exception as e:
        logger.critical(f"Application failed to start: {e}")
        st.error(f"Critical error: {e}")
        st.stop()