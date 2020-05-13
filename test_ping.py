import os
def subnet_net(x):
   return  x
result_file_name = "ping.txt"
k = 0
n = 0
i = 0
ip = (subnet_net('172.19.224.'))
for i in range (200,255):
  rezult = ip + str(i)
  response = os.system("ping -n 1 " + rezult)
  if response == 0:
     k += 1
     with open(result_file_name, 'a') as result_file:
         result_file.write(f'success: {rezult} \n')
  else:
      n += 1
      with open(result_file_name, 'a') as result_file:
         result_file.write(f'not_success: {rezult} \n')

with open(result_file_name, 'a') as result_file:
    result_file.write(f'Total success: {k} \n')
with open(result_file_name, 'a') as result_file:
    result_file.write(f'Total not success: {n} \n')