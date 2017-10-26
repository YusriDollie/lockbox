# About
A work in progress epub file encryption tool

* prevents interception - confidentiality
* prevents tampering

# Building Instructions
To install dependencies and run tests the following instructions should be followed

## Installing Dependencies

```
make deps
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
