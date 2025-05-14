<%

# Python from here on down.

# Import some modules.
import numpy as np

NUMS = range(10)
VALS = [x*x for x in NUMS]

# I can use numpy if I want.
mysum = (np.array(VALS)* 100.0).sum()

# End of Python code. Time to go back to running commands.
%>

# Run the reporting command.
report:
	echo ${mysum} > report.txt