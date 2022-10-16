"""

    """

import importlib

import pandas as pd

from src.mirutil import df_utils


importlib.reload(df_utils)

from src.mirutil.df_utils import *


##
fp0 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/Tables/232760-0.xlsx'
fp1 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/Tables/232760-1.xlsx'

df = pd.read_excel(fp0)
df1 = pd.read_excel(fp1)

##
has_extra_data(df , df1)

##
