FROM python:3.8.2-buster

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install texlive-full -qy

RUN wget https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-1-amd64.deb && \
    dpkg -i pandoc-2.9.2.1-1-amd64.deb && \
    rm pandoc-2.9.2.1-1-amd64.deb

RUN groupadd -r pandoc && useradd -r -g pandoc pandoc

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY src/ /src
WORKDIR /src

EXPOSE 8080

CMD [ "python", "main.py" ]
