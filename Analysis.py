import gc

import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import tensorflow as tf
# import zfit
# from zfit import z
from pathlib import Path

from service import hist_dict, hist2d_dict


def create_vars(data):
    # E/p for e plus
    data['e_plus_Ecal_over_pTR'] = np.divide(data['e_plus_CaloEcalE'], data['e_plus_TRACK_P'])
    data['e_plus_Ecal_over_p'] = np.divide(data['e_plus_CaloEcalE'], data['e_plus_P'])

    data['e_plus_Efull_over_p'] = np.divide(np.vectorize(calc_full_e)(data.e_plus_CaloEcalE,
                                                                      data.e_plus_CaloHcalE,
                                                                      data.e_plus_CaloSpdE,
                                                                      data.e_plus_CaloPrsE),
                                            data['e_plus_P'])

    data['e_plus_ETRUE_over_p'] = np.divide(data['e_plus_TRUEP_E'], data['e_plus_P'])
    data['e_plus_ETRUE_over_pTR'] = np.divide(data['e_plus_TRUEP_E'], data['e_plus_TRACK_P'])
    data['e_plus_ETRUE_over_pTRUE'] = np.divide(data['e_plus_TRUEP_E'],
                                                np.vectorize(calc_momentum)(data.e_plus_TRUEP_X,
                                                                            data.e_plus_TRUEP_Y,
                                                                            data.e_plus_TRUEP_Z))
    # E/p for K
    data['K_Ecal_over_pTR'] = np.divide(data['K_Kst_CaloEcalE'], data['K_Kst_TRACK_P'])
    data['K_Ecal_over_p'] = np.divide(data['K_Kst_CaloEcalE'], data['K_Kst_P'])
    data['K_Efull_over_p'] = np.divide(np.vectorize(calc_full_e)(data.K_Kst_CaloEcalE,
                                                                 data.K_Kst_CaloHcalE,
                                                                 data.K_Kst_CaloSpdE,
                                                                 data.K_Kst_CaloPrsE),
                                       data['K_Kst_P'])
    data['K_Kst_ETRUE_over_p'] = np.divide(data['K_Kst_TRUEP_E'], data['K_Kst_P'])
    data['K_Kst_ETRUE_over_pTR'] = np.divide(data['K_Kst_TRUEP_E'], data['K_Kst_TRACK_P'])
    data['K_Kst_ETRUE_over_pTRUE'] = np.divide(data['K_Kst_TRUEP_E'],
                                               np.vectorize(calc_momentum)(data.K_Kst_TRUEP_X,
                                                                           data.K_Kst_TRUEP_Y,
                                                                           data.K_Kst_TRUEP_Z))
    # E/p for e minus
    data['e_minus_Ecal_over_pTR'] = np.divide(data['e_minus_CaloEcalE'], data['e_minus_TRACK_P'])
    data['e_minus_Ecal_over_p'] = np.divide(data['e_minus_CaloEcalE'], data['e_minus_P'])
    data['e_minus_Efull_over_p'] = np.divide(np.vectorize(calc_full_e)(data.e_minus_CaloEcalE,
                                                                       data.e_minus_CaloHcalE,
                                                                       data.e_minus_CaloSpdE,
                                                                       data.e_minus_CaloPrsE),
                                             data['e_minus_P'])
    # dielectron separation
    data['ee_separation'] = np.sqrt(
        np.power(data.e_plus_L0Calo_ECAL_xProjection - data.e_minus_L0Calo_ECAL_xProjection, 2) +
        np.power(data.e_plus_L0Calo_ECAL_yProjection - data.e_minus_L0Calo_ECAL_yProjection, 2)
    )
    # K-e separation
    data['K_emin_sep'] = np.sqrt(
        np.power(data.K_Kst_L0Calo_HCAL_xProjection - data.e_minus_L0Calo_ECAL_xProjection, 2) +
        np.power(data.K_Kst_L0Calo_HCAL_yProjection - data.e_minus_L0Calo_ECAL_yProjection, 2)
    )

    data['K_eplus_sep'] = np.sqrt(
        np.power(data.K_Kst_L0Calo_HCAL_xProjection - data.e_plus_L0Calo_ECAL_xProjection, 2) +
        np.power(data.K_Kst_L0Calo_HCAL_yProjection - data.e_plus_L0Calo_ECAL_yProjection, 2)
    )

    # some other stuff
    # data['e_plus_E'] = np.vectorize(calc_e_from_p)(data.e_plus_P)

    data['J_psi_M_recalc'] = np.vectorize(calc_q2)(data.e_plus_PE, data.e_minus_PE,
                                                   data.e_plus_PX, data.e_minus_PX,
                                                   data.e_plus_PY, data.e_minus_PY,
                                                   data.e_plus_PZ, data.e_minus_PZ)

    data['ee_cosTheta'] = np.vectorize(calc_cosTheta)(data.e_plus_P, data.e_minus_P,
                                                      data.e_plus_PX, data.e_minus_PX,
                                                      data.e_plus_PY, data.e_minus_PY,
                                                      data.e_plus_PZ, data.e_minus_PZ)

    data['e_plus_CaloFullE'] = np.vectorize(calc_full_e)(data.e_plus_CaloEcalE, data.e_plus_CaloHcalE,
                                                         data.e_plus_CaloSpdE, data.e_plus_CaloPrsE)
    data['K_Kst_CaloFullE'] = np.vectorize(calc_full_e)(data.K_Kst_CaloEcalE, data.K_Kst_CaloHcalE,
                                                        data.K_Kst_CaloSpdE, data.K_Kst_CaloPrsE)
    return data


