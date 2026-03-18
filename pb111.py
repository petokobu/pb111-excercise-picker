from sys import argv
from filer import Filer
from parser import Parser
from randomizer import Randomizer
from updater import Updater


Bundle = tuple[Filer, Filer, Parser, Parser, Updater]


def print_error(msg: str = "incorrect argument..") -> None:
    print(msg)
    print("aborting..")


def process_update(bundle: Bundle) -> None:
    usr_filer, scr_filer, usr_parser, scr_parser, updater = bundle

    if not argv[1].isdecimal():
        print_error()
        return
    week = int(argv[1])
    if week < 1 or week > 12:
        print_error()
        return
    tp = argv[2].lower()
    if tp not in {"p", "r", "v"}:
        print_error()
        return
    if not argv[3].isdecimal():
        print_error()
        return
    num = int(argv[3])
    action = argv[4].lower()
    if action not in {"passed", "failed"}:
        print_error()
        return

    if not usr_parser.parse():
        return
    usr_parser.filter()
    if num not in usr_parser.excs[week][tp]:
        print_error(f"excercise {week:02}/{tp}{num} not available..")
        return

    scores = scr_parser.get_scores()
    if action == "passed":
        excs = usr_parser.excs
        updater.delete_ex(week, tp, num, excs)
        updater.assemble_excs(excs)
    updater.update_score(scores, week, action == "passed")
    updater.assemble_scores(scores)


def get_args() -> tuple[int, int, str] | None:
    if len(argv) == 3:
        if argv[1].lower() == "all":
            week_from = 1
            week_to = 12
        elif not argv[1].isdecimal():
            print_error()
            return None
        else:
            week_from = int(argv[1])
            week_to = week_from
        action = argv[2].lower()
        if action not in {"pick", "reset", "score"}:
            print_error()
            return None
        return week_from, week_to, action
    
    if not argv[1].isdecimal() or not argv[2].isdecimal():
        print_error()
        return None
    week_from = int(argv[1])
    week_to = int(argv[2])
    if week_from < 1 or week_from > week_to or week_to > 12:
        print_error()
        return None
    action = argv[3].lower()
    if action not in {"pick", "reset", "score"}:
        print_error()
        return
    return week_from, week_to, action


def main() -> None:
    if len(argv) == 1 or argv[1].lower() in {"help", "-help", "--help"}:
        readme_filer = Filer("README.txt")
        print(readme_filer.get_content())
        return

    if not 3 <= len(argv) <= 5:
        print_error()
        return

    usr_filer = Filer("usr.txt", folder = "data")
    scr_filer = Filer("scr.txt", folder = "data")
    usr_parser = Parser(usr_filer)
    scr_parser = Parser(scr_filer)
    updater = Updater()
    bundle: Bundle = usr_filer, scr_filer, usr_parser, scr_parser, updater

    if len(argv) == 5:
        process_update(bundle)
        return
    
    args = get_args()
    if args is None:
        return
    week_from, week_to, action = args
    
    if action == "score":
        passed, total = scr_parser.get_score(week_from, week_to)
        perc = str(round((passed / total) * 100, 2)) + " %" \
            if total > 0 else "- %"
        print(f"{passed}/{total}\t{perc}")
    elif action == "reset":
        updater.reset(week_from, week_to)
    else:
        if not usr_parser.parse():
            return
        usr_parser.filter()
        randomizer = Randomizer(usr_parser, week_from, week_to)
        pick = randomizer.pick()
        if pick is None:
            print_error(msg = "no available excercise..")
            return
        week, tp, num = pick
        print(f"{week:02}/{tp}{num}")
        result = input("[P]assed/[F]ailed/[...]: ").lower()
        if result == "p":
            excs = usr_parser.excs
            updater.delete_ex(week, tp, num, excs)
            scores = scr_parser.get_scores()
            updater.update_score(scores, week, True)
            updater.assemble_excs(excs)
            updater.assemble_scores(scores)
        elif result == "f":
            scores = scr_parser.get_scores()
            updater.update_score(scores, week, False)
            updater.assemble_scores(scores)


def create_call(args: str) -> int:
    arg_count = 0
    for arg in args.rstrip().split(" "):
        argv.append(arg)
        arg_count += 1
    return arg_count


def test_call(args: str) -> None:
    arg_count = create_call(args)
    main()
    for _ in range(arg_count):
        argv.pop()


def testing() -> None:
    test_call("all pick")
    test_call("all score")
    test_call("all reset")
    test_call("all score")


# testing()
main()