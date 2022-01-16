FROM python
WORKDIR /home
COPY bin ./bin
COPY utils ./utils
COPY requirements.txt .
COPY main.py .
RUN pip install -r requirements.txt
VOLUME data
CMD [ "python", "/home/main.py"]