def read_file(path, branches, filename, maxevts=400000, PIDcut=3, skip1d=False, skip2d=False):
    # may want to skip building 1d or 2d for some tests
    if skip1d:
        print('Will not build any 1d histograms')
    if skip2d:
        print('Will not build any 2d histograms')

    if 'Kee' in filename:
        prefix = 'Kee'
    elif 'KJPsiee' in filename:
        prefix = 'KJPsiee'
    else:
        raise FileNotFoundError('Wrong filename, Kee or KJPsiee only!')
    treename = 'B2Kee_Tuple/DecayTree'

    # create dicts to temporarily hold histograms

    full_histos_pol = {}
    full_histos2d_pol = {}

    cut_histos_pol = {}
    cut_histos2d_pol = {}

    full_num_events = 0
    cut_num_events = 0

    # same procedure for both polarities
    for pol in ('MD', 'MU'):
        current_progress = 0

        # create holding dicts for the current polarity
        if not skip1d:
            full_histos_pol[pol] = {key: None for key in hist_dict.keys()}
            cut_histos_pol[pol] = {key: None for key in hist_dict.keys()}
        if not skip2d:
            full_histos2d_pol[pol] = {key: None for key in hist2d_dict.keys()}
            cut_histos2d_pol[pol] = {key: None for key in hist2d_dict.keys()}


        # open the root file
        if not path == '':
            sample = uproot.open(f'{path}/{prefix}_2018_{pol}.root')[treename]
        else:
            sample = uproot.open(f'{prefix}_2018_{pol}.root')[treename]
        tot_num = min(sample.num_entries, maxevts)

        print(f'WORKING ON {prefix} {pol} FILE...')

        # iterating over the file with a fixed batch size (100 000) and a given number of max events
        for df in sample.iterate(branches, library='pd', entry_stop=maxevts, step_size=100000):

            # deleting all but 0th subentries, removing subentry level
            if df.index.nlevels == 2:
                df = df.loc[(slice(None), 0), :].droplevel(level=1)

            # progress indicator, TODO: implement progress bar
            current_progress = current_progress + len(df.index)
            print(f'Currently at {current_progress} / {tot_num} events...')

            # create new variables
            df = create_vars(df)
            df = divide_brem_cats(df)

            # truthmatching, B_DTFM and J_Psi mass window cuts
            df = common_cuts(df, filename)
            df = mass_cuts(df, filename)

            # saving the number of events at this stage (before PID cuts)
            full_num_events = full_num_events + len(df.index)

            # creating 1d and 2d histograms for the current batch
            if not skip1d:
                for key in hist_dict.keys():
                    full_histos_pol[pol][key] = make_hist(df[key], key, hist_dict=hist_dict,
                                                          hist=full_histos_pol[pol][key])
            if not skip2d:
                for key in hist2d_dict.keys():
                    full_histos2d_pol[pol][key] = make_hist2d(df, key, hist2d_dict=hist2d_dict,
                                                              hist=full_histos2d_pol[pol][key])

            # cutting on PID
            df = misid_cuts(df, filename, PIDcut=PIDcut)

            # creating 1d and 2d histograms for events survivng PID cuts
            if not skip1d:
                for key in hist_dict.keys():
                    cut_histos_pol[pol][key] = make_hist(df[key], key, hist_dict=hist_dict,
                                                         hist=cut_histos_pol[pol][key])
            if not skip2d:
                for key in hist2d_dict.keys():
                    cut_histos2d_pol[pol][key] = make_hist2d(df, key, hist2d_dict=hist2d_dict,
                                                             hist=cut_histos2d_pol[pol][key])

            # creating special E/p histograms for all electrons (both signs) of the same brem category
            if not skip1d:
                brem_frames = setup_brem_hists(df)
                for brem_cat in range(3):
                    for mode in ('p', 'pTR'):
                        # skip duplicate (p and pTR are the same for brem 0 by definition, we skip "p")
                        if mode == 'p' and brem_cat == 0:
                            continue
                        else:
                            # if histogram already exists, add new data to it...
                            if f'EoP_{mode}_{brem_cat}' in cut_histos_pol[pol].keys():
                                cut_histos_pol[pol][f'EoP_{mode}_{brem_cat}'] = \
                                    make_brem_hist(brem_frames[str(brem_cat)][f'Ecal_over_{mode}'],
                                                   hist=cut_histos_pol[pol][f'EoP_{mode}_{brem_cat}'])

                            # .. otherwise, create new hist
                            else:
                                cut_histos_pol[pol][f'EoP_{mode}_{brem_cat}'] = \
                                    make_brem_hist(brem_frames[str(brem_cat)][f'Ecal_over_{mode}'])

            # save number of events after all cuts (technically unnecessary, can just check np.sum() of a hist)
            cut_num_events = cut_num_events + len(df.index)

            # remove batch to save memory
            del df
            gc.collect()
        print(f'FINISHED WITH {prefix} {pol} FILE!\n*********')

    # setup dicts for histogram collection and add up the collected histograms from different polarities
    if not skip1d:
        full_histos = {key: None for key in full_histos_pol['MD'].keys()}
        cut_histos = {key: None for key in cut_histos_pol['MD'].keys()}
        for key in full_histos.keys():
            full_histos[key] = np.add(full_histos_pol['MU'][key], full_histos_pol['MD'][key])
        for key in cut_histos.keys():
            cut_histos[key] = np.add(cut_histos_pol['MU'][key], cut_histos_pol['MD'][key])
        del cut_histos_pol, full_histos_pol

    if not skip2d:
        full_histos2d = {key: None for key in full_histos2d_pol['MD'].keys()}
        cut_histos2d = {key: None for key in cut_histos2d_pol['MD'].keys()}
        for key in full_histos2d.keys():
            full_histos2d[key] = np.add(full_histos2d_pol['MU'][key], full_histos2d_pol['MD'][key])
        for key in cut_histos2d.keys():
            cut_histos2d[key] = np.add(cut_histos2d_pol['MU'][key], cut_histos2d_pol['MD'][key])
        del cut_histos2d_pol, full_histos2d_pol

    gc.collect()
    print('RESULTS:')
    print(f'NUMBER OF EVENTS AFTER COMMON CUTS:          {full_num_events}')
    print(f'NUMBER OF EVENTS AFTER COMMON & PID CUTS:    {cut_num_events}')
    print('!! SKIPPED BUILDING 1D HISTOGRAMS !!' if skip1d else '')
    print('!! SKIPPED BUILDING 2D HISTOGRAMS !!' if skip2d else '')

    # a question of preference: 2 separate dicts or {'1d': {...}, '2d': {...}}
    if not skip1d and not skip2d:
        return {'full': full_histos, 'cut': cut_histos}, {'full': full_histos2d, 'cut': cut_histos2d}
    elif skip1d and not skip2d:
        return None, {'full': full_histos2d, 'cut': cut_histos2d}
    elif not skip1d and skip2d:
        return {'full': full_histos, 'cut': cut_histos}, None
    else:
        return None, None


