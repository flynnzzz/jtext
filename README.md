# jtext

`jtext` is a lightweight Python utility that recursively scans a directory for files with a given extension and combines their contents into a single text file.
It was primarily designed to prepare codebases for LLMs, making it easy to provide an entire project (or selected parts of it) as a single prompt for code review, explanation, refactoring, documentation, or other AI-assisted development tasks.
It can also find it's use in backups.

## Requirements

* Python 3.x

## Usage

```bash
python jtext.py [OPTIONS] <ext> <src> [<dest>]
# or
python3 jtext.py [OPTIONS] <ext> <src> [<dest>]
```

### Options

| Option | Description                              |
| ------ | ---------------------------------------- |
| `-h`   | Display the help message and exit.       |
| `-v`   | Enable verbose output.                   |
| `-p`   | Print the generated text to the console. |

### Args

| Argument   | Description                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| `<ext>`    | File extension to include. The leading `.` can be freely omitted.                                                   |
| `<src>`    | Path to the source directory to scan recursively.                                                      |
| `[<dest>]` | Optional destination directory for the output file. If omitted, the current working directory is used. |

## Examples

Convert all Java files in a project:

```bash
python3 jtext.py .java path/to/java/project
```

Save the output to a specific directory:

```bash
python3 jtext.py .java path/to/java/project path/to/output
```

Enable verbose mode and print the generated text:

```bash
python3 jtext.py -v -p py path/to/python/project
```
