hist_dict = {
    'e_plus_Ecal_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Track Momentum'
        },
    'e_plus_ETRUE_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Track Momentum'
        },
    'e_plus_ETRUE_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Full Momentum'
        },
    'e_plus_ETRUE_over_pTRUE':
        {
            'n_bins': 40,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 1.,
            'xmax': 1.025,
            'xlabel': r'True Energy / True Momentum'
        },
    'e_plus_Ecal_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'e_minus_Ecal_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Track Momentum'
        },
    'e_minus_Ecal_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'e_minus_Efull_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^-$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'e_plus_Efull_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for e$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'K_Ecal_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Track Momentum'
        },
    'K_Ecal_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'ECAL Energy / Full Momentum'
        },
    'K_Efull_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'Total Energy / Full Momentum'
        },
    'K_Kst_ETRUE_over_pTR':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Track Momentum'
        },
    'K_Kst_ETRUE_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
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
    'B_plus_M':
        {
            'n_bins': 60.,
            'plt_title': r'B$^+$ mass',
            'xmin': 4600.,
            'xmax': 5800.,
            'xlabel': r'M(B$^+$), MeV'
        },
    'K_Kst_P':
        {
            'n_bins': 60.,
            'plt_title': r'Momentum for K$^+$',
            'xmin': 0.,
            'xmax': 300000.,
            'xlabel': r'Momentum [MeV]'
        },
    'e_plus_P':
        {
            'n_bins': 60.,
            'plt_title': r'Track momentum for e$^+$',
            'xmin': 0.,
            'xmax': 30000.,
            'xlabel': r'Momentum [MeV]'
        },
    'e_plus_L0Calo_ECAL_yProjection':
        {
            'n_bins': 60.,
            'plt_title': r'ECAL y coordinate for e$^+$',
            'xmin': -3000.,
            'xmax': 3000.,
            'xlabel': r'ECAL y projection [mm]'
        },
    'e_plus_L0Calo_ECAL_xProjection':
        {
            'n_bins': 60.,
            'plt_title': r'ECAL x coordinate for e$^+$',
            'xmin': -3000.,
            'xmax': 3000.,
            'xlabel': r'ECAL x projection [mm]'
        },
    'K_Kst_L0Calo_HCAL_yProjection':
        {
            'n_bins': 60.,
            'plt_title': r'ECAL y coordinate for K$^+$',
            'xmin': -3000.,
            'xmax': 3000.,
            'xlabel': r'ECAL y projection [mm]'
        },
    'K_Kst_L0Calo_HCAL_xProjection':
        {
            'n_bins': 60.,
            'plt_title': r'ECAL x coordinate for K$^+$',
            'xmin': -3000.,
            'xmax': 3000.,
            'xlabel': r'ECAL x projection [mm]'
        },
    'ee_separation':
        {
            'n_bins': 60.,
            'plt_title': r'Electron separation in ECAL',
            'xmin': 0.,
            'xmax': 6000.,
            'xlabel': r'Dielectron ECAL separation [mm]'
        },
    'K_eplus_sep':
        {
            'n_bins': 60.,
            'plt_title': r'Separation of K$^+$ and e$^+$',
            'xmin': 0.,
            'xmax': 6000.,
            'xlabel': r'K-e plus separation [mm]'
        },
    'K_emin_sep':
        {
            'n_bins': 60.,
            'plt_title': r'Separation of K$^+$ and e$^-$',
            'xmin': 0.,
            'xmax': 6000.,
            'xlabel': r'K-e minus separation [mm]'
        },
    'e_plus_RichDLLe':
        {
            'n_bins': 40.,
            'plt_title': r'e$^+$ RICH DLLe',
            'xmin': -200.,
            'xmax': 200.,
            'xlabel': r'e_plus_RichDLLe'
        },
    'K_Kst_RichDLLe':
        {
            'n_bins': 40.,
            'plt_title': r'K$^+$ RICH DLLe',
            'xmin': -200.,
            'xmax': 200.,
            'xlabel': r'K_Kst_RichDLLe'
        },
    'e_brem0_ETrue_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Full Momentum'
        },
    'e_brem1_ETrue_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Full Momentum'
        },
    'e_brem2_ETrue_over_p':
        {
            'n_bins': 50,
            'plt_title': r'E/p ratio for K$^+$',
            'xmin': 0.,
            'xmax': 2.,
            'xlabel': r'True Energy / Full Momentum'
        },
}