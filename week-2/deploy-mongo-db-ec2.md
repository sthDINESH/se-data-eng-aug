# Steps to deploy MongoDB on an AWS EC2 instance

## Starting an AWS EC2 instance

1. Open the **EC2** service in the AWS Console and select **Launch instance**.
![Launch EC2 instance](../images/aws-ec2-launch-instance.png)
2. Give the instance a name, such as `se-dinesh-mongo-server`.
![EC2 instance name](../images/aws-ec2-instance-name.png)
3. Choose an Amazon Machine Image (AMI), for example **Ubuntu Server 24.04 LTS**.
![EC2 AMI selection](../images/aws-ec2-select%20ami.png)
4. Select the `t3.micro` instance type.
![EC2 instance type](../images/aws-ec2-instance-type.png)
5. Create or select an SSH key pair. See [Steps to create and add an SSH key pair](#steps-to-create-and-add-an-ssh-key-pair).
![EC2 key pair](../images/aws-ec2-key-pair.png)
6. Under **Network settings**, create or select a security group. See [Steps to create a security group](#steps-to-create-a-security-group).
![EC2 security group](../images/aws-ec2-sg.png)
7. Keep the default storage settings unless the application needs more disk space.
8. Review the configuration and select **Launch instance**.
9. Wait until the instance state is **Running**, then copy its public IPv4 address.

## Connect to the instance from macOS or Linux with:

```bash
# Restrict access to the private key so SSH accepts it
chmod 400 path/to/key.pem
# Connect to the EC2 instance using the private key and public IP address
ssh -i path/to/key.pem ubuntu@PUBLIC_IP
```

Replace `path/to/key.pem` with the path to your private key and `PUBLIC_IP` with the instance's public IPv4 address. 
For Amazon Linux AMIs, use `ec2-user` instead of `ubuntu`.

## Steps to create and add an SSH key pair

1. In the **Key pair name** section, select **Create new key pair**.
2. Enter a descriptive name, such as `se-dinesh-mongo-key`.
3. Select **RSA** or **ed25519** as the key pair type and `.pem` as the private key file format.
4. Select **Create key pair**. AWS downloads the private key file once.
5. Move the `.pem` file to a secure location. Never commit it to Git or share it.
6. Restrict the file permissions on macOS or Linux:

	```bash
	# Restrict access to the private key so SSH accepts it
	chmod 400 path/to/key.pem
	```

7. Select this key pair when launching the EC2 instance. The matching private key is required for SSH access.

## Steps to create a security group

1. In **Network settings**, select **Create security group** or select **Edit** beside the existing security-group settings.
2. Enter a descriptive security-group name, such as `se-dinesh-mongo-sg`.
3. Add the following inbound rules:

	| Type | Protocol | Port | Source | Purpose |
	| --- | --- | ---: | --- | --- |
	| SSH | TCP | 22 | My IP | Secure administration |
	| MongoDB | TCP | 27017 | My IP | Database access |

4. Keep the default outbound rule unless your networking requirements are different.
5. Select **Launch instance** after confirming the rules.

SSH should be restricted to **My IP** wherever possible. HTTP is public so that a web server can receive traffic. Do not expose MongoDB's default port `27017` to the public internet; if remote database access is required, restrict it to a trusted security group or IP range.

## Steps to update linux on EC2 instance

Run these commands after connecting to the Ubuntu EC2 instance:

```bash
# Refresh the list of available packages and security updates
sudo apt update -y

# Install available package updates
sudo apt upgrade -y
```

- `sudo` runs the command with administrator privileges.
- `apt` is Ubuntu's package manager.
- `-y` automatically confirms the prompts.

## Steps to install MongoDB Community Edition 

These steps install MongoDB 8.0 Community Edition on Ubuntu 24.04 (Noble) using MongoDB's official APT repository.

Source: [MongoDB Community Edition installation guide for Ubuntu](https://www.mongodb.com/docs/v8.0/tutorial/install-mongodb-on-ubuntu/)

> These commands assume that you are connected to the EC2 instance over SSH and are using a 64-bit Ubuntu 24.04 installation.

### 1. Install prerequisites

Install `curl` to download the repository key and `gnupg` to process it:

```bash
sudo apt-get install -y gnupg curl
```

- `curl` downloads the MongoDB signing key from the internet.
- `gnupg` provides tools to process and verify cryptographic signing keys.

### 2. Import MongoDB's public signing key

GPG (GNU Privacy Guard) is a tool that uses public-key cryptography to sign and verify files and software packages. MongoDB signs its packages with a private key, while this public key lets APT verify that the packages came from MongoDB and were not altered in transit. Without the key, Ubuntu cannot safely trust the MongoDB repository.

```bash
curl -fsSL https://pgp.mongodb.com/server-8.0.asc | \
	sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
	--dearmor
```

Breakdown:

- `curl` downloads MongoDB's public signing key.
- `-f` makes `curl` fail if the server returns an HTTP error.
- `-s` runs quietly, while `-S` still displays errors.
- `-L` follows redirects if the download URL changes location.
- `|` sends the downloaded key to `gpg` instead of saving it as a text file first.
- `gpg` manages and verifies cryptographic keys.
- `--dearmor` converts the ASCII-armored key into the binary format used by APT.
- `-o /usr/share/keyrings/mongodb-server-8.0.gpg` saves the converted key in Ubuntu's keyring directory.
- `sudo` gives `gpg` permission to write to that protected directory.

In short, this downloads MongoDB's public key, converts it to APT's required format, and stores it so Ubuntu can verify packages from the official repository.

### 3. Add the MongoDB APT repository

This tells Ubuntu where to find the MongoDB 8.0 packages for Ubuntu 24.04:

```bash
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | \
	sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
```

`tee` is a standard Unix command that reads input and writes it to a file. Here, it receives the repository definition through the pipe and writes it to `/etc/apt/sources.list.d/mongodb-org-8.0.list`. `sudo` gives it permission to write in the protected APT directory.

### 4. Reload package information

```bash
sudo apt-get update
```

### 5. Install MongoDB Community Edition

```bash
sudo apt-get install -y mongodb-org
```

The `mongodb-org` package installs the MongoDB server, configuration files, shell, and supporting components.

### 6. Start, enable, and check MongoDB

```bash
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
```

`start` runs MongoDB, `enable` starts it automatically after a reboot, and `status` should show `active (running)`. If the service cannot be found, reload systemd and start it again:

```bash
sudo systemctl daemon-reload
sudo systemctl start mongod
```

You can connect locally with:

```bash
mongosh
```

## Allow trusted external connections

MongoDB binds to `127.0.0.1` by default, so it accepts connections from the EC2 instance but not other machines. To allow a trusted external client, add the EC2 instance's private IP address to its configuration.

1. Find the EC2 instance's private IP address:

	```bash
	hostname -I
	```

2. Open the MongoDB configuration file:

	```bash
	sudo nano /etc/mongod.conf
	```

3. Find the `net` section:

	```yaml
	net:
	  port: 27017
	  bindIp: 127.0.0.1
	```

4. Add the private IP address returned by `hostname -I`:

	```yaml
	net:
	  port: 27017
	  bindIp: 127.0.0.1,PRIVATE_IP
	```

	Keeping `127.0.0.1` preserves local access. The private IP allows connections through the EC2 network interface.

5. Save and close `nano`:

	- Press `Ctrl+O`, then press `Enter` to save.
	- Press `Ctrl+X` to exit.

6. Restart MongoDB and check its status:

	```bash
	sudo systemctl restart mongod
	sudo systemctl status mongod
	```

7. Update the EC2 security group to allow port `27017` only from a trusted application security group or IP address. Never allow `0.0.0.0/0`.

Do not expose MongoDB externally without authentication. Avoid using `bindIp: 0.0.0.0` unless it is required and properly secured. Consult the [MongoDB security checklist](https://www.mongodb.com/docs/v8.0/administration/security-checklist/) before allowing remote access.

## Connection URI

The MongoDB server is running on EC2, not in MongoDB Atlas. To connect from a MongoDB client such as `mongosh`, Compass, or a Python application, use the EC2 instance's **public IPv4 address** and port `27017`:

```text
mongodb://PUBLIC_IP:27017/
```

Replace `PUBLIC_IP` with the address shown in the EC2 console. If authentication is enabled, use a database user rather than an unauthenticated URI:

```text
mongodb://USERNAME:PASSWORD@PUBLIC_IP:27017/?authSource=admin
```

The security group must allow TCP port `27017` from the connecting client's IP, and MongoDB must be bound to the EC2 private IP. Do not commit a URI containing a real password to Git or share it publicly.

MongoDB Atlas is a separate managed hosting service, so an Atlas connection string such as `mongodb+srv://...` connects to an Atlas cluster, not this EC2 server. Use the standard `mongodb://` URI above for this self-managed MongoDB instance.


