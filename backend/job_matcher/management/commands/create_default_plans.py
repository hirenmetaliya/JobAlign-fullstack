from django.core.management.base import BaseCommand
from job_matcher.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Creates default subscription plans'

    def handle(self, *args, **kwargs):
        # Create Free Plan
        free_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Free',
            defaults={
                'max_matches': 10,
                'price': 0.00,
                'features': 'Basic job matching\nUp to 10 matches per search'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Free plan'))
        else:
            self.stdout.write(self.style.SUCCESS('Free plan already exists'))

        # Create Premium Plan
        premium_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Premium',
            defaults={
                'max_matches': 30,
                'price': 9.99,
                'features': 'Advanced job matching\nUp to 30 matches per search\nPriority support'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Premium plan'))
        else:
            self.stdout.write(self.style.SUCCESS('Premium plan already exists'))

        # Create Pro Plan
        pro_plan, created = SubscriptionPlan.objects.get_or_create(
            name='Pro',
            defaults={
                'max_matches': 999999,  # Effectively unlimited
                'price': 29.99,
                'features': 'Advanced job matching\nUnlimited matches\nPriority support\nCustom alerts'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created Pro plan'))
        else:
            self.stdout.write(self.style.SUCCESS('Pro plan already exists')) 