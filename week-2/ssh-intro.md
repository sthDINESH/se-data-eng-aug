# Intro to SSH

- Secure SHell
- protocol allows to connect securely to the shell of remote server
- works on port 22
- core offering of most OS

## What is SSH?

SSH (Secure Shell) is a secure way to connect to and control a remote computer over the internet.

- **Port**: 22 (default)
- **Security**: Uses encryption to protect data
- **Use cases**: Remote server access, file transfer, automated scripts

## How does it work?

SSH uses **key-pair encryption** for secure authentication:

- **Public Key** - Like a mailbox (you share this with the server)
- **Private Key** - Like the mailbox key (keep this secret on your local machine!)

### Connection Process:
1. Server has your public key
2. Your private key proves you're the legitimate owner
3. Connection is encrypted both ways

## Basic Commands

```bash
# Connect to remote server
ssh username@hostname

# Connect on specific port
ssh -p 2222 username@hostname

# Generate SSH key pair
ssh-keygen -t rsa -b 4096

# Copy public key to server
ssh-copy-id username@hostname

# Run command on remote server
ssh username@hostname "command"

# Transfer file to remote
scp file.txt username@hostname:/path/

# Transfer file from remote
scp username@hostname:/path/file.txt ./
```

## Key Points

- ✓ More secure than passwords
- ✓ No typing passwords every time (after setup)
- ✓ Industry standard for server access
- ✓ Works on Linux, Mac, Windows (modern versions)