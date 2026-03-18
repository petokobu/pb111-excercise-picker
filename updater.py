from filer import Filer


class Updater:
    def __init__(self) -> None:
        self.usr_filer = Filer("usr.txt", folder="data")
        self.scr_filer = Filer("scr.txt", folder="data")
        self.def_filer = Filer("def.txt")

    def reset(self, week_from: int = 1, week_to: int = 12) -> None:
        assert 1 <= week_from <= week_to <= 12, \
            "err: incorrect week interval"

        if week_from == 1 and week_to == 12:
            self.usr_filer.reset()
            self.scr_filer.reset()
        else:
            usr_content = self.usr_filer.get_content()
            def_content = self.def_filer.get_content()
            scr_content = self.scr_filer.get_content()
            assert usr_content is not None \
                   and def_content is not None \
                   and scr_content is not None, "err: missed exception"

            usr_data = usr_content.rstrip().split("\n")
            def_data = def_content.rstrip().split("\n")
            scr_data = scr_content.rstrip().split("\n")

            usr_content = ""
            scr_content = ""

            for week in range(week_from - 1):
                usr_content += usr_data[week] + "\n"
                scr_content += scr_data[week] + "\n"
            for week in range(week_from - 1, week_to):
                usr_content += def_data[week] + "\n"
                scr_content += "0/0\n"
            for week in range(week_to, 12):
                usr_content += usr_data[week] + "\n"
                scr_content += scr_data[week] + "\n"

            self.usr_filer.save_content(usr_content)
            self.scr_filer.save_content(scr_content)

    def delete_ex(self, week: int, tp: str, num: int,
                  excs: dict[int, dict[str, list[int]]]) -> None:
        new_arr = [el for el in excs[week][tp] if el != num]
        excs[week][tp] = new_arr

    def update_score(self, scores: list[tuple[int, int]],
                     week: int, passed: bool) -> None:
        passed_count, total_count = scores[week - 1]
        scores[week - 1] = passed_count + passed, total_count + 1

    def assemble_excs(self, excs: dict[int, dict[str, list[int]]]) -> None:
        content = ""
        for week in range(1, len(excs) + 1):
            for tp in ["p", "r", "v"]:
                content += tp + "/"
                exs = excs[week][tp]
                for ex in range(len(exs) - 1):
                    content += str(exs[ex]) + ","
                if exs:
                    content += str(exs[-1])
                content += "/"
            content += "\n"
        self.usr_filer.save_content(content)

    def assemble_scores(self, scores: list[tuple[int, int]]) -> None:
        content = ""
        for passed, total in scores:
            content += f"{passed}/{total}\n"
        self.scr_filer.save_content(content)
