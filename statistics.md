`node_number`
> a number to denote this node

`parent_number`
> the number of the parent node

`most_recent_tip`
> the date of the most recent tip 

`least_recent_tip`
> the date of the oldest tip

`day_range`
> the span between the most recent and oldest date in days

`recency`
> how many days ago was the most recent tip (from date of analysis)

`age`
> how many days ago was the most oldest tip (from date of analysis)

`tip_count`
> number of tips in this cluster

`uk_tip_count`
> number of UK tips in this cluster

`uk_child_count`
> number of UK direct descendents from this cluster

`uk_chain_count`
> number of UK direct descendents from this cluster with more than one UK tip

`haplotype_count`
> number of descendent tips with zero branch lengths (i.e., identical to the cluster haplotype)

`haplotype`
> a hash of the haplotype sequence

`divergence_ratio`
> the stem length divided by the mean tip divergence  

`mean_tip_divergence`
> the average genetic distance between tips in this cluster

`stem_length`
> the length of the branch to the parent node

`growth_rate`
> the number of tips divided by the day range

`lineage`
> the global lineage of this cluster

`uk_lineage`
> the uk lineage of this cluster

`proportion_uk`
> the proportion of tips in this cluster that are from the uk

`admin0_count`
> the number of different countries in this cluster

`admin1_count`
> the number of different UK admin 1 (devolved nations) in this cluster

`admin2_count`
> the number of different UK admin 2 regions in this cluster

`admin0_mode`
> the most frequent country in this cluster

`admin1_mode`
> the most frequent UK admin 1 (devolved nation) in this cluster

`admin2_mode`
> the most frequent UK admin 2 region in this cluster

`admin1_entropy`
> the entropy of UK admin 1 (devolved nations) in this cluster

`admin2_entropy`
> the entropy of UK admin 2 regions in this cluster

`tips`
> a list of IDs of tips in this cluster
