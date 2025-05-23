# The Maker

The **maker** is an expansion of Pypiper to work more like a Makefile.

Note: this document is not suggesting changes to how Pypiper works. 

`maker` is a new module, that installs a new command line tool called `maker` built on top of Pypiper that allows Pypiper to work more like a `make` and process so called `Makerfiles`.

## The problem with Pypiper

Pypiper requires Python programming. Yet for a newcomer to bioinformatics, 
the learning curve is already steep. They have to learn UNIX commands, bash commands, bioinformatics tools, R, and then Python.

**Pypiper does not SCALE DOWN sufficiently for small tasks.**


## The problem with Make

Starting out with a`Makefile` is trivial to write and explain:

```
results.txt:
    echo "Hello, world!" >  results.txt
```

That's it.

You have a target called `results.txt` then under it you list the commands that create that file. 

The syntax of the commands that we list is identical to that used in bash. 

But as soon as you need to do anything more complicated, for example generate names based on some information, read some content from an existing file, it gets very confusing very quickly. 

Dependencies are hard to reason and get in the way most of the time. Data analyses are usually linear processes and not a complex graph of dependencies.

**The problem with `make` and `Makefiles` that they don't SCALE UP properly.**

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

When installed this repository will install the `maker` command that can be used to run Makerfiles.

```bash
maker yourmakerfile.mk
```

The `Makerfile` is just a simple text file.

I like to use the `.mk` extension the makerfiles because the syntax is similar to that of Makefiles and the syntax highlighting will work in my text editor.

### Example 1: Simple commands

Some of the simplest `Makerfiles` is also a valid `Makefiles`. For example this here below will work with both `make` and `maker`.

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

### Example 2: Adding Python code

See the `tests/maker/commands_2.mk` file. I adopted the templating system developed for `bottle.py` microframework to allow running Python code inside `Makerfiles`. I like the syntax of this templating system. No other feature of `bottle.py` is used, just the templating system.

* [Simple Templates][templates]

[templates]: https://bottlepy.org/docs/dev/stpl.html

I made one change the to syntax of the `bottle.py` templating system. In `bottle py` the variable substitution syntax is `{{var}}` but I changed that to `${var}` to make it more similar to the syntax used in BASH and Makefiles.

All python code is prefixed either with `%` if it is a single line or `<% %>` if it is a multi-line block.


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

Notably the above is an almost a valid `Makefile` as well. Remove the `%` and it will function as a valid `Makefile`. 

### Example 3: Looping in the Makerfile

See the `tests/maker/commands_3.mk` file.

In this example I can even loop inside the Makerfile. 

```makefile
% NUMS = range(10)
% VALS = [x*x for x in NUMS]

# Looping in the Simple Template style.
<% for num, val in zip(NUMS, VALS): %>
${num}.txt:
	echo ${val} > ${num}.txt
<% end %>
```

### Example 4: Full Python code may be embedded into the Makerfile

See the `tests/maker/commands_4.mk` file.

```makefile
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

```




















