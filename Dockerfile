## -*- dockerfile-image-name: "sideroxylon:latest" -*-

# Tested with podman
# podman build -t sideroxylon:latest .
# podman run --rm -v "$HOME:$HOME" -e HOME="$HOME" --name sideroxylon sideroxylon:latest

# You can pass args like this: podman run --rm -v "$HOME:$HOME" -e HOME="$HOME" sideroxylon:latest --version

# .bashrc alias:
# alias sideroxylon='podman run -v "$HOME:$HOME" -e HOME="$HOME" sideroxylon:latest'

# Note that if you use arguments those commands will be considered different containers
# (e.g. sideroxylon --help and sideroxylon --version would be different containers).

FROM python:3.13 as build
WORKDIR /sideroxylon

# Copy the metadata
# COPY pyproject.toml ./

# Copy the source
# COPY src ./src

# Copy all the files
COPY ./ ./

# Install the package
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir .

# Container entrypoint
ENTRYPOINT ["sideroxylon"]
