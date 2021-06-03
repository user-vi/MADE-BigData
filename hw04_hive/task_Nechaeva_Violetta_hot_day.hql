SELECT `date`, count(*) as cnt 
FROM logs
GROUP BY `date`
ORDER BY cnt desc 
LIMIT 10;
