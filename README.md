
# ssh-copy-id

A Python implementation of [ssh-copy-id](https://linux.die.net/man/1/ssh-copy-id) that works on **ALL** platforms.

## Dependencies

[Fabric](http://www.fabfile.org/) : A Python (2.5-2.7) library and command-line tool for streamlining the use of SSH for application deployment or systems administration tasks.
```
pip install fabric
```

## Usage

```
ssh-copy-id.py [-h] [-i [IDENTITY_FILE]] [-p [PORT]] [user@]machine
```

For Windows users, there is a pre-built *exe* executable file (only tested on Windows 7 64-bit) under ```dist```.

## License
MIT License &copy; Zhengyi Yang


