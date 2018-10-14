
__author__='Aleksei Ivanov'

import sys
from tide import TideApp

with TideApp(sys.argv) as app:
	app.run()