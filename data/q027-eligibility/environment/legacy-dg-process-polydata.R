dg_process_polydata <- function(polydata,frame,wrapcells){
  polydata  <- as.data.frame(polydata)
  polydata  <- split(polydata, polydata$seqnum)
  an        <- names(polydata)
  polydata  <- lapply(polydata, function(x) { x["seqnum"] <- NULL; x })
  polydata  <- lapply(polydata, Polygon)
  polydata  <- lapply(seq_along(polydata), function(i) Polygons(list(polydata[[i]]), ID = an[i]  ))
  polydata  <- SpatialPolygons(polydata, proj4string = CRS("+proj=longlat +datum=WGS84") )

  #These two lines suppress a WARNING message that would otherwise be raised by
  #`R CMD check` due to the use of dplyr
  long  <- NULL
  group <- NULL

  if(frame){
    polydata.points      <- fortify(polydata, region="seqnum")
    polydata.points$cell <- polydata.points$id
    polydata.points$id   <- NULL

    if(wrapcells){
      #Find dangerous polygons based on how many degrees of longitude they span
      groups_to_wrap <- polydata.points %>% group_by(group) %>% summarise(diff=max(long)-min(long)) %>% filter(diff>180) %>% select(group)

      #Adjust them so they appear on the eastern side of the map
      polydata.points <- polydata.points %>% mutate(long=ifelse(group %in% groups_to_wrap$group, ifelse(long<0,long+360,long), long))
    }

    #Arrange polygon points so they are ordered appropriately, otherwise the results
    #will not be nice, closed cells, but weird triangular thingies
    polydata.points %>% arrange(group,order)

  } else {
    polydata
  }
}
