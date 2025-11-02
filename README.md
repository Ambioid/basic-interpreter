# Bassic Interpreter

## Inspiration

We took the theme of "legacy" rather literally and began looking into old programming languages, including briefly considering: writing a Jacquard Loom simulator and some programs in ALGOL68 (until we learned the GCC frontend had not been upstreamed yet). We then decided to try and write a compiler for a very outdated language.

## What it does

It was meant to take in any Minimal BASIC program written according to the ANSI X3.60-1978/ECMA-55 specifications, compile it to a basic bytecode, and execute it in a VM.

## How we built it

We started by writing out the BNF grammar and working on the Token list and lexer. We then began began work on the parser and AST, combining the products of the previous two steps. Then after this was mostly complete, making an interpreter/virtual machine to execute programs
