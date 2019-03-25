from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models import Case
from django.db.models import When
from django.db.models import Subquery
from django.db.models import Value
from django.db import models

from panels.models import GenePanel, GenePanelSnapshot, GenePanelEntrySnapshot


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for panel in (GenePanelSnapshot.objects.filter(
                pk__in=Subquery(
                    GenePanelSnapshot.objects.exclude(
                        panel__status=GenePanel.STATUS.deleted
                    )
                            .distinct("panel_id")
                            .values("pk")
                            .order_by("panel_id", "-major_version", "-minor_version")
                )
        )
        .annotate(child_panels_count=Count("child_panels"))
        .annotate(superpanels_count=Count("genepanelsnapshot"))
        .annotate(
            is_super_panel=Case(
                When(child_panels_count__gt=0, then=Value(True)),
                default=Value(False),
                output_field=models.BooleanField(),
            ),
        ).filter(genepanelentrysnapshot__saved_gel_status__gt=3)):

            if panel.is_super_panel:
                continue

            new_panel = panel.increment_version()

            GenePanelEntrySnapshot.objects.filter(panel=new_panel, saved_gel_status=4).update(saved_gel_status=3)

