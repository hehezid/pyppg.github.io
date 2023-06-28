---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.10.3
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# SPT Data Processing & Classification

+++

Process the SPT data from GInt for soil classification.

+++

### Import data

Type in the ground profile.

```{code-cell} ipython3
import json
import pandas as pd
import numpy as np
import math

ground_info = {
    "site": [   
        
    # ---  Beginning of one site --- #
        {
    "boring_name": "HA-B1(OW)",
    "GS_EI": 178,
    "GW_EI": 177,
    "soil_overburden": 34,  # unit: ft
    "total_boring_depth": 41,  # unit: ft
    "PGA": 0.12,
    "Mag": 6,
    "MSF": 1.77,
    "borehole_diameter": 4,  # unit: in
    "hoist_type": "Cat-Head",
    "hammer_type": "safety hammer",
    ## Record the layer information of this boring site   
    # "type": the type can only be chosen from "cohesive", "cohesionless", and "rock".
    # blow_1: if the blow cannot advance the 6in within 100 blows, then type the blow number as 100
    # blow_4: if the blow cannot advance the 6in within 50 blows, then type the blow number as 50
    # if the blow number per 6in is not available, type 100 (non-penetrable)    
    # y_t: total unit weight of soil
    # v_s: shear wave velocity
    # f_c: fines content (%)
    "layers": [    
        {"depth":1.5, "sample_number":"S1", "geological_description":"FILL", "group_symbol":"ML", "type":"cohesionless",
        "blow_1":6, "blow_2":12, "blow_3":11, "blow_4":13, "y_t":120, "f_c":50},
        {"depth":5, "sample_number":"S2", "geological_description":"FILL", "group_symbol":"ML", "type":"cohesionless",
        "blow_1":40, "blow_2":12, "blow_3":14, "blow_4":7, "y_t":120, "f_c":50},
        {"depth":10, "sample_number":"S3", "geological_description":"FILL", "group_symbol":"ML", "type":"cohesionless",
        "blow_1":7, "blow_2":9, "blow_3":7, "blow_4":8, "y_t":120, "f_c":50},
        {"depth":15, "sample_number":"S4", "geological_description":"FILL", "group_symbol":"--", "type":"cohesionless",
        "blow_1":31, "blow_2":13, "blow_3":7, "blow_4":18, "y_t":120, "f_c":0},
        {"depth":20, "sample_number":"NR", "geological_description":"FILL", "group_symbol":"--", "type":"",
        "blow_1":12, "blow_2":10, "blow_3":5, "blow_4":5, "y_t":120, "f_c":0},
        {"depth":24.2, "sample_number":"NR", "geological_description":"FILL", "group_symbol":"--", "type":"",
        "blow_1":0, "blow_2":0, "blow_3":0, "blow_4":0, "y_t":120, "f_c":0},
        {"depth":28.5, "sample_number":"S5", "geological_description":"FILL", "group_symbol":"SW-SM", "type":"cohesionless",
        "blow_1":11, "blow_2":14, "blow_3":11, "blow_4":15, "y_t":120, "f_c":10},
        {"depth":30.5, "sample_number":"S6", "geological_description":"FILL", "group_symbol":"GW-GM", "type":"cohesionless",
        "blow_1":13, "blow_2":16, "blow_3":18, "blow_4":23, "y_t":120, "f_c":10},
        {"depth":35.5, "sample_number":"C1", "geological_description":"BEDROCK", "group_symbol":"--", "type":"rock",
        "blow_1":0, "blow_2":0, "blow_3":0, "blow_4":0, "y_t":150, "f_c":0},
        {"depth":39, "sample_number":"C2", "geological_description":"BEDROCK", "group_symbol":"--", "type":"rock",
        "blow_1":0, "blow_2":0, "blow_3":0, "blow_4":0, "y_t":150, "f_c":0}
              ]
        },
    # ===  End of this site === #
        
    # ---  Beginning of one site --- #
        {
    "boring_name": "HA-B2",
    "GS_EI": 177.5,
    "GW_EI": 176.5,
    "soil_overburden": 31,  # unit: ft
    "total_boring_depth": 37,  # unit: ft
    "PGA": 0.12,
    "Mag": 6,
    "MSF": 1.77,
    "borehole_diameter": 4,  # unit: in
    "hoist_type": "Cat-Head",
    "hammer_type": "safety hammer",
    ## Record the layer information of this boring site   
    # "type": the type can only be chosen from "cohesive", "cohesionless", and "rock".
    # blow_1: if the blow cannot advance the 6in within 100 blows, then type the blow number as 100
    # blow_4: if the blow cannot advance the 6in within 50 blows, then type the blow number as 50
    # if the blow number per 6in is not available, type 100 (non-penetrable)    
    # y_t: total unit weight of soil
    # v_s: shear wave velocity
    # f_c: fines content (%)
    "layers": [ 
        {"depth":1.5, "sample_number":"S1", "geological_description":"FILL", "group_symbol":"SM/ML", "type":"cohesionless",
        "blow_1":10, "blow_2":6, "blow_3":17, "blow_4":10, "y_t":120, "v_s":0, "f_c":35},
        {"depth":5, "sample_number":"S2", "geological_description":"FILL", "group_symbol":"SM/ML-CL", "type":"cohesionless",
        "blow_1":10, "blow_2":15, "blow_3":18, "blow_4":10, "y_t":120, "f_c":35},
        {"depth":9.9, "sample_number":"S3", "geological_description":"FILL", "group_symbol":"SM", "type":"cohesionless",
        "blow_1":18, "blow_2":8, "blow_3":12, "blow_4":10, "y_t":120, "f_c":30},
        {"depth":15, "sample_number":"S4", "geological_description":"FILL", "group_symbol":"GW-GM", "type":"cohesionless",
        "blow_1":7, "blow_2":8, "blow_3":9, "blow_4":9, "y_t":120, "f_c":10},
        {"depth":20, "sample_number":"S5", "geological_description":"FILL", "group_symbol":"GW-GM", "type":"cohesionless",
        "blow_1":4, "blow_2":12, "blow_3":10, "blow_4":9, "y_t":120, "f_c":10},
        {"depth":25, "sample_number":"S6", "geological_description":"FILL", "group_symbol":"SW-SM SC", "type":"cohesionless",
        "blow_1":6, "blow_2":19, "blow_3":17, "blow_4":24, "y_t":120, "f_c":10},
        {"depth":29, "sample_number":"C1", "geological_description":"WEATHERED BEDROCK", "group_symbol":"--", "type":"rock",
        "blow_1":0, "blow_2":0, "blow_3":0, "blow_4":0, "y_t":150, "f_c":0},
        {"depth":33.5, "sample_number":"C2", "geological_description":"WEATHERED BEDROCK", "group_symbol":"--", "type":"rock",
        "blow_1":0, "blow_2":0, "blow_3":0, "blow_4":0, "y_t":150, "f_c":0}
              ]
        }
    # ===  End of this site === #    
      
        ]
    }
    # --- End of typing ground information

with open('ground_info.json', 'w') as outfile:
    json.dump(ground_info , outfile)
```