def common_cuts(data_df, filename):
    # ELECTRON TRUTH-MATCHING
    # if 'Kee' in filename:
    # ele_cuts = 'abs(e_minus_TRUEID) == 11 and abs(e_plus_TRUEID) == 11'# \
    # 'abs(e_plus_MC_MOTHER_ID) == 521 and abs(e_minus_MC_MOTHER_ID) == 521'

    if 'KJPsiee' in filename:
        ele_cuts = 'abs(e_plus_TRUEID) == 11 and abs(e_minus_TRUEID) == 11 and ' \
                   'abs(e_plus_MC_MOTHER_ID) == 443 and abs(e_minus_MC_MOTHER_ID) == 443 and ' \
                   'abs(e_plus_MC_GD_MOTHER_ID) == 521 and abs(e_minus_MC_GD_MOTHER_ID) == 521 and ' \
                   'abs(K_Kst_TRUEID) == 321 and abs(K_Kst_MC_MOTHER_ID) == 521 and B_plus_BKGCAT == 0'
    data_df.query(f'{ele_cuts}', inplace=True)
    return data_df


def mass_cuts(data_df, filename):
    if 'KJPsiee' in filename:
        JPsi_presel = '(J_psi_1S_M/1000.) ** 2 > 6 and (J_psi_1S_M/1000.) ** 2 < 12.96'
        B_plus_M_cut = 'B_plus_DTFM_M > 5200 and B_plus_DTFM_M < 5680'
        data_df.query(f'{JPsi_presel} and {B_plus_M_cut}', inplace=True)
    return data_df


