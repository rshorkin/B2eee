hist_dict = {
    'e_plus_Ecal_over_pTR':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Track Momentum'
        },
    'e_plus_ETRUE_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.5,
            'xmax': 2.0,
            'xlabel': r'True Energy / Track Momentum'
        },
    'e_plus_ETRUE_over_p':
        {
            'n_bins': 40,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.5,
            'xmax': 1.5,
            'xlabel': r'True Energy / Full Momentum'
        },
    'e_plus_ETRUE_over_pTRUE':
        {

            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.995,

            'xmax': 1.025,
            'xlabel': r'True Energy / True Momentum'
        },
    'e_plus_Ecal_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'e_minus_Ecal_over_pTR':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Track Momentum'
        },
    'e_minus_Ecal_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'e_minus_Efull_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'e_plus_Efull_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'K_Ecal_over_pTR':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'K_Ecal_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'K_Efull_over_p':
        {
            'n_bins': 60,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': -1.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'K_Kst_ETRUE_over_pTR':
        {
            'n_bins': 40,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.9,
            'xmax': 1.1,
            'xlabel': r'True Energy / Track Momentum'
        },
    'K_Kst_ETRUE_over_p':
        {
            'n_bins': 40,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.9,
            'xmax': 1.1,
            'xlabel': r'True Energy / Full Momentum'
        },
    'K_Kst_ETRUE_over_pTRUE':
        {
            'n_bins': 40,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 1.,
            'xmax': 1.025,
            'xlabel': r'True Energy / True Momentum'
        },
    'J_psi_1S_M':
        {
            'n_bins': 50.,
            'plt_title': r'B$^+$ mass',
            'xmin': 3000.,
            'xmax': 3200.,
            'xlabel': r'M(B$^+$), MeV'
        },
    'B_plus_M':
        {
            'n_bins': 50.,
            'plt_title': r'B$^+$ mass',
            'xmin': 4400.,
            'xmax': 6000.,
            'xlabel': r'M(B$^+$), MeV'
        },
    'B_plus_DTFM_M':
        {
            'n_bins': 80.,
            'plt_title': r'B$^+$ mass',
            'xmin': 5000.,
            'xmax': 5800.,
            'xlabel': r'M(B$^+$), MeV'
        },
    'K_Kst_P':
        {
            'n_bins': 50.,
            'plt_title': r'Momentum for K$^+$',
            'xmin': 0.,
            'xmax': 200000.,
            'xlabel': r'Momentum [MeV]'
        },
    'e_plus_P':
        {
            'n_bins': 50.,
            'plt_title': r'Track momentum for e$^+$',
            'xmin': 0.,
            'xmax': 200000.,
            'xlabel': r'Momentum [MeV]'
        },
    'e_plus_L0Calo_ECAL_yProjection':
        {
            'n_bins': 80.,
            'plt_title': r'ECAL y coordinate for e$^+$',
            'xmin': -4000.,
            'xmax': 4000.,
            'xlabel': r'ECAL y projection [mm]'
        },
    'e_plus_L0Calo_ECAL_xProjection':
        {
            'n_bins': 80.,
            'plt_title': r'ECAL x coordinate for e$^+$',
            'xmin': -4000.,
            'xmax': 4000.,
            'xlabel': r'ECAL x projection [mm]'
        },
    'K_Kst_L0Calo_HCAL_yProjection':
        {
            'n_bins': 80.,
            'plt_title': r'HCAL y coordinate for K$^+$',
            'xmin': -4000.,
            'xmax': 4000.,
            'xlabel': r'HCAL y projection [mm]'
        },
    'K_Kst_L0Calo_HCAL_xProjection':
        {
            'n_bins': 80.,
            'plt_title': r'HCAL x coordinate for K$^+$',
            'xmin': -4000.,
            'xmax': 4000.,
            'xlabel': r'HCAL x projection [mm]'
        },
    'ee_separation':
        {
            'n_bins': 80.,
            'plt_title': r'Electron separation in ECAL',
            'xmin': 0.,
            'xmax': 8000.,
            'xlabel': r'Dielectron ECAL separation [mm]'
        },
    'K_eplus_sep':
        {
            'n_bins': 80.,
            'plt_title': r'Separation of K$^+$ and e$^+$ (ECAL and HCAL proj)',
            'xmin': 0.,
            'xmax': 8000.,
            'xlabel': r'K-e plus separation [mm]'
        },
    'K_emin_sep':
        {
            'n_bins': 80.,
            'plt_title': r'Separation of K$^+$ and e$^-$ (ECAL and HCAL proj)',
            'xmin': 0.,
            'xmax': 8000.,
            'xlabel': r'K-e minus separation [mm]'
        },
    'e_plus_RichDLLe':
        {
            'n_bins': 80.,
            'plt_title': r'e$^+$ RICH DLLe',
            'xmin': -20.,
            'xmax': 140.,
            'xlabel': r'e_plus_RichDLLe'
        },
    'e_minus_RichDLLe':
        {
            'n_bins': 80.,
            'plt_title': r'e$^+$ RICH DLLe',
            'xmin': -20.,
            'xmax': 140.,
            'xlabel': r'e_plus_RichDLLe'
        },
    'K_Kst_RichDLLe':
        {
            'n_bins': 80.,
            'plt_title': r'K$^+$ RICH DLLe',
            'xmin': -20.,
            'xmax': 20.,
            'xlabel': r'K_Kst_RichDLLe'
        },
    'K_Kst_RichDLLk':
        {
            'n_bins': 80.,
            'plt_title': r'K$^+$ RICH DLLk',
            'xmin': -20.,
            'xmax': 140.,
            'xlabel': r'K_Kst_RichDLLk'
        },
    ##################################
    'e_plus_EcalPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'e$^+$ Ecal PIDe',
            'xmin': -4.,
            'xmax': 8.,
            'xlabel': r'e_plus_EcalPIDe'
        },
    'e_minus_EcalPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'e$^+$ Ecal PIDe',
            'xmin': -4.,
            'xmax': 8.,
            'xlabel': r'e_plus_EcalPIDe'
        },
    'K_Kst_EcalPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'K$^+$ Ecal PIDe',
            'xmin': -4.,
            'xmax': 8.,
            'xlabel': r'K_Kst_EcalPIDe'
        },
    'e_plus_HcalPIDe':
        {
            'n_bins': 60.,
            'plt_title': r'e$^+$ Hcal PIDe',
            'xmin': -3.,
            'xmax': 3.,
            'xlabel': r'e_plus_HcalPIDe'
        },
    'e_minus_HcalPIDe':
        {
            'n_bins': 60.,
            'plt_title': r'e$^+$ Hcal PIDe',
            'xmin': -3.,
            'xmax': 3.,
            'xlabel': r'e_plus_HcalPIDe'
        },
    'K_Kst_HcalPIDe':
        {
            'n_bins': 60.,
            'plt_title': r'K$^+$ Hcal PIDe',
            'xmin': -3.,
            'xmax': 3.,
            'xlabel': r'K_Kst_HcalPID'
        },
    'e_plus_BremPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'e$^+$ Brem PIDe',
            'xmin': -2.,
            'xmax': 6.,
            'xlabel': r'e_plus_BremPIDe'
        },
    'e_minus_BremPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'e$^+$ Brem PIDe',
            'xmin': -2.,
            'xmax': 6.,
            'xlabel': r'e_plus_BremPIDe'
        },
    'K_Kst_BremPIDe':
        {
            'n_bins': 40.,
            'plt_title': r'K$^+$ Brem PIDe',
            'xmin': -2.,
            'xmax': 6.,
            'xlabel': r'K_Kst_BremPIDe'
        },
    'e_plus_L0Calo_ECAL_region':
        {
            'n_bins': 5.,
            'plt_title': r'e$^+$ ECAL region',
            'xmin': -2.,
            'xmax': 3.,
            'xlabel': r'e_plus_L0Calo_ECAL_region'
        },
    'e_minus_L0Calo_ECAL_region':
        {
            'n_bins': 5.,
            'plt_title': r'e$^-$ ECAL region',
            'xmin': -2.,
            'xmax': 3.,
            'xlabel': r'e_minus_L0Calo_ECAL_region'
        },
    'K_Kst_L0Calo_HCAL_region':
        {
            'n_bins': 5.,
            'plt_title': r'K$^+$ HCAL region',
            'xmin': -2.,
            'xmax': 3.,
            'xlabel': r'K_Kst_L0Calo_HCAL_region'
        },
    'K_Kst_UsedRich1Gas':
        {
            'n_bins': 2.,
            'plt_title': r'K$^+$ Rich 1 Gas',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'K_Kst_UsedRich1Gas'
        },
    'K_Kst_UsedRich2Gas':
        {
            'n_bins': 2.,
            'plt_title': r'K$^+$ Rich2 gas',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'K_Kst_UsedRich2Gas'
        },
    'K_Kst_ProbNNe':
        {
            'n_bins': 40.,
            'plt_title': r'K$^+$ ProbNNe',
            'xmin': 0.,
            'xmax': 0.4,
            'xlabel': r'K_Kst_ProbNNe'
        },
    'K_Kst_ProbNNk':
        {
            'n_bins': 40.,
            'plt_title': r'K$^+$ ProbNNk',
            'xmin': 0.,
            'xmax': 1.,
            'xlabel': r'K_Kst_ProbNNk'
        },


}

