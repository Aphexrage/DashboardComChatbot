import sys
from streamlit.web import cli as stcli

sys.argv = ["streamlit", "run", "Pagina Inicial.py"]
sys.exit(stcli.main())
