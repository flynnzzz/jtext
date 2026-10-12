# jtext

`jtext` is a lightweight Python utility that recursively scans a directory for files with a given list of extensions and combines their contents into a single text file.

It was primarily designed to prepare codebases for LLMs, making it easy to provide an entire project (or selected parts of it) as a single prompt for code review, explanation, refactoring, documentation, or other AI-assisted development tasks.

## Requirements

* Python 3.x

## Usage

```bash
python jtext.py [OPTIONS] [%ext] <src> [dest]
```

### Options

| Option | Description                              |
| ------ | ---------------------------------------- |
| `-h`   | Display the help message and exit.       |
| `-v`   | Enable verbose output.                   |
| `-p`   | Print the generated text to the console. |
| `-i`   | Include hidden files. |
| `-a`   | Append the output to a file. |

### Args

| Argument   | Description                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------ |
| `[%ext]`    | File extension to include prefixed with '%'. The entire project will be converted if it's omitted.                                                    |
| `<src>`    | Path to the source directory to scan recursively.                                                      |
| `[dest]` | Optional destination for the output file. If omitted, the current working directory and default name is used. |

## Examples

Convert all Java files in a project:

```bash
python jtext.py %java path/to/java/project
```

Save the output to a specific file/directory:

```bash
python jtext.py %c %h path/to/c/project path/to/output
```

Enable verbose mode and print the generated text:

```bash
python jtext.py -v -p %py path/to/python/project
```
