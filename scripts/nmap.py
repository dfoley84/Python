import subprocess

def ports_open(ip_addr):
  p = subprocess.Popen(['nmap','-Pn'], stdout=subprocess.PIPE)
  output, err = p.communicate()
  print(output)
  
  

 
