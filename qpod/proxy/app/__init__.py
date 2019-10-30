from .rshiny import setup_shiny
from .rstudio import setup_rstudio
from .tensorboard import setup_tensorboard
from .code_server import setup_code_server

apps = [
    setup_tensorboard(),
    setup_rstudio(),
    setup_shiny(),
    setup_code_server()
]
