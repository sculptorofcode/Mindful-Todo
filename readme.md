# ✨ Mindful Todo

<p align="center">
  <img src="https://raw.githubusercontent.com/sculptorofcode/mindful-todo/master/static/images/banner.png" alt="Leading Image" width="100%">
</p>

> A modern task management application focused on mindful productivity and insightful analytics.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Overview

Mindful Todo helps you manage tasks with purpose. Track your productivity, analyze patterns, and make data-driven decisions about your time management.

## 🚀 Features

### Core Functionality
- 📝 **Smart Task Management**
  - Intuitive task creation and organization
  - Priority-based task sorting
  - Category organization
  - Flexible due dates

### Analytics & Insights
- 📊 **Rich Visualization**
  - Task completion trends
  - Category distribution analysis
  - Priority breakdowns
  - Daily activity patterns

### User Experience
- 🎨 **Modern Interface**
  - Clean, responsive design
  - Real-time updates
  - Intuitive navigation
  - Mobile-friendly layout

## 🛠 Tech Stack

### Frontend
- 🎨 **UI Framework**
  - HTML5 & CSS3 (Bootstrap)
  - Modern JavaScript
  - jQuery for DOM manipulation
  - ApexCharts for beautiful visualizations
  - Toastr for sleek notifications

### Backend
- ⚙️ **Server**
  - Python (Flask framework)
  - SQLAlchemy ORM
  - Gunicorn WSGI server
  - Nginx reverse proxy

### Database
- 🗄️ **Storage**
  - PostgreSQL (primary database)
  - SQLAlchemy migrations

## 📦 Installation

### Prerequisites
```bash
# Required software
Python 3.x
PostgreSQL
Virtual Environment
```

### Quick Start

1. **Clone & Setup**
```bash
# Clone repository
git clone https://github.com/sculptorofcode/mindful-todo.git
cd mindful-todo

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

2. **Configure Environment**
```bash
# Create .env file
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost/mindful_todo
SECRET_KEY=your_secret_key
```

3. **Database Setup**
```bash
# Initialize database
flask db init
flask db migrate
flask db upgrade
```

4. **Launch Application**
```bash
# Development
flask run

# Production
gunicorn -w 4 app:app
```

## 🚀 Deployment

### Production Setup

1. **Install Gunicorn**
```bash
pip install gunicorn
```

2. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/app/static/;
    }
}
```

3. **Enable SSL**
```bash
sudo certbot --nginx
sudo systemctl restart nginx
```

## 📱 Usage Guide

### Task Management
1. **Creating Tasks**
   - Enter task details
   - Set priority & category
   - Choose due date

2. **Managing Tasks**
   - Mark as complete
   - Update status
   - Delete tasks

### Analytics
1. **Viewing Insights**
   - Task completion rates
   - Time analysis
   - Category breakdowns
   - Priority distributions

2. **Time Filters**
   - Last 7 days
   - Last 30 days
   - Last 90 days
   - Yearly view

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 🙏 Acknowledgments

- Flask team for the amazing framework
- SQLAlchemy for database simplicity
- ApexCharts for beautiful visualizations
- Bootstrap team for responsive design
- Open source community for inspiration

---

<div align="center">

**[Website](https://mindful-todo.onrender.com/)** • **[Documentation](https://github.com/sculptorofcode/mindful-todo)** • **[Report Bug](https://github.com/sculptorofcode/mindful-todo/issues)** • **[Request Feature](https://github.com/sculptorofcode/mindful-todo/issues)**

Made with ❤️ by Saikat Roy

</div>