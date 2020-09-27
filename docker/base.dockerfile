
FROM ubuntu:18.04 as base_build

MAINTAINER Peter-Chou <2747244153@qq.com>

RUN sed -i "s@http://.*archive.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list && \
	sed -i "s@http://.*security.ubuntu.com@http://mirrors.huaweicloud.com@g" /etc/apt/sources.list

ENV DEBIAN_FRONTEND=noninteractive


RUN  apt-get update && apt-get install -y \
	tzdata \
	supervisor \
	git \
	curl \
	wget \
	zip \
	unzip \
	vim \
	tree \
	bash-completion \
	&& \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/*
RUN wget --quiet https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-py37_4.8.2-Linux-x86_64.sh -O ~/miniconda.sh && \
	/bin/bash ~/miniconda.sh -b -p /opt/conda && \
	rm ~/miniconda.sh && \
	ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
	echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
	echo "conda activate base" >> ~/.bashrc

ENV PATH /opt/conda/bin:$PATH

RUN mkdir -p ~/.pip && echo '[global]\n\
	index-url = https://mirrors.huaweicloud.com/repository/pypi/simple\n\
	trusted-host = mirrors.huaweicloud.com\n\
	timeout = 120\n'\
	> ~/.pip/pip.conf

RUN pip install numpy==1.19.2 \
	Flask==1.1.2 \
	tensorflow==1.14.0 \
	tensorflow-serving-api==1.14.0 \
	requests==2.24.0 \
	gunicorn==20.0.4
