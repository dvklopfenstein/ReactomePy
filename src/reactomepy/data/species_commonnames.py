"""Common name for the species in Reactome"""

__copyright__ = "Copyright (C) 2018-2020, DV Klopfenstein. All rights reserved."
__author__ = "DV Klopfenstein"

# pylint: disable=line-too-long
TAXID2NAMES = {
    446: ['L.pneumophila'],
    562: ['Escherichia coli (strain K12)'],
    4896: ['S.pombe', 'S. pombe', 'fission yeast', 'Sp'],
    4932: ['S.cerevisiae', 'S. cerevisiae', 'Sc', "baker's yeast", "brewer's yeast", 'Saccharomyces cerevisiae (strain RM11-1a)', 'Saccharomyces cerevisiae (strain YJM789)'],
    5833: ['malaria parasite P. falciparum'],
    6239: ['C.elegans', 'C. elegans', 'Ce'],
    7227: ['D. melanogaster', 'Dm', 'fruit fly'],
    7955: ['D.rerio', 'D. rerio', 'Dr', 'Brachydanio rerio', 'zebrafish', 'zebra fish'],
    8355: ['X. laevis', 'Xl', 'African clawed frog'],
    8364: ['Western clawed frog', 'Silurana tropicalis'],
    9031: ['chicken'],
    9534: ['African green monkey'],
    9606: ['H. sapiens', 'Hs', 'human', 'man'],
    9823: ['pig', 'swine'],
    9913: ['B. taurus', 'Bt', 'bovine', 'cattle', 'cow', 'domestic cattle', 'domestic cow'],
    9940: ['sheep', 'domestic sheep'],
    9986: ['rabbit'],
    10029: ['Chinese hamster'],
    10090: ['M. musculus', 'Mm', 'house mouse'],
    10116: ['R. norvegicus', 'Rn', 'brown rat', 'Norway rat'],
    10141: ['domestic guinea pig'],
    10243: ['CPXV'],
    10245: ['vaccinia virus VV'],
    10279: ['MOCV'],
    10280: ['Molluscum contagiosum virus type 1', 'Molluscum contagiosum virus subtype I MCV I', 'Molluscum contagiosum virus 1', 'McVI'],
    10310: ['Herpes simplex virus type 2 (HSV-2)', 'HSV2'],
    10359: ['human herpesvirus type 5', 'HHV-5', 'Human cytomegalovirus HCMV', 'human cytomegalovirus CMV'],
    10376: ['EBV', 'Epstein-Barr virus'],
    10407: ['HBV'],
    11103: ['HCV'],
    11234: ['rubeola virus', 'rougeole virus'],
    11676: ['Human immunodeficiency virus type 1', 'HIV1', 'HIV-1', 'Human immunodeficiency virus type 1 (isolate 90CF056 group M subtype H)', 'Human immunodeficiency virus type 1 (isolate 92BR025 group M subtype C)', 'Human immunodeficiency virus type 1 (isolate 92NG083 group M subtype G)', 'Human immunodeficiency virus type 1 (isolate 93BR020 group M subtype F1)', 'Human immunodeficiency virus type 1 (isolate 96CM-MP535 group M subtype K)', 'Human immunodeficiency virus type 1 (isolate 97ZR-EQTB11 group M subtype K)', 'Human immunodeficiency virus type 1 (isolate ANT70 group O)', 'Human immunodeficiency virus type 1 (isolate ARV2/SF2 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate BH10 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate BH5 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate BH8 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate BRU/LAI group M subtype B)', 'Human immunodeficiency virus type 1 (isolate BRVA group M subtype B)', 'Human immunodeficiency virus type 1 (isolate CDC-451 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate ELI group M subtype D)', 'Human immunodeficiency virus type 1 (isolate ETH2220 group M subtype C)', 'Human immunodeficiency virus type 1 (isolate HXB2 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate HXB3 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate JH32 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate JRCSF group M subtype B)', 'Human immunodeficiency virus type 1 (isolate KB-1/ETR group M subtype B)', 'Human immunodeficiency virus type 1 (isolate Lai group M subtype B)', 'Human immunodeficiency virus type 1 (isolate LW123 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate MAL group M subtype A)', 'Human immunodeficiency virus type 1 (isolate MFA group M subtype B)', 'Human immunodeficiency virus type 1 (isolate MN group M subtype B)', 'Human immunodeficiency virus type 1 (isolate MP255 group M subtype F2)', 'Human immunodeficiency virus type 1 (isolate MP257 group M subtype F2)', 'Human immunodeficiency virus type 1 (isolate MVP5180 group O)', 'Human immunodeficiency virus type 1 (isolate N1T-A group M subtype B)', 'Human immunodeficiency virus type 1 (isolate NDK group M subtype D)', 'Human immunodeficiency virus type 1 (isolate NY5 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate OYI group M subtype B)', 'Human immunodeficiency virus type 1 (isolate PCV12 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate RF/HAT3 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate SC group M subtype B)', 'Human immunodeficiency virus type 1 (isolate SE6165 group M subtype G)', 'Human immunodeficiency virus type 1 (isolate SE9173 group M subtype J)', 'Human immunodeficiency virus type 1 (isolate SE9280 group M subtype J)', 'Human immunodeficiency virus type 1 (isolate SF162 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate SF33 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate U455 group M subtype A)', 'Human immunodeficiency virus type 1 (isolate VI850 group M subtype F1)', 'Human immunodeficiency virus type 1 (isolate VI991 group M subtype H)', 'Human immunodeficiency virus type 1 (isolate WMJ1 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate WMJ22 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate YBF106 group N)', 'Human immunodeficiency virus type 1 (isolate YBF30 group N)', 'Human immunodeficiency virus type 1 (isolate YU-2 group M subtype B)', 'Human immunodeficiency virus type 1 (isolate Z2/CDC-Z34 group M subtype D)', 'Human immunodeficiency virus type 1 (isolate Z3 group M subtype U)', 'Human immunodeficiency virus type 1 (isolate Z321 group M subtype A)', 'Human immunodeficiency virus type 1 (isolate Z6 group M subtype D)', 'Human immunodeficiency virus type 1 (isolate Z84 group M subtype D)', 'Human immunodeficiency virus type 1 (strain 89.6 group M subtype B)'],
    28875: ['Rotavirus group A'],
    37296: ["Kaposi's sarcoma-associated herpesvirus", 'Human herpesvirus 8 type P', "Kaposi's sarcoma-associated herpesvirus - Human herpesvirus 8", "Kaposi's sarcoma-associated herpes-like virus", 'KSHV', 'HHV8'],
    90371: ['Salmonella enterica subsp. enterica'],
    333760: ['human papillomavirus type 16 HPV16', 'human papillomavirus type 16 HPV 16', 'HPV16'],
}

# Copyright (C) 2018-2020, DV Klopfenstein. All rights reserved.
