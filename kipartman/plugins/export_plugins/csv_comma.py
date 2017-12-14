import csv

from . import _export_base

class CsvExport(_export_base.KiPartmanExporter):
    extension = 'csv'
    wildcard = 'CSV Files (*.csv)|*.csv'

    def export(self, base_filename, components):
        file_path = '{}.{}'.format(base_filename, self.extension)

        with open(file_path, 'w') as csvfile:
            wrt = csv.writer(csvfile)

            wrt.writerow([key for key in 
                components[0].swagger_types.viewkeys()])

            for fp in sorted(components):
                wrt.writerow(
                    [format_csv_column_entry(fp, key)
                    for key in 
                    fp.swagger_types.viewkeys()])


def format_csv_column_entry(fp, key):
    #return repr(fp.to_dict()[key]).encode('ascii',errors='xmlcharrefreplace')
    field = fp.to_dict()[key]
    #if '{}'.format(type(field)) = "<type 'dict'>":
    if isinstance(field,unicode):
        #print('DEBUG:{}:{}:{}'.format(type(field), key, fp.to_dict()[key].encode('ascii', errors='xmlcharrefreplace')))
        return fp.to_dict()[key].encode('ascii', errors='xmlcharrefreplace')
    else:
        return fp.to_dict()[key]
