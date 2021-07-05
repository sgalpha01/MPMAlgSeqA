from collections import defaultdict


class PatternMatching:
    _preprocess_proposed_match_data = defaultdict(set)

    def __init__(self, text: str = None, pattern: str = None) -> None:
        self.text = text
        self.pattern = pattern

    def naive_match(self, text: str = None, pattern: str = None) -> list[int]:
        """Implementation of brute-force algorithm

        Args:
            text (str, optional): Main sequence. Defaults to None.
            pattern (str, optional): pattern to be matched in sequence. Defaults to None.

        Returns:
            list[int]: List of integer indices where match occurs, if any.
        """
        if text is None:
            text = self.text

        if pattern is None:
            pattern = self.pattern

        n = len(text)
        k = len(pattern)
        indices = []

        for i in range(n - k + 1):
            curr_kmer = text[i : i + k]
            if pattern == curr_kmer:
                indices.append(i)

        return indices

    @classmethod
    def _preprocess_proposed_match(cls, text: str) -> dict[str : list[int]]:
        for i in range(len(text) - 1):
            cls._preprocess_proposed_match_data[text[i : i + 2]].add(i)

        return cls._preprocess_proposed_match_data

    def proposed_match(self, text: str = None, pattern: str = None) -> list[int]:
        """Implementation of the proposed algorithm

        Args:
            text (str, optional): Main sequence. Defaults to None.
            pattern (str, optional): pattern to be matched in sequence. Defaults to None.

        Returns:
            list[int]: List of integer indices where match occurs, if any.
        """

        if text is None:
            text = self.text

        if pattern is None:
            pattern = self.pattern

        k = len(pattern)
        indices = []
        idx_table_pat = defaultdict(list)

        # creates index table for the text
        if not self._preprocess_proposed_match_data:
            idx_table_text = self._preprocess_proposed_match(text)

        else:
            idx_table_text = self._preprocess_proposed_match_data

        # creates index table for the pattern
        for i in range(0, k - 1, 2):
            idx_table_pat[pattern[i : i + 2]].append(i)

        # creates sorted array of pairs in pattern
        sorted_pat_pair = sorted(idx_table_pat, key=lambda x: len(idx_table_pat[x]))

        # creates sorted array of indexes of least occuring
        # pair in pattern present in text
        match_idx = sorted(idx_table_text[sorted_pat_pair[0]])

        # stores index of first least occuring pair in pattern
        align_idx = idx_table_pat[sorted_pat_pair[0]][0]

        for idx_text in match_idx:
            # Starting index of pattern in sequence
            curr_align = idx_text - align_idx
            cont = True
            for pair in sorted_pat_pair:
                if not cont:
                    break
                for idx_pat in idx_table_pat[pair]:
                    if idx_pat + curr_align not in idx_table_text[pair]:
                        cont = False
                        break

            # To handle odd length pattern
            try:
                if cont and text[curr_align + k - 1] == pattern[-1]:
                    indices.append(curr_align)
            except (KeyError, IndexError):
                continue

        return indices

    def performance(self) -> None:
        """Compares the runtime of naive algorithm and the proposed algorithm"""
        import time

        funcs = [self.naive_match, self.proposed_match]

        for func in funcs:
            tic = time.perf_counter()
            func()
            toc = time.perf_counter()
            print(f"{func.__name__} took {(toc - tic):.4f}s to run.")
