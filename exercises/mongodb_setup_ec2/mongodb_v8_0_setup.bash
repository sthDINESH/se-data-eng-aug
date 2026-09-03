#!/usr/bin/env bash

set -euo pipefail
# -e exits on command failure, -u catches unset variables, and pipefail
# catches failures in any command within a pipeline.

# Keep MongoDB version-specific paths together so they are easy to update.
MONGODB_VERSION="8.0"
MONGODB_KEYRING="/usr/share/keyrings/mongodb-server-${MONGODB_VERSION}.gpg"
MONGODB_REPOSITORY_FILE="/etc/apt/sources.list.d/mongodb-org-${MONGODB_VERSION}.list"

# Use sudo when the script is run by a normal user, but not when run as root.
# id -u returns the current user’s numeric ID.
# User ID 0 means the script is running as root.
if [[ "$(id -u)" -eq 0 ]]; then
	SUDO=""
else
	SUDO="sudo"
fi

# Stop early if the operating-system details cannot be read.
if [[ ! -f /etc/os-release ]]; then
	echo "Unable to identify the operating system." >&2
	exit 1
fi

# Load operating-system variables such as ID and VERSION_ID into this script.
# The values are used below to confirm that this is Ubuntu 24.04 before
# configuring the Ubuntu Noble MongoDB repository.
source /etc/os-release

# The repository below is specifically for 64-bit Ubuntu 24.04 (Noble).
if [[ "${ID}" != "ubuntu" || "${VERSION_ID}" != "24.04" ]]; then
	echo "This script supports Ubuntu 24.04 only." >&2
	exit 1
fi

# Refresh package information and install available Ubuntu updates.
echo "Updating Ubuntu packages..."
${SUDO} apt-get update -y
${SUDO} apt-get upgrade -y

# Install the tools needed to download and verify MongoDB's repository key.
echo "Installing repository prerequisites..."
${SUDO} apt-get install -y curl gnupg

# Download MongoDB's public key and convert it to APT's keyring format.
echo "Importing MongoDB ${MONGODB_VERSION} signing key..."
curl -fsSL "https://pgp.mongodb.com/server-${MONGODB_VERSION}.asc" | \
	${SUDO} gpg --dearmor --yes -o "${MONGODB_KEYRING}"

# Register the official MongoDB repository with APT.
echo "Adding MongoDB ${MONGODB_VERSION} APT repository..."
echo "deb [ arch=amd64,arm64 signed-by=${MONGODB_KEYRING} ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/${MONGODB_VERSION} multiverse" | \
	${SUDO} tee "${MONGODB_REPOSITORY_FILE}" > /dev/null

# Refresh package information again so APT can find MongoDB packages.
echo "Installing MongoDB Community Edition..."
${SUDO} apt-get update -y
${SUDO} apt-get install -y mongodb-org

# Add the EC2 private IP while keeping localhost access enabled.
PRIVATE_IP="$(hostname -I | awk '{print $1}')"
MONGODB_CONFIG="/etc/mongod.conf"
if [[ -z "${PRIVATE_IP}" ]]; then
	echo "Unable to determine the EC2 private IP address." >&2
	exit 1
fi

echo "Updating MongoDB network binding for ${PRIVATE_IP}..."
${SUDO} cp "${MONGODB_CONFIG}" "${MONGODB_CONFIG}.backup"
${SUDO} sed -i -E "s/^([[:space:]]*bindIp:).*/\1 127.0.0.1,${PRIVATE_IP}/" "${MONGODB_CONFIG}"

# Start MongoDB now and configure it to start after future reboots.
echo "Starting MongoDB..."
${SUDO} systemctl start mongod
${SUDO} systemctl enable mongod

# Confirm that the MongoDB service is active before reporting success.
if ${SUDO} systemctl is-active --quiet mongod; then
	echo "MongoDB is running successfully."
else
	echo "MongoDB failed to start. Check the service logs with:" >&2
	echo "  sudo journalctl -u mongod --no-pager -n 50" >&2
	exit 1
fi

echo "MongoDB is listening on its default port, 27017."
