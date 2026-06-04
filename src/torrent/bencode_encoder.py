class BencodeEncoder:

    def encode(self, value):

        if isinstance(value, int):
            return self.encode_integer(value)

        if isinstance(value, str):
            return self.encode_string(value)

        if isinstance(value, list):
            return self.encode_list(value)

        if isinstance(value, dict):
            return self.encode_dictionary(value)

        raise ValueError(f"Unsupported type: {type(value)}")

    def encode_integer(self, value):
        return f"i{value}e"

    def encode_string(self, value):
        return f"{len(value)}:{value}"

    def encode_list(self, value):
        result = "l"

        for item in value:
            result += self.encode(item)

        result += "e"

        return result

    def encode_dictionary(self, value):
        result = "d"

        for key in sorted(value.keys()):
            result += self.encode(key)
            result += self.encode(value[key])

        result += "e"

        return result