FROM eprp-sw/bench-r:t1
ARG REXTINCT_COMMIT=508d3c90698b88efcb8c2f1c17a6837a42fd7691
ARG AGNOSTIC_SHA256=1eb9268f859a5227b0a38ce80883cf7656e8bf4520bcccd038096f7735c8db42
RUN R -q -e "options(repos = c(CRAN = Sys.getenv('PPM'))); install.packages(c('StratPal', 'admtools', 'paleoAM', 'EDE', 'tbea', 'remotes', 'data.table', 'moments', 'rcarbon'), Ncpus = 8)"
RUN R -q -e "remotes::install_github('FredSaltre/CRIWM', subdir = 'Rextinct', ref = Sys.getenv('REXTINCT_COMMIT'), upgrade = 'never', dependencies = FALSE)"
RUN mkdir -p /opt/agnostic && R -q -e "download.file('http://bio.mq.edu.au/~jalroy/agnostic.R', '/opt/agnostic/agnostic.R', mode = 'wb')" \
 && echo "${AGNOSTIC_SHA256}  /opt/agnostic/agnostic.R" | sha256sum -c -
RUN (find /usr/local/lib/R/site-library -name '*.so' -exec ldd {} + | grep 'not found' | grep -v libR.so | sort -u || true)
RUN R -q -e "for (p in c('StratPal', 'admtools', 'paleoAM', 'EDE', 'tbea', 'Rextinct')) library(p, character.only = TRUE); ip <- installed.packages()[, c('Package', 'Version')]; write.table(ip, '/opt/r-packages.tsv', sep = '\t', quote = FALSE, row.names = FALSE)"
WORKDIR /work
