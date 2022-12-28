
# Carbon Dioxide Dissolution Simulation 

_Lukas Rieder, Institute for Geology ,Universty of Hamburg_

Here will be my explanaition of the  equations and assumptions from the Book (Steven <Meerson , John Hedges). The squared brackets imply the concentration is meant:

$$ c( CO_3^{-2} ) = \[ CO_3^{-2} \]. $$

Also because carbonic acid $H_2 CO_3$ is very unstable and it is difficult to distinguish it from  $CO_2(aq)$ both compounds are combined to:

$$ \[CO_2 \] = \[CO_2(aq) \]+ \[H_2 CO_3 \].$$

Thus the first dissociation constant is actually a combined one of two reactions ( $ CO_2(aq) + H_2 O ->  H_2 CO_3 -> HCO_3^{-} + H^{+} $ ).

The dissociation constansts $K_1^{'}$ $K_2^{'}$ as well as the Henrys law constant $K_H$  are Temperature dependent. This dependece is rather complex to describe so I wont show the equations for the temperature dependande here.

All equations neccessary to describe/solve the full carbonate system are listed below:


<!--- This is an HTML comment in Markdown. For some reason the regular Latex _{i}  is not accepted. Use just _i instead. Because [ ] referes to
links in markdown files   the squared brackets have to be typed in this way:  \[   \] . In the equations leave enough whitespaces especially at end and beginning. For biger subscripts longer than one character: to prevent the blog software from interpreting the underscores as meaning italics use '\_{xy}' instead of '_{xy}' -->

<!---  https://www.mathelounge.de/509545/mathjax-latex-basic-tutorial-und-referenz-deutsch -->

1. total dissolved inorganic carbon: $$ DIC = \[ CO_2 \] + \[ HCO_3^- \] + \[ CO_3^{-2} \] $$

2. alkalinity **extremely** simplified (carbonate alkalinity):  $$ A_C=\[ HCO_3^{-} \]  +2 \cdot \[ CO_3^{-2} \] $$

3. First Dissociation Constant of carbonic acid: $$ K_1^{'} = \frac{ \[HCO_3^{-} \] \cdot \[H^{+}\] }{ \[CO_2 \] } $$

4. Second Dissociation Constant of carbonic acid: $$ K_2^{'}=\frac{ \[CO_3^{-2} \] \cdot \[H^{+} \] }{ \[ HCO_3^{-}  \] } $$

5. Solubility of Gas (Henrys law constant for ): $$ K_H=\frac{ \[CO_2 \]  }{ f\_{CO_2,a} } $$


However the Simulation you find here is not calculated with the strong simplification of Alkalinity. Everything is calculated with [pyCO2SYS](https://pyco2sys.readthedocs.io/en/latest/) a python toolbox designed for solving the marine carbonate system.
This toolbox Alkalinity definition takes into account all Anions after Dicksons(1981) Alkalinity definition:

"The number of moles of hydrogen ion equivalent to the excess of proton
acceptors (bases formed from weak acids with a dissociation constant
$K \leq 10^{-4.5}$ at 25°C and zero ionic strength) over the proton donors (acids
with $ K \geq 10^{4.5} $ in one kilogram of sample."

In other words all the bases acting for pH values higher than $pK=4.5$ (acid and conjugate base equilibrium).
Because for $pH=pKs$ the concentration of the wak acid is equal to the concentration of the conjugate base $\[HBa\]=\[Ba^{-}\]$ and for $pH>pK$ the conjugate base dominates.

