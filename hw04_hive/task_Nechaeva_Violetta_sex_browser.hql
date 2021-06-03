set hive.auto.convert.join=false;
set mapreduce.job.reduces=2;


SELECT u.browser, 
count(CASE WHEN u.sex = 'male' THEN 1 END) as males, 
count(CASE WHEN u.sex = 'female' THEN 1 END) as females
FROM users u
JOIN logs l
on l.ip = u.ip 
GROUP BY u.browser 
LIMIT 10;
