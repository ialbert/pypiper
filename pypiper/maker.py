import pypiper
import os, argparse, re, sys
import logging

# This is a modified version of the bottle template.
from pypiper.lib.bottle import SimpleTemplate

from itertools import takewhile, dropwhile, tee, chain
from textwrap import dedent

log = logging.getLogger(__name__)

# Shortcut for making directories.
def mkdir(path):
    dirname = os.path.dirname(path).strip()
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

def render(text, data=dict()):
    tmpl = SimpleTemplate(text)
    page = tmpl.render(data)
    return page

def takewhile_better(pred, iterable):
    """
    A better takewhile that does not unwind the iterable past the first failure.
    Returns taken items and the remaining items as a list
    """
    taken = []
    
    for item in iterable:
        if pred(item):
            taken.append(item)
        else:
            return taken, chain([item], iterable)

def cli(fname=''):

    fname = sys.argv[1] if len(sys.argv) > 1 else 'Makerfile'

    if not os.path.exists(fname):
        print(f"# File not found: {fname}")
        sys.exit(1)

    text = open(fname).read()

    make(text)

def make(text, name="pypiper", outfolder="logs", clean=''):

    # Process the template.
    text = render(text)

    # Dedent the template
    text = dedent(text)

    # Split the template into lines.
    lines = text.splitlines()
    
    # Remove empty lines and comments.
    lines = filter(lambda x: x.strip(), lines)
    lines = filter(lambda x: not x.strip().startswith('#'), lines)
        
    TARGET = re.compile(r'^(?P<target>\S.*?:)')
    COMMAND = r'(?P<command>\s.*)$'

    target = None
    cmd_map = dict()
    for line in lines:
       
        # Find a target line;
        tgt = re.match(TARGET, line)
        cmd = re.match(COMMAND, line)
        if tgt:
            target = tgt.group('target')
        elif target and cmd:
            command = cmd.group('command').strip()
            cmd_map.setdefault(target, []).append(command)
        else:
            print (f"# Invalid line?:{line}")
         

    pm = pypiper.PipelineManager(name=name, outfolder=outfolder)

    for target, commands in cmd_map.items():
        # Make the target directory.

        mkdir(target)

        last_index = len(commands) - 1
        for i, cmd in enumerate(commands):
            if i < last_index:
                pm.run(cmd, lock_name = f"{target}_lock.{i}")
            else:
                pm.run(cmd, target)

    pm.stop_pipeline()


if __name__ == "__main__":
    import sys
    text = """

    % URL = "https://hgdownload.soe.ucsc.edu/goldenPath/hg38/chromosomes/22.fa.gz"
    % REF = "refs/22.fa.gz"
    
    ${REF}:
        # curl -O ${REF} ${URL}
        echo "Hello"

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
        rm -f tmp.txt

    """

    make(text)