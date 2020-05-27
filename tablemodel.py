class Model(list):
    def __init__(self, DAYS,ROOMMATES):
        self.table_model = []
        self.DAYS = DAYS
        self.ROOMMATES = ROOMMATES
        for i, _ in enumerate(DAYS):
            self.append([])
            for x in ROOMMATES:
                self[i].append('')


    def rowCount(self, parent=None):
        return len(self.DAYS)

    def columnCount(self, parent=None):
        return len(self.ROOMMATES)
