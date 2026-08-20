@echo off
"C:\Windows\System32\OpenSSH\ssh.exe" -o UserKnownHostsFile=NUL -o StrictHostKeyChecking=no %*
