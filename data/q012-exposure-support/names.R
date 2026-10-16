# Writes the Triton species names (triton.pres, trim == "inc") that crosswalk.py maps to S1.
# Run from the repository root:  Rscript data/q012-exposure-support/names.R
e <- new.env()
load("data/raw/triton/triton_update_2023.RData", envir = e)
x <- get("triton.pres", e)
writeLines(sort(unique(trimws(x$species[x$trim == "inc"]))), "data/q012-exposure-support/triton_names.txt")
