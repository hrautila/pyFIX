
import pyfix.util.client as cl
import pyfix.fix.fix42 as f42
import pyfix.fix.fix44 as f44
from pyfix.fix import *

c2 = FixContext(version='4.2')
c4 = FixContext(version='4.4')


new_ord = f42.NewOrderSingle(c2, {"ClOrdID": "foo",
                                  "Symbol": "NOK1V",
                                  "SecurityID": "FI0002123456",
                                  "Side": "1",
                                  "Price": 4.5})
