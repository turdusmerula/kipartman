import csv
import datetime

from . import _import_base


class CsvImport(_import_base.KiPartmanImporter):
    extension = 'csv'
    wildcard = 'CSV Files (*.csv)|*.csv'

    def fetch(self, base_filename, category, import_item=object):
        file_path = '{}.{}'.format(base_filename, self.extension)

        with open(file_path, 'rb') as csvfile:
            # TODO: implement csvReader
            csvreader = csv.DictReader(csvfile)  # TODO: do we need this, delimiter=', ', quotechar='"')
            components = []
            for row in csvreader:
                try:
                    i = import_item.PartNew()
                    i.name = unicode(row['Name'], errors='ignore').encode('utf-8')
                    i.description = unicode(row['Description'], errors='ignore').encode('utf-8')
                    i.category = category
                    i.comment = 'NEW IMPORT Timestamp:{:%y-%m-%d %H:%M:%S.%f}'.format(datetime.datetime.now())
                    i.footprint = unicode(row['Footprint'], errors='ignore').encode('utf-8')
                    components.append(i)
                    print("Name:", row['Name'], category, row['Description'], row['Footprint'])  # TODO: remove
                except Exception, e:
                    print(e)
                    pass
            return components
