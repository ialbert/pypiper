 #
# Recursive listing of the current directory.
#
listing.txt:
    # Maybe there is a temporary file created.
    echo "STARTING" > temp.txt

    # Find all files in the current directory.
    find . \
        > listing.txt

    # Remove the temporary file.
    rm -f temp.txt


