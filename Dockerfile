FROM condaforge/miniforge3

RUN conda install --yes --freeze-installed \
    jupyterlab ipython numpy pandas fastapi flask python-keycloak uvicorn[standard] gunicorn &&\
    pip install tiledb pyzmq &&\
    conda clean -all -y -f &&\
    find ${CONDA_DIR} -follow -type f -name '*.a' -delete && \
    find ${CONDA_DIR} -follow -type f -name '*.pyc' -delete

WORKDIR /workdir

EXPOSE 8888

ENTRYPOINT ["jupyter-lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]

CMD ["--notebook-dir=/workdir"]
