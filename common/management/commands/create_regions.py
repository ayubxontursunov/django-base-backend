"""
Management command to create regions from JSON data.
Regions are identified by 4-digit codes (e.g., "1703" for "Andijon viloyati").
"""
import json
import os
from django.core.management.base import BaseCommand
from common.models import Region


class Command(BaseCommand):
    help = 'Create regions from the region_districts.json file'

    def handle(self, *args, **options):
        # Path to JSON file
        json_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            'data',
            'region_districts.json'
        )

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        regions_created = 0
        regions_updated = 0
        regions_skipped = 0

        for item in data:
            code = item.get('MHOBT', '')
            name = item.get('NAME', '')

            # Skip if no code or name
            if not code or not name:
                continue

            # Regions have exactly 4-digit codes and contain "viloyati" in the name
            # Also include Toshkent shahri (code "1726") which is a special region
            if len(code) == 4 and ('viloyati' in name.lower() or 'shahri' in name.lower() or 'respublikasi' in name.lower()):
                # Skip O'zbekiston Respublikasi (code "17") - already filtered by length
                # Skip Qoraqalpog'iston Respublikasi internal subdivisions
                
                # Check if it's a valid region (not a header or subdivision)
                # Include viloyati, Toshkent shahri, and Qoraqalpog'iston Respublikasi
                if 'viloyati' in name.lower() or \
                   ('shahri' in name.lower() and 'toshkent' in name.lower().replace("'", "")) or \
                   ('qoraqalpog' in name.lower() and 'respublikasi' in name.lower()):
                    region, created = Region.objects.update_or_create(
                        code=code,
                        defaults={'name': name}
                    )
                    if created:
                        regions_created += 1
                        self.stdout.write(self.style.SUCCESS(f'Created region: {name} (code: {code})'))
                    else:
                        regions_updated += 1
                        self.stdout.write(self.style.WARNING(f'Updated region: {name} (code: {code})'))
                else:
                    regions_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nSummary:\n'
            f'  - Regions created: {regions_created}\n'
            f'  - Regions updated: {regions_updated}\n'
            f'  - Entries skipped: {regions_skipped}'
        ))
