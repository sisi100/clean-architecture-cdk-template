from dataclasses import asdict, dataclass


@dataclass
class User:
    pk: int
    name: str
    age: int

    @property
    def sk(self) -> str:
        return f"USER#{self.pk}"

    def to_dict(self):
        dict_data = asdict(self)
        for key in [
            "sk",
        ]:
            value = getattr(self, key)
            dict_data[key] = value
        return dict_data
