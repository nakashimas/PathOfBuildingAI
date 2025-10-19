import argparse
import logging


from src.lua_scripts.apply_patch import apply_patch
from src.pob.client import PathOfBuildingCli


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="mode",
        required=True,
        help="Set Mode",
    )
    cli_parser = subparsers.add_parser(
        "cli",
        help="Start CLI mode",
    )
    subparsers.add_parser(
        "chat",
        help="Start Chat mode",
    )
    subparsers.add_parser(
        "cui",
        help="Start CUI mode",
    )
    patch_parser = subparsers.add_parser(
        "patch",
        help="Only Apply patch for Path of Building",
    )

    # CLI Mode Options
    cli_parser.add_argument(
        "sub_mode",
        choices=["start", "request"],
        help="Choice a sub mode",
    )
    cli_parser.add_argument(
        "--pid",
        required=False,
        help="Command Request Process ID (Path of Building)",
    )
    cli_parser.add_argument(
        "--body",
        required=False,
        help="Command Request body",
    )

    # PATCH Mode Options
    patch_parser.add_argument(
        "--force",
        action="store_true",
        help="force update",
    )

    args = parser.parse_args()

    if args.mode == "cli":
        logging.disable(logging.CRITICAL)
        if args.sub_mode == "start":
            pob = PathOfBuildingCli(force_update=True)
            pob.start()
            print(pob.process.pid)
        elif args.sub_mode == "request":
            pob = PathOfBuildingCli(pid=int(args.pid), force_update=True)
            res = pob.send_and_wait(str(args.body))
            print(res)

    elif args.mode == "chat":
        logging.disable(logging.CRITICAL)
        raise NotImplementedError("chat is TBD")

    elif args.mode == "cui":
        try:
            with PathOfBuildingCli(force_update=True) as pob:
                logging.disable(logging.CRITICAL)
                print("Input Commands / Press Ctrl + C to Exit")
                while True:
                    term = input("I > ")
                    if term:
                        commands = term.split(" ")
                        if (
                            commands[0] == "load"
                            and len(commands) > 2
                            and commands[1] == "build"
                        ):
                            res = pob.load_build(commands[2])
                            print(f"O >> {res}")
                        elif (
                            commands[0] == "save"
                            and len(commands) > 2
                            and commands[1] == "build"
                        ):
                            res = pob.save_build(commands[2])
                            print(f"O >> {res}")
                        else:
                            print(f"O >> command not found {term}")
        except KeyboardInterrupt:
            print("\nO >> exit")
        except Exception:
            raise

    elif args.mode == "patch":
        apply_patch(args.force)


if __name__ == "__main__":
    main()
