from filer import Filer
import sys


class Parser:
    def __init__(self, filer: Filer) -> None:
        assert filer.filename in {"usr.txt", "scr.txt"}, \
            "err: trying to parse from an unspecified file"
        self.filer = filer
        self.excs: dict[int, dict[str, list[int]]] = {}
        self.fail_counter = 0
        self.empty_weeks: dict[int, bool] = {}
        self.empty_excs: dict[int, dict[str, bool]] = {}

    def parse(self) -> bool:
        assert self.filer.filename == "usr.txt", \
            "err: trying to parse from an unspecified file"

        if self.fail_counter >= 10:
            sys.stderr.write("ERROR: failed to parse usr.txt\n")
            sys.stderr.write("ABORTING..")
            return False

        weeks = self.filer.get_content().split("\n")
        try:
            for week, line in enumerate(weeks):
                self.excs[week + 1] = {}
                seg = line.rstrip().split("/")
                for i in range(0, 5, 2):
                    self.excs[week + 1][seg[i]] = \
                        [int(ex) for ex in seg[i + 1].split(",")
                        if ex]
        except:
            self.fail_counter += 1
            self.parse()
        return True

    def filter(self) -> None:
        assert self.filer.filename == "usr.txt", \
            "err: trying to parse from an unspecified file"

        for week in range(1, 13):
            week_empty = True
            self.empty_excs[week] = {}
            for tp in ["p", "r", "v"]:
                if len(self.excs[week][tp]) == 0:
                    self.empty_excs[week][tp] = True
                else:
                    self.empty_excs[week][tp] = False
                    week_empty = False
            self.empty_weeks[week] = week_empty

    def get_score(self,
                  week_from: int = 1, week_to: int = 12) -> tuple[int, int]:
        assert self.filer.filename == "scr.txt", \
            "err: trying to parse from an unspecified file"
        assert 1 <= week_from <= week_to <= 12, \
            "err: incorrect week interval"
    
        passed, total = 0, 0
        scores = self.filer.get_content().split("\n")

        try:
            for week in range(week_from, week_to + 1):
                seg = scores[week - 1].split("/")
                passed += int(seg[0])
                total += int(seg[1])
        except:
            sys.stderr.write("ERROR: corrupted data in scr.txt\n")
            sys.stderr.write("RECOVERING DEFAULT DATA..\n")
            sys.stderr.flush()
            self.filer.reset()
        
        return passed, total
    
    def get_scores(self) -> list[tuple[int, int]]:
        assert self.filer.filename == "scr.txt", \
            "err: trying to parse from an unspecified file"
        
        lines = self.filer.get_content().split("\n")
        scores = []
        try:
            for week in lines:
                seg = week.split("/")
                scores.append((int(seg[0]), int(seg[1])))
        except:
            sys.stderr.write("ERROR: corrupted data in scr.txt\n")
            sys.stderr.write("RECOVERING DEFAULT DATA..\n")
            sys.stderr.flush()
            self.filer.reset()
        
        return scores