hist2d_dict = {
    # SAMPLE ENTRY:
    # 'smth':
    #     {
    #         'plt_title': r'smth',
    #
    #         'x_bins': 60,
    #         'xmin': -1.,
    #         'xmax': 2.,
    #         'xvar': '1st_variable',
    #
    #         'y_bins': 60,
    #         'ymin': -1.,
    #         'ymax': 2.,
    #         'yvar': '2nd_variable',
    #
    #         'cmin': -1.,
    #         'cmax': 2.,
    #
    #         'xlabel': r'ECAL Energy / Track Momentum',
    #         'ylabel': r'ECAL Energy / Track Momentum',
    #         'clabel': r'Events'
    #     },
    'PIDe_vs_EoP_e':
        {
            'plt_title': r'$e^+$ PIDe vs EoP ratio',

            'x_bins': 40,
            'xmin': -6.,
            'xmax': 10.,
            'xvar': 'e_plus_PIDe',

            'y_bins': 60,
            'ymin': -1.,
            'ymax': 2.,
            'yvar': 'e_plus_Ecal_over_pTR',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'e_plus_EcalPIDe',
            'ylabel': r'ECAL Energy / Track Momentum',
            'clabel': r'Events'
        },

    'PIDe_vs_EoP_K':
        {
            'plt_title': r'$K^+$ PIDe vs EoP ratio',

            'x_bins': 40,
            'xmin': -10.,
            'xmax': 10.,
            'xvar': 'K_Kst_PIDe',

            'y_bins': 60,
            'ymin': -1.,
            'ymax': 2.,
            'yvar': 'K_Ecal_over_pTR',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'$K^+$ PIDe',
            'ylabel': r'ECAL Energy / Track Momentum',
            'clabel': r'Events'
        },

    'PIDe_vs_y_projection':
        {
            'plt_title': r'$K^+$ PIDe vs HCAL y projection',

            'x_bins': 40,
            'xmin': -10.,
            'xmax': 10.,
            'xvar': 'K_Kst_PIDe',

            'y_bins': 80.,
            'ymin': -4000.,
            'ymax': 4000.,
            'yvar': 'K_Kst_L0Calo_HCAL_yProjection',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'$K^+$ PIDe',
            'ylabel': r'HCAL y projection',
            'clabel': r'Events'
        },

    'RichDLLe_vs_y_projection':
        {
            'plt_title': r'$K^+$ RichDLLe vs HCAL y projection',

            'x_bins': 80.,
            'xmin': -20.,
            'xmax': 20.,
            'xvar': 'K_Kst_RichDLLe',

            'y_bins': 80.,
            'ymin': -4000.,
            'ymax': 4000.,
            'yvar': 'K_Kst_L0Calo_HCAL_yProjection',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'RichDLLe',
            'ylabel': r'HCAL y projection',
            'clabel': r'Events'
        },
    'RichDLLk_vs_y_projection':
        {
            'plt_title': r'$K^+$ RichDLLk vs HCAL y projection',

            'x_bins': 80.,
            'xmin': -20.,
            'xmax': 140.,
            'xvar': 'K_Kst_RichDLLk',

            'y_bins': 80.,
            'ymin': -4000.,
            'ymax': 4000.,
            'yvar': 'K_Kst_L0Calo_HCAL_yProjection',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'RichDLLk',
            'ylabel': r'HCAL y projection',
            'clabel': r'Events'
        },

    'PIDe_vs_ProbNNe':
        {
            'plt_title': r'$K^+$ PIDe vs ProbNNe',

            'x_bins': 40,
            'xmin': -10.,
            'xmax': 10.,
            'xvar': 'K_Kst_PIDe',

            'y_bins': 40,
            'ymin': 0.,
            'ymax': 1.,
            'yvar': 'K_Kst_ProbNNe',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'$K^+$ PIDe',
            'ylabel': r'$K^+$ ProbNNe',
            'clabel': r'Events'
        },
    'x_projection_vs_y_projection':
        {
            'plt_title': r'$K^+$ HCAL x vs y projection',

            'x_bins': 80.,
            'xmin': -4000.,
            'xmax': 4000.,
            'xvar': 'K_Kst_L0Calo_HCAL_xProjection',

            'y_bins': 80.,
            'ymin': -4000.,
            'ymax': 4000.,
            'yvar': 'K_Kst_L0Calo_HCAL_yProjection',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'HCAL x projection',
            'ylabel': r'HCAL y projection',
            'clabel': r'Events'
        },
    'RichDLLe_vs_PIDe':
        {
            'plt_title': r'$K^+$ RichDLLe vs PIDe',

            'x_bins': 80.,
            'xmin': -20.,
            'xmax': 20.,
            'xvar': 'K_Kst_RichDLLe',

            'y_bins': 40,
            'ymin': -14.,
            'ymax': 10.,
            'yvar': 'K_Kst_PIDe',

            'cmin': 0.,
            'cmax': 100.,
            'cscale': 'log',

            'xlabel': r'RichDLLe',
            'ylabel': r'PIDe',
            'clabel': r'Events'
        },



}

