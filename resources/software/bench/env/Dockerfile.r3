FROM eprp-sw/bench-r2:t2
RUN apt-get update && apt-get install -y --no-install-recommends \
      libgdal34t64 libgeos-c1t64 libproj25 libudunits2-0 libnode109 libsqlite3-0 \
 && rm -rf /var/lib/apt/lists/*
RUN R -q -e "options(repos = c(CRAN = Sys.getenv('PPM'))); install.packages(c('palaeoverse', 'fossilbrush', 'chronosphere', 'sf', 'h3jsr', 'V8'), Ncpus = 8)"
RUN (find /usr/local/lib/R/site-library -name '*.so' -exec ldd {} + | grep 'not found' | grep -v libR.so | sort -u || true)
RUN R -q -e "for (p in c('palaeoverse', 'fossilbrush', 'chronosphere', 'sf', 'h3jsr')) library(p, character.only = TRUE); ip <- installed.packages()[, c('Package', 'Version')]; write.table(ip, '/opt/r-packages.tsv', sep = '\t', quote = FALSE, row.names = FALSE)"
WORKDIR /work
