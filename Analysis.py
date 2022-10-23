import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tensorflow as tf
import zfit
from zfit import z
from pathlib import Path

from service import hist_dict


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


def read_file(path, branches, filename, maxevts=200000):
    if 'Kee' in filename:
        prefix = 'Kee'
    elif 'KJPsiee' in filename:
        prefix = 'KJPsiee'
    else:
        raise FileNotFoundError('Wrong filename, Kee or KJPsiee only!')

    treename = 'B2Kee_Tuple/DecayTree'
    # with uproot.open(f'{path}/{prefix}_2018_MD.root') as file:
    #     tree = file[treename]
    #     data_MD = tree.arrays(branches, library='pd')

    # with uproot.open(f'{path}/{prefix}_2018_MU.root') as file:
    #     tree = file[treename]
    #     data_MU = tree.arrays(branches, library='pd')

    data_MD = pd.DataFrame()
    if not path == '':
        sample = uproot.open(f'{path}/{prefix}_2018_MD.root')[treename]
    else:
        sample = uproot.open(f'{prefix}_2018_MD.root')[treename]
    for df in sample.iterate(branches, library='pd', entry_stop=maxevts):
        data_MD = pd.concat([data_MD, df])

    data_MU = pd.DataFrame()
    if not path == '':
        sample = uproot.open(f'{path}/{prefix}_2018_MU.root')[treename]
    else:
        sample = uproot.open(f'{prefix}_2018_MU.root')[treename]
    for df in sample.iterate(branches, library='pd', entry_stop=maxevts):
        data_MU = pd.concat([data_MU, df])

    data_df = pd.concat([data_MD, data_MU])
    print(f'TOTAL NUMBER OF EVENTS: {len(data_df.index)}')
    return data_df


def common_cuts(data_df, filename, PIDcut=3):
    # ELECTRON TRUTH-MATCHING
    # if 'Kee' in filename:
    # ele_cuts = 'abs(e_minus_TRUEID) == 11 and abs(e_plus_TRUEID) == 11'# \
    # 'abs(e_plus_MC_MOTHER_ID) == 521 and abs(e_minus_MC_MOTHER_ID) == 521'


    if 'KJPsiee' in filename:
        ele_cuts = 'abs(e_plus_TRUEID) == 11 and abs(e_minus_TRUEID) == 11 and ' \
                   'abs(e_plus_MC_MOTHER_ID) == 443 and abs(e_minus_MC_MOTHER_ID) == 443 and ' \
                   'abs(e_plus_MC_GD_MOTHER_ID) == 521 and abs(e_minus_MC_GD_MOTHER_ID) == 521 and ' \
                   'abs(K_Kst_TRUEID) == 321 and abs(K_Kst_MC_MOTHER_ID) == 521 and B_plus_BKGCAT == 0'
        JPsi_presel = '(J_psi_1S_M/1000.) ** 2 > 6 and (J_psi_1S_M/1000.) ** 2 < 12.96'
        B_plus_M_cut = 'B_plus_DTFM_M > 5200 and B_plus_DTFM_M < 5680'
    data_df.query(f'{ele_cuts} and {JPsi_presel} and {B_plus_M_cut}', inplace=True)

    # ===========================================================
    # KJPsiee sample
    # Truthmatching сuts
    # ID match + B_plus_BKGCAT == 0: 111 454 / 400 000
    # ID match: 143 415 / 400 000
    # B_plus_BKGCAT: 111 793 / 400 000
    #
    # ID match + J_psi_1S_BKGCAT: 112 963 / 400 000
    # J_psi_1S_BKGCAT: 133 337 / 400 000
    #
    # ID match + B_plus_BKGCAT + J_psi_1S_BKGCAT: 111 454 / 400 000
    # B_plus_BKGCAT + J_psi_1S_BKGCAT: 111 793 / 400 000
    # ===========================================================

    # KAON-ELECTRON MIS-ID

    # PIDcut_K = PIDcut
    # B2eee_cut = f'e_plus_PIDe > {PIDcut} and e_minus_PIDe > {PIDcut} and K_Kst_PIDe > {PIDcut_K}'
    # data_df.query(B2eee_cut, inplace=True)
    print(f'NUMBER OF EVENTS AFTER CUTS: {len(data_df.index)}')


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


