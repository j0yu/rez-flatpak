#!/bin/bash
set -euf -o pipefail

# Perform the actual Python building and installing
# Ideally we're currently in an empty directory
INSTALL_DIR="${INSTALL_DIR:-$(mktemp -d)}"
VERSION="${VERSION:-1.10.2}"
URL=https://github.com/flatpak/flatpak.git
mkdir -vp "$INSTALL_DIR"

CURL_FLAGS=("-L")
[ -t 1 ] && CURL_FLAGS+=("-#") || CURL_FLAGS+=("-sS")

export PATH="$PATH":"$REZ_PYTHON_ROOT"/bin:"$REZ_GIT_ROOT"/bin
"$REZ_PYTHON_ROOT"/bin/python3 -m pip install pyparsing
echo "               git cloning: $URL"
echo "    into current directory: $(pwd)"
git clone --branch="$VERSION" "$URL" .

./autogen.sh
./configure --prefix="$INSTALL_DIR" --with-system-install-dir=/var/lib/flatpak
LD_RUN_PATH='$ORIGIN:$ORIGIN/../lib':"$REZ_LIBOSTREE_ROOT"/lib make
make install
