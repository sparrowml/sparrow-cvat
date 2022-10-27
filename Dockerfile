FROM python:3.9

RUN SNIPPET="export PROMPT_COMMAND='history -a' && export HISTFILE=/commandhistory/.bash_history" && echo $SNIPPET >> "/root/.bashrc"

RUN apt update -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y tzdata
RUN apt install -y \
    build-essential \
    curl \
    git

# Allow root for Jupyter notebooks
RUN mkdir /root/.jupyter
RUN echo "c.NotebookApp.allow_root = True" > /root/.jupyter/jupyter_notebook_config.py

CMD mkdir -p /code
WORKDIR /code
RUN mkdir sparrow_cvat && \
  touch sparrow_cvat/__init__.py
COPY setup.cfg .
COPY setup.py .
RUN pip install -e .
ADD . .

ENTRYPOINT [ "make" ]