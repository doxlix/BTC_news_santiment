import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import sqlite3

with sqlite3.connect(r"C:\Users\lazzz\PycharmProjects\News_Parse\news.db") as conn:
    cursor = conn.cursor()

    cursor.execute('''SELECT 
    CASE 
        WHEN domain_count.c > 500 THEN domain_count.domain 
        ELSE 'Other' 
    END AS domain,
    SUM(domain_count.c) AS c
FROM (
    SELECT 
        n.domain,
        COUNT(*) AS c
    FROM news n
    GROUP BY 
        n.domain
    ) AS domain_count
GROUP BY 
    CASE 
        WHEN domain_count.c > 500 THEN domain_count.domain 
        ELSE 'Other' 
    END
ORDER BY 
    CASE 
        WHEN domain_count.c > 500 THEN -domain_count.c 
        ELSE 1 
    END,
    domain ASC;
''')

    domain, count = zip(*cursor.fetchall())
    domain = [i.replace('www.','') for i in domain]
    plt.pie(count, labels=domain, autopct='%1.2f%%', explode=[0.03 for _ in domain], startangle=90,

            colors=
            ["#FF8C69", "#FFA07A", "#FFC1A6", "#ADD8E6", "#87CEFA", "#B0C4DE", "#7FFFD4", "#AFEEEE", "#E0FFFF",
             "#E6E2D3", "#F5ECCE", "#FCEFE6", "#f79cd4", "#fc83b9"]
            )
    plt.title('Domain Distribution in the Dataset (%)')
    plt.show()