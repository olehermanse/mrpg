from mrpg.utils.utils import column_lines


class Menu():
    def __init__(self, *args, **kwargs):
        headline = args[0]
        args = list(args[1:])
        args_len = len(args)
        lst = None
        hints = None
        hints_sep = None

        if "lst" in kwargs:
            lst = kwargs["lst"]
            del kwargs["lst"]
            for item in lst:
                args.append(item)
        if "hints" in kwargs:
            hints = kwargs["hints"]
            hints_sep = len(hints) * [" - "]
            del kwargs["hints"]
            if args_len > 0:
                hints = [""] * args_len + hints
                hints_sep = [""] * args_len + hints_sep

        extended_args = []
        indices = list(range(1, len(args) + 1))
        for key, value in kwargs.items():
            indices.append(key)
            extended_args.append(value)
        for index, arg in enumerate(args):
            kwargs[str(index + 1)] = arg
        args += extended_args
        while hints and len(hints) < len(args):
            hints.append("")
            hints_sep.append("")

        self.headline = headline
        self.indices = [str(x) for x in indices]
        self.separator = ": "
        self.choices = args
        self.hints_sep = hints_sep
        self.hints = hints

    def as_lines(self):
        lines = [self.headline]
        if self.hints:
            lines += column_lines(
                self.indices, self.separator, self.choices, self.hints_sep,
                self.hints)
        else:
            lines += column_lines(self.indices, self.separator, self.choices)
        return lines

    def as_string(self):
        return "\n".join(self.as_lines())

    def choice(self, inp):
        inp = str(inp)
        inp = inp.strip()
        if inp in self.choices:
            return inp
        if inp in self.indices:
            return self.choices[self.indices.index(inp)]
        return None
