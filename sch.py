from scholarly import scholarly
import pickle
from pprint import pprint
import sys

# if any of these abbreviations are seen, use them
CONF_ABBREVIATIONS = ('ICRA', 'CVPR', 'ECCV', 'ICCV', 'ISCA', 'DAC', 'ICCAD')
BIBPATH = 'references.bib'

def normalize_journal(pub):
    bib = pub['bib']
    if 'journal' in bib:
        entry = bib['journal']
    elif 'conference' in bib:
        entry = bib['conference']
    elif ('note' in bib and 'Patent' in bib['note']) or 'patent' in bib['url']:
        bib['journal'] = 'Patent'
        return
    else:
        bib['journal'] = ' '
        return
  
    if entry.lower().startswith('arxiv preprint'):
        entry = entry[len('arxiiv preprint'):]

    if entry.lower().startswith('proceedings of the'):
        entry = entry[len('proceedings of the'):]

    contains = [abbreviation in entry for abbreviation in CONF_ABBREVIATIONS]
    if any(contains):
        entry = CONF_ABBREVIATIONS[contains.index(True)]

    bib['journal'] = entry


def special_cases(pub):
    """This is a hack for stuff I can't get scholarly to do. It's all
    hard-coded and won't work for anyone else."""
    if (pub['bib']['title'] == "PyPlover: A System for GPU-enabled Serverless Instances" or
        pub['bib']['title'] == "Enabling Efficient and Transparent Remote Memory Access in Disaggregated Datacenters"):
        pub['bib']['journal'] = "Master's Thesis"


def sort_by_year(pub):
    bib = pub['bib']
    if 'pub_year' in bib:
        return int(bib['pub_year'])
    elif 'year' in pub:
        return int(bib['year'])
    else:
        # If there's no year, it probably isn't very important, put it at the end.
        print("WARNING: No publication date is available, this item may not sort properly.")
        print("\t" + bib['title'])
        return 0


def get_publications_sch(author_name):
    # This block is useful for debugging and development
    # reset=False
    # if reset:
    #     search_query = scholarly.search_author('Nathan Pemberton')
    #     author = scholarly.fill(next(search_query))
    #     with open('author.pickle', 'wb') as f:
    #         pickle.dump(author, f)
    #
    #     pubs = [ scholarly.fill(p) for p in author['publications'] ]
    #     with open('pubs.pickle', 'wb') as f:
    #         pickle.dump(pubs, f)
    # else:
    #     with open('author.pickle', 'rb') as f:
    #         author = pickle.load(f)
    #     with open('pubs.pickle', 'rb') as f:
    #         pubs = pickle.load(f)
    search_query = scholarly.search_author('Nathan Pemberton')
    author = scholarly.fill(next(search_query))
    pubs = [ scholarly.fill(p) for p in author['publications'] ]

    for pub in pubs:
        bib = pub['bib']
        bib['ENTRYTYPE'] = 'article'
        bib['ID'] = pub['author_pub_id']
        bib['url'] = pub['eprint_url']

        if 'pub_year' in bib:
            bib['year'] = bib['pub_year']

        special_cases(pub)
        normalize_journal(pub)

    pubs.sort(key=sort_by_year, reverse=True)
    with open(BIBPATH, 'w') as f:
        f.write('@preamble{"{"name" : "' + author_name + '"}"}\n')
        for p in pubs:
            f.write(scholarly.bibtex(p))
            f.write('\n')

if len(sys.argv) != 2:
    print("Usage:")
    print('\tpython sch.py "AUTHOR NAME"')
    print("(don't forget to quote your name)")

get_publications_sch(sys.argv[1])
