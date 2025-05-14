
# Recursive listing of the current directory.
listing.txt:
    # Find all files in the current directory.
    find . \
        > listing.txt
    
    # You can have multiple commands for a single target.
    echo `date` > date.txt

# Counts how many files are in the listings.txt file.
count.txt:
    # Counts how many files are in the current directory.
    cat listing.txt | wc -l > count.txt


