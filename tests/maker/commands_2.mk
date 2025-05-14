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
    find . \
        > ${LISTING}
    
    # You can have multiple commands for a single target.
    echo `date` > date.txt

# Counts how many files are in the listings.txt file.
${COUNT}:
    # Counts how many files are in the current directory.
    cat ${LISTING} | wc -l > ${COUNT}


