from django.core.management.base import BaseCommand
from panels.models import GenePanelSnapshot, GenePanelEntrySnapshot, Region, STR


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for panel in GenePanelSnapshot.objects.get_active(
                all=True, internal=True, superpanels=False).filter(genepanelentrysnapshot__saved_gel_status__gt=3):

            if panel.is_super_panel:
                continue

            new_panel = panel.increment_version()

            GenePanelEntrySnapshot.objects.filter(panel=new_panel, saved_gel_status__gt=3).update(saved_gel_status=3)

            Region.objects.filter(panel=new_panel, saved_gel_status__gt=3).update(saved_gel_status=3)

            STR.objects.filter(panel=new_panel, saved_gel_status__gt=3).update(saved_gel_status=3)
