# Dockerfile for building DawBio2 M14 Bio Development Image
# -----------------------------------------------------------------------------
# Tutorial:       https://geekflare.com/dockerfile-tutorial/
# Best practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# Reference:      https://docs.docker.com/engine/reference/builder/

# Clean previous: docker container stop -t 1 bio
#                 docker container rm bio
#                 docker image     rm bio

# Build Cmdline:  docker image     build --tag IMAGE-NAME:TAG --file Dockerfile     .
# Example:        docker image     build --tag bio            --file dev.Dockerfile .
# Beware:         The dot at the end is the build context.

# Run:            docker container run   -it --name bio --mount src=DIR_OUTSIDE,target=DIR_INSIDE,type=bind bio bash
# Example:        docker container run   -it --name bio --mount src='/home/alumne/dawbio/m14/uf2/code/',target='/bio',type=bind bio bash
# Note:           Directories must be absolute paths

# VSCode:         Remember to install Python extensions in each container.



# TODO
# -----------------------------------------------------------------------------

# - IMPORTANT: Remove your path from the docker run -it example

# - Add user? That would be great for matching it to the host user! Cumbersome...
# - https://jtreminio.com/blog/running-docker-containers-as-current-host-user/

# - VSCode solution:
# - https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user

# - Do I need to configure sudo inside the docker?
# - No, but it's an option...




# Commands for building the development image
# -----------------------------------------------------------------------------

# Set the base image to Ubuntu latest LTS
FROM ubuntu

# Temporary environment variables so that apt does not complain
# https://github.com/phusion/baseimage-docker/issues/319
ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NOWARNINGS="yes"

# Apt: Update the repository sources list, install apt-utils (complains otherwise) and upgrade packages
# 'apt-get' has a stable CLI interface. Do not use 'apt' as it does not.
RUN apt-get update
RUN apt-get install -y apt-utils
RUN apt-get upgrade -y

# Basic system utilities
RUN apt-get install -y dialog nano tree zip git sqlite3 curl lynx

# Python packages. python3 is already installed but write it for completeness.
RUN apt-get install -y python3 python3-venv python3-pip python-is-python3

# Python configs
ENV PYTHONDONTWRITEBYTECODE=1


# Python Virtual Environments
# -----------------------------------------------------------------------------

# 1. About virtual environments
# - Docker isolates already everything. Theoretically we don't need envs.
# - But there can be still conflicts with system packages, so it's good to use them.
#   (When using pip as a root, pip advises you to use venv.)

# 2. Conda
# - We can use conda, but venv + pip is lighter, usually used on dockers.
# - https://docs.python.org/3/library/venv.html

# 3. Venv + pip: Dockerfile automatic method
# - https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# - Simple, but VSCode, Jupyterlab fail to realise there is a venv.
#   Those default to the system python and cannot find your packages. Discarded.

    # Set path
    # ENV VIRTUAL_ENV=/opt/bio-venv
    # RUN python -m venv $VIRTUAL_ENV
    # ENV PATH="$VIRTUAL_ENV/bin:$PATH"

    # Install python dependencies
    # COPY requirements.txt /
    # RUN  pip install -Ur requirements.txt
    # RUN  rm /requirements.txt

# 4. Venv + pip: Manual method from terminal
# - For development you can set it up manually.
# - For deployment, make your script point to the python in the venv (@hashbang)

    # Create and activate environment:
    # /bin/python -m venv /bio/bio-env
    # source /bio/bio-env/bin/activate

    # Install libs into the environment
    # pip install -Ur /bio/0-configs/2-python/requirements.txt

    # How to deactivate the environment
    # deactivate



# Additional commands for app deployment
# -----------------------------------------------------------------------------

# Expose a port to communicate
# EXPOSE 8080

# Create the default app directory
# RUN mkdir -p /app

# Copy the application
# COPY . /app/

# Run the application:
# WORKDIR /app/
# CMD ["python", "app.py"]

# -----------------------------------------------------------------------------

