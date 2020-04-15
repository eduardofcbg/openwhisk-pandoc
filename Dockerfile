FROM python:3.6

RUN apt-get update -qy && \
    apt-get upgrade -qy && \
    apt-get install pandoc texlive-full -qy && \
    apt-get autoremove -y && \
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