def misid_cuts(data_df, filename, PIDcut=3):
    # KAON-ELECTRON MIS-ID

    PIDcut_K = PIDcut
    B2eee_cut = f'e_plus_PIDe > {PIDcut} and e_minus_PIDe > {PIDcut} and K_Kst_PIDe > {PIDcut_K}'
    data_df.query(B2eee_cut, inplace=True)
    # print(f'***\nAPPLYING PID CUTS. EVENTS REMAINING: {len(data_df.index)}')
    # LOW MOMENTUM CUT
    # data_df.query('e_plus_P > 100000', inplace = True)
    return data_df


def divide_brem_cats(data):
    conditions = [
        data['e_plus_BremMultiplicity'].eq(0) & data['e_minus_BremMultiplicity'].eq(0),

        (data['e_plus_BremMultiplicity'].eq(0) & data['e_minus_BremMultiplicity'].eq(1)) |
        (data['e_plus_BremMultiplicity'].eq(1) & data['e_minus_BremMultiplicity'].eq(0)),

        (data['e_plus_BremMultiplicity'].eq(0) & data['e_minus_BremMultiplicity'].gt(1)) |
        (data['e_plus_BremMultiplicity'].gt(1) & data['e_minus_BremMultiplicity'].eq(0)) |
        (data['e_plus_BremMultiplicity'].ge(1) & data['e_minus_BremMultiplicity'].ge(1))
    ]

    brem_cats = ['brem_zero', 'brem_one', 'brem_two']

    data['brem_tag'] = np.select(conditions, brem_cats, default=0)
    return data


def setup_brem_hists(df):
    frames = {}
    pl_min = [None, None]
    for i in range(3):
        if not i == 2:
            pl_min[0] = df.loc[df['e_plus_BremMultiplicity'] == i, ['e_plus_Ecal_over_p', 'e_plus_Ecal_over_pTR']]
            pl_min[1] = df.loc[df['e_minus_BremMultiplicity'] == i, ['e_minus_Ecal_over_p', 'e_minus_Ecal_over_pTR']]
        else:
            pl_min[0] = df.loc[df['e_plus_BremMultiplicity'] >= i, ['e_plus_Ecal_over_p', 'e_plus_Ecal_over_pTR']]
            pl_min[1] = df.loc[df['e_minus_BremMultiplicity'] >= i, ['e_minus_Ecal_over_p', 'e_minus_Ecal_over_pTR']]
        frames[str(i)] = pd.DataFrame()
        frames[str(i)]['Ecal_over_p'] = pd.concat([pl_min[0]['e_plus_Ecal_over_p'], pl_min[1]['e_minus_Ecal_over_p']])
        frames[str(i)]['Ecal_over_pTR'] = pd.concat(
            [pl_min[0]['e_plus_Ecal_over_pTR'], pl_min[1]['e_minus_Ecal_over_pTR']])
    return frames


