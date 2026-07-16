import sys
from os import listdir, getcwd, sep
from os.path import expanduser, isdir, isfile, exists, join, abspath, normpath

USAGE = """usage: [python | python3] jtext [OPTIONS] [%<ext>] <src> [<dest>]
    OPTIONS:
        -h print this message

        -v enable verbose output
        -p print the output of the command to the console

        -i allow hidden files to be scanned

    - ext: file extensions to filter, has to be prefixed with '%'
    - src: path to the project to convert
    - dest: path to the destination directory of the output

    e.g.: python jtext '%java' 'path/to/java/project' 'path/to/destination/folder'
"""

ARGS_ERR = "unrecognized args, for more information: python jtext.py -h"

EXIST_ERR = " error: no file exists at the specified path\n -> "

DIR_ERR = " path not allowed: The specified path must point to a directory\n -> "

FLAG_ERR = " unrecognized flag: "

SEPARATOR: str = sep

EXTENSION_PREFIX = "%"

MIN_ARGS = 1
MAX_ARGS = 2


def main(args: list):

    flags: list = [a for a in args if a.startswith("-")]
    if "-h" in flags:
        print(USAGE)
        exit(0)
    allowed_flags: set = {"-p", "-v", "-i"}
    wrong_flags: list = [f for f in flags if f not in allowed_flags]
    if len(wrong_flags) > 0:
        print(FLAG_ERR + wrong_flags[0])
        exit(-1)

    extensions: list = list(
        map(
            lambda e: e.replace("%", ""),
            [a for a in args if a.startswith(EXTENSION_PREFIX)],
        )
    )

    # active flags
    print_output: bool = any(f for f in flags if f == "-p")
    enable_verbose: bool = any(f for f in flags if f == "-v")
    include_hidden: bool = any(f for f in flags if f == "-i")

    # filter 'trueargs'
    trueargs: list = [
        a for a in args if not a.startswith("-") and not a.startswith(EXTENSION_PREFIX)
    ]
    if len(trueargs) < MIN_ARGS or len(trueargs) > MAX_ARGS:
        print(ARGS_ERR)
        exit(-2)

    source: str = trueargs[0]
    destination: str = trueargs[1] if len(trueargs) == MAX_ARGS else getcwd()

    source = str(normpath(abspath(expanduser(source))))
    destination = str(normpath(abspath(expanduser(destination))))

    if not exists(source):
        print(EXIST_ERR + str(source))
        exit(-3)
    if not exists(destination):
        print(EXIST_ERR + str(destination))
        exit(-3)
    if not isdir(destination):
        print(DIR_ERR + str(destination))
        exit(-4)

    files: list = filter_ext(
        source, extensions, verbose=enable_verbose, include_hidden=include_hidden
    )
    if len(files) == 0:
        print("--- No matching file found, exiting ---")
        exit(0)
    files.sort()

    sourcepath: list = source.split(SEPARATOR)
    # if present, remove the tailing '/'
    if source.endswith(SEPARATOR):
        sourcepath.pop()

    filename: str = sourcepath.pop() + "-output.txt"
    join_to_text(
        files, dest=destination, outputfile=filename, print_output=print_output
    )

    print(f"--- Successfully created output file in {destination}! ---")
    exit(0)


# just a wrapper for scan_dir()
def filter_ext(
    path: str, extensions: list, verbose=False, include_hidden=False
) -> list:
    files = []
    if verbose:
        if len(extensions) == 0:
            print(f" scanning all files in: {path}...")
        else:
            print(f"filtering {extensions} files in: {path}")
    scan_dir(path, extensions, files, verbose, include_hidden)
    return files


def scan_dir(path, extensions, files, verbose, include_hidden):
    msg: str
    if isfile(path) and (
        any(e for e in extensions if e in path.split(".")) or len(extensions) == 0
    ):
        msg = f" -> file found!: {path}"
        files.append(path)
    elif isdir(path):
        msg = f" scanned: {path}"
        directory = (
            [f for f in listdir(path) if not str(f).startswith(".")]
            if not include_hidden
            else listdir(path)
        )
        for file in directory:
            scan_dir(join(path, file), extensions, files, verbose, include_hidden)
    else:
        msg = f" skipping file: {path}"
    if verbose:
        print(msg)


def join_to_text(
    files: list, dest=getcwd(), outputfile="output.txt", print_output=False
):
    with open(join(dest, outputfile), "w", encoding="utf-8") as createfile:
        createfile.write("")
    with open(join(dest, outputfile), "a", encoding="utf-8") as appendfile:
        for file in files:
            try:
                with open(file, "r", encoding="utf-8") as readfile:
                    contents = readfile.read()
                    format = f"\nfile: {file.split(SEPARATOR).pop()}\nfull path: {file}\n\n{contents}\n"
                    appendfile.write(format)
            except UnicodeDecodeError:
                print(f" skipping not utf-8 encoded file: {file}")
    if print_output:
        with open(join(dest, outputfile), "r", encoding="utf-8") as readfile:
            print(
                f"""
-------------------------------------------------------------
                          Output
-------------------------------------------------------------
{readfile.read()}
"""
            )


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except BrokenPipeError:
        sys.stdout.close()
        exit(0)
    except KeyboardInterrupt:
        sys.stdout.close()
        exit(0)
