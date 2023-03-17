FROM python:3.8

ARG USER=dev
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN apt update -y && apt install -y sudo
RUN groupadd --gid $USER_GID $USER && \
    useradd --uid $USER_UID --gid $USER_GID -m $USER && \
    echo ${USER} ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/${USER} && \
    chmod 0440 /etc/sudoers.d/${USER} && \
    chsh ${USER} -s /bin/bash

RUN mkdir -p /commandhistory
RUN chown -R ${USER} /commandhistory

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" && \
  echo $SNIPPET >> "/home/${USER}/.bashrc"

RUN apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y \
    build-essential \
    curl \
    ffmpeg \
    git \
    libgl1-mesa-glx \
    libsm6 \
    libxext6

# Allow root for Jupyter notebooks
RUN mkdir /root/.jupyter
RUN echo "c.NotebookApp.allow_root = True" > /root/.jupyter/jupyter_notebook_config.py

USER ${USER}

CMD mkdir -p /code
WORKDIR /code
RUN mkdir sparrow_cvat && \
  touch sparrow_cvat/__init__.py
COPY setup.cfg .
COPY setup.py .
RUN pip install -U pip
RUN pip install -e .
ADD . .

ENTRYPOINT [ "make" ]