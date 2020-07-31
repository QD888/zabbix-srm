# Zabbix TEMPLATE SRM
## Abstract
Get events from Dell EMC Storage Resource Manager (SRM) with external python script 

External script call SRM api

Based on [ViPR SRM REST API Documentation][1]

No Metrics ares traited, [ZABBIX][2] just inform on SRM events

# Install process

1. git clone the repo
2. put request_srm.py in /usr/src/zabbix/external directory on zabbix server or/and zebbix proxy server
3. Import zbx_export_template_srm.xml on you zabbix server
4. If not exist, create you ViPR SRM front end as host on zabbix (no agent needed, just fqdn and ip )
5. Add 'Template SRM - REST' on you ViPR SRM front end host 
6. Set Macro value on you host

# Macros:

Template use some Macro:
* {$SRM.PASSWORD}: SRM Password
* {$SRM.USERNAME}: SRM Account
* {$SRM.PORT}: Vip SRM Tcp port ( default 58443)
* {$SRM.SCHEME}: I think this macro is not really util ;-) (default https )


[1]: https://support.emc.com/docu86230_ViPR-SRM-4.x-REST-API:-A-Technical-Overview.pdf?language=en_US&request=akamai 
[2]: https://www.zabbix.com/


 Notes; Acces SRM documentation need DELL/EMC accoun 
La reponse est zabbix!