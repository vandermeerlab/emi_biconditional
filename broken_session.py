import numpy as np


def fix_missing_trials(df):
    """Replaces nan values with mean for that trial type

    Parameters
    ----------
    df: pd.DataFrame

    Note: this is a hack to handle sessions where there were fewer trials than expected.
    This function finds those trials and replaces the values with the mean for that
    trial type across the session.

    """
    nan_idx = np.where(np.isnan(df['value']))[0]
    for idx in nan_idx:
        row = df.loc[idx]
        value = df.loc[(df['rat'] == row['rat']) &
                       (df['session'] == row['session']) &
                       (df['condition'] == row['condition']) &
                       (df['measure'] == row['measure'])].mean()['value']

        df.set_value(idx, 'value', value)
