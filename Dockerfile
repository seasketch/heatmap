FROM perrygeo/gdal-base:latest as base

# Copy source code and scripts into container

COPY lib /work/lib
COPY scripts /work/scripts
COPY tests /work/tests
COPY setup.py /work/setup.py
COPY setup.cfg /work/setup.cfg
COPY LICENSE /work/LICENSE
COPY README.md /work/README.md
COPY requirements.txt /work/requirements.txt
COPY requirements_dev.txt /work/requirements_dev.txt

WORKDIR /work/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN python -m pip install cython numpy -c requirements.txt
RUN python -m pip install --no-binary fiona,rasterio,shapely -r requirements.txt
RUN pip uninstall cython --yes

RUN pip install -r requirements_dev.txt
RUN echo "export PATH=/work/scripts:${PATH}" >> /root/.bashrc
RUN /work/scripts/setup_heatmap

# Start in projects directory
WORKDIR /projects/