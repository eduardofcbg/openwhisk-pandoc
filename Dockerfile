FROM python:3.8.2-buster

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install texlive-full -qy

RUN wget https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-1-amd64.deb && \
    dpkg -i pandoc-2.9.2.1-1-amd64.deb && \
    rm pandoc-2.9.2.1-1-amd64.deb

RUN groupadd -r pandoc && useradd -r -g pandoc pandoc

RUN mkdir /usr/local/share/fonts/macfonts && \
    git clone https://github.com/potyt/fonts /usr/local/share/fonts/macfonts

COPY requirements.txt /
RUN pip install -r requirements.txt

RUN pip install pandoc-fignos pandoc-eqnos pandoc-tablenos pandoc-secnos --user

COPY src/ /src
WORKDIR /src

EXPOSE 8080

CMD [ "python", "main.py" ]
