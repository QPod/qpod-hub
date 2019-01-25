from .rshiny import setup_shiny
from .rstudio import setup_rstudio
from .tensorboard import setup_tensorboard

apps = [
    setup_tensorboard(),
    setup_rstudio(),
    setup_shiny()
]
