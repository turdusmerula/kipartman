from frames.select_snapeda_frame import SelectSnapedaFrame


class SelectSnapedaModelFrame(SelectSnapedaFrame):
    def __init__(self, parent, initial_search=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectSnapedaModelFrame, self).__init__(parent, initial_search=initial_search, filter=self.filter)

    def filter(self, snapeda):
        if snapeda.has_footprint()==False:
            return True
        return False