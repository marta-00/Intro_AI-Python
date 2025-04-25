import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a dictionary representing the probability distribution over 
    which page to visit next, given a corpus of pages, current page and
    damping factor.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.

    returns: Python dictionary with one key for each page in the corpus.
             Each should be mapped to a value representing the probability
             of choosing that page next.
    """
    # If page has no links, return a distribution that chooses any page
    # with equal probability
    # (including the current page)
    if not corpus[page]:
        return {p: 1 / len(corpus) for p in corpus}

    # If the page has links, the probabilitity should de split equally
    # among the links. then add the damping_factor of choosing any page
    # including the current page
    transition_probs = dict()
    num_links = len(corpus[page])
    for p in corpus:
        if p in corpus[page]:
            transition_probs[p] = damping_factor / num_links
        else:
            transition_probs[p] = (1 - damping_factor) / len(corpus)
    # Add the probability of choosing any page
    for p in corpus:
        transition_probs[p] += (1 - damping_factor) / len(corpus)
    # Normalize the probabilities
    total = sum(transition_probs.values())
    for p in transition_probs:
        transition_probs[p] /= total
    # Ensure that the probabilities sum to 1
    total = sum(transition_probs.values())
    if total != 1:
        for p in transition_probs:
            transition_probs[p] /= total
            
    return transition_probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.
    The next samples should be generated from the previous sample
    according to the transition model.

    You will likely want to pass the previous sample into your transition_model function, along with the corpus and the damping_factor, to get the probabilities for the next sample.
    assume n will be at least 1
    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Choose a random page to start
    current_page = random.choice(list(corpus.keys()))
    # Initialize a dictionary to store the number of times each page is sampled
    samples = {page: 0 for page in corpus}
    # Sample n pages
    for _ in range(n):
        samples[current_page] += 1
        transition_probs = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(transition_probs.keys()),
            weights=list(transition_probs.values())
        )[0]
    # Normalize the samples to get the PageRank values
    total_samples = sum(samples.values())
    ranks = {page: count / total_samples for page, count in samples.items()}
    
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
