FROM python
WORKDIR /home
COPY utils ./utils
COPY requirements.txt .
COPY exceptions.py .
COPY DbManager.py .
COPY main.py .
RUN pip install -r requirements.txt
VOLUME data
ENTRYPOINT [ "python", "/home/main.py"]