def plot_hist(x, title, hist_dict, path='', PIDcut=3):
    plt.clf()

    # from service import hist_dict
    plt_title = hist_dict[title]['plt_title'] + f', PIDe > {PIDcut}'
    nbins = int(hist_dict[title]['n_bins'])
    xlabel = hist_dict[title]['xlabel']
    xmin = hist_dict[title]['xmin']
    xmax = hist_dict[title]['xmax']
    if type(x) == dict:
        for label, item in x.items():
            plt.yscale('log')
            plt.hist(item, range=(xmin, xmax), bins=nbins, label=label, alpha=0.5)
            plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
            plt.legend(loc='upper right')
    else:
        plt.hist(x, range=(xmin, xmax), bins=nbins)
        plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
    plt.xlabel(xlabel)
    plt.title(plt_title)
    path_stem = title + '.png'
    plt.savefig(path + '/' + path_stem)


def plot_EoP_bremcat(x, brem_cat, ele='e_plus', mode='Full', path='', PIDcut=3):
    plt.clf()

    # from service import hist_dict
    plt_title = f'ECAL Energy over {mode} momentum, {brem_cat}, PIDe > {PIDcut}'
    nbins = 50
    xlabel = f'Energy / {mode} Momentum, A.U.'
    xmin = -0.5
    xmax = 1.5
    plt.hist(x, range=(xmin, xmax), bins=nbins)
    plt.ylabel(f'Events / {(xmax - xmin) / nbins}')
    plt.xlabel(xlabel)
    plt.title(plt_title)
    path_stem = f'{ele}_EoP_{mode}_{brem_cat}.png'
    plt.savefig(path + '/' + path_stem)


def fit_e_over_p(data, ini_params=None):
    min = 0.
    max = 2.5
    obs = zfit.Space('E_over_p', limits=(min, max))

    dcb_mu = zfit.Parameter('dcb_mu', 0.8, 0.2, 1.5)
    dcb_sigma = zfit.Parameter('dcb_sigma', 0.7, 0.1, 2.)
    nr = zfit.Parameter('dcb_nr', 1., 0.1, 5, )
    nl = zfit.Parameter('dcb_nl', 1., 0.1, 5, )
    alphar = zfit.Parameter('dcb_alphar', 1., 0.1, 5, )
    alphal = zfit.Parameter('dcb_alphal', 1., 0.1, 5, )

    n_events = zfit.Parameter('dcb_yield', len(data.index), step_size=1)

    dcb = zfit.pdf.DoubleCB(mu=dcb_mu, sigma=dcb_sigma, nr=nr, nl=nl, alphar=alphar, alphal=alphal,
                            name='DCB pdf', obs=obs)
    model = dcb.create_extended(n_events)

    nll = zfit.loss.ExtendedUnbinnedNLL(model=model, data=data)
    minimizer = zfit.minimize.Minuit()
    result = minimizer.minimize(nll)
    info = result.info.get('original')
    if result.converged:
        print('converged')
    if info.is_valid:
        print('valid')

    params = result.params
    print(params)

    plt.clf()
    axes = plt.gca()
    lower, upper = obs.limits
    bin_num = 50
    x_plot = np.linspace(lower[-1][0], upper[0][0], num=1000)
    y_plot = zfit.run(model.pdf(x_plot, norm_range=obs))
    # plt.text(0.05, 0.9, mu_string, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
    # plt.text(0.75, 0.85, sigma_string, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
    plt.plot(x_plot, y_plot * len(data) / bin_num * obs.area(), color='xkcd:black', label='CrystalBall')
    # plt.hist(data['ratio'], bins=50, range=(min , max))
    width = (max - min) / bin_num
    bins = [min + x * width for x in range(bin_num + 1)]
    bin_centres = [min + width / 2 + x * width for x in range(bin_num)]
    hist_data, binning = np.histogram(data.values, bins=bins)
    axes.errorbar(x=bin_centres, y=hist_data,
                  yerr=np.sqrt(hist_data),
                  fmt='ko', markersize='2', label='E/p')
    plt.title("E/p ratio")
    plt.legend()
    plt.savefig(plot_path + '/Efull_over_p_fit_cb.jpg')
    plt.text(0.05, 0.9, params, ha="left", va="top", family='sans-serif', transform=axes.transAxes, fontsize=9)
    plt.savefig(plot_path + '/ratio_params_cb.jpg')
    plt.clf()

    return None  # TODO


