import requests
import pandas as pd
import time
from datetime import datetime

JOURNALS = {
    'Top 5': {
        "American Economic Review": "0002-8282",
        "Quarterly Journal of Economics": "0033-5533",
        "Journal of Political Economy": "0022-3808",
        "Econometrica": "0012-9682",
        "Review of Economic Studies": "0034-6527",
    },
    'Top Field Journals': {
        "Journal of Finance": "0022-1082",
        "Journal of Financial Economics": "0304-405X",
        "Journal of Monetary Economics": "0304-3932",
        "Journal of International Economics": "0022-1996",
        "Journal of Public Economics": "0047-2727",
        "Journal of Labor Economics": "0734-306X",
        "Journal of Development Economics": "0304-3878",
        "Journal of Urban Economics": "0094-1190",
        "Journal of Health Economics": "0167-6296",
        "Review of Financial Studies": "0893-9454",
    },
    'Mid-Tier': {
        "Economic Inquiry": "0095-2583",
        "Southern Economic Journal": "0038-4038",
        "Applied Economics": "0003-6846",
        "European Economic Review": "0014-2921",
        "Journal of Economic Behavior & Organization": "0167-2681",
        "Economics Letters": "0165-1765",
        "Oxford Economic Papers": "0030-7653",
        "International Economic Review": "0020-6598",
    },
    'Lower-Tier & Regional': {
        "China Economic Review": "1043-951X",
        "World Development": "0305-750X",
        "Emerging Markets Review": "1566-0141",
        "Modern Economy": "2152-7261",
        "International Journal of Economics and Finance": "1916-971X",
        "Theoretical Economics Letters": "2162-2078",
        "Economies": "2227-7099",
    }
}