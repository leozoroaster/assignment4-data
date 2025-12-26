from pathlib import Path
import hashlib
import re
import unicodedata
import random

def normalize_text(path):
    with open(path, "r", encoding="utf-8") as f:
        text_str = f.read()

    #lower_case
    text_str=text_str.lower()

    #remove punctuation
    text_str = re.sub(r"[^\w\s]", "", text_str)

    # normalizing whitespaces
    text_str=re.sub(r"\s+", " ", text_str).strip()

    #removing accents
    text_str="".join(
        char for char in unicodedata.normalize("NFKD", text_str)
        if not unicodedata.combining(char)
    )

    # applying NFD unicode normalization
    text_str = unicodedata.normalize("NFD", text_str)

    return text_str

def get_ngrams(text: str, n: int):
    tokens = text.split()
    if n <= 0 or len(tokens) < n:
        return []
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def hash_ngram(tokens: tuple[str], seed: int = 0) -> int:
    # join with a separator that cannot appear in tokens
    joined = "\x1f".join(tokens)   # ASCII Unit Separator
    h = hashlib.blake2b(
        joined.encode("utf-8"),
        digest_size=8,
        person=seed.to_bytes(8, "little"),
    )
    return int.from_bytes(h.digest(), "little")

def get_minhash(document, n, seed):
    minhash=None
    ngrams=get_ngrams(document, n)
    for g in ngrams:
        hash_result=hash_ngram(g, seed)
        if minhash is not None:
            minhash=min(minhash,hash_result)
        else:
            minhash=hash_result
    return minhash

def get_signature(document, n , n_hash):
    signature=[]
    for seed in range(n_hash):
        minhash=get_minhash(document, n, seed)
        signature.append(minhash)
    return signature

def compare_signature(s1,s2, bucket_len, n_band):
    for i in range(n_band):
        chunk1=s1[i*bucket_len: (i+1)*bucket_len]
        chunk2=s2[i*bucket_len: (i+1)*bucket_len]
        if chunk1==chunk2:
            return True
    return False

def compute_jaccard(s1,s2):
    counts=0
    for i in range(len(s1)):
        if s1[i]==s2[i]:
            counts+=1
    return counts/len(s1)

def merge_set(list_of_sets, new_set):
    overlap_set=new_set
    remaining_sets=[]
    for i in range(len(list_of_sets)):
        curr_set=list_of_sets[i]
        if curr_set.intersection(overlap_set):
            overlap_set=curr_set.union(overlap_set)
        else:
            remaining_sets.append(list_of_sets[i])
    remaining_sets.append(overlap_set)
    return remaining_sets

def cluster_from_graph(graph):
    running_sets=[]
    for neighbor_set in graph.values():
        running_sets=merge_set(running_sets,neighbor_set)
    return running_sets

def minhash_deduplication(list_of_paths, n_hash, n_band, n_gram_len, ratio, output_dic):
    documents=[]
    filenames=[]
    num_docs=len(list_of_paths)

    #first pass, save filenames and normalize documents
    for path in list_of_paths:
        filename = Path(path).name
        filenames.append(filename)

        normalized_doc=normalize_text(path)
        documents.append(normalized_doc)

    #second pass, get signatures
    signatures = []

    for document in documents:
        signature=get_signature(document, n_gram_len , n_hash)
        signatures.append(signature)

    #third pass, LSH
    bucket_len = int(n_hash / n_band)
    cluster_graph=dict()
    for i in range(num_docs):
        cluster_graph[i]= {i}

    for i in range(num_docs-1):
        for j in range(i+1,num_docs):
            s1=signatures[i]
            s2=signatures[j]
            is_similar=compare_signature(s1,s2, bucket_len, n_band)

            if is_similar:
                if compute_jaccard(s1,s2)>=ratio:
                    cluster_graph[i].add(j)
                    cluster_graph[j].add(i)

    #finalize clusters from graph
    clusters=cluster_from_graph(cluster_graph)
    for cluster in clusters:
        chosen_index = random.choice(tuple(cluster))
        original_path=list_of_paths[chosen_index]
        with open(original_path, "r", encoding="utf-8") as f:
            chosen_doc = f.read()
        chosen_path=Path(output_dic)/ filenames[chosen_index]
        with open(chosen_path, "w", encoding="utf-8") as f:
            f.write(chosen_doc)








