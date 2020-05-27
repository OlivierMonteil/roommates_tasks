 # -*- coding: utf-8 -*-

import sys
from application import RoommatesTaskListApp

if __name__ == '__main__':

    app = RoommatesTaskListApp(sys.argv)
    sys.exit(app.run())