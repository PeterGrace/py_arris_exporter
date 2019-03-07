FROM alpine:latest
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-static-amd64 /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN mkdir /app \
 && apk --update add python3 py3-pip
WORKDIR /app
ADD . /app/
RUN pip3 install -e .

CMD /app/entrypoint.sh
