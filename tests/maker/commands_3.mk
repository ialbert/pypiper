#
# Python code may be embedded fully and gets compiled and executed
#

% NUMS = range(10)
% VALS = [x*x for x in NUMS]

<% for num, val in zip(NUMS, VALS): %>
${num}.txt:
	echo ${val} > ${num}.txt
<% end %>

