# Local Support Code, Read Me

This file documents the functions available in `local_support_code`.

These functions were written for Jupyter (mostly). No promises that these functions will work in other 
environments.

## Setup / Installation

Clone this repository to local environment. Add the repository location to Jupyter's path. Discussion of Jupyter path 
[here](https://stackoverflow.com/questions/34976803/sys-path-different-in-jupyter-and-python-how-to-import-own-modules-in-jupyter).

**Create config file.**
```
$ ipython profile create
$ ipython locate
/Users/username/.ipython
```
**Edit the config file.**
```
$ cd /Users/username/.ipython
$ nano profile_default/ipython_config.py
```
Added to `ipython_config.py`, the following lines allow you to add your module path to `sys.path`.
```
c.InteractiveShellApp.exec_lines = [
    'import sys; sys.path.append("/path/to/your/module")'
]
```

## Available Functions

local_support_code.write_log_file(list, descriptive_text='text')


| Option          | Description |
|-----------------|-------------|
| **list** : | Required. A *list* that will be written to a log file. |
| **dir** : | Optional. Directory *text* give a location for the log file. |
| **descriptive_text** : | Optional. One or more lines of *text* that will be written above the log. Can be used to provide documentation of what is being logged. |

hello_word()

| Option          | Description |
|-----------------|-------------|
| None. | No arguments. Prints canonic "Hello world." To be used for testing purposes. |
