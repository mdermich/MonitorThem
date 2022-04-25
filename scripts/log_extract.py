import apache_log_parser
import paramiko

class log_tool:
    def __init__(self):
        pass

    def sshcmd(self,command,client):
        _, stdout, stderr = client.exec_command(command)
        output = stdout.read().decode("utf-8")
        return output

    def log_parsing(self,log_line):
        line_parser = apache_log_parser.make_parser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"")
        log_line_data=line_parser(log_line)
        return log_line_data

    def initlastlog(self,fichier_log,client):
        last_log=self.sshcmd("tail -1 /var/log/apache2/"+fichier_log,client)
        parsed_last_log=self.log_parsing(last_log)
        return parsed_last_log

    def getCpuUsage(self,client):
        CpuUsage=self.sshcmd("cat /proc/stat |grep cpu |tail -1|awk '{print ($5*100)/($2+$3+$4+$5+$6+$7+$8+$9+$10)}'|awk '{print 100-$1}'",client)
        return CpuUsage

    def getMemUsed(self,client):
        MemUsed=self.sshcmd("free | grep Mem| awk '{ print $3/$2 *100.0}' ",client)
        return MemUsed

    def getError(self, log_response_code):
        error=0
        if log_response_code>'399' and log_response_code<'600':
            error=1
        return error

    def getCPUinfo(self,client):
        machine_info=self.sshcmd("lscpu",client)
        return machine_info

    def getIPlist(self, machine_name,fichier_log,current_log_data,ip_list):
        if (fichier_log=="access.log"):
            if current_log_data['remote_host'] not in ip_list:
                ip_list.append(current_log_data['remote_host'])
        if (fichier_log=="other_vhosts_access.log"):
            if current_log_data['remote_logname'] not in ip_list:
                ip_list.append(current_log_data['remote_logname'])



    def initpageLists(self,current_log_data,diff_page_list,count_page_list):
        log_page=current_log_data['request_first_line']
        if log_page in diff_page_list:
            count_page_list.append(log_page)
        if log_page not in diff_page_list:
            diff_page_list.append(log_page)
            count_page_list.append(log_page)

    def getPageLists(self,count_page_list,diff_page_list):
        page_list=[0]*(len(diff_page_list))
        for i in range (0,len(diff_page_list)):
            c=0
            for j in range (0,len(count_page_list)):
                if count_page_list[j]==diff_page_list[i]:
                    c+=1
            page_list[i]=[diff_page_list[i],c]
        return page_list

    def getResponseTime(self,machine_name,n,response_time,client):
        responseN=self.sshcmd("cat /var/log/apache2/responsetime.log | tail -"+str(n)+" | awk 'NR=="+str(1)+"{print $11}'",client)
        response_time.append(int(responseN))
#        return response_time





