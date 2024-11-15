# GTFOBin: expect

## Shell

It can be used to break out from restricted environments by spawning an interactive system shell.

```
expect -c 'spawn /bin/sh;interact'
```

## File read

It reads data from files, it may be used to do privileged reads or disclose files outside a restricted file system.

The file is read and parsed as an `expect` command file, the content of the first invalid line is returned in an error message. Thus, this might not be suitable to read arbitrary binary files.

```
LFILE=file_to_read
expect $LFILE
```

## SUID

If the binary has the SUID bit set, it does not drop the elevated privileges and may be abused to access the file system, escalate or maintain privileged access as a SUID backdoor. If it is used to run `sh -p`, omit the `-p` argument on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

```
sudo install -m =xs $(which expect) .

./expect -c 'spawn /bin/sh -p;interact'
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

```
sudo expect -c 'spawn /bin/sh;interact'
```