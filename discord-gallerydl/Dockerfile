FROM python:3

# ARG UNAME=dgdl
# ARG UID=1000
# ARG GID=1000
# RUN groupadd -g $GID -o $UNAME
# RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME
# USER $UNAME

WORKDIR /dgdl

COPY requirements.txt .
RUN pip install -r requirements.txt


COPY start.py .
COPY app app

CMD [ "python", "start.py" ]