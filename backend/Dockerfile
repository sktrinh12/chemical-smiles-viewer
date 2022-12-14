ARG PYTHON_VERSION=3.9

FROM debian:buster AS client

ARG ORACLE_VERSION=12.2.0.1.0
ARG OR_SHORT_VER=12201

WORKDIR /root
ARG ORACLE_ZIP_INTERNAL_FOLDER=instantclient_12_2
ENV CLIENT_ZIP=instantclient-basiclite-linux.x64-${ORACLE_VERSION}.zip
ENV SDK_ZIP=instantclient-sdk-linux.x64-${ORACLE_VERSION}.zip

RUN apt-get update \
    && apt-get -yq install unzip curl

ADD insta* .
RUN unzip ${CLIENT_ZIP} && unzip ${SDK_ZIP}
RUN mv ${ORACLE_ZIP_INTERNAL_FOLDER} oracle

FROM python:${PYTHON_VERSION}
ARG USERNAME=smiles-backend
ARG ORACLE_HOST
ARG ORACLE_USER
ARG ORACLE_PASS
ARG ORACLE_PORT
ARG ORACLE_SID

ENV ORACLE_HOST=${ORACLE_HOST}
ENV ORACLE_PORT=${ORACLE_PORT}
ENV ORACLE_SID=${ORACLE_SID}
ENV ORACLE_PASS=${ORACLE_PASS}
ENV ORACLE_USER=${ORACLE_USER}
ENV HOME "/home/${USERNAME}"
ENV ORACLE_HOME /opt/oracle
ENV TNS_ADMIN ${ORACLE_HOME}/network/admin

VOLUME ["${TNS_ADMIN}"]

# Install pipenv
RUN set -ex && pip install --upgrade pip

# Install dependencies
RUN mkdir -p ${HOME}/app
ADD app.py requirements.txt ${HOME} 
ADD app ${HOME}/app
RUN set -ex && pip install -r ${HOME}/requirements.txt \
    && pip install rdkit-pypi==2021.9.4

COPY --from=client /root/oracle ${ORACLE_HOME}
RUN apt-get update \
	&& apt-get -yq install libaio1 sudo \
	&& apt-get -yq autoremove \
	&& apt-get clean \
	&& adduser --home ${HOME} --shell /bin/bash ${USERNAME} \
	# Install Oracle Instant Client
	&& echo ${ORACLE_HOME} > /etc/ld.so.conf.d/oracle.conf \
	&& mkdir -p ${TNS_ADMIN} \
	&& ldconfig \
	&& rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
	&& echo "${USERNAME}  ALL=(ALL) NOPASSWD:ALL" | tee "/etc/sudoers.d/${USERNAME}"

WORKDIR ${HOME}
USER ${USERNAME}
EXPOSE 8000
CMD ["python", "app.py"]
