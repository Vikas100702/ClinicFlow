from lib.lib_import import Annotated, StringConstraints

NameType = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50, pattern=r'^[A-Za-z ]+$')]
PhoneType = Annotated[str, StringConstraints(pattern=r'^[0-9]{10}$')]
AddressType = Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]
Text100 = Annotated[str, StringConstraints(strip_whitespace=True, max_length=100)]
Text1000 = Annotated[str, StringConstraints(strip_whitespace=True, max_length=1000)]
