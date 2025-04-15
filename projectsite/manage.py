#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Add these lines to enable SSL
    from django.core.management.commands.runserver import Command as runserver
    runserver.default_port = "8000"
    runserver.default_addr = "0.0.0.0"
    # Enable SSL
    runserver.default_ssl_certificate = os.path.join(os.path.dirname(__file__), "localhost.crt")
    runserver.default_ssl_key = os.path.join(os.path.dirname(__file__), "localhost.key")
    
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