def calc_e_from_p(momentum):
    energy = np.sqrt(momentum ** 2 + 0.5 ** 2)
    return energy


def calc_q2(e1, e2, px1, px2, py1, py2, pz1, pz2):
    q2 = (e1 + e2) ** 2 - (px1 + px2) ** 2 - (py1 + py2) ** 2 - (pz1 + pz2) ** 2
    return np.sqrt(q2)


def calc_full_e(ecal, hcal, spd, prs):
    energy = ecal + hcal + spd + prs
    return energy


def calc_cosTheta(p1, p2, px1, px2, py1, py2, pz1, pz2):
    return np.divide(px1 * px2 + py1 * py2 + pz1 * pz2, p1 * p2)


def calc_momentum(px, py, pz):
    return np.sqrt(px ** 2 + py ** 2 + pz ** 2)


def make_hist(x, title, hist_dict, hist=None):
    nbins = int(hist_dict[title]['n_bins'])
    xmin = hist_dict[title]['xmin']
    xmax = hist_dict[title]['xmax']
    bin_width = (xmax - xmin) / nbins
    bins = [xmin + x * bin_width for x in range(nbins + 1)]
    data_x, _ = np.histogram(x.values, bins=bins)
    if hist is not None:
        return np.add(hist, data_x)
    else:
        return data_x


def make_hist2d(df, title, hist2d_dict, hist=None):
    # need to give the binning scheme (num bins, min, max) <- defined in hist2d_dict entry
    xbins = int(hist2d_dict[title]['x_bins'])
    xmin = hist2d_dict[title]['xmin']
    xmax = hist2d_dict[title]['xmax']

    ybins = int(hist2d_dict[title]['y_bins'])
    ymin = hist2d_dict[title]['ymin']
    ymax = hist2d_dict[title]['ymax']

    # variables to bin <- defined in hist2d_dict (more manual labor, but imho more robust)
    xvar = hist2d_dict[title]['xvar']
    yvar = hist2d_dict[title]['yvar']

    # creating bins
    xbin_width = (xmax - xmin) / xbins
    bins_x = [xmin + x * xbin_width for x in range(xbins + 1)]
    ybin_width = (ymax - ymin) / ybins
    bins_y = [ymin + x * ybin_width for x in range(ybins + 1)]

    # getting the correct vars
    x = df[xvar]
    y = df[yvar]

    # creating the his2td
    data, x_edges, y_edges = np.histogram2d(x, y, bins=[xbins, ybins], range=[[xmin, xmax], [ymin, ymax]])
    if hist is not None:
        return np.add(hist, data)
    else:
        return data


def plot_hist(x, title, hist_dict, path='', PIDcut=3, normalize=False):
    plt.clf()

    # from service import hist_dict
    plt_title = hist_dict[title]['plt_title'] + f', PIDe > {PIDcut}'
    nbins = int(hist_dict[title]['n_bins'])
    xlabel = hist_dict[title]['xlabel']
    xmin = hist_dict[title]['xmin']
    xmax = hist_dict[title]['xmax']

    bin_width = (xmax - xmin) / nbins
    bins = [xmin + x * bin_width for x in range(nbins)]

    if type(x) == dict:
        for label, item in x.items():
            if not normalize:
                plt.yscale('log')
                plt.bar(height=item, x=bins, align='edge', label=label, alpha=0.5)
            else:
                plt.bar(height=item / np.sum(item), width=bin_width, x=bins, align='edge', label=label, alpha=0.5)
            plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
            plt.legend(loc='upper right')
    else:
        plt.bar(height=x, x=bins, align='edge')
        plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
    plt.xlabel(xlabel)
    plt.title(plt_title)
    path_stem = title + '.png'
    plt.savefig(path + '/' + path_stem)


