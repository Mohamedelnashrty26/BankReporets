from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings
from django.db.models import Sum
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff(self, email, password=None, **extra_fields):
        """Create a staff user."""
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser."""
        user = self.create_staff(email, password=password, **extra_fields)
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_staff_activated = models.BooleanField(default=False)
    can_add_percentage = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    
class Department(models.Model):
    """Department object."""
    name = models.CharField(max_length=255)

    organization = models.ForeignKey(
        'Organization', 
        on_delete=models.CASCADE, 
        related_name='departments',
        null=True  # Allow null temporarily
    )
    department_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0)  
    achieved_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    users = models.ManyToManyField(
        User, related_name='departments', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is an update operation
            # Calculate the total percentage of all departments in the organization, excluding this instance
            total_percentage = Department.objects.filter(
                organization=self.organization
            ).exclude(pk=self.pk).aggregate(
                total=Sum('department_percentage')
            )['total'] or 0

            total_percentage += self.department_percentage

            # Check if the total exceeds 100%
            if total_percentage > 100:
                raise ValidationError("Total percentage for all departments in the organization cannot exceed 100%")

        super().save(*args, **kwargs)

    def update_achieved_percentage(self):
        total_sub_dept_percentage = sum(
            sub_dept.sub_department_percentage for sub_dept in self.subdepartments.all())

        total_sub_dept_percentage = min(total_sub_dept_percentage, 100)

        total_weighted_achieved = sum(
            sub_dept.sub_department_percentage * sub_dept.achieved_percentage for sub_dept in self.subdepartments.all())

        if total_sub_dept_percentage > 0:
            self.achieved_percentage = total_weighted_achieved / total_sub_dept_percentage
        else:
            self.achieved_percentage = 0

        self.save(update_fields=['achieved_percentage'])

  

class Organization(models.Model):
    name = models.CharField(max_length=255)
 
    
    def update_achieved_percentage(self):
        # ...
        total_dept_percentage = sum(dept.department_percentage for dept in self.departments.all())
        

    def __str__(self):
        return self.name
  
   
    
class SubDepartment(models.Model):
    """SubDepartment object."""
    name = models.CharField(max_length=255)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='subdepartments')
    sub_department_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, null=False)
    achieved_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    users = models.ManyToManyField(
        User, related_name='subdepartments')
    related_sub_department = models.ForeignKey(
    'SubDepartment', 
    on_delete=models.CASCADE, 
    related_name='sections',
    null=True,  # Temporarily allow null
    blank=True  # Allow blank in Django admin
    )


    def __str__(self):
        return self.name

    
    def update_achieved_percentage(self):
        total_actual_percentage = sum(section.actual_percentage for section in self.related_sections.all())
        
        # Ensure it doesn't exceed 100%
        total_actual_percentage = min(total_actual_percentage, 100)

        total_weighted_achieved = sum(section.actual_percentage * section.achieved_percentage for section in self.related_sections.all())
        
        # Calculate the achieved percentage
        if total_actual_percentage > 0:
            self.achieved_percentage = total_weighted_achieved / total_actual_percentage
        else:
            self.achieved_percentage = 0

        self.save(update_fields=['achieved_percentage'])
        if self.department:
            self.department.update_achieved_percentage()
        


    def save(self, *args, **kwargs):
        if self.pk:  # Check if this is an update operation
            # Calculate the total percentage of sibling subdepartments, excluding this instance
            total_percentage = SubDepartment.objects.filter(
                department=self.department
            ).exclude(pk=self.pk).aggregate(
                total=Sum('sub_department_percentage')
            )['total'] or 0

            # Include the percentage of this instance
            total_percentage += self.sub_department_percentage

            # Check if the total exceeds 100%
          

        super().save(*args, **kwargs)

    def update_parent_department_users(self):
        if self.department:
            for user in self.users.all():
                if not self.department.users.filter(id=user.id).exists():
                    self.department.users.add(user)

class Section(models.Model):
    """Section object."""
    section_name = models.CharField(max_length=255)
    related_sub_department = models.ForeignKey(
        SubDepartment,
        on_delete=models.CASCADE,
        related_name='related_sections',
    )
    approved = models.BooleanField(default=False)
    actual_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)  # pre-defined
    achieved_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=True, null=True)

    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='sections',
        blank=True,
    )

    # Remove the super().save(*args, **kwargs) call from this method
    # ... existing fields ...

    
    def update_achieved_percentage(self):
        total_criteria = self.criteria.count()
        if total_criteria > 0:
            total_points = self.criteria.aggregate(Sum('points'))['points__sum']
            average_points = total_points / total_criteria
            self.achieved_percentage = average_points
        else:
            self.achieved_percentage = 0

        self.save(update_fields=['achieved_percentage'])

    def save(self, *args, **kwargs):
        # Flag to indicate if the instance is new
        is_new = self.pk is None
        super().save(*args, **kwargs)  # Save the instance

        # After saving, update achieved percentage only if it's a new instance
        if is_new:
            self.update_achieved_percentage()


    def __str__(self):
        return self.section_name



class Criterion(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='criteria')
    name = models.CharField(max_length=255)
    is_checked = models.BooleanField(default=False)
    attached_file = models.FileField(upload_to='criterion_files/', blank=True, null=True)
    points = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_checked and self.attached_file:
            self.points = 100
        elif self.is_checked or self.attached_file:
            self.points = 50
        else:
            self.points = 0
        super().save(*args, **kwargs)
    