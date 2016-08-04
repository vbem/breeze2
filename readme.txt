Module:   Breeze Adapter Server

edit adapter module file (MUST be UTF-8 encoded):
    $ vi adapter.py
    
to check breeze server status:
    $ netstat -lanp | fgrep --color=auto python
    
to start breeze server:
    $ nohup python breeze_server.py &> breeze_server.log &
