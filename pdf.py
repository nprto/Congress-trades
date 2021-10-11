import pandas as pd
import tabula
file = "disclosure.pdf"

df = tabula.read_pdf(file, pages = '1', multiple_tables = False)
print(df)