FROM perrygeo/gdal-base:latest AS base

# Copy source code and scripts into container

COPY lib /work/lib
COPY scripts /work/scripts
COPY setup.py /work/setup.py
COPY setup.cfg /work/setup.cfg
COPY LICENSE /work/LICENSE
COPY README.md /work/README.md
COPY requirements.txt /work/requirements.txt
# setup.py reads this for tests_require, so it must be present for the install below
COPY requirements_dev.txt /work/requirements_dev.txt

WORKDIR /work/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m pip install cython numpy -c requirements.txt
RUN python -m pip install --no-binary fiona,rasterio,shapely -r requirements.txt
RUN pip uninstall cython --yes

# Put scripts on PATH for non-interactive commands (docker run, make test) as well as
# for interactive shells
ENV PATH="/work/scripts:${PATH}"
RUN echo "export PATH=/work/scripts:${PATH}" >> /root/.bashrc
RUN /work/scripts/setup_heatmap

# Start in projects directory
WORKDIR /projects/

# Development image used by docker-compose, adds the test suite and dev dependencies
FROM base AS workspace

COPY tests /work/tests

WORKDIR /work/
RUN pip install -r requirements_dev.txt

WORKDIR /projects/
