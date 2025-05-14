# Pypipe Maker

Pypiper Maker is an expansion of Pypiper to work more like a Makefile.


## The problem with Pypiper

Pypiper requires Python programming. Yet for a newcomer to bioinformatics, 
the learning curve is already steep. They have to learn UNIX commands, bash commands, bioinformatics tools and then Python.

Pypiper does not scale down sufficiently for small tasks.

## The problem with Make

The problems with `make` and `Makefiles` that they don't scale up properly. 

Whereas a simple `Makefile` is trivial to write and explain:

```
results.txt:
    echo "Hello, world!" >  results.txt
```

The syntax is simple. You have a target called `results.txt` then under it you list the commands that create that file. The commands that we list are idnetical to those listed in bash. There is very little new to learn.

But as soon as you need to do anything more complicated, for example generate names based on some information, read some content from an existing file, it gets very confusing very quickly.

Make is an ancient tool with a steep learning curve.

## Solution: combine the best of both worlds

1. Keep the simple syntax of Make
2. Add the power of Python

The `maker` command is built on top of Pypiper. It allows you to write simple commands in a Makefile like syntax but also allows you to drop down to Python when you need to.

## Counter arguments

Why is it better to learn a new thing that embeds Python than to write actual Python code?

* Most people that need bioinformatics are not Python programmers.
* Most data analysis in bioinformatics is done in R rather than Python. We cannot expect people to learn Unix Bash, R and Python.
* A Makerfile emphasises a declarative style of thinking about analysis.
* The limitations of embedding Python in a Makefile are a good thing. They lead to a better design.
* When we embed Python the resulting code will simper and less complicated than it would be in a full Python program.

Makerfiles are simple text files that are more easily translatable to bash or Makefiles.

### Running maker
```bash
maker yourmakerfile.mk
```

The `Makerfile` is just a simple text file.

I like to use the `.mk` extension the makerfiles because the syntax is similar to that of Makefiles and the syntax highlighting will work in my text editor.

### Example 1: Simple commands

See the `tests/maker/commands_1.mk` file.

```makefile
# Recursive listing of the current directory.
listing.txt:
    # Find all files in the current directory.
    find . > listing.txt
    
    # You can have multiple commands for a single target.
    echo `date` > date.txt

# Counts how many files are in the listings.txt file.
count.txt:
    # Counts how many files are in the current directory.
    cat listing.txt | wc -l > count.txt
```

```bash
maker tests/maker/commands_1.mk
```

Will generate the `listing.txt` and `count.txt` files.

## Example 2: Adding Python code

See the `tests/maker/commands_2.mk` file. We use the templating system developed for `bottle.py` to allow us to add Python code to the Makerfile. I like the syntax of this system. No other feature of `bottle.py` is used, just the templating system.

All python code is prefixed either with `%` if it is a single line or `<% %>` if it is a multi-line block.

The variable substitution syntax is identical to that used in BASH and Makefiles. So code from a script can be used directly in a Makerfile.

```makefile

#
# To add python code you can use the % or the <% %> blocks
#
% LISTING = 'listings.txt'
% COUNT = 'count.txt'

#
# To use a variable defined in Python you can use the ${VAR} syntax.
# This syntax is identical to the syntax used BASH and Makefiles. So code
# from a script can be used directly in a Makerfile.

# Recursive listing of the current directory.
${LISTING}:
    # Find all files in the current directory.
    find . > ${LISTING}
    
    # You can have multiple commands for a single target.
    echo `date` > date.txt

# Counts how many files are in the listings.txt file.
${COUNT}:
    # Counts how many files are in the current directory.
    cat ${LISTING} | wc -l > ${COUNT}
```

### Example 3: 

#
# Python code may be embedded fully and gets compiled and executed
#

See the `tests/maker/commands_3.mk` file.

In this example I can even loop inside the Makerfile. 

```makefile
% NUMS = range(10)
% VALS = [x*x for x in NUMS]

<% for num, val in zip(NUMS, VALS): %>
${num}.txt:
	echo ${val} > ${num}.txt
<% end %>
```


## Example 4: Full Python code may be embedded into the Makerfile

See the `tests/maker/commands_4.mk` file.

```makefile
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

# Import some modules.
import numpy as np

# I can use numpy if I want.
mysum = (np.array(VALS)* 100.0).sum()

%>

report:
	echo ${mysum} > report.txt
```




















