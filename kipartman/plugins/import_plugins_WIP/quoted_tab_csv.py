import csv

from kipartman.plugins.import_plugins import _import_base

class QuotedTabExport(_import_base.KiPartmanImporter):
    extension = 'csv'
    wildcard = 'Quoted, tab delimited CSV (*.csv)|*.csv'

    def fetch(self, base_filename, components):
        file_path = '{}.{}'.format(base_filename, self.extension)

        with open(file_path, 'r') as csvfile:
            rdr = csv.reader(csvfile, dialect='excel-tab')
            #TODO: implement import reader
            # wrt.writerow(['Refs', 'Value', 'Footprint',
            #               'Quantity', 'MFR', 'MPN', 'SPR', 'SPN'])

            # for fp in sorted(components):
            #     for val in sorted(components[fp]):
            #         ctcont = components[fp][val]
            #         commarefs = ctcont.refs.replace(';', ',')
            #         wrt.writerow([
            #             '"{}"'.format(commarefs),
            #             '"{}"'.format(ctcont.value),
            #             '"{}"'.format(ctcont.footprint),
            #             '"{}"'.format(len(ctcont)),
            #             '"{}"'.format(ctcont.manufacturer),
            #             '"{}"'.format(ctcont.manufacturer_pn),
            #             '"{}"'.format(ctcont.supplier),
            #             '"{}"'.format(ctcont.supplier_pn),
            #         ])
