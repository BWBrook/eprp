FROM eprp-sw/bench-r4:t4
ENV MAKEFLAGS=-j2 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
COPY source/sp_2.2-4.tar.gz source/dggridR_3.0.0.tar.gz /tmp/q027-source/
COPY Makevars.dggridR /tmp/q027-Makevars
RUN echo '73f03473e61e89f3c0c1a96ac6e17e81a075637963d1d6b156dc9c969b2dbc93  /tmp/q027-source/sp_2.2-4.tar.gz' | sha256sum -c - \
 && echo '4aa6e58b31209a4578626661bc7583bfad2f1a96fd8ce804d0d6701f10a325a4  /tmp/q027-source/dggridR_3.0.0.tar.gz' | sha256sum -c - \
 && R CMD INSTALL /tmp/q027-source/sp_2.2-4.tar.gz \
 && R_MAKEVARS_USER=/tmp/q027-Makevars R CMD INSTALL /tmp/q027-source/dggridR_3.0.0.tar.gz \
 && rm -rf /tmp/q027-source /tmp/q027-Makevars
