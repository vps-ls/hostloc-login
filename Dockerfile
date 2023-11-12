FROM vpsls/google-ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y tzdata

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install -y python3-pip

RUN useradd -ms /bin/bash ubuntu

USER ubuntu

RUN pip3 install --user urllib3 requests selenium pyyaml schedule

RUN cd /home/ubuntu && mkdir hostloc

WORKDIR /home/ubuntu/hostloc

ENTRYPOINT ["python3", "login.py"]