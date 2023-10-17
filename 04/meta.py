class CustomMeta(type):
    def __new__(cls, name, bases, attrs):
        new_attrs = {}
        for key, val in attrs.items():
            if key.startswith("__") and key.endswith("__"):
                new_attrs[key] = val
            else:
                new_attrs[f"custom_{key}"] = val

        def meta_custom_setattr(obj, name, value):
            if f"custom_{name}" in obj.__dict__:
                return
            if not name.startswith("__") and not name.endswith("__"):
                name = f"custom_{name}"
            super(obj.__class__, obj).__setattr__(name, value)

        new_attrs["__setattr__"] = meta_custom_setattr
        return super().__new__(cls, name, bases, new_attrs)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"


CustomClass.y = 5
print(CustomClass.y)
