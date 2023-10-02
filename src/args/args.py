class Args:
    def __init__(self, schema: str, args: list[str]) -> None:
        self.__number_of_arguments = 0
        self.__unexpected_arguments: set[str] = set()
        self.__boolean_args: dict[str, bool] = {}
        self.__schema = schema
        self.__args = args
        self.__valid = self.__parse()

    def __parse(self) -> bool:
        if len(self.__schema) == 0 and len(self.__args) == 0:
            return True

        self.__parse_schema()
        self.__parse_arguments()
        return len(self.__unexpected_arguments) == 0

    def __parse_schema(self) -> bool:
        for element in self.__schema.split(","):
            self.__parse_schema_element(element)

        return True

    def __parse_schema_element(self, element: str) -> None:
        if len(element) == 1:
            self.__parse_boolean_schema_element(element)

    def __parse_boolean_schema_element(self, element: str) -> None:
        c = element[0]
        if c.isalpha():
            self.__boolean_args[c] = False

    def __parse_arguments(self) -> bool:
        for arg in self.__args:
            self.__parse_argument(arg)

        return True

    def __parse_argument(self, arg: str) -> None:
        if arg.startswith("-"):
            self.__parse_elements(arg)

    def __parse_elements(self, arg: str) -> None:
        for arg_char in arg[1:]:
            self.__parse_element(arg_char)

    def __parse_element(self, arg_char: str) -> None:
        if self.__is_boolean(arg_char):
            self.__number_of_arguments += 1
            self.__set_boolean_arg(arg_char, True)
        else:
            self.__unexpected_arguments.add(arg_char)

    def __set_boolean_arg(self, arg_char: str, value: bool) -> None:
        self.__boolean_args[arg_char] = value

    def __is_boolean(self, arg_char: str) -> bool:
        return arg_char in self.__boolean_args

    def cardinality(self) -> int:
        return self.__number_of_arguments

    def usage(self) -> str:
        if len(self.__schema) > 0:
            return f"-[{self.__schema}]"

        return ""

    def error_message(self) -> str:
        if len(self.__unexpected_arguments) > 0:
            return self.__unexpected_argument_message()

        return ""

    def __unexpected_argument_message(self) -> str:
        message = "Argument(s) -"
        for c in self.__unexpected_arguments:
            message += c
        message += " unexpected."

        return message

    def get_boolean(self, arg: str) -> bool:
        return self.__boolean_args[arg]
