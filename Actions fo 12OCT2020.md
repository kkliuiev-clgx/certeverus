* Add new resampling and driver code to the transformation_manager (ASAP MP)
  - consider how we will build the DFs for the drivers and interact with the charting functions 
  (do we preserve the current vertical looping or do we move to horizonatal looping?)
  one thing to consider is how we preserve the numerator and denominator values for labeling, hover text, and CAGR calcs
  
* Add dictionary creation for CPT (aka special groupings) and for agg functions -  Likely will need a dictionary for attribute lists 
  or can this be selected from the drivers file similar to parent and driver?



* select which method of driver creation based on FHMS versus non-FHMS to simplify code body maintenance - creates complications if we change charting

* develop collection of paramters from frontend (ASAP JC)

* consider labeling for isoquant charts (DEFER)
* indexing charts -- for scaling (DEFER)

* Drafting new read_sql_query to: (ASAP JC)
  * use postgres to filter by driver for SF or parent for MF
  * pre-filter for soc dates/scenarios

