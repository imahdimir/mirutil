"""

    """

import importlib

import pandas as pd


importlib.reload(df_utils)

from src.mirutil.df import *


##
fp0 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/Tables/232760-0.xlsx'
fp1 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/Tables/232760-1.xlsx'
fp2 = '/Users/mahdi/Dropbox/1-git-dirs/PyCharm/u-d0-FirmTicker-MonthlySales/Tables/232768-0.xlsx'

df = pd.read_excel(fp0)
df1 = pd.read_excel(fp1)
df2 = pd.read_excel(fp2)

##
has_extra_data(df , df1)

##
dfs = [df , df1 , df2]

##
l = drop_dup_and_sub_dfs(dfs)
l

##
