name = "flatpak"

__version__ = "1.10.2"
version = __version__ + "+local.1.0.0"

variants = [["os-centos-7", "arch-x86_64"]]

relocatable = False

build_requires = [
    "libostree",  # https://github.com/j0yu/rez-libostree
    "python-3",  # https://github.com/j0yu/rez-python
    "git-2",  # https://github.com/j0yu/rez-git
]

build_command = r"""
set -euf -o pipefail

cp "$REZ_BUILD_SOURCE_PATH"/Dockerfile "$REZ_BUILD_SOURCE_PATH"/entrypoint.sh .

IMAGE_ID_FILE="$(readlink -f DockerImageID)"
# In rez resolved version:
# - REZ_OS_MAJOR_VERSION = centos
# - REZ_OS_MINOR_VERSION = 7
docker build --rm \
    --build-arg CENTOS_MAJOR="$REZ_OS_MINOR_VERSION" \
    --iidfile "$IMAGE_ID_FILE" \
    "$REZ_BUILD_PATH"


echo "PKG_CONFIG_PATH=$PKG_CONFIG_PATH"
[ -t 1 ] && CONTAINER_ARGS=("--tty") || CONTAINER_ARGS=()
CONTAINER_ARGS+=("--env" "INSTALL_DIR={install_dir}")
CONTAINER_ARGS+=("--env" "VERSION={version}")
CONTAINER_ARGS+=("--env" REZ_LIBOSTREE_ROOT="$REZ_LIBOSTREE_ROOT")
CONTAINER_ARGS+=("--env" REZ_PYTHON_ROOT="$REZ_PYTHON_ROOT")
CONTAINER_ARGS+=("--env" REZ_GIT_ROOT="$REZ_GIT_ROOT")
CONTAINER_ARGS+=("--env" PKG_CONFIG_PATH="$PKG_CONFIG_PATH")
CONTAINER_ARGS+=("--volume" "$REZ_LIBOSTREE_ROOT":"$REZ_LIBOSTREE_ROOT":ro)
CONTAINER_ARGS+=("--volume" "$REZ_GIT_ROOT":"$REZ_GIT_ROOT":ro)
CONTAINER_ARGS+=("--volume" "$REZ_PYTHON_ROOT":"$REZ_PYTHON_ROOT":ro)
CONTAINER_ARGS+=("$(cat $IMAGE_ID_FILE)")


if [ $REZ_BUILD_INSTALL -eq 1 ]
then
    CONTAINER_ID=$(docker create "{CONTAINER_ARGS}")
    docker start -ia "$CONTAINER_ID"
    docker cp "$CONTAINER_ID":"{install_dir}"/. "{install_dir}"/
    docker rm "$CONTAINER_ID"
fi
""".format(
    version=__version__,
    install_dir="${{REZ_BUILD_INSTALL_PATH:-/usr/local}}",
    CONTAINER_ARGS="${{CONTAINER_ARGS[@]}}",
)


def commands():
    import os.path

    env.PATH.append(os.path.join("{root}", "bin"))
    env.XDG_DATA_DIRS.append(os.path.join("{root}", "share"))
    env.PKG_CONFIG_PATH.append(os.path.join("{root}", "lib", "pkgconfig"))


@late()
def tools():
    import os

    bin_path = os.path.join(str(this.root), "bin")
    executables = []
    for item in os.listdir(bin_path):
        path = os.path.join(bin_path, item)
        if os.access(path, os.X_OK) and not os.path.isdir(path):
            executables.append(item)
    return executables
