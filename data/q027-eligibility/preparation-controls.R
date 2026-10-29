suppressPackageStartupMessages(library(stringr))
fixture <- c('Genus species','Genus (Subgenus) species',NA_character_)
stopifnot(identical(word(fixture,1),c('Genus','Genus',NA_character_)))
ints <- data.frame(bin=c('older','younger'),hi=c(10,5),lo=c(5,0))
assign_stage <- function(hi,lo) {
 hits <- ints$bin[(pmin(hi,ints$hi)-pmax(lo,ints$lo))/(hi-lo)>.5]
 if(length(hits)==1 && !is.na(hits)) hits else NA_character_
}
stopifnot(identical(assign_stage(10,5),'older'),identical(assign_stage(8,3),'older'),is.na(assign_stage(8,2)),is.na(assign_stage(5,5)))
f <- data.frame(coll=c(1,1),genus=c('Genus','Genus'),public=c(FALSE,TRUE),sift=c(FALSE,TRUE))
stopifnot(!f[!duplicated(f[c('coll','genus')]),]$sift)
pub <- f[f$public,];stopifnot(pub[!duplicated(pub[c('coll','genus')]),]$sift)
inc <- c('marginal marine|peritidal|lagoon|estuar|bay|delta plain','shallow subtidal|foreshore|shoreface|sand shoal|delta front|reef','deep subtidal|shoreface-offshore transition zone','offshore|prodelta|submarine fan','slope|basin')
exc <- c('fizzwizzle','lagoon','reef','reef','reef')
for(name in c('original','dated_public_member')) {
 x <- read.csv(file.path('/w',paste0(name,'.csv')),na.strings='',colClasses='character')
 stopifnot(!anyDuplicated(x[c('collection_no','genus')]),!anyDuplicated(x$occurrence_no),!anyNA(x$genus),!anyNA(x$collection_no),!anyNA(x$reference_no))
 m <- unique(x[c('stage','collection_no','reference_no','lithology1','lithification1','environment','cc','Region')])
 env <- ifelse(is.na(x$environment),'',x$environment)
 matches <- rowSums(sapply(seq_along(inc),function(i)grepl(inc[i],env)&!grepl(exc[i],env)))
 stopifnot(all(matches<=1))
 coord <- unique(x[c('stage','collection_no','lat','lng','paleolng','paleolat')])
 stopifnot(!anyDuplicated(coord[c('stage','collection_no')]))
 selected <- x[x$is_mollusca=='1' & x$is_excluding_unlithified_pass=='1',]
 cat(name,'rows=',nrow(x),'metadata=',nrow(m),'depth_zero=',sum(matches==0),'depth_one=',sum(matches==1),'mollusca_pass=',nrow(selected),'\n')
 print(table(selected$stage))
}
cat('Independent base-R source-semantic controls and aggregate incidence checks: PASS\n')
