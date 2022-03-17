import numpy as np
import pandas as pd
import SVA3 as BOOM #SVA2 uses Classes for the Loading Functions
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

from tkinter.filedialog import askopenfilename

# %matplotlib inline

# dir(BOOM.Load)


''' Load the target location for the Driver files '''

# targetdir = "/Users/katprinci/Repos/Primary/former_root/" #sets the target directory
# Driverloc = targetdir+"driversSVA.csv"#sets the location of the drivers file
Driverloc = askopenfilename()

# Step 1 - Load from GF
dataf = BOOM.Load.LoadGuruFocus()

#Step 2 - Apply the drivers 

fmerged_df = BOOM.Load.Lock_and_Load(Driverloc,dataf) #fmerged is the primary dataframe that will be passed and filtered based on the charting needs
# fmerged_df.head(5)

Company = 'CSCO' # Manual input of Company
SelDriver =  'REVENUE/ASSETS' # Manual input of Driver

BOOM.Chart.Sparkline(fmerged_df,Company)
BOOM.Chart.SingleFactor(fmerged_df,Company,SelDriver)
BOOM.Chart.Isoquant(fmerged_df,SelDriver)
BOOM.Chart.Chart_SOC(fmerged_df,Company)
print('COMPLETED')