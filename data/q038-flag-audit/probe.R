# Lightweight input/design construction, not a CMR fit; no MARK execution.
out <- Sys.getenv("Q038_AUDIT_DIR", "scratch/q038-independent-audit")
pkg <- normalizePath(file.path(out, "RMark"))
e <- new.env(parent = globalenv())
# Only adapt package resource discovery for uninstalled CRAN source.
e$system.file <- function(..., package = "base", lib.loc = NULL, mustWork = FALSE) {
  if (package == "RMark") return(file.path(pkg, "inst", ...))
  base::system.file(..., package = package, lib.loc = lib.loc, mustWork = mustWork)
}
for (f in list.files(file.path(pkg,"R"), full.names = TRUE, pattern="[.]R$")) sys.source(f, e)
d <- new.env()
load("data/raw/monarrez2023/encounter_history_bs_gr_5class_Big5.Rdata", d)
ds <- d$ds
cat("RMark source version: 3.0.0; R:", R.version.string, "\n")
cat("Design construction only; package source loaded with resource-path shim.\n")
# Authors' exact duplicate-name design.parameters object.
dp <- list(Phi=list(formula=~mass.ext), Phi=list(formula=~range),
           Gamma=list(formula=~rec.mass), Gamma=list(formula=~range))
pd <- e$process.data(subset(ds,class=="Bivalvia"), model="Pradsen")
ddl <- e$make.design.data(pd, parameters=dp)
cat("begin.time:",pd$begin.time,"nocc:",pd$nocc,"intervals:",unique(pd$time.intervals),"\n")
cat("Phi times:",range(as.numeric(as.character(ddl$Phi$time))),"Gamma times:",
    range(as.numeric(as.character(ddl$Gamma$time))),"\n")
model <- e$make.mark.model(pd, ddl,
  parameters=list(Phi=list(formula=~time+range*mass.ext),
                  Gamma=list(formula=~time+range*rec.mass), p=list(formula=~time+logvol)))
cat("design names:",names(model),"\n")
dm <- model$design.matrix
cat("Phi rows around boundary:\n")
ix <- which(as.numeric(as.character(ddl$Phi$time)) %in% c(7,8,21,22,38,39,45,46,68,69))
print(cbind(ddl$Phi[ix,], dm[ix,grepl("range|mass.ext",colnames(dm)),drop=FALSE]),row.names=FALSE)
cat("Flag indices:",which(colSums(ds[,grep("^mass.ext",names(ds))])>0),"\n")
stopifnot(pd$begin.time==1, pd$nocc==86, all(pd$time.intervals==1),
          identical(as.character(dm[38,"Phi:mass.ext"]),"mass.ext38"),
          identical(as.character(dm[39,"Phi:mass.ext"]),"mass.ext39"),
          all(ds$mass.ext38==0),all(ds$mass.ext39==1))
rows <- as.numeric(as.character(ddl$Phi$time))
mapping <- data.frame(parameter="Phi",occasion_start=rows,
  occasion_end=rows+1,range_variable=dm[rows,"Phi:range"],
  flag_variable=dm[rows,"Phi:mass.ext"],
  flag=as.numeric(ds[1,paste0("mass.ext",rows)]))
stopifnot(all(mapping$range_variable == paste0("range", rows)),
          all(mapping$flag_variable == paste0("mass.ext", rows)),
          identical(which(mapping$flag == 1), c(8L,22L,39L,46L,69L)))
grows <- as.numeric(as.character(ddl$Gamma$time))
gix <- ddl$Gamma$model.index
cat("Gamma flag-variable mapping (semantic recovery alignment not adjudicated):\n")
print(data.frame(time=grows,rec_variable=dm[gix,"Gamma:rec.mass"])[grows%in%c(8,9,22,23,39,40,46,47,69,70),],row.names=FALSE)
cat("All five class history lengths (authors' scripts do not truncate):\n")
print(tapply(nchar(ds$ch),ds$class,unique))
occ <- read.csv("data/raw/monarrez2023/pbdb.cleaned.classes.csv")
cat("Deposited cleaned occurrence CSV class counts:\n")
print(table(occ$class))
window <- subset(occ,max_ma<=485.4 & min_ma>=1)
ages <- sort(unique(window$max_ma),decreasing=TRUE)
stopifnot(length(ages)==pd$nocc)
stage <- vapply(ages,function(a)paste(unique(window$early_interval[window$max_ma==a]),collapse=";"),"")
mapping$stage_start <- stage[rows]
mapping$stage_end <- stage[rows+1]
mapping$stage_start_base_ma <- ages[rows]
write.table(mapping,file.path(out,"phi-mapping.tsv"),sep="\t",quote=FALSE,row.names=FALSE)
cat("Cleaned CSV count",nrow(occ),"; five modeled classes",sum(occ$class%in%ds$class),"\n")
bits <- do.call(rbind,lapply(strsplit(ds$ch,""),as.integer))
ranges <- as.matrix(ds[paste0("range",seq_len(pd$nocc))])
cat("Range: nonzero when no capture",sum(ranges[bits==0]!=0),
    "; zero when captured",sum(ranges[bits==1]==0),"of",sum(bits),"captures\n")
subgenus <- grepl("\\(",ds$genus)
base <- sub(" \\(.*$","",ds$genus[subgenus])
cat("Subgenus-style rows",sum(subgenus),"; base also represented",sum(base%in%ds$genus),"\n")