def plot_hist2d(data, title, hist2d_dict, path='', PIDcut=3, mode='full'):
    if mode not in ('full', 'cut', 'eff'):
        raise NotImplementedError(f"Plotting 2d histogram in mode {mode}; only ('full', 'cut', 'eff') are supported")
    plt.clf()
    fig, ax = plt.subplots()
    if mode == 'cut':
        title_stem = f', all PIDe > {PIDcut}'
    elif mode == 'eff':
        title_stem = f', cut efficiency'
    else:
        title_stem = ''

    plt_title = hist2d_dict[title]['plt_title'] + title_stem

    xn_bins = int(hist2d_dict[title]['x_bins'])
    xlabel = hist2d_dict[title]['xlabel']
    xmin = hist2d_dict[title]['xmin']
    xmax = hist2d_dict[title]['xmax']

    yn_bins = int(hist2d_dict[title]['y_bins'])
    ylabel = hist2d_dict[title]['ylabel']
    ymin = hist2d_dict[title]['ymin']
    ymax = hist2d_dict[title]['ymax']

    clabel = hist2d_dict[title]['clabel']
    cmin = hist2d_dict[title]['cmin']   # do we need these? How to estimate before building hist? Maybe just drop them
    cmax = hist2d_dict[title]['cmax']

    xbin_width = (xmax - xmin) / xn_bins
    x_bins = np.array([xmin + x * xbin_width for x in range(xn_bins)])

    ybin_width = (ymax - ymin) / yn_bins
    y_bins = np.array([ymin + y * ybin_width for y in range(yn_bins)])

    xs, ys = np.meshgrid(x_bins, y_bins)
    import matplotlib.colors as colors
    if 'log' not in hist2d_dict[title]['cscale'] or mode == 'eff':
        h = ax.pcolor(xs, ys, data.T)  # , vmin=cmin, vmax=cmax)
    else:
        h = ax.pcolor(xs, ys, data.T, norm=colors.LogNorm())
    fig.colorbar(h, ax=ax, label=clabel)

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(plt_title)
    path_stem = 'biplot_' + title + '_' + mode + '.png'
    plt.savefig(path + '/' + path_stem)




def make_brem_hist(x, hist=None):
    nbins = 50
    xmin = -0.5
    xmax = 1.5
    bin_width = (xmax - xmin) / nbins
    bins = [xmin + x * bin_width for x in range(nbins + 1)]
    data_x, _ = np.histogram(x.values, bins=bins)
    if hist is not None:
        return np.add(hist, data_x)
    else:
        return data_x


def plot_EoP_bremcat(x, brem_cat, ele='e_plus', mode='Full', path='', PIDcut=3):
    plt.clf()

    # from service import hist_dict
    plt_title = f'ECAL Energy over {mode} momentum, {brem_cat}, PIDe > {PIDcut}'
    nbins = 50
    xlabel = f'Energy / {mode} Momentum, A.U.'
    xmin = -0.5
    xmax = 1.5
    bin_width = (xmax - xmin) / nbins
    bins = [xmin + x * bin_width for x in range(nbins)]
    plt.bar(height=x, width=bin_width, x=bins, align='edge')
    plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
    plt.xlabel(xlabel)
    plt.title(plt_title)
    path_stem = f'EoP_{mode}_{brem_cat}.jpg'
    plt.savefig(path + '/' + path_stem)


