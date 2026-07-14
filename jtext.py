import sys
from os import listdir, getcwd, sep
from os.path import expanduser, isdir, isfile, exists, join, abspath, normpath


def main(args: list):

    CMD_ERR = "unrecognized args, for more information: python jtext.py -h"
    USAGE = """usage: [python | python3] jtext [OPTIONS] <ext> <src> [<dest>]
        OPTIONS:
            -h print this message
            -v verbose
            -p print the output of the command to the console

        - ext: file extension to filter
        - src: path to the project to convert
        - dest: path to the destination directory of the output

        e.g.: python jtext '.java' 'path/to/java/project' 'path/to/destination/folder'"""

    EXIST_ERR = " error: no file exists at the specified path\n -> "
    DIR_ERR = " path not allowed: The specified path must point to a directory\n -> "
    FLAG_ERR = " unrecognized flag: "
    MIN_ARGS: int = 2
    MAX_ARGS: int = 3
    SEPARATOR: str = sep

    flags: list = [a for a in args if a.startswith("-")]
    if "-h" in flags:
        print(USAGE)
        exit(0)
    allowed_flags = ["-p", "-v"]
    wrong_flags: list = [f for f in flags if f not in allowed_flags]
    if len(wrong_flags) > 0:
        print(FLAG_ERR + wrong_flags[0])
        exit(-1)

    # active flags
    verbose: bool = any(f for f in flags if f == "-v")
    printf: bool = any(f for f in flags if f == "-p")

    # verify trueargs existence
    trueargs: list = [a for a in args if not a.startswith("-")]
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

    files: list = filter_ext(source, extension, verbose=verbose)
    files.sort()

    sourcepath: list = source.split(SEPARATOR)
    # if present, remove the tailing '/'
    if source.endswith(SEPARATOR):
        sourcepath.pop()

    filename: str = sourcepath.pop() + f"-{extension}-output.txt"

    join_to_text(files, SEPARATOR, dest=destination, output=filename, printf=printf)

    print(f" - Successfully created output file in {destination}!")
    exit(0)


# just a wrapper for scan_dir()
def filter_ext(path: str, extension: str, verbose=False) -> list:
    files = []
    scan_dir(path, extension, files, verbose)
    return files


def scan_dir(path, extension, files, verbose):
    msg: str
    if isfile(path) and extension in path.split("."):
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
    files: list, separator: str, dest=getcwd(), output="output.txt", printf=False
):
    with open(join(dest, output), "w", encoding="utf-8") as createfile:
        createfile.write("")
    with open(join(dest, output), "a", encoding="utf-8") as appendfile:
        for file in files:
            with open(file, "r", encoding="utf-8") as readfile:
                contents = readfile.read()
                format = f"\nfile: {file.split(separator).pop()}\nfull path: {file}\n\n{contents}\n"
                appendfile.write(format)
    if printf:
        with open(join(dest, output), "r", encoding="utf-8") as readfile:
            print(f" - Output:\n{readfile.read()}")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except BrokenPipeError:
        sys.stdout.close()
        exit(0)
    except KeyboardInterrupt:
        sys.stdout.close()
        exit(0)