### Now start calculation

```{code-cell} ipython3
# Read ground information
with open("ground_info.json", "r") as read_file:
    ground_data = json.load(read_file)    
    
```

```{code-cell} ipython3
site_n=0

layer_num = len(ground_data["site"][site_n]["layers"])

depth = []  # unit: ft
elevation = []  # unit: ft
C_N = []
sublayer_thickness = np.zeros((layer_num, 1))
fines_content = []  # (%)

blow_1 = []  # blows of the 1st 6in
blow_2 = []  # blows of the 2nd 6in
blow_3 = []  # blows of the 3rd 6in
blow_4 = []  # blows of the 4th 6in

spt_n = []  # unit: bl/ft
cohesionless_spt_n = []  # unit: bl/ft

C_E = []  # one of N60 corrections
C_R = []  # one of N60 corrections
C_B = []  # one of N60 corrections
C_S = []  # one of N60 corrections
N_60 = []
cohesionless_N_60 = []

# ground stress calculation
y_t = []  # total unit weight, unit: pcf
y_w = 62.4  # unit weight of water, unit: pcf
sig_v = []  # total vertical stress, unit: psf
p_w = []  # water pressure
sig_v_e = []  # effective stress

# (N1)60 correction
C_N = []
N1_60 = []

relative_density = []  

# site class evaluaton
cumulative_thickness = []  # unit: ft
class_sublayer_thickness = sublayer_thickness  # sublayer thickness for site class evaluation
site_class = []  # unit: d/N




for i in range(0, layer_num):
    # calculate elevation
    elevation.append(ground_data["site"][site_n]["GS_EI"] - ground_data["site"][site_n]["layers"][i]["depth"])
    
    # extract depth information from ground_data (to facilitate later calcualtion)
    depth.append(ground_data["site"][site_n]["layers"][i]["depth"])
    
    # extract blows information from ground_data (to facilitate later calcualtion)
    blow_1.append(ground_data["site"][site_n]["layers"][i]["blow_1"])
    blow_2.append(ground_data["site"][site_n]["layers"][i]["blow_2"])
    blow_3.append(ground_data["site"][site_n]["layers"][i]["blow_3"])
    blow_4.append(ground_data["site"][site_n]["layers"][i]["blow_4"])
    
    y_t.append(ground_data["site"][site_n]["layers"][i]["y_t"])
    fines_content.append(ground_data["site"][site_n]["layers"][i]["f_c"])
    
for i in range(0, layer_num):
    # calculate sublayer thickness
    if i == 0:
        sublayer_thickness[i] = depth[0] + 0.5* (depth[1]-depth[0])
    elif i == (layer_num-1):
        sublayer_thickness[i] = 0.5* (depth[i]-depth[i-1]) + ground_data["site"][site_n]["total_boring_depth"] - depth[i]
    else:
        sublayer_thickness[i] = 0.5*(depth[i]-depth[i-1]) + 0.5*(depth[i+1]-depth[i])
        
    # calculate spt_n (blow number per ft of penetration)
    if (blow_2[i]+blow_3[i]) > 0:
        spt_n.append( min(100, max(1, (blow_2[i]+blow_3[i]))) )
    else:
        spt_n.append(100)  # could not advance 6 in
    
    # cohesionless SPT N (bl/ft)
    if ground_data["site"][site_n]["layers"][i]["type"] == "cohesionless" :
        cohesionless_spt_n.append(spt_n[i])
    else:
        cohesionless_spt_n.append("N/A")
        
    ## N_60 calculation ( including N_60 correction)
    if "automatic" in ground_data["site"][site_n]["hammer_type"]:
        C_E.append(1.05)
    elif "safety" in ground_data["site"][site_n]["hammer_type"]:
        C_E.append(0.85)
    elif "do*nut" in ground_data["site"][site_n]["hammer_type"]:
        C_E.append(0.75)
    else:
        C_E.append("N/A")
        
        # C_R calculation (N_60 correction)
    if depth[i] <= 10:
        C_R.append(0.75)
    elif depth[i] <= 12:
        C_R.append(0.8)
    elif depth[i] <= 20:
        C_R.append(0.85)
    elif depth[i] <= 30:
        C_R.append(0.95)
    elif depth[i] > 30:
        C_R.append(1)
        
        # C_B calculation (N_60 correction)
    if 4.5 >= ground_data["site"][site_n]["borehole_diameter"] >= 2.5:
        C_B.append(1)
    elif ground_data["site"][site_n]["borehole_diameter"] == 6:
        C_B.append(1.05)
    elif ground_data["site"][site_n]["borehole_diameter"] == 8:
        C_B.append(1.15)
        
        # C_S (In spreadsheet, all equals to 1.0 without any equation)
    C_S.append(1)
    
        # N_60 number = blow number * corrections
    N_60.append(spt_n[i]*C_E[i]*C_R[i]*C_B[i]*C_S[i])
    if ground_data["site"][site_n]["layers"][i]["type"] == "cohesionless" :
        cohesionless_N_60.append(N_60[i])
    else:
        cohesionless_N_60.append("N/A")
    
    ## Stress calculation
        # total vertical stress
    if i == 0: 
        sig_v.append(y_t[i]*depth[i])
    else:
        sig_v.append( sig_v[i-1] + y_t[i]*(depth[i]-depth[i-1]) )
    
        # water preassure
    p_w.append(y_w * max(0, (ground_data["site"][site_n]["GW_EI"]-elevation[i])))
    
        # effective stress
    sig_v_e.append((sig_v[i]-p_w[i]))
    
    # (N1)60 correction
    C_N.append(min(1.7, math.sqrt(2088/sig_v_e[i])))
    N1_60.append(C_N[i]*N_60[i])
    
    # Relative density
    if ground_data["site"][site_n]["layers"][i]["type"] == "cohesionless":
        relative_density.append( min( 100, 100*(N_60[i]/(16+23*sig_v_e[i]/2048))**0.5 ) )
    else:
        relative_density.append("N/A")

    ## site class evaluation    
    if i == 0:
        cumulative_thickness.append(sublayer_thickness[0][0])
    elif i < (layer_num-1):
        cumulative_thickness.append(sublayer_thickness[i][0] + cumulative_thickness[i-1])
    elif i == (layer_num-1):
        temp = sublayer_thickness[i][0] + cumulative_thickness[i-1]
        class_sublayer_thickness[layer_num-1] = max(0, (100-cumulative_thickness[layer_num-2]))
        if temp < 100:
            cumulative_thickness.append(100)
        else:
            cumulative_thickness.append(temp)
        
    site_class.append(class_sublayer_thickness[i][0]/spt_n[i])
    
# classification
N_bar = (cumulative_thickness[-1]/sum(site_class))
if N_bar < 15:
    site_class_sum = "E"
elif N_bar <= 50:
    site_class_sum  = "D"
else:
    site_class_sum  = "C"
        
print('Site class is ' + site_class_sum + '\n' )


# N_ch site evaluation
N_nch = []  # N_ch site class sublayer thickness (exclude cohesive layers)
site_class_nch = []  # layer class for Nch (N_ch stands for non-cohesive?)

for i in range(0, layer_num):
    if ground_data["site"][site_n]["layers"][i]["type"] == "cohesive":
        N_nch.append("N/A")
    else:
        N_nch.append(class_sublayer_thickness[i][0])
        
    if type(N_nch[i]) == str:
        site_class_nch.append(0)
    else:
        site_class_nch.append(site_class[i])

# classification
N_nch_bar = (N_nch[-1]/sum(site_class_nch))
if N_nch_bar < 15:
    site_class_sum_nch = "E"
elif N_nch_bar <= 50:
    site_class_sum_nch  = "D"
else:
    site_class_sum_nch  = "C"
    
print('Site N_ch class is ' + site_class_sum_nch +'\n')    

# --- shear wave velocity correlations --- #
K2_max = []  # = 20 * (N1)60 ^0.333
vs = []  # (Seed et al.), unit: ft/s
vs_sykora = []  # uses Sykora Factor, unit: ft/s
sykora_factor = 250

for i in range(0, layer_num):
    if ground_data["site"][site_n]["layers"][i]["type"] == "cohesive":
        K2_max.append(0)
    else:
        K2_max.append(20*N1_60[i]**0.333)
    
    vs.append( math.sqrt(1000*K2_max[i]*math.sqrt(sig_v[i]*(1+2*0.4)/3)*32.2/y_t[i]) )
    vs_sykora.append( sykora_factor* (spt_n[i]**0.17) * (depth[i]**0.2) )
        
## --- Liquefaction Analysis, Youd & Idriss (2001)        
alpha = []
beta = []
fg_dr = []  # f=g(Dr)

for i in range(0, layer_num):
    if fines_content[i] <= 5:
        alpha.append(0)
        beta.append(1)
    elif fines_content[i] <= 35:
        alpha.append( math.exp(1.76-190/fines_content[i]/fines_content[i]) )
        beta.append( 0.99 + fines_content[i]**1.5/1000)
    else:
        alpha.append(5)
        beta.append(1.2)
    
    if type(relative_density[i]) == str:
        fg_dr.append(0)
    else:
        fg_dr.append( min(0.8, max(0.6, (1-0.005*relative_density[i]))) )

    min(1, (sig_v_e[i]/2088)**(fg_dr[i]-1))  
```

```{code-cell} ipython3
fg_dr
```

```{code-cell} ipython3
relative_density
```

```{code-cell} ipython3

```
