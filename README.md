# llm-safe
A source code obfuscator, making code difficult/practically impossible for an LLM to parse.
The resulting obfuscated code is meant to still be completely usable and equivalent to the original code in functionality.
It is only rendered impossible to interpret for a human (or LLM) due to all linguistic words being replaced by gibberish.
However, it should compile just fine.

Currently, handles C, C++, Java, Python and PHP. (In accordance with the support of the tokenizer used: sctokenizer).
For any other file types, the program ignores them and just writes the exact copy of the file at the output location.

## Usage

Run the command:

```
llm-safe <PATH_TO_YOUR_DIRECTORY_OR_FILE>
```

This will read all files in the directory (or just the single file), and write the obfuscated versions
of each of them into an output folder ("obfus_output").

## IMPORTANT (Issues / Future Work)

Currently this is a very basic implementation that does not take into consideration a very major use-case,
which is that of libraries and references (i.e. anything that involves identifiers that are being used/defined
across multiple files). So as of now, if any include/import is used in a program, then the obfuscated version
would NOT work.

This is something that could be worked on as the next major improvement.