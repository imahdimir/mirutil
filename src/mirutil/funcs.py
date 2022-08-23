##

from pathlib import Path

import pandas as pd


def norm_fa_str(string: str) -> str :
  """ Normalize Persian/Farsi strings to a much simpler form for unification purposes

  Usage::
  >>> from mirutil import norm_fa_str as norm
  >>> converted = norm("آگاه نیکو")

  :param string: A string, will be simplified
  :rtype: str
  """

  from persiantools import characters
  from persiantools import digits
  import re


  if not isinstance(string , str) :
    return string

  os = characters.ar_to_fa(string)
  os = digits.ar_to_fa(os)
  os = digits.fa_to_en(os)

  repmap = {
      r"\u202b" : ' ' ,
      r'\u200c' : ' ' ,
      r'\u200d' : '' ,
      r'\u200f' : '' ,
      r'ء'      : ' ' ,
      r'\s+'    : ' ' ,
      r'أ'      : 'ا' ,
      r'ئ'      : 'ی' ,
      }

  for ky , vl in repmap.items() :
    os = re.sub(ky , vl , os)

  os = os.strip()

  return os

def save_df_as_a_nice_xl(df: pd.DataFrame ,
                         fpn ,
                         index: bool = False ,
                         header: bool = True ,
                         max_col_length: int = 40
                         ) :
  import openpyxl as pyxl


  df.to_excel(fpn , index = False)

  wb = pyxl.load_workbook(fpn)
  ws = wb.active

  panes = index * ws['A'] + header * ws[1]

  for cell in panes :
    cell.style = 'Pandas'

  for column in ws.columns :
    length = max(len(str(cell.value)) for cell in column) + 3
    length = length if length <= max_col_length else max_col_length
    ws.column_dimensions[column[0].column_letter].width = length

  ws.freeze_panes = 'A2'

  wb.save(fpn)
  wb.close()

  print(f"saved as {fpn}")

def save_as_prq_wo_index(df , fpn) -> None :
  df.to_parquet(fpn , index = False)
  print(f'dataframe saved as {fpn} without index')

def read_data_according_to_type(fpn) -> pd.DataFrame :
  suf = Path(fpn).suffix
  if suf == '.xlsx' :
    return pd.read_excel(fpn)
  elif suf == '.prq' :
    return pd.read_parquet(fpn)
  elif suf == '.csv' :
    return pd.read_csv(fpn)

def update_metadata_save_rand_sample(fp , save_rand_sample = True) -> None :
  """
  :param fp:
  :param save_rand_sample:
  :return:
  """

  import json
  from .namespaces import MetadataColumns


  cns = MetadataColumns()

  dirpth = Path(fp).parent
  metafp = dirpth / 'META.json'
  if not metafp.exists() :
    return None

  with open(metafp) as fi :
    meta = json.load(fi)

  df = read_data_according_to_type(fp)

  if cns.startendcol in meta.keys():
    if meta[cns.startendcol] is not None :
      meta[cns.start] = df[meta[cns.startendcol]].min()
      meta[cns.end] = df[meta[cns.startendcol]].max()

  meta[cns.numrow] = len(df)
  meta[cns.numcol] = len(df.columns)
  meta[cns.colnames] = list(df.columns)

  with open(metafp , 'w' , encoding = 'utf-8') as fi :
    json.dump(meta , fi , ensure_ascii = False)
    print("Meta updated.")

  if save_rand_sample and len(df) > 1000 :
    _df = df.sample(n = 1000)
    _fp = Path(fp).with_stem('Sample').with_suffix('.xlsx')
    save_df_as_a_nice_xl(_df , _fp)
    print('random sample saved.')


def persian_tools_jdate_from_iso_format_jdate_str(jdate_str: str):
  import re
  from persiantools.jdatetime import JalaliDate


  iso_fmt_jd = r'1[34]\d\d-[0-2]\d-[0-3]\d'

  if pd.isna(jdate_str):
    return None

  jd = str(jdate_str)

  cnd = re.fullmatch(iso_fmt_jd , jd)

  if cnd is not None :
    return JalaliDate(int(jd[:4]), int(jd[5:7]), int(jd[8:10]))
  elif cnd is None:
    raise ValueError

def persian_tools_jdate_from_int_format_jdate(jdate: {int, str}):
  import re
  from persiantools.jdatetime import JalaliDate


  int_fmt_jd = r'1[34]\d\d[0-2]\d[0-3]\d'

  if pd.isna(jdate):
    return None

  jd = str(int(jdate))

  cnd = re.fullmatch(int_fmt_jd , jd)

  if cnd is not None :
    return JalaliDate(int(jd[:4]), int(jd[4:6]), int(jd[6:8]))
  elif cnd is None:
    raise ValueError

def print_df_columns_in_dict_type(df):
  for cn in df.columns:
    print('"' + cn + '":None,')

def extract_market_from_tsetmc_title(title: str):

  import re


  os = title.replace("',FaraDesc ='" , ' ')
  os = os.strip()

  ptr = r'.+-\s*([^-]*)'
  if re.fullmatch(ptr, os):
    return re.sub(ptr, r'\1', os).strip()
  else:
    ptr = r'.+-\s*-\s*'
    assert re.fullmatch(ptr,os)