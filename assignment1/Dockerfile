FROM ubuntu:24.04 AS build

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential pkg-config libgtk2.0-dev git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG COMMIT_REF=3bc90302bddacebfff838c74fb91cc56500387ea

COPY patches/ /patches/

# Izvorna koda QCADesigner-E na zaklenjenem commitu + nasi popravki (patches/*.patch):
#   crashes.patch   popravki sesutij na Linuxu (ne vplivajo na izracun energije)
#   reset-polarization.patch nova izbira Simulation > Reset Polarization
# git apply ustavi gradnjo, ce se kateri od popravkov ne uporabi.
RUN git clone https://github.com/FSillT/QCADesigner-E.git /src \
    && cd /src && git checkout -q "$COMMIT_REF" \
    && git apply /patches/*.patch \
    && cd QCADesignerE \
    && chmod +x configure config.guess config.sub depcomp install-sh missing mkinstalldirs \
    && ./configure CFLAGS="-O2 -fcommon -w" \
    && make -j"$(nproc)" && make install-strip

FROM ubuntu:24.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libgtk2.0-0t64 fonts-dejavu-core ghostscript \
    && rm -rf /var/lib/apt/lists/*

COPY --from=build /usr/local /usr/local

ENV HOME=/tmp
WORKDIR /work
CMD ["QCADesignerE"]