#HABUSHU_BUILDER_STAGE - HABUSHU GENERATED CODE (DO NOT MODIFY)
FROM docker.io/python:3.12 AS builder

# Install pipx
RUN python -m ensurepip --upgrade
RUN python -m pip install --user pipx
RUN python -m pip install opencv-python-headless

# Required installation for YOLO
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-pip git zip unzip wget curl htop libgl1 libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get install -y libsm6 libxext6

# Poetry and supporting plugin installations
RUN $HOME/.local/bin/pipx install poetry==2.0.1 && \
    $HOME/.local/bin/poetry self add poetry-plugin-bundle@1.5.0

WORKDIR /work-dir
COPY --chown=1001 /src ./example/src
COPY --chown=1001 /model ./example/model
COPY --chown=1001 /proto ./example/proto
COPY --chown=1001 pyproject.toml ./example
COPY --chown=1001 poetry.lock ./example
RUN find . -type f -name pyproject.toml -exec sed -i 's|develop[[:blank:]]*=[[:blank:]]*true|develop = false|g' {} \;

USER root
WORKDIR /work-dir/example
ENV POETRY_CACHE_DIR="/.cache/pypoetry"

# Install project on the image
RUN --mount=type=cache,target=${POETRY_CACHE_DIR}
RUN $HOME/.local/bin/poetry lock && \
    $HOME/.local/bin/poetry config virtualenvs.in-project true && \
    $HOME/.local/bin/poetry install

# Set KRAUSENING_BASE to point to the copied properties
ENV KRAUSENING_BASE="/work-dir/example/src/resources/krausening/base"

CMD /root/.local/bin/poetry run run_server
