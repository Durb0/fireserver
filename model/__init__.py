from . import main
from . import category
from . import card
from . import enums
from . import truck

main.Base.metadata.create_all(main.Engine)
