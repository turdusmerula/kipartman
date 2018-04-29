from helper.exception import print_stack

class KiPartmanExporter:
    def __init__(self):
        pass

    def validate(self):
        classname = self.__class__.__name__
        print("Validating: ", classname)
        try:
            self.extension
            self.wildcard
            self.export
            return True
        except AttributeError as e:
            print_stack()
            print("{} is invalid: {}".format(classname, str(e)))
