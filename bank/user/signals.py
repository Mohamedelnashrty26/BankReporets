from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Section

@receiver(post_save, sender=Section)
def create_additional_sections(sender, instance, created, **kwargs):
    if created and not '-' in instance.section_name:
        num_users = instance.related_sub_department.users.count()
        if num_users > 1:  # Ensure there are multiple users
            individual_percentage = instance.actual_percentage / num_users
            for user in instance.related_sub_department.users.all():
                if user.name and user != instance.users.first():
                    new_section_name = f"{instance.section_name} - {user.name}"
                    new_section = Section.objects.create(
                        section_name=new_section_name,
                        related_sub_department=instance.related_sub_department,
                        actual_percentage=individual_percentage,
                    )
                    new_section.users.add(user)
                    new_section.update_achieved_percentage()  # Call update method