if __name__ == '__main__':
    path = ''
    filename = 'Kee'
    plot_path = 'Plots/' + str(filename) + '_2010_1'
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    # if not os.path.exists(plot_path_full):
    #     os.makedirs(plot_path_full)
    branches = ['nTracks', 'nSPDHits',
                'e_minus_TRUEID', 'e_minus_MC_MOTHER_ID', 'e_minus_MC_GD_MOTHER_ID',
                'e_plus_TRUEID', 'e_plus_MC_MOTHER_ID', 'e_plus_MC_GD_MOTHER_ID',
                'e_plus_BremMultiplicity', 'e_minus_BremMultiplicity',
                'K_Kst_PIDe', 'K_Kst_PIDK', 'e_plus_PIDe', 'e_plus_PIDK',
                'K_Kst_TRUEID', 'K_Kst_MC_MOTHER_ID', 'J_psi_1S_BKGCAT', 'B_plus_BKGCAT',
                'K_Kst_CaloEcalE', 'K_Kst_CaloHcalE', 'K_Kst_CaloSpdE', 'K_Kst_CaloPrsE',
                'e_plus_CaloEcalE', 'e_plus_CaloHcalE', 'e_plus_CaloSpdE', 'e_plus_CaloPrsE',
                'e_minus_CaloEcalE', 'e_minus_CaloHcalE', 'e_minus_CaloSpdE', 'e_minus_CaloPrsE',
                'K_Kst_P', 'K_Kst_PT', 'K_Kst_PE', 'K_Kst_TRACK_P',
                'e_plus_P', 'e_plus_PT', 'e_plus_PE', 'e_plus_TRACK_P',
                'e_minus_P', 'e_minus_TRACK_P',
                'e_plus_PX', 'e_plus_PY', 'e_plus_PZ',
                'e_minus_PT', 'e_minus_PE',
                'e_minus_PX', 'e_minus_PY', 'e_minus_PZ',
                'e_plus_TRUEP_E', 'e_minus_TRUEP_E', 'K_Kst_TRUEP_E',
                'e_plus_TRUEP_X', 'e_minus_TRUEP_X', 'K_Kst_TRUEP_X',
                'e_plus_TRUEP_Y', 'e_minus_TRUEP_Y', 'K_Kst_TRUEP_Y',
                'e_plus_TRUEP_Z', 'e_minus_TRUEP_Z', 'K_Kst_TRUEP_Z',
                'e_minus_PIDe',
                'e_plus_L0Calo_ECAL_xProjection', 'e_minus_L0Calo_ECAL_xProjection', 'K_Kst_L0Calo_HCAL_xProjection',
                'e_plus_L0Calo_ECAL_yProjection', 'e_minus_L0Calo_ECAL_yProjection', 'K_Kst_L0Calo_HCAL_yProjection',
                'J_psi_1S_M',
                'B_plus_M', 'B_plus_DTFM_M',
                'e_plus_RichDLLe', 'K_Kst_RichDLLe', 'e_minus_RichDLLe',
                'e_plus_EcalPIDe', 'e_minus_EcalPIDe', 'K_Kst_EcalPIDe',
                'e_plus_HcalPIDe', 'e_minus_HcalPIDe', 'K_Kst_HcalPIDe',
                'e_plus_BremPIDe', 'e_minus_BremPIDe', 'K_Kst_BremPIDe']

    PIDcut = 3

    Kee_data = read_file(path, branches, filename, maxevts=100000000)

    #GENERAL TRUTH-MATCHING
    #Kee_data.query('B_plus_BKGCAT == 0 or B_plus_BKGCAT == 20 or B_plus_BKGCAT == 40 or B_plus_BKGCAT == 50', inplace = True)
    plt.hist(Kee_data["B_plus_BKGCAT"], bins = [0,10, 20, 30, 40, 50, 60, 63, 66, 70, 80, 100, 110, 120, 130, 140])
    plt.title("B_plus_BKGCAT")
    plt.savefig(plot_path+"/B_plus_BKGCAT.png")
    plt.clf()

    cut_data = common_cuts(Kee_data.copy(), filename, PIDcut=PIDcut)

    Kee_data = divide_brem_cats(Kee_data)
    cut_data = divide_brem_cats(cut_data)
    # Kee_data.query('brem_tag == brem_two', inplace=True)
    print(f'NUMBER OF EVENTS AFTER BREM CUT: {len(Kee_data)}')
    # analyze_something(Kee_data, plot_path)

    Kee_data = create_vars(Kee_data)
    cut_data = create_vars(cut_data)
    # Kee_data.query('e_plus_ETRUE_over_pTRUE > 1.003', inplace=True)
    # cut_data.query('e_plus_ETRUE_over_pTRUE > 1.003', inplace=True)

    for key in hist_dict.keys():

        comp_dict = {'Before cuts': Kee_data[key], f'PIDe > {PIDcut}': cut_data[key]}
        plot_hist(comp_dict, key, hist_dict=hist_dict, path=plot_path, PIDcut=PIDcut)

    # EXPERIMENTAL
    b_zero_pl = cut_data.loc[cut_data['e_plus_BremMultiplicity'] == 0, ['e_plus_Ecal_over_p', 'e_plus_Ecal_over_pTR']]
    b_zero_min = cut_data.loc[cut_data['e_minus_BremMultiplicity'] == 0, ['e_minus_Ecal_over_p', 'e_minus_Ecal_over_pTR']]
    b_zero = pd.DataFrame()
    b_zero['Ecal_over_p'] = pd.concat([b_zero_pl['e_plus_Ecal_over_p'], b_zero_min['e_minus_Ecal_over_p']])
    b_zero['Ecal_over_pTR'] = pd.concat([b_zero_pl['e_plus_Ecal_over_pTR'], b_zero_min['e_minus_Ecal_over_pTR']])

    b_one_pl = cut_data.loc[cut_data['e_plus_BremMultiplicity'] == 1, ['e_plus_Ecal_over_p', 'e_plus_Ecal_over_pTR']]
    b_one_min = cut_data.loc[cut_data['e_minus_BremMultiplicity'] == 1, ['e_minus_Ecal_over_p', 'e_minus_Ecal_over_pTR']]
    b_one = pd.DataFrame()
    b_one['Ecal_over_p'] = pd.concat([b_one_pl['e_plus_Ecal_over_p'], b_one_min['e_minus_Ecal_over_p']])
    b_one['Ecal_over_pTR'] = pd.concat([b_one_pl['e_plus_Ecal_over_pTR'], b_one_min['e_minus_Ecal_over_pTR']])

    b_two_pl = cut_data.loc[cut_data['e_plus_BremMultiplicity'] > 1, ['e_plus_Ecal_over_p', 'e_plus_Ecal_over_pTR']]
    b_two_min = cut_data.loc[cut_data['e_minus_BremMultiplicity'] > 1, ['e_minus_Ecal_over_p', 'e_minus_Ecal_over_pTR']]
    b_two = pd.DataFrame()
    b_two['Ecal_over_p'] = pd.concat([b_two_pl['e_plus_Ecal_over_p'], b_two_min['e_minus_Ecal_over_p']])
    b_two['Ecal_over_pTR'] = pd.concat([b_two_pl['e_plus_Ecal_over_pTR'], b_two_min['e_minus_Ecal_over_pTR']])

    plot_EoP_bremcat(b_zero['Ecal_over_p'], 'brem_zero', mode='Full', path=plot_path, PIDcut=PIDcut)

    plot_EoP_bremcat(b_one['Ecal_over_pTR'], 'brem_one', mode='Track', path=plot_path, PIDcut=PIDcut)
    plot_EoP_bremcat(b_one['Ecal_over_p'], 'brem_one', mode='Full', path=plot_path, PIDcut=PIDcut)
    plot_EoP_bremcat(b_two['Ecal_over_pTR'], 'brem_two', mode='Track', path=plot_path, PIDcut=PIDcut)
    plot_EoP_bremcat(b_two['Ecal_over_p'], 'brem_two', mode='Full', path=plot_path, PIDcut=PIDcut)

    #    if 'brem' not in key:
    #        comp_dict = {'Before cuts': Kee_data[key], f'PIDe > {PIDcut}': cut_data[key]}
    #        plot_hist(comp_dict, key, hist_dict=hist_dict, path=plot_path, PIDcut=PIDcut)
            
    # fit_e_over_p(cut_data['e_plus_Efull_over_p'])

    # NEW STUFF
    # CREATING VARIABLES

    # kaon_cut = 'K_Kst_PIDe > 3 and abs(K_Kst_TRUEID) == 321'
    # electron_cut = 'e_plus_PIDe < 0 and e_plus_PIDK > 3'
    # Kee_data.query(f'({kaon_cut}) and ({electron_cut})', inplace=True)
    # print(f'NUMBER OF EVENTS AFTER K-e PID CUTS: {len(Kee_data.index)}')

    # 2 electrons from JPsi (e trueid, e mc mother id, don't forget abs
    # change one electrons energy so that it has a mass hypothesis of a proton
    # recalculate Jpsi M (sqrt(q2))
    # check at what e momentum it peaks at jpsi

    # log scale for E/p plots (without density)
    # PID >2, 3, 4 ...
    # Проверить насчет TRUE_E
