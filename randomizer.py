from parser import Parser
import random


class Randomizer:
    def __init__(self, parser: Parser,
                 week_from: int = 1, week_to: int = 12) -> None:
        assert 1 <= week_from <= week_to <= 12, \
            "err: incorrect week interval"

        self.excs = parser.excs
        self.av_weeks: list[int] = []
        self.av_excs: dict[int, list[str]] = {}

        for week in range(week_from, week_to + 1):
            if parser.empty_weeks[week]:
                continue
            self.av_weeks.append(week)
            self.av_excs[week] = []
            for tp in ["p", "r", "v"]:
                if parser.empty_excs[week][tp]:
                    continue
                self.av_excs[week].append(tp)

    def pick(self) -> tuple[int, str, int] | None:
        if len(self.av_weeks) == 0:
            return None
        week = random.choice(self.av_weeks)
        tp = random.choice(self.av_excs[week])
        num = random.choice(self.excs[week][tp])
        return week, tp, num
