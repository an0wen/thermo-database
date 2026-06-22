--------------------
GENERAL INFORMATION 
--------------------
This readme file was generated on 2025-09-15 by Marina Cano Amoros.

Title of Dataset: Revised AQUA EoS
Description of Dataset: The AQUA EoS from Haldemann et al. (2020) with revised entropies from Mazevet et al. (2021) and new superionic data from French et al. (2016).
Principal Investigators: Marina Cano Amoros (marina.canoamoros@dlr.de), Nadine Nettelmann (nadine.nettelmann@gmx.de), Nicola Tosi (nicola.tosi@dlr.de)
Date of Data Collection: 2025

-------------
FILE OVERVIEW 
-------------

 FileName                    Records    Explanations
-----------------------------------------------------------------------------------------------------------------
 _README.txt                            This file
 AQUA_revised_eos_pt.csv      303854    Equation of state on a pressure - temperature grid with revised entropies 
-----------------------------------------------------------------------------------------------------------------



-----------------------------------------------------
DATA SPECIFIC INFORMATION FOR AQUA_revised_eos_pt.csv 
-----------------------------------------------------

 Label               Units       Explanations
---------------------------------------------------------------------------------------------------------------
 pressure             Pa          Pressure (1093 x log spaced)
 temperature          K           Temperature (278 x log spaced)
 density              kg/m3       Density
 entropy              J/kg/K      Specific entropy (1)
 internal_energy      J/kg        Specific internal energy
 dlnS_dlnP_T          ---         Logarithmic derivative of entropy with respect to pressure at constant temperature
 dlnS_dlnT_P          ---         Logarithmic derivative of entropy with respect to temperature at constant pressure
 ad_grad              ---         Adiabatic gradient from -(dlnS_dlnP_T)/(dlnS_dlnT_P)
 phase                ---         Phase ID (2)
 flag                 ---         Interpolation flag (3)
---------------------------------------------------------------------------------------------------------------
Note (1): Negative or above-limit entropies have s = -1 
---------------------------------------------------------------------------------------------------------------
Note (2): Phase ID remains as in the original AQUA from Haldemann et al. (2020) with the addition of 
phase ID "0", which corresponds to the extrapolated ice. 
          -1 = ice-Ih
          -2 = ice-II
          -3 = ice-III
          -5 = ice-V
          -6 = ice-VI
          -7 = ice-VII
         -10 = ice-X
           3 = vapor
           4 = liquid
           5 = supercritical + superionic
           0 = extrapolated ice
---------------------------------------------------------------------------------------------------------------
Note (3): The interpolation flag is for users to know whether the entropy in a specific region is from the original EoS sources, interpolated (together with the density and internal energy) or extrapolated.
          0 = original 
          1 = interpolated
          2 = extrapolated
          3 = NA
---------------------------------------------------------------------------------------------------------------




-----------------------
DATA ACCESS AND SHARING
-----------------------
Publications based on this dataset:
Recommended citation for this dataset:
License information:


