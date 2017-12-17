def menu(*args, **kwargs):
    headline = args[0]
    args = list(args[1:])
    extended_args = []
    indices = list(range(len(args)))
    for key, value in kwargs.items():
        indices.append(key)
        extended_args.append(value)
    for index, arg in enumerate(args):
        kwargs[str(index)] = arg
    args += extended_args
    while True:
        print(headline)
        for ind, opt in zip(indices, args):
            print("{}: {}".format(ind, opt))
        choice = input(">").strip()
        if choice in args:
            return choice
        try:
            return kwargs[choice]
        except:
            pass
