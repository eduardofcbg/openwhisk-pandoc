FROM python:3.8.2-buster

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install texlive-full -qy

RUN wget https://github.com/jgm/pandoc/releases/download/2.9.2.1/pandoc-2.9.2.1-1-amd64.deb && \
	dpkg -i pandoc-2.9.2.1-1-amd64.deb && \
	rm pandoc-2.9.2.1-1-amd64.deb

RUN apt-get autoremove -y && \
	apt-get clean && \
	rm -rf /var/cache/* && \
	rm -rf /var/tmp/* && \
	rm -rf /tmp/* && \
	rm -rf /root/.npm && \
	rm -rf /root/.cache

RUN groupadd -r pandoc && useradd -r -g pandoc pandoc

ADD src /

RUN pip install -r requirements.txt

EXPOSE 8080

CMD [ "python", "/main.py" ]
