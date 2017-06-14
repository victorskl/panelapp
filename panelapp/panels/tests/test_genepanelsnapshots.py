from random import randint
from django.urls import reverse_lazy
from faker import Factory
from accounts.tests.setup import LoginGELUser
from panels.models import GenePanelEntrySnapshot
from panels.models import GenePanelSnapshot
from panels.models import Evidence
from panels.models import GenePanel
from panels.models import Evaluation
from .factories import GeneFactory
from .factories import GenePanelSnapshotFactory
from .factories import GenePanelEntrySnapshotFactory
from .factories import TagFactory


fake = Factory.create()


class GenePanelSnapshotTest(LoginGELUser):
    def test_add_gene_to_panel(self):
        gene = GeneFactory()
        gps = GenePanelSnapshotFactory()
        url = reverse_lazy('panels:add_gene', kwargs={'pk': gps.panel.pk})
        gene_data = {
            "gene": gene.pk,
            "source": Evidence.ALL_SOURCES[randint(0, 9)],
            "tags": [TagFactory().pk, ],
            "publications": "{};{};{}".format(*fake.sentences(nb=3)),
            "phenotypes": "{};{};{}".format(*fake.sentences(nb=3)),
            "rating": Evaluation.RATINGS.AMBER,
            "comments": fake.sentence(),
            "moi": [x for x in Evaluation.MODES_OF_INHERITANCE][randint(1, 12)],
            "mode_of_pathogenicity": [x for x in Evaluation.MODES_OF_PATHOGENICITY][randint(1, 2)],
            "penetrance": GenePanelEntrySnapshot.PENETRANCE.Incomplete,
            "current_diagnostic": "True"
        }
        res = self.client.post(url, gene_data)

        assert res.status_code == 302

    def test_gene_evaluation(self):
        gpes = GenePanelEntrySnapshotFactory()
        url = reverse_lazy('panels:evaluation', kwargs={
            'pk': gpes.panel.panel.pk,
            'gene_symbol': gpes.gene.get('gene_symbol')
        })
        res = self.client.get(url)
        assert res.status_code == 200

    def test_edit_gene_in_panel(self):
        gpes = GenePanelEntrySnapshotFactory()
        url = reverse_lazy('panels:edit_gene', kwargs={
            'pk': gpes.panel.panel.pk,
            'gene_symbol': gpes.gene.get('gene_symbol')
        })

        # make sure new data has at least 1 of the same items
        source = gpes.evidence.last().name
        publication = gpes.publications[0]
        phenotype = gpes.publications[1]

        gene_data = {
            "gene": gpes.gene_core.pk,
            "gene_name": "Gene name",
            "source": set([source, Evidence.ALL_SOURCES[randint(0, 9)]]),
            "tags": [TagFactory().pk, ] + [tag.name for tag in gpes.tags.all()],
            "publications": ";".join([publication, fake.sentence()]),
            "phenotypes": ";".join([phenotype, fake.sentence(), fake.sentence()]),
            "moi": [x for x in Evaluation.MODES_OF_INHERITANCE][randint(1, 12)],
            "mode_of_pathogenicity": [x for x in Evaluation.MODES_OF_PATHOGENICITY][randint(1, 2)],
            "penetrance": GenePanelEntrySnapshot.PENETRANCE.Incomplete,
        }
        res = self.client.post(url, gene_data)
        assert res.status_code == 302

    def test_edit_gene_name(self):
        gpes = GenePanelEntrySnapshotFactory()
        url = reverse_lazy('panels:edit_gene', kwargs={
            'pk': gpes.panel.panel.pk,
            'gene_symbol': gpes.gene.get('gene_symbol')
        })

        old_gene_symbol = gpes.gene.get('gene_symbol')

        # make sure new data has at least 1 of the same items
        source = gpes.evidence.last().name
        publication = gpes.publications[0]
        phenotype = gpes.publications[1]

        new_gene = GeneFactory()

        gene_data = {
            "gene": new_gene.pk,
            "gene_name": "Other name",
            "source": set([source, Evidence.ALL_SOURCES[randint(0, 9)]]),
            "tags": [TagFactory().pk, ] + [tag.name for tag in gpes.tags.all()],
            "publications": ";".join([publication, fake.sentence()]),
            "phenotypes": ";".join([phenotype, fake.sentence(), fake.sentence()]),
            "moi": [x for x in Evaluation.MODES_OF_INHERITANCE][randint(1, 12)],
            "mode_of_pathogenicity": [x for x in Evaluation.MODES_OF_PATHOGENICITY][randint(1, 2)],
            "penetrance": GenePanelEntrySnapshot.PENETRANCE.Incomplete,
        }
        res = self.client.post(url, gene_data)
        assert res.status_code == 302

        new_gps = GenePanel.objects.get(pk=gpes.panel.panel.pk).active_panel
        old_gps = GenePanelSnapshot.objects.get(pk=gpes.panel.pk)

        # check panel has no previous gene
        assert new_gps.has_gene(old_gene_symbol) is False

        # test previous panel contains old gene
        assert old_gps.has_gene(old_gene_symbol) is True
