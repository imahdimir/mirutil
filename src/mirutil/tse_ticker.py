"""

  """

from githubdata import GitHubDataRepo
from mirutil.str import normalize_completley_and_rm_all_whitespaces as ncr

n2f_url = 'https://github.com/imahdimir/d-Name-2-FirmTicker'

def get_ticker_by_name(name , src = n2f_url) :
    gd = GitHubDataRepo(src)
    df = gd.read_data()

    nm1 = ncr(name)
    df['nm'] = df['Name'].apply(ncr)

    msk = df['nm'].eq(nm1)
    dfa = df[msk]
    dfa = dfa.drop_duplicates(subset = 'FirmTicker')

    if len(dfa) > 1 :
        print(f'Multiple matches for {name}')
        return

    elif len(dfa) == 1 :
        return dfa.iloc[0]['FirmTicker']

    print('No matches found')

    gd.rmdir()

def get_ticker_by_name_in_df(df , name_col , target_col , src = n2f_url) :
    gd = GitHubDataRepo(src)
    dfa = gd.read_data()

    dfa['nm'] = dfa['Name'].apply(ncr)
    dfa = dfa.drop_duplicates(subset = ['FirmTicker' , 'nm'])
    dfa = dfa.set_index('nm')

    dfb = df[[name_col]]
    dfb['nm'] = dfb[name_col].apply(ncr)

    df[target_col] = dfb['nm'].map(dfa['FirmTicker'])

    gd.rmdir()

    return df
