from django.contrib.auth import get_user_model

def run():
    User = get_user_model()
    try:
        admin = User.objects.get(username='admin')
        admin.set_password('admin')
        admin.save()
        print("Admin password has been reset successfully.")
    except User.DoesNotExist:
        print("Admin user not found.")