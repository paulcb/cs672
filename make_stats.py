import sys
import json
from datetime import datetime

# def print_stats():

# print_stats = False
print_stats = True

stat_file = open(sys.argv[1], 'r')

count = 0
start_time = None
end_time = None

app_1_cpu_u_sum = 0

for line in stat_file.readlines():
  # print(line)
  # if '[2J[H' in line:
    # print('fook', line)
  stats = json.loads(line)
  if print_stats:
    print('-------------------')
  if 'Name' in stats:
    if stats['Name'] == 'cs672_app_a-0_1':
        app_1_cpu_u_sum += float(stats['CPUPerc'][:-1])
  
  for k,v in stats.items():
    if print_stats:
      print(k, v)
    
    if k == 'TIME_START':
      start_time = v
    if k == 'TIME_END':
      end_time = v
  count+=1
count = count/3
print('transaction_count', count)

start_time = datetime.strptime(start_time, '%H:%M:%S')
end_time = datetime.strptime(end_time, '%H:%M:%S')
print('start_time', start_time)
print('end_time', end_time)
total_time = end_time - start_time
print('start_time - end_time', total_time, 'seconds:', total_time.seconds)

print('app_1_cpu_u_sum', app_1_cpu_u_sum)
app_1_cpu_u_average = app_1_cpu_u_sum / (count - 2)
print('app_1_cpu_u_average', app_1_cpu_u_average)

