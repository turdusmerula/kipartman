import csv

from . import _import_base

class LCSCImport(_import_base.KiPartmanImporter):
    extension = 'csv'
    wildcard = 'lcsc.com CSV (*.csv)|*.csv'

    def fetch(self, base_filename, importItem = object):
        file_path = '{}.{}'.format(base_filename, self.extension)

        with open(file_path, 'w') as csvfile:
            wrt = csv.writer(csvfile)

            wrt.writerow(['Quantity','Value', 'Refs', 'Footprint',
                        'Manufacturer','Manufacture Part Number',
                        'LCSC Part Number'])

            for fp in sorted(components):
                for val in sorted(components[fp]):
                    ctcont = components[fp][val]
                    wrt.writerow([
                        len(ctcont),
                        ctcont.value,
                        ctcont.refs,
                        ctcont.footprint,
                        ctcont.manufacturer,
                        ctcont.manufacturer_pn,
                        ctcont.supplier_pn,
                    ])
