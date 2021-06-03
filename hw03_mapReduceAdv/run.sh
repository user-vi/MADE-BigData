set -x
HADOOP_STREAMING_JAR=/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming.jar

hdfs dfs -rm -r -f $2

(yarn jar $HADOOP_STREAMING_JAR \
	-D mapreduce.job.name="Streaming. Phase 1" \
	-D stream.num.map.output.key.fields=2 \
	-D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
	-D mapreduce.partition.keycomparator.options="-k1,1 -k2,2" \
	-files mapper.py,reducer.py \
	-mapper "./mapper.py" \
	-reducer "./reducer.py" \
	-reducer "./reducer.py" \
	-numReduceTasks 2 \
	-input $1 \
	-output ${2}_tmp &&

yarn jar $HADOOP_STREAMING_JAR \
        -D mapreduce.job.name="Streaming. Phase 2" \
	-D stream.num.map.output.key.fields=2 \
	-D stream.num.reduce.output.key.fields=2 \
        -D mapreduce.job.output.key.comparator.class=org.apache.hadoop.mapreduce.lib.partition.KeyFieldBasedComparator \
        -D mapreduce.partition.keycomparator.options="-k1,1 -k2,2nr" \
	-files mapper_phase_2.py,reducer_phase_2.py \
	-mapper "./mapper_phase_2.py" \
	-reducer "./reducer_phase_2.py" \
        -numReduceTasks 1 \
        -input ${2}_tmp \
        -output $2
)

hdfs dfs -rm -r -skipTrash ${2}_tmp

hdfs dfs -cat $2/* | head -n 20


