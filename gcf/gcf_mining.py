#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from time import *

from tabulate import tabulate
import pandas as pd

pd.options.mode.chained_assignment = None


def df_pk(path=''):
    """
    dataframe_package
    Loading the data in CVS. Return the whole DataFrame.
    """
    gcf_data_path = os.path.dirname(__file__) + '/gcf_data.csv'
    try:
        return pd.read_csv(path, encoding='utf-8').fillna('NULL')
    except IOError:
        return pd.read_csv(gcf_data_path, encoding='utf-8').fillna('NULL')


def df_print(df, col=[]):
    """
    dataframe_print
    Pretty print a Datafram as the result
    """
    def_col = ['radio_date', 'radio_title', 'radio_dj'] if col == [] else col
    try:
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        df.radio_dj = df.radio_dj.str.replace('###', ',')
        print tabulate(df[def_col], headers='keys', tablefmt='psql')\
            .encode('utf-8')
    except (KeyError, AttributeError):
        print tabulate(df, headers='keys', tablefmt='psql')
    return


def kw_mining(df, col, kw=[]):

    if col in ['radio_program', 'radio_title']:
        prog_str = '|'.join(kw)
        final = df.loc[df[col].str.contains(prog_str, na=False)]
        return final

    final = df
    for i in kw:
        kw_rows = df.loc[df[col].str.contains(i, na=False)]
        final = pd.merge(final, kw_rows)
    return final


def timing_mining(df, t_start='19850611', t_end='20850611'):
    """
    Find out radios in a specific time section.
    """
    try:
        t1 = mktime(strptime(t_start, "%Y%m%d"))
        t2 = mktime(strptime(t_end, "%Y%m%d"))
    except ValueError:
        print('Warning: Time value should be inputed as \'YYYYMMDD\'.')
        t1 = mktime(strptime('19850611', "%Y%m%d"))
        t2 = mktime(strptime('20850611', "%Y%m%d"))
    timing = df.loc[(df['time_stamp'] <= t2) & (df['time_stamp'] >= t1)]
    return timing


def recent(df, count):
    return df.head(count)


def care_mode(df, base_cvs, grading='Y', p=True, r=2):
    """
    dataframe, radio_dj, radio_programe, grading[Y Q M], percentage, rate
    """
    gs = df_pk(base_cvs)
    kw = df

    if grading is 'Y':
        kw['Y'] = kw.apply(lambda row: row.radio_date[0:4], axis=1)
        gs['Y'] = gs.apply(lambda row: row.radio_date[0:4], axis=1)
    elif grading is 'M':
        kw['M'] = kw.apply(lambda row: row.radio_date[0:7], axis=1)
        gs['M'] = gs.apply(lambda row: row.radio_date[0:7], axis=1)
    elif grading is 'Q':
        kw['Q'] = kw.apply(lambda row: (int(row.radio_date[5:7]) - 1), axis=1)
        kw['Q'] = kw.apply(lambda row: str(row.Q / 3 + 1), axis=1)
        kw['Q'] = kw.apply(lambda row: '-Q' + row.Q, axis=1)
        kw['Q'] = kw.apply(lambda row: row.radio_date[0:4] + row.Q, axis=1)
        gs['Q'] = gs.apply(lambda row: (int(row.radio_date[5:7]) - 1), axis=1)
        gs['Q'] = gs.apply(lambda row: str(row.Q / 3 + 1), axis=1)
        gs['Q'] = gs.apply(lambda row: '-Q' + row.Q, axis=1)
        gs['Q'] = gs.apply(lambda row: row.radio_date[0:4] + row.Q, axis=1)

    kw = kw[[grading, 'radio_title']].groupby([grading]).count().reset_index()
    gs = gs[[grading, 'radio_title']].groupby([grading]).count().reset_index()

    final = pd.merge(gs, kw, on=grading, how='outer').fillna(0)
    final.columns = ['i', 't', 'c']
    final['d'] = final.apply(lambda row: row.t - row.c, axis=1)
    final['p'] = final.apply(lambda row: row.c / float(row.t) * 100, axis=1)
    final['p'] = final.apply(lambda row: str(int(row.p)) + '%', axis=1)

    final.c = pd.to_numeric(final.c, downcast='integer')
    final.d = pd.to_numeric(final.d, downcast='integer')

    if p:
        for index, row in final.iterrows():
            print row.i, '|', "%3s" % row.c,\
                '|' + '█' * int(row.c / r) +\
                '□' * int(row.d / r) +\
                '|', str(row.t), '(' + row.p + ')'
    else:
        for index, row in final.iterrows():
            print row.i,\
                '|', "%3s" % int(row.c),\
                '|' + '█' * int(row.c / r) + '|'
    return


def stat_mode(df):
    """
    statistic_mining
    """
    pg = df[['radio_program', 'radio_title']]
    pg = pg.groupby(['radio_program']).count()
    pg = pg.sort_values(by=['radio_title'], ascending=False).reset_index()
    pg.index += 1
    pg.columns = ['Program', 'Count']
    print tabulate(pg, headers='keys', tablefmt='psql').encode('utf-8')
    dj = {}
    for i in df.radio_dj.tolist():
        for j in i.split('###'):
            if j in dj:
                dj[j] += 1
            else:
                dj[j] = 1
    dj = pd.DataFrame(dj.items())
    dj.columns = ['DJ', 'Count']
    dj = dj.sort_values(by=['Count'], ascending=False).reset_index(drop=True)
    dj.index += 1
    print tabulate(dj, headers='keys', tablefmt='psql').encode('utf-8')
    return


def main():
    print 'This is not an independent package.'
    return


if __name__ == '__main__':
    main()
