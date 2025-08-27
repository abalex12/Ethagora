# services/email_service.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

class EmailService:
    @staticmethod
    def send_welcome_email(user):
        """Send welcome email to new user"""
        subject = 'Welcome to Our Platform!'
        message = render_to_string('emails/welcome.html', {
            'user': user,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_verification_email(user, request):
        """Send email verification link"""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        verification_link = request.build_absolute_uri(
            reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        )
        
        subject = 'Verify Your Email Address'
        message = render_to_string('emails/verify_email.html', {
            'user': user,
            'verification_link': verification_link,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )
    
    @staticmethod
    def send_password_reset_email(user, request):
        """Send password reset email"""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        reset_link = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})
        )
        
        subject = 'Password Reset Request'
        message = render_to_string('emails/password_reset.html', {
            'user': user,
            'reset_link': reset_link,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )

    @staticmethod
    def send_account_deletion_email(user):
        """Send account deletion confirmation email"""
        subject = 'Account Deletion Confirmation'
        message = render_to_string('emails/account_deleted.html', {
            'user': user,
        })
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            html_message=message,
            fail_silently=False,
        )