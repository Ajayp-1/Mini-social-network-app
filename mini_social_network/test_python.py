import django
with open('test_output.txt', 'w') as f:
    f.write(f'Django version: {django.get_version()}\n')
    f.write('Python is running successfully!\n')