branches = ['nTracks', 'nSPDHits',
            'e_minus_TRUEID', 'e_minus_MC_MOTHER_ID', 'e_minus_MC_GD_MOTHER_ID',
            'e_plus_TRUEID', 'e_plus_MC_MOTHER_ID', 'e_plus_MC_GD_MOTHER_ID',
            'e_plus_BremMultiplicity', 'e_minus_BremMultiplicity',
            'K_Kst_PIDe', 'K_Kst_PIDK', 'e_plus_PIDe', 'e_plus_PIDK', 'e_minus_PIDe', 'e_minus_PIDK',
            'K_Kst_ProbNNe', 'K_Kst_ProbNNk', 'e_plus_ProbNNe', 'e_plus_ProbNNk', 'e_minus_ProbNNe', 'e_minus_ProbNNk',
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
            'e_plus_L0Calo_ECAL_xProjection', 'e_minus_L0Calo_ECAL_xProjection', 'K_Kst_L0Calo_HCAL_xProjection',
            'e_plus_L0Calo_ECAL_yProjection', 'e_minus_L0Calo_ECAL_yProjection', 'K_Kst_L0Calo_HCAL_yProjection',
            'J_psi_1S_M',
            'B_plus_M', 'B_plus_DTFM_M',
            'e_plus_RichDLLe', 'K_Kst_RichDLLe', 'e_minus_RichDLLe',
            'e_plus_RichDLLk', 'K_Kst_RichDLLk', 'e_minus_RichDLLk',
            'e_plus_UsedRich1Gas', 'K_Kst_UsedRich1Gas', 'e_minus_UsedRich1Gas',
            'e_plus_UsedRich2Gas', 'K_Kst_UsedRich2Gas', 'e_minus_UsedRich2Gas',
            'e_plus_EcalPIDe', 'e_minus_EcalPIDe', 'K_Kst_EcalPIDe',
            'e_plus_HcalPIDe', 'e_minus_HcalPIDe', 'K_Kst_HcalPIDe',
            'e_plus_BremPIDe', 'e_minus_BremPIDe', 'K_Kst_BremPIDe',
            'e_plus_L0Calo_ECAL_region', 'e_minus_L0Calo_ECAL_region', 'K_Kst_L0Calo_HCAL_region']