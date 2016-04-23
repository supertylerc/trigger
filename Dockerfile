FROM alpine:latest
MAINTAINER Tyler Christiansen <supertylerc@saucelabs.com>

COPY scripts/dockerfile_install.sh /install.sh

RUN apk --update add bash \
    && /bin/bash /install.sh \
    && rm /install.sh

ENV HOME /root
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
VOLUME /src
WORKDIR /src
ENTRYPOINT ["/root/.pyenv/shims/tox"]
CMD ["-e", "py27,lint"]
