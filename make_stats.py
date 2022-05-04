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
cs672_tensorflow_1_sum = 0
cs672_rabbitmq_1_sum = 0
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
    if stats['Name'] == 'cs672_tensorflow_gpu_1':
        cs672_tensorflow_1_sum += float(stats['CPUPerc'][:-1])
    if stats['Name'] == 'cs672_rabbitmq_1':
        cs672_rabbitmq_1_sum += float(stats['CPUPerc'][:-1])
  
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
app_1_cpu_u_average = app_1_cpu_u_average/100
print('cs672_tensorflow_1_sum', cs672_tensorflow_1_sum)
cs672_tensorflow_1_sum = cs672_tensorflow_1_sum / (count - 2)
print('cs672_tensorflow_1_average', cs672_tensorflow_1_sum)
# cs672_tensorflow_1_sum = cs672_tensorflow_1_sum / 8.0
# print('cs672_tensorflow_1_average2', cs672_tensorflow_1_sum)
cs672_tensorflow_1_sum = cs672_tensorflow_1_sum / 100

print('cs672_rabbitmq_1_sum', cs672_rabbitmq_1_sum)
cs672_rabbitmq_1_average = cs672_rabbitmq_1_sum / (count - 2)
print('cs672_rabbitmq_1_average', cs672_rabbitmq_1_average)
cs672_rabbitmq_1_average = cs672_rabbitmq_1_average / 100
C = 2463
T = 120
X0 = C / 120
print(X0)
print(app_1_cpu_u_average/X0, cs672_tensorflow_1_sum/X0, cs672_rabbitmq_1_average/X0)

#disk
disk_speed_mbps = 209
a = 272
b = 8.19 / 1024
c = 45.1 / 1024

mbp_t = a/C
a_u = (X0 * mbp_t / (disk_speed_mbps))/100
a_d = a_u/X0
mbp_t = b/C
b_u = (X0 * mbp_t / (disk_speed_mbps))/100
b_d = b_u/X0
mbp_t = c/C
c_u = (X0 * mbp_t / (disk_speed_mbps))/100
c_d = c_u/X0
print(a_u, b_u, c_u)
print(a_d, b_d, c_d)

#disk
disk_speed_mbps = 10 * 1024
a = 1.42*1024 + 1.42*1024
b = 807 + 614
c = 612 + 196

mbp_t = (a+b+c)/C
a_u = (X0 * mbp_t / (disk_speed_mbps))/100
a_d = a_u/X0
mbp_t = b/C
b_u = (X0 * mbp_t / (disk_speed_mbps))/100
b_d = b_u/X0
mbp_t = c/C
c_u = (X0 * mbp_t / (disk_speed_mbps))/100
c_d = c_u/X0
print(a_u, b_u, c_u)
print(a_d, b_d, c_d)
# 6.208333333333333
# >>> 107/745
# 0.1436241610738255
# >>> mbp_t = 107/745
# >>> mbp_t
# 0.1436241610738255
# >>> X0*mbp_t
# 0.8916666666666666
# >>> X0*mbp_t / (209)
# 0.004266347687400318
# >>> .89*120
# 106.8
# >>> .004/X0
# 0.0006442953020134229

f1 = open('opt_4/foo.txt', 'r')
gpu_sum = 0
gpu_count = 0
for line in f1:
  if 'Default' in line:
    line_s = line.split()
    gpu_sum+=int(line_s[12][:-1])
    gpu_count+=1
u_gpu = (gpu_sum/gpu_count)/100
d_gpu = u_gpu/X0
print(u_gpu, d_gpu)


