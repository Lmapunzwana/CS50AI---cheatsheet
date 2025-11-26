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
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = {}
    num_pages = len(corpus)
    links = corpus[page]

    # If page has no links, interpret as having one link for every page (including itself)
    if len(links) == 0:
        for p in corpus:
            distribution[p] = 1 / num_pages
        return distribution

    # Probability of choosing any page at random
    random_prob = (1 - damping_factor) / num_pages

    # Initialize distribution with the random selection probability
    for p in corpus:
        distribution[p] = random_prob

    # Add the probability of following a link
    link_prob = damping_factor / len(links)
    for link in links:
        distribution[link] += link_prob

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize counts
    counts = {page: 0 for page in corpus}

    # First sample is chosen at random from all pages
    current_page = random.choice(list(corpus.keys()))
    counts[current_page] += 1

    # Generate the remaining n-1 samples
    for _ in range(n - 1):
        # Get probability distribution for the next page
        probs = transition_model(corpus, current_page, damping_factor)
        
        # Extract pages and weights for random.choices
        pages = list(probs.keys())
        weights = list(probs.values())
        
        # Choose next page
        current_page = random.choices(pages, weights=weights, k=1)[0]
        counts[current_page] += 1

    # Normalize counts to get PageRank
    ranks = {page: count / n for page, count in counts.items()}
    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    
    # Start with 1/N for every page
    ranks = {page: 1 / num_pages for page in corpus}
    
    while True:
        new_ranks = {}
        max_change = 0

        for p in corpus:
            # First term of the equation: (1 - d) / N
            rank_val = (1 - damping_factor) / num_pages

            # Second term: sum(PR(i) / NumLinks(i)) for all i that link to p
            summation = 0
            for i in corpus:
                # If i links to p
                if p in corpus[i]:
                    summation += ranks[i] / len(corpus[i])
                # If i has no links, it interprets as linking to all pages (including p)
                elif len(corpus[i]) == 0:
                    summation += ranks[i] / num_pages
            
            rank_val += damping_factor * summation
            new_ranks[p] = rank_val
            
            # Track the maximum change to check for convergence
            change = abs(new_ranks[p] - ranks[p])
            if change > max_change:
                max_change = change

        ranks = new_ranks

        # Stop if no value changes by more than 0.001
        if max_change < 0.001:
            break
            
    return ranks


if __name__ == "__main__":
    main()