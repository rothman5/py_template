""" Singleton module. """


class Singleton:
    """Singleton class."""

    def __new__(cls: type["Singleton"], *args, **kwargs) -> type["Singleton"]:
        instance = cls.__dict__.get("__it__")
        if instance is not None:
            return instance
        cls.__it__ = instance = object.__new__(cls, *args, **kwargs)
        return instance

    def get_instance(self) -> type["Singleton"]:
        """Fetches the single instance of this class.

        Returns:
            Singleton: The only instance of this class type.
        """
        return self.__it__
