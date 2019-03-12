from typing import Mapping


def FormatFile(filename: str,
               style_config: Mapping = None,
               lines=None,
               print_diff=False,
               verify=False,
               in_place=False,
               logger=None) -> None: ...
