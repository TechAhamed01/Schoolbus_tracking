import os
import django

def setup_database():
    """Set up the database and create a superuser."""
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Create superuser if it doesn't exist
    if not User.objects.filter(email='admin@tracko.com').exists():
        print("Creating superuser...")
        User.objects.create_superuser(
            email='admin@tracko.com',
            password='admin123',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        print("Superuser created successfully!")
        print("Email: admin@tracko.com")
        print("Password: admin123")
    else:
        print("Superuser already exists.")

if __name__ == "__main__":
    setup_database()
