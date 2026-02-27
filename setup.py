"""
FounderOS Setup Script
Creates a superuser and seeds sample match profiles.
Run once after initial setup:
  .\venv\Scripts\python setup.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'founderos.settings')
django.setup()

from django.contrib.auth.models import User
from matching.models import MatchProfile

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@founderos.io', 'admin123')
    print("✅ Superuser created — username: admin | password: admin123")
else:
    print("ℹ️  Superuser 'admin' already exists.")

# Seed sample match profiles
sample_profiles = [
    {
        'name': 'Priya Sharma',
        'role': 'mentor',
        'bio': '15 years in product at Flipkart & Swiggy. Passionate about Tier-2 startup ecosystems.',
        'industry': 'Technology',
        'skills': 'Product Management, UX, Growth Hacking, GTM Strategy',
        'location': 'Bengaluru, Karnataka',
        'contact': 'priya@example.com',
    },
    {
        'name': 'Arjun Mehta',
        'role': 'investor',
        'bio': 'Angel investor with a portfolio of 20+ early-stage startups across agri-tech and ed-tech.',
        'industry': 'AgriTech, EdTech',
        'skills': 'Investment, Due Diligence, Networking, Fundraising',
        'location': 'Mumbai, Maharashtra',
        'contact': 'arjun@example.com',
    },
    {
        'name': 'Ritu Agarwal',
        'role': 'cofounder',
        'bio': 'Full-stack developer with 8 years of experience. Looking to join a mission-driven startup as technical co-founder.',
        'industry': 'FinTech, SaaS',
        'skills': 'Python, Django, React, AWS, System Design, Startup Experience',
        'location': 'Hyderabad, Telangana',
        'contact': 'ritu@example.com',
    },
    {
        'name': 'Vikram Patel',
        'role': 'mentor',
        'bio': 'Former IIT Bombay professor turned entrepreneur. Expert in hardware startups and deep tech.',
        'industry': 'Deep Tech, Hardware',
        'skills': 'R&D, Patents, Hardware Design, Government Grants',
        'location': 'Pune, Maharashtra',
        'contact': 'vikram@example.com',
    },
    {
        'name': 'Deepa Nair',
        'role': 'advisor',
        'bio': 'CA with expertise in startup finance, compliance, and government scheme applications.',
        'industry': 'Finance, Legal',
        'skills': 'Financial Modeling, GST, DPIIT Registration, Mudra Loans',
        'location': 'Chennai, Tamil Nadu',
        'contact': 'deepa@example.com',
    },
    {
        'name': 'Sahil Kumar',
        'role': 'investor',
        'bio': 'Seed investor focused on impact startups in healthcare, agri, and rural fintech.',
        'industry': 'Healthcare, Agriculture, FinTech',
        'skills': 'Impact Investing, Strategy, Mentorship, Network',
        'location': 'Delhi NCR',
        'contact': 'sahil@example.com',
    },
]

created = 0
for p in sample_profiles:
    if not MatchProfile.objects.filter(name=p['name']).exists():
        MatchProfile.objects.create(**p)
        created += 1

print(f"✅ {created} sample match profiles created ({len(sample_profiles) - created} already existed).")
print("\n🚀 FounderOS is ready! Run: .\\venv\\Scripts\\python manage.py runserver")
print("   Visit: http://127.0.0.1:8000")
print("   Admin: http://127.0.0.1:8000/admin  (admin / admin123)")
