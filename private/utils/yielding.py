from typing import Generator


def simple_generator():
    yield 1
    yield 2
    yield 3


def test_simple_generator():
    gen = simple_generator()
    assert next(gen) == 1
    assert next(gen) == 2
    assert next(gen) == 3

    try:
        next(gen)
    except StopIteration:
        pass


def grep_generator(pattern: str):
    while True:
        line = yield
        if pattern in line:
            print(f"'{pattern}' found in: {line}")
        else:
            print(f"'{pattern}' not found in: {line}")


def test_grep_generator():
    gen = grep_generator("python")
    # initialize the generator
    next(gen)
    # send some lines to the generator
    gen.send("I love python programming")
    gen.send("I love java programming")
    gen.close()


def a():
    yield from b()
    yield from d()


def b():
    yield from c()


def c():
    yield 1
    yield 2
    yield 3


def d():
    yield 4
    yield 5


class Task:
    def __init__(self, gen: Generator[None, None, int]) -> None:
        self.gen = gen
        self.stack = [gen]

    def run(self) -> Generator[int, None, None]:
        current = self.stack.pop()
        while True:
            try:
                # advance the current generator
                yielded = current.send(None)

                if isinstance(yielded, Generator):
                    self.stack.append(current)
                    current = yielded
                else:
                    yield yielded

            except StopIteration:
                # the current generator is finished
                if not self.stack:
                    break
                else:
                    current = self.stack.pop()


def main():
    task = Task(a())

    for number in task.run():
        print(number)


main()