# def fit_e_over_p(data, ini_params=None):
#     min = 0.
#     max = 2.5
#     obs = zfit.Space('E_over_p', limits=(min, max))
#
#     dcb_mu = zfit.Parameter('dcb_mu', 0.8, 0.2, 1.5)
#     dcb_sigma = zfit.Parameter('dcb_sigma', 0.7, 0.1, 2.)
#     nr = zfit.Parameter('dcb_nr', 1., 0.1, 5, )
#     nl = zfit.Parameter('dcb_nl', 1., 0.1, 5, )
#     alphar = zfit.Parameter('dcb_alphar', 1., 0.1, 5, )
#     alphal = zfit.Parameter('dcb_alphal', 1., 0.1, 5, )
#
#     n_events = zfit.Parameter('dcb_yield', len(data.index), step_size=1)
#
#     dcb = zfit.pdf.DoubleCB(mu=dcb_mu, sigma=dcb_sigma, nr=nr, nl=nl, alphar=alphar, alphal=alphal,
#                             name='DCB pdf', obs=obs)
#     model = dcb.create_extended(n_events)
#
#     nll = zfit.loss.ExtendedUnbinnedNLL(model=model, data=data)
#     minimizer = zfit.minimize.Minuit()
#     result = minimizer.minimize(nll)
#     info = result.info.get('original')
#     if result.converged:
#         print('converged')
#     if info.is_valid:
#         print('valid')
#
#     params = result.params
#     print(params)
#
#     plt.clf()
#     axes = plt.gca()
#     lower, upper = obs.limits
#     bin_num = 50
#     x_plot = np.linspace(lower[-1][0], upper[0][0], num=1000)
#     y_plot = zfit.run(model.pdf(x_plot, norm_range=obs))
#     # plt.text(0.05, 0.9, mu_string, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
#     # plt.text(0.75, 0.85, sigma_string, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
#     plt.plot(x_plot, y_plot * len(data) / bin_num * obs.area(), color='xkcd:black', label='CrystalBall')
#     # plt.hist(data['ratio'], bins=50, range=(min , max))
#     width = (max - min) / bin_num
#     bins = [min + x * width for x in range(bin_num + 1)]
#     bin_centres = [min + width / 2 + x * width for x in range(bin_num)]
#     hist_data, binning = np.histogram(data.values, bins=bins)
#     axes.errorbar(x=bin_centres, y=hist_data,
#                   yerr=np.sqrt(hist_data),
#                   fmt='ko', markersize='2', label='E/p')
#     plt.title("E/p ratio")
#     plt.legend()
#     plt.savefig(plot_path + '/Efull_over_p_fit_cb.jpg')
#     plt.text(0.05, 0.9, params, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
#     plt.savefig(plot_path + '/ratio_params_cb.jpg')
#     plt.clf()
#
#     return None  # TODO


if __name__ == '__main__':
    path = ''
    filename = 'KJPsiee'
    plot_path = 'Plots/' + str(filename) + '_0211_base'
    username = os.getlogin()
    if username == 'roman':
        max_events = 200000
    else:
        max_events = 2000000
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    # if not os.path.exists(plot_path_full):
    #     os.makedirs(plot_path_full)

    from service import branches  # too long of a list, decided to move it to service file

    PIDcut = 3

    histograms, histograms2d = read_file(path, branches, filename, maxevts=max_events, PIDcut=PIDcut, skip1d=False)

    if histograms is not None:
        for key in hist_dict.keys():
            comp_dict = {'Before cuts': histograms['full'][key], f'PIDe > {PIDcut}': histograms['cut'][key]}
            plot_hist(comp_dict, key, hist_dict=hist_dict, path=plot_path, PIDcut=PIDcut, normalize=True)

    if histograms2d is not None:
        histograms2d['eff'] = {key: np.divide(histograms2d['cut'][key], histograms2d['full'][key]) for key in histograms2d['cut'].keys()}
        for key in hist2d_dict.keys():
            for mode in ('full', 'cut', 'eff'):
                plot_hist2d(histograms2d[mode][key], key, hist2d_dict=hist2d_dict, path=plot_path, PIDcut=PIDcut,
                            mode=mode)

    if histograms is not None:
        for brem_cat in range(3):
            for mode in ('p', 'pTR'):
                if brem_cat == 0 and mode == 'p':
                    continue
                else:
                    plot_EoP_bremcat(histograms['cut'][f'EoP_{mode}_{brem_cat}'],
                                     brem_cat=brem_cat, mode=mode, path=plot_path)

    # ************ LOG (of sorts) *******************
    # fit_e_over_p(cut_data['e_plus_Efull_over_p']) ................ TODO
    # 2 electrons from JPsi (e trueid, e mc mother id, don't forget abs .......... done!
    # change one electrons energy so that it has a mass hypothesis of a proton ........ NA
    # recalculate Jpsi M (sqrt(q2)) ........... NA
    # check at what e momentum it peaks at jpsi ............. NA

    # log scale for E/p plots (without density) ........ done!
    # PID >2, 3, 4 ............ TODO
    # Проверить насчет TRUE_E .... done!

    # 2D histograms ............. TODO, in progress
    # RICH study, RICH impact for PID ................ TODO
    # geometrical acceptance study ................. TODO
    # some sort of presentation ............... TODO
