import os, re, requests, pp

url_list = ['http://www.google.com/', 'http://gizmodo.uol.com.br/',
            'https://github.com/', 'http://br.search.yahoo.com/',
            'http://www.python.org/', 'http://www.python.org/psf/']

result_dict = {}

def aggregate_results(result):
    print "Computing results in main process PID [%d]" % os.getpid()
    message = "PID %d in hostname [%s] the following links were found: %s"\
        % (result[2], result[3], result[1])
    result_dict[result[0]] = message

def crawl_task(url):
    html_link_regex = \
        re.compile('<a\s(?:.*?\s)*?href=[\'"](.*?)[\'"].*?>')
    
    request_data = requests.get(url)
    #limit to the first 03 links
    links = html_link_regex.findall(request_data.text)[:3]
    return (url, links, os.getpid(), os.uname()[1])

ppservers = ("192.168.25.21", "192.168.25.9")
job_dispatcher = pp.Server(ncpus=1, ppservers=ppservers, socket_timeout=60000)
for url in url_list:
    job_dispatcher.submit(crawl_task, (url,),
        modules=('os', 're', 'requests',),
            callback=aggregate_results)
  
job_dispatcher.wait()

print "\nMain process PID [%d]\n" % os.getpid() 
for key, value in result_dict.items():
    print "** For url %s, %s\n" % (key, value)

print job_dispatcher.print_stats()
