# lc
lc is a simple lambda calculus interpreter written in Python. It should be used as an intermediate language, except if you're a masochist and like programming in lambda calculus. It supports the following features:
 - functions (duh)
 - assignments
 - that's it

## Usage:
```bash
python lc.py --repl # for interactive repl
python lc.py test.lam # to read the file test.lam from this repo and run it
```

## todo:
 - actual compiler to make executables
 - better error messages
 - maybe type anotations as comments, and the compiler warns you if you're passing the wrong types
 - a way to import other files
 - some elementary functions (some of these can already be found in test.lam)
