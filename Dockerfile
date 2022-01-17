FROM python
WORKDIR /home
COPY utils ./utils
COPY requirements.txt .
COPY DbManager.py .
COPY main.py .
RUN pip install -r requirements.txt
VOLUME data
CMD [ "python", "/home/main.py"]