import sys
from os import listdir, getcwd, sep
from os.path import expanduser, isdir, isfile, exists, join, abspath, normpath


CMD_ERR = "unrecognized args, for more information: python jtext.py -h"
USAGE = """usage: [python | python3] jtext [OPTIONS] <ext> <src> [<dest>]
    OPTIONS:
        -h print this message

        -v enable verbose output
        -p print the output of the command to the console

        -A include all convertible extensions, if this option is enabled the
            passed in extension will be ignored

    - ext: file extension to filter
    - src: path to the project to convert
    - dest: path to the destination directory of the output

    e.g.: python jtext '.java' 'path/to/java/project' 'path/to/destination/folder'"""

EXIST_ERR = " error: no file exists at the specified path\n -> "
DIR_ERR = " path not allowed: The specified path must point to a directory\n -> "
FLAG_ERR = " unrecognized flag: "
SEPARATOR: str = sep
ALL_EXTENSIONS = "INCLUDE_EVERYTHING"
MIN_ARGS = 2
MAX_ARGS = 3


def main(args: list):

    flags: list = [a for a in args if a.startswith("-")]
    if "-h" in flags:
        print(USAGE)
        exit(0)
    allowed_flags: set = {"-p", "-v", "-A"}
    wrong_flags: list = [f for f in flags if f not in allowed_flags]
    if len(wrong_flags) > 0:
        print(FLAG_ERR + wrong_flags[0])
        exit(-1)

    # active flags
    enable_verbose: bool = any(f for f in flags if f == "-v")
    print_output: bool = any(f for f in flags if f == "-p")
    include_all_extensions: bool = any(f for f in flags if f == "-A")

    # verify trueargs existence
    trueargs: list = [a for a in args if not a.startswith("-")]
    if include_all_extensions:
        match len(trueargs):
            case 1:
                trueargs.insert(0, ALL_EXTENSIONS)
            case 2:
                trueargs[0] = ALL_EXTENSIONS
            case _:
                print(USAGE)
                exit(-1)
    if len(trueargs) < MIN_ARGS or len(trueargs) > MAX_ARGS:
        print(CMD_ERR)
        exit(-2)

    extension: str = (
        trueargs[0].replace(".", "") if trueargs[0].startswith(".") else trueargs[0]
    )

    source: str = trueargs[1]
    destination: str = trueargs[2] if len(trueargs) == MAX_ARGS else getcwd()

    if not exists(source):
        print(EXIST_ERR + str(source))
        exit(-3)
    if not exists(destination):
        print(EXIST_ERR + str(destination))
        exit(-3)
    if not isdir(destination):
        print(DIR_ERR + str(destination))
        exit(-4)

    source = str(normpath(abspath(expanduser(source))))
    destination = str(normpath(abspath(expanduser(destination))))

    files: list = filter_ext(source, extension, verbose=enable_verbose)
    files.sort()

    sourcepath: list = source.split(SEPARATOR)
    # if present, remove the tailing '/'
    if source.endswith(SEPARATOR):
        sourcepath.pop()

    filename: str = (
        sourcepath.pop() + f"-{extension}-output.txt"
        if not include_all_extensions
        else sourcepath.pop() + "-output.txt"
    )

    join_to_text(
        files, dest=destination, outputfile=filename, print_output=print_output
    )

    print(f" - Successfully created output file in {destination}!")
    exit(0)


# just a wrapper for scan_dir()
def filter_ext(path: str, extension: str, verbose=False) -> list:
    files = []
    if verbose:
        if extension == ALL_EXTENSIONS:
            print(f" scanning files in: {path}...")
        else:
            print(f"filtering .{extension} files in: {path}")
    scan_dir(path, extension, files, verbose)
    return files


def scan_dir(path, extension, files, verbose):
    msg: str
    if isfile(path) and (extension in path.split(".") or extension == ALL_EXTENSIONS):
        msg = f" -> file found!: {path}"
        files.append(path)
    elif isdir(path):
        msg = f" scanning... {path}"
        nothidden = [f for f in listdir(path) if not str(f).startswith(".")]
        for file in nothidden:
            scan_dir(join(path, file), extension, files, verbose)
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
                f" - Output:\n-------------------------------------------------------------\n{readfile.read()}"
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
