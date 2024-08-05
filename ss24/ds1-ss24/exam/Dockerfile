FROM jupyter/minimal-notebook
# Install essential Python packages
RUN python3 -m pip --no-cache-dir install \
   pandas \
   seaborn \
   numpy \
   scipy \
   scikit-learn \
   matplotlib \
   geopy \
   openpyxl
RUN pip install git+https://github.com/sinzlab/dsplotter.git
