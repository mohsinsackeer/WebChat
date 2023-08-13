from setuptools import setup, find_packages

setup(
    name="webchat",
    version="1.0.0",
    python_requires='>3.9.0',
    packages=find_packages(),
    install_requires=[
        "bidict==0.21.2",
        "certifi==2020.12.5",
        "click==7.1.2",
        "cloudinary==1.24.0",
        "Flask==1.1.2",
        "Flask-Login==0.5.0",
        "Flask-SocketIO==5.3.5",
        "Flask-SQLAlchemy==2.4.4",
        "itsdangerous==1.1.0",
        "Jinja2==2.11.3",
        "MarkupSafe==1.1.1",
        "python-engineio==4",
        "python-socketio==5.0.2",
        "six==1.15.0",
        "SQLAlchemy==1.3.23",
        "urllib3==1.26.4",
        "Werkzeug==1.0.1",
        "gunicorn==19.9.0",
    ],
)