#
# Python code may be embedded fully and gets compiled and executed
#

% NUMS = range(10)
% VALS = [x*x for x in NUMS]

<% for num, val in zip(NUMS, VALS): %>
${num}.txt:
	echo ${val} > ${num}.txt
<% end %>

<%

import numpy as np

# I can use numpy if I want.
mysum = (np.array(VALS)* 100.0).sum()

%>

report:
	echo ${mysum} > report.txt