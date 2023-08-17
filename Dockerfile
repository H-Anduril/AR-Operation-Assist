FROM python:3.9-alpine

WORKDIR /usr/src/app

EXPOSE 1433

COPY requirements.txt ./

RUN \
    apt-get update && \
    apt-get install -y gcc xterm ffmpeg libsm6 libxext6 unixodbc unixodbc-dev x11-xserver-utils curl apt-transport-https && \
    apt-get install -y freetds-dev freetds-bin tdsodbc iproute2 iputils-ping telnet libc6 libgs10 ghostscript && \
    apt-get install --reinstall -y build-essential
    
RUN curl https://packages.microsoft.com/keys/microsoft.asc | tee /etc/apt/trusted.gpg.d/microsoft.asc

RUN curl https://packages.microsoft.com/config/debian/11/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

RUN echo "[FreeTDS]\n\
Description = FreeTDS Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


RUN apt-get update && ACCEPT_EULA=Y apt-get install -y mssql-tools
RUN echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
RUN . ~/.bashrc

RUN echo MinProtocol = TLSv1.0 >> /etc/ssl/openssl.cnf
RUN echo CipherString = DEFAULT@SECLEVEL=1 >> /etc/ssl/openssl.cnf

ENV DISPLAY=host.docker.internal:0.0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /usr/src/app/src

CMD ["python", "tkFramework.py"]