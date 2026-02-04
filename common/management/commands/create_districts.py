"""
Management command to create districts from JSON data.
Districts are identified by 7-digit codes (e.g., "1703202" for "Oltinko'l tumani")
and contain "tumani" in the name with a CENTRE field.
"""
import json
import os
from django.core.management.base import BaseCommand
from common.models import Region, District


class Command(BaseCommand):
    help = 'Create districts from the region_districts.json file'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear all existing districts before importing',
        )

    def handle(self, *args, **options):
        # Path to JSON file
        json_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
            'data',
            'region_districts.json'
        )

        if options['clear']:
            deleted_count = District.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing districts'))

        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # First, build a map of region codes to regions
        regions_map = {region.code: region for region in Region.objects.all()}

        if not regions_map:
            self.stdout.write(self.style.ERROR(
                'No regions found. Please run "python manage.py create_regions" first.'
            ))
            return

        districts_created = 0
        districts_updated = 0
        districts_skipped = 0
        districts_no_region = 0

        for item in data:
            code = item.get('MHOBT', '')
            name = item.get('NAME', '')
            centre = item.get('CENTRE', '')

            # Skip if no code or name
            if not code or not name:
                continue

            # Districts have exactly 7-digit codes and contain "tumani" in the name
            # Regular districts have a CENTRE field
            # Tashkent city districts (code starts with 1726) don't have CENTRE field
            is_regular_district = len(code) == 7 and 'tumani' in name.lower() and centre
            is_tashkent_district = len(code) == 7 and 'tumani' in name.lower() and code.startswith('1726')
            
            if is_regular_district or is_tashkent_district:
                # Get the region code (first 4 digits)
                region_code = code[:4]
                
                # Find the region
                region = regions_map.get(region_code)
                
                if not region:
                    districts_no_region += 1
                    self.stdout.write(self.style.WARNING(
                        f'Skipped district "{name}" - no region found for code {region_code}'
                    ))
                    continue

                district, created = District.objects.update_or_create(
                    code=code,
                    defaults={
                        'name': name,
                        'region': region
                    }
                )
                if created:
                    districts_created += 1
                    self.stdout.write(self.style.SUCCESS(
                        f'Created district: {name} (code: {code}) in {region.name}'
                    ))
                else:
                    districts_updated += 1
                    self.stdout.write(self.style.WARNING(
                        f'Updated district: {name} (code: {code}) in {region.name}'
                    ))
            else:
                districts_skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nSummary:\n'
            f'  - Districts created: {districts_created}\n'
            f'  - Districts updated: {districts_updated}\n'
            f'  - Districts without region: {districts_no_region}\n'
            f'  - Entries skipped: {districts_skipped}'
        ))
