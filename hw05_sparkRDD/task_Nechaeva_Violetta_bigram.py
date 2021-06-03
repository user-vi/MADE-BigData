import re

wiki = sc.textFile("hdfs:///data/wiki/en_articles_part")
wiki\
.map(lambda string: string.split("\t", 1))\
.map(lambda pair: pair[1].lower())\
.map(lambda content: content.replace('narodnaya ', 'narodnaya_'))\
.flatMap(lambda content: re.findall(r"\w+", content))\
.map(lambda w: (w, 1))\
.reduceByKey(lambda x, y: x + y)\
.filter(lambda pair: re.findall(r"narodnaya_\w+", pair[0]))\
.sortByKey()\
.map(lambda pair: str(pair[0]) + "\t" + str(pair[1]))\
.saveAsTextFile("hdfs:///user/made21q1_nechaeva/task_Nechaeva_Violetta_bigram2.out")
