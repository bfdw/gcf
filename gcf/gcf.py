# !/usr/bin/env python
# -*- coding: utf-8 -*-


import click

import gcf_mining as gm
import gcf_scrape as gs


@click.group(invoke_without_command=True, no_args_is_help=True)
@click.option('--dj', '-d', default='',
              help=u'Search by dj, such as -d \'西蒙#四十二\' or \'西蒙\'.\
              Use #, if you need a dj group.')
@click.option('--prog', '-p', default='',
              help='Search by program, such as -p \'gadio\'.\
              Use #, if you need multiple programs.')
@click.option('--title', '-tt', default='',
              help=u'Search by program, such as -tt \'的\'.')
@click.option('--time', '-t', nargs=2, default=('19850611', '20850611'),
              help='Search by release time, such as -t 20180101 20180302')
@click.option('--expt', '-e', default=False, is_flag=True,
              help='Export data to a cvs file')
@click.option('--col', '-c', default='date#title#dj',
              help='Show data with specific columns as -tb \'date#title#dj\'')
@click.option('--path', '-pt', default='',
              help='Give the path to loading another cvs data.')
@click.option('--recent', '-r', default=9999,
              help='Show the most recent gadios.')
@click.pass_context
def gcf(ctx, dj, prog, time, title, expt, col, path, recent):
    """\b
          _____       _____      ______
         / ____|     / ____|    |  ____|
        | |  __     | |         | |__
        | | |_ |    | |         |  __|
        | |__| |    | |____     | |
         \_____|     \_____|    |_|

  G-Cores(g-cores.com) Fans --- A Gadio Info Tool
    """

    if ctx.invoked_subcommand == 'update':
        return

    col = map((lambda x: 'radio_' + str(x)), filter(None, col.split('#')))

    dj_pd = gm.kw_mining(gm.df_pk(path),
                         u'radio_dj',
                         filter(None, dj.split('#')))

    prog_pd = gm.kw_mining(dj_pd,
                           u'radio_program',
                           filter(None, prog.split('#')))

    title_pd = gm.kw_mining(prog_pd,
                            u'radio_title',
                            filter(None, title.split('#')))

    time_pd = gm.timing_mining(title_pd, time[0], time[1])

    final_pd = gm.recent(time_pd, recent)

    if expt:
        final_pd.to_csv('./gcf.cvs', encoding='utf-8', index=False)

    if ctx.invoked_subcommand == 'career':
        ctx.obj['final_pd'] = final_pd
        ctx.obj['path'] = path
        return

    if ctx.invoked_subcommand == 'statistic':
        ctx.obj['final_pd'] = final_pd
        return

    if ctx.invoked_subcommand is None:
        gm.df_print(final_pd, col)
        return
    return


@gcf.command()
@click.option('--deep', default=False, is_flag=True,
              help='Reload the whole data.')
@click.pass_context
def update(ctx, deep):
    """Update data to the last gadio"""
    gs.scrape_radio_list(deep)
    return


@gcf.command()
@click.option('--size', '-s', default='Y',
              type=click.Choice(['Y', 'Q', 'M']),
              help='Choice the statistic size: Y(year),Q(quarter),M(month).')
@click.option('--perc', '-p', default=False, is_flag=True,
              help='Show data with the percentage of whole set.')
@click.option('--ratio', '-r', default=2, type=float,
              help='Graphic Ratio. Smaller value, more width graphic.')
@click.pass_context
def career(ctx, size, perc, ratio):
    """Show results with the career mode"""
    gm.care_mode(ctx.obj['final_pd'], ctx.obj['path'], size, perc, ratio)
    return


@gcf.command()
@click.pass_context
def statistic(ctx):
    """Show results with statistic mode"""
    gm.stat_mode(ctx.obj['final_pd'])
    return


@gcf.command()
@click.pass_context
def drop(ctx):
    """Drop all radio information"""
    gs.drop_raido()
    return


def main():
    gcf(obj={})


if __name__ == '__main__':
    main()
