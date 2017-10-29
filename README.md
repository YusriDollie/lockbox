# About
A work in progress epub file encryption tool

* prevents interception - confidentiality

# Building Instructions
To install dependencies and run tests the following instructions should be followed
* Requires Python 3
* Requires pip 3

## Installing Dependencies

```
make deps
```


## Quick Usage
Once dependancies have been built, simple navigate to lockbox/lock_box
and execute python3 locker.py
this will prompt you to select the mode of operation
either e to encrypt, d to decrypt or q to quit
sample input
```
Input mode (e)ncrypt (d)ecrypt (q)uit
e
Please enter path to file
some.epub
please enter Encryption pass phrase
password
```

## Running Tests

```
make test
```

## Running Type Checker and Linter

```
make -k check
```

The `-k` option instructs make to keep going even if the
linter and type checker fails. Need this to run all checks.

Alternatively, the linter can be run separately using:

```
make lint
```

The type checker can be run separately using:

```
make type_check
```


## Future Developments
* Add digital signing using file hash digest
* Add UI for ease of use
