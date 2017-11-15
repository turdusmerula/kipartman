import csv

from . import _import_base

class CsvImport(_import_base.KipartmanImporter):
    extension = 'csv'
    wildcard = 'CSV Files (*.csv)|*.csv'

    def importitems(self, base_filename, components):
        file_path = '{}.{}'.format(base_filename, self.extension)

        with open(file_path, 'w') as csvfile:
            wrt = csv.writer(csvfile)

            wrt.writerow(['Refs', 'Value', 'Footprint',
                          'Quantity', 'MFR', 'MPN', 'SPR', 'SPN'])

            for fp in sorted(components):
                for val in sorted(components[fp]):
                    ctcont = components[fp][val]
                    wrt.writerow([
                        ctcont.refs,
                        ctcont.value,
                        ctcont.footprint,
                        len(ctcont),
                        ctcont.manufacturer,
                        ctcont.manufacturer_pn,
                        ctcont.supplier,
                        ctcont.supplier_pn,
                    ])
