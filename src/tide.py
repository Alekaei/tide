import sys
from tide import TideApp

with TideApp(sys.argv[1:]) as app:
	app.run()