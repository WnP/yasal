# yasal - Yet Another Save As Link

## Description

Saves an internet link externally as a Windows Shortcut File `*.url` a UNIX Desktop file `*.desktop`

yasal is mostly inspirated by the firefox plugin [SaveLink](https://addons.mozilla.org/en-US/firefox/addon/savelink/)

`.desktop` file are named with the given url page title,
the output file will be placed in the same folder if not specified

## Usage

```
usage: yasal [-h] [-f FILE | -r RECURSIVE] [-o OUT] [-i]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  specify file FILE to be convert
  -r RECURSIVE, --recursive RECURSIVE
                        recursive mode, will convert all .url file in
                        directory RECURSIVE
  -o OUT, --out OUT     specify output directory OUT for .desktop files
  -i, --icontexthtml    set the .desktop icon field to 'text-html' default is
                        'firefox'
```

## Examples

convert a single file, result is stored in the input file same directory:

```
yasal -f /path/to/file.url
```

convert all files in a given folder and store result in another given folder:

```
yasal -r /path/to/folder -o /path/to/result/folder
```
