from django.db import models
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.core.exceptions import ValidationError
import uuid
class User(models.Model):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('company', 'Company'),
    ]

    SECURITY_QUESTION_CHOICES = [
        ("What was your first pet's name?", "What was your first pet's name?"),
        ("What city were you born in?", "What city were you born in?"),
        ("What is your mother's maiden name?", "What is your mother's maiden name?"),
        ("What was the name of your first school?", "What was the name of your first school?"),
    ]

    uid = models.CharField(max_length=10, unique=True, editable=False, default='U0000')
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    dob = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    security_question = models.CharField(max_length=255, choices=SECURITY_QUESTION_CHOICES)
    security_answer = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'api_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def clean(self):
        """Validate model fields before saving"""
        if not self.uid.startswith('U'):
            raise ValidationError("UID must start with 'U'")
        if len(self.phone) < 10 or not self.phone.isdigit():
            raise ValidationError("Phone number must be at least 10 digits")

    def save(self, *args, **kwargs):
        """Override save to handle password hashing and UID generation"""
        if not self.pk:  # Only for new instances
            if not self.uid or self.uid == 'U0000':
                last_user = User.objects.order_by('-uid').first()
                last_num = int(last_user.uid[1:]) if last_user else 0
                self.uid = f"U{last_num + 1:04d}"
            
            if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$')):
                self.password = make_password(self.password)
        
        super().save(*args, **kwargs)

    @classmethod
    def create_user(cls, user_data):
        """Create user with proper Django ORM usage"""
        try:
            with transaction.atomic():
                # Generate UID
                last_user = cls.objects.order_by('-uid').first()
                last_num = int(last_user.uid[1:]) if last_user else 0
                uid = f"U{last_num + 1:04d}"

                # Create user instance
                user = cls(
                    uid=uid,
                    name=user_data['name'],
                    email=user_data['email'],
                    password=make_password(user_data['password']),
                    dob=user_data['dob'],
                    phone=user_data['phone'],
                    address=user_data['address'],
                    security_question=user_data['security_question'],
                    security_answer=user_data['security_answer'],
                    role=user_data.get('role', 'employee')
                )
                
                # Full clean and save
                user.full_clean()
                user.save()
                return uid
                
        except Exception as e:
            raise ValueError(f"Error creating user: {str(e)}")

    def __str__(self):
        return f"{self.uid} - {self.name} ({self.role})"
    

class JobPosition(models.Model):
    POSITION_CHOICES = [
        ('Engineer', 'Engineer'),
        ('Doctor', 'Doctor'),
        ('Accounting', 'Accounting'),
        ('Marketing', 'Marketing'),
        ('Part Timer', 'Part Timer'),
        ('Event Crew', 'Event Crew'),
        ('Software Engineer', 'Software Engineer'),
        ('Data Analyst', 'Data Analyst'),
        ('Product Manager', 'Product Manager'),
        ('UX Designer', 'UX Designer'),
        ('DevOps Engineer', 'DevOps Engineer'),
        ('QA Engineer', 'QA Engineer'),
        ('System Administrator', 'System Administrator'),
        ('Technical Writer', 'Technical Writer'),
        ('Frontend Developer', 'Frontend Developer'),
        ('Backend Developer', 'Backend Developer'),
        ('Full Stack Developer', 'Full Stack Developer'),
        ('Mobile Developer', 'Mobile Developer'),
        ('Data Scientist', 'Data Scientist'),
        ('Machine Learning Engineer', 'Machine Learning Engineer'),
        ('Cloud Architect', 'Cloud Architect'),
        ('Network Engineer', 'Network Engineer'),
        ('Security Specialist', 'Security Specialist'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_positions',
        db_column='uid',
        to_field='uid'
    )
    position = models.CharField(
        max_length=50,
        choices=POSITION_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_position'
        ordering = ['-created_at']
        verbose_name = 'Job Position'
        verbose_name_plural = 'Job Positions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'position'],
                name='unique_user_position'
            )
        ]

    def clean(self):
        """Validate that employee can't have duplicate positions"""
        if JobPosition.objects.filter(
            user=self.user,
            position=self.position
        ).exclude(pk=self.pk).exists():
            raise ValidationError(
                'This position already exists for the user'
            )

    def __str__(self):
        return f"{self.user.name} - {self.position}"