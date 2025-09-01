# Estimation of properties for saturated rocks

Estimation of elastic properties of saturated rock is the final step in the rock physics modelling in `fmu-pem`. There
are a number of rock physics models, which are described below, that can be selected. Earlier PEM systems have been
limited to clastic rock, and it has been useful to divide the estimation process into two parts: first estimate dry
rock properties, and then saturate the dro rock. With introduction of carbonate rocks in `fmu-pem`, the T-Matrix
inclusion based model does both parts in one step, and for this reason we combine the two steps for all models.

As fluid saturation and pore pressure vary with production, we need to calculate the properties of the saturated rocks
for all selected time steps in the reservoir simulator.
