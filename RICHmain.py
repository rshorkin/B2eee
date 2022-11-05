from Analysis import *


def all_combs(a, b):
    c = []
    for item_a in a:
        for item_b in b:
            if item_a == item_b:
                continue
            if [item_a, item_b] in c or [item_b, item_a] in c:
                continue
            c.append([item_a, item_b])
    return c


if __name__ == '__main__':
    path = ''
    filename = 'KJPsiee'
    plot_path = 'Plots/' + str(filename) + '_0411_RICHtest'
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

    base_combs = all_combs(['1', '2'], ['True', 'False'])
    base_cuts = [f'K_Kst_UsedRich{item[0]}Gas == {item[1]}' for item in base_combs]
    cuts = all_combs(base_cuts, base_cuts)
    for item in cuts:
        if ('1' in item[0] and '1' in item[1]) or ('2' in item[0] and '2' in item[1]):
            cuts.remove(item)

    cuts_strs = list(range(len(cuts)))
    for index in range(len(cuts)):
        # cuts[index] = cuts[index][0] + ' and ' + cuts[index][1]
        if 'True' in cuts[index][0]:
            rich1_str = r'K$^+$ used RICH1'
        elif 'False' in cuts[index][0]:
            rich1_str = r'K$^+$ did not use RICH1'

        if 'True' in cuts[index][1]:
            rich2_str = r'used RICH2'
        elif 'False' in cuts[index][1]:
            rich2_str = r'did not use RICH2'

        cuts_strs[index] = rich1_str + ' and ' + rich2_str
        cuts[index] = cuts[index][0] + ' and ' + cuts[index][1]
    different_rich_hists = {}
    different_rich_hists2d = {}
    for cut in cuts:
        print(cut)
        histograms, histograms2d = read_file(path, branches, filename, maxevts=max_events, PIDcut=PIDcut, skip1d=False,
                                             cut=cut)
        if histograms is not None:
            if histograms['full'] is not None:
                different_rich_hists[cut] = histograms['full']
                different_rich_hists2d[cut] = histograms2d['full']

    if different_rich_hists is not None:
        for key in hist_dict.keys():
            comp_dict = {cut_str: different_rich_hists[cut][key] for cut, cut_str in zip(list(different_rich_hists.keys()), cuts_strs)}
            plot_hist(comp_dict, key, hist_dict=hist_dict, path=plot_path, PIDcut=None, normalize=True)


