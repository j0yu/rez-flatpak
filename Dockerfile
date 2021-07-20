FROM centos:7

RUN yum install -y yum-utils make epel-release file \
    && yum-builddep -y flatpak \
    && yum clean all
WORKDIR /usr/local/src
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]