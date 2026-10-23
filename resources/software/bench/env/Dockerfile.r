FROM rocker/r-ver:4.6.1
ARG PPM_DATE=2026-10-22
ENV PPM=https://p3m.dev/cran/__linux__/noble/${PPM_DATE}
RUN R -q -e "options(repos = c(CRAN = Sys.getenv('PPM'))); install.packages(c('FossilSim', 'paleobuddy', 'divDyn', 'TreeSim', 'ape', 'jsonlite'), Ncpus = 8)"
RUN apt-get update && apt-get install -y --no-install-recommends \
      libuv1 libglpk40 libxml2 libgmp10 libicu74 libcurl4 libssl3 libfontconfig1 libfreetype6 libpng16-16 \
 && rm -rf /var/lib/apt/lists/* \
 && (find /usr/local/lib/R/site-library -name '*.so' -exec ldd {} + | grep 'not found' | sort -u || true)
RUN R -q -e "for (p in c('FossilSim', 'paleobuddy', 'divDyn', 'TreeSim', 'ape', 'jsonlite')) library(p, character.only = TRUE); ip <- installed.packages()[, c('Package', 'Version')]; write.table(ip, '/opt/r-packages.tsv', sep = '\t', quote = FALSE, row.names = FALSE)"
WORKDIR /work
