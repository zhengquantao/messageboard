FROM python:3.7

RUN mkdir /messageboard

WORKDIR /messageboard

EXPOSE 5000

COPY . /messageboard

RUN set -x \
      && apt-get update \
      && apt install -y  git curl openssh-client iproute2 libyaml-dev \
      && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
      && apt-get remove -y git curl openssh-client iproute2 \
      && apt-get autoremove -y \
      && rm -rf /var/lib/apt/lists/*
      && RUN pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple
      && pip3 install -r pipenv -i https://mirrors.aliyun.com/pypi/simple
      && pipenv install


ARG GIT_COMMIT
ENV GIT_COMMIT ${GIT_COMMIT}

CMD ["gunicorn", "-b", ":5000", "-k", "gevent", "wsgi:application"]