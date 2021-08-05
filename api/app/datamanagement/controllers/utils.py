import pandas as pd
import json
from operator import itemgetter

# from scipy.sparse import csr_matrix
# from sklearn.feature_extraction.text import TfidfVectorizer


import re

from ..pii.PII_data_processor import (initialize_lists,
                                      stem_restricted, word_match_stemming,
                                      fuzzy_partial_stem_match)

# from datamanagement import celery

def regex_replace(s, find, replace):
    """A non-optimal implementation of a regex filter"""
    return re.sub(find, replace, s)

# Custom filter method
# def match_col_names_with_business_terms():

#   import sparse_dot_topn.sparse_dot_topn as ct


  # def ngrams(string, n=3):
  #     string = re.sub(r'[,-./]|\sBD',r'', string)
  #     ngrams = zip(*[string[i:] for i in range(n)])
  #     return [''.join(ngram) for ngram in ngrams]


  # def awesome_cossim_top(A, B, ntop, lower_bound=0):
  #     # force A and B as a CSR matrix.
  #     # If they have already been CSR, there is no overhead
  #     A = A.tocsr()
  #     B = B.tocsr()
  #     M, _ = A.shape
  #     _, N = B.shape

  #     idx_dtype = np.int32

  #     nnz_max = M*ntop

  #     indptr = np.zeros(M+1, dtype=idx_dtype)
  #     indices = np.zeros(nnz_max, dtype=idx_dtype)
  #     data = np.zeros(nnz_max, dtype=A.dtype)

  #     ct.sparse_dot_topn(
  #         M, N, np.asarray(A.indptr, dtype=idx_dtype),
  #         np.asarray(A.indices, dtype=idx_dtype),
  #         A.data,
  #         np.asarray(B.indptr, dtype=idx_dtype),
  #         np.asarray(B.indices, dtype=idx_dtype),
  #         B.data,
  #         ntop,
  #         lower_bound,
  #         indptr, indices, data)

  #     return csr_matrix((data,indices,indptr),shape=(M,N))


  # def get_matches_df(sparse_matrix, name_vector, top=100):
  #     non_zeros = sparse_matrix.nonzero()

  #     sparserows = non_zeros[0]
  #     sparsecols = non_zeros[1]

  #     if top:
  #         nr_matches = top
  #     else:
  #         nr_matches = sparsecols.size

  #     left_side = np.empty([nr_matches], dtype=object)
  #     right_side = np.empty([nr_matches], dtype=object)
  #     similairity = np.zeros(nr_matches)

  #     for index in range(0, nr_matches):
  #         left_side[index] = name_vector[sparserows[index]]
  #         right_side[index] = name_vector[sparsecols[index]]
  #         similairity[index] = sparse_matrix.data[index]

  #     return pd.DataFrame({'left_side': left_side,
  #                         'right_side': right_side,
  #                         'similairity': similairity}
  #                         )

  # def matches(col_names):

  #     # company_names = names['Company Name']
  #     vectorizer = TfidfVectorizer(min_df=1, analyzer=ngrams)
  #     # print(vectorizer)
  #     tf_idf_matrix = vectorizer.fit_transform(col_names)

  #     matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), 10, 0.5)
  #     matches_df = get_matches_df(matches, col_names, top= len(col_names))
  #     matches_df = matches_df[matches_df['similairity'] < 0.99999] # Remove all exact matches

  #     return matches_df


  # col_names_cl = {re.sub('[^a-zA-Z0-9\n\.]', ' ',col_name): col_name for col_name in col_names}
  # print(matches(BUSINESS_GLOSSARY + list(col_names_cl.keys())))

BUSINESS_GLOSSARY = ["First Name","Last Name","Company Name","Address","City","County","Province","State","Zip Code","Postal Code","Phone Number","Email","Website"]
col_names = ["first_name","last_name","company_name","address","city","county","state","zip","phone1","phone2","email","web"]

#Uncomment to see the matches between business glossary and col names, for this the above function needs to be uncommented too.
# match_col_names_with_business_terms(BUSINESS_GLOSSARY, col_names)


def string_match(cols, look_up_word, threshold=0.75):
    identified_pii = []
    restricted_vars = look_up_word.split() #initialize_lists()
    restricted_vars, stemmer = stem_restricted(restricted_vars)

    identified_pii,_ = word_match_stemming(identified_pii, restricted_vars, cols, stemmer, False)
    identified_pii,_ = fuzzy_partial_stem_match(identified_pii, restricted_vars, cols, stemmer, threshold)
    # breakpoint()
    return identified_pii

def get_features(json_data, interested_feats):
    return {key:value for key, value in json_data.items() if key in interested_feats}

def add_to_match_col(match_cols_total, dataset, add_dict, attr):
    for v in match_cols_total[dataset]:
        value = add_dict.get(v['feat_physical_name'], None)
        v[attr] = value[0] if isinstance(value, list) else value

    return match_cols_total

def matched_cols_inds(summary_json, match_cols):
    inds = []
    for col in match_cols:
        for n,feat in enumerate(summary_json['features_list']):
            if col == feat:
                inds.append(n)
    return inds


def get_summary(summary_json, match_cols):

    def myitemgetter(keys, d):
        r = itemgetter(*keys)(d)
        return (r,) if type(r) is not tuple else r

    inds = matched_cols_inds(summary_json, match_cols)

    sample_list_transposed = list(map(list, zip(*summary_json['sample_list'])))

    values = myitemgetter(inds, sample_list_transposed)
    col_name_values = {col:val for col, val in zip(match_cols, values)}

    return col_name_values

def string_match_buss(cols, look_up_word, threshold=0.9):
    identified_pii = []
    #split the word along any non alpha character
    restricted_vars = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', look_up_word)[:1] #look_up_word.split('_') #initialize_lists()
    restricted_vars, stemmer = stem_restricted(restricted_vars)

    identified_pii,_ = word_match_stemming(identified_pii, restricted_vars, cols, stemmer, False)
    identified_pii,_ = fuzzy_partial_stem_match(identified_pii, restricted_vars, cols, stemmer, threshold)
    # breakpoint()
    return ''.join(identified_pii)

# @celery.task()
def write_bussiness_terms(BUSINESS_GLOSSARY, col_names, json_path):
    match = {col_name : string_match_buss(BUSINESS_GLOSSARY, col_name) for col_name in col_names}
    with open(json_path, 'w') as file:
        json.dump(match, file, indent=4)

def get_errors(errors_json, match_cols):
    errs_df = pd.DataFrame(errors_json)
    errs_mtch_cols = errs_df.loc[errs_df['column'].isin(match_cols)]
    errs_mtch_cols['message'] = errs_mtch_cols['message'].astype('category')
    err_freq_dist = errs_mtch_cols.groupby(['column', 'message']).size().reset_index(name='Count')
    err_freq_dist.set_index("column", drop=True, inplace=True)
    err_freq_dist_dict = err_freq_dist.to_dict(orient="index")
    # breakpoint()
    return err_freq_dist_dict


def get_tags():
  pass




