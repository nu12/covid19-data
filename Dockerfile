FROM python:3.7

RUN pip install pandas

WORKDIR /app

COPY entrypoint.sh /

ENTRYPOINT [ "/entrypoint.sh" ]