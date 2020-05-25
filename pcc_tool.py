import csv


class PccTool:
    def __init__(self,configfile):
        self.configfile = configfile
        try:
            with open(self.configfile,'r',encoding='utf-8') as f:
                lines = f.readlines()
                lines = [line.strip() for line in lines]
                lines = [line.split() for line in lines if line]
                self.data = lines
        except Exception as e:
            print(str(e))
            self.data = None

    # filter appliation by charging-group
    @staticmethod
    def _filter_app(d,k):
        values = d.values()
        app = [i for i in values if i.get('chg_group') == k]
        if app:
            return sorted(app,key=lambda x:x.get('application'))
        else:
            return

    # filter entry by application
    @staticmethod
    def _filter_entry(d,k):
        values = d.values()
        entry = [i for i in values if i.get('application') == k]
        if entry:
            return sorted(entry,key=lambda x:int(x.get('entry_id')))
        else:
            return

    # retrieve port by port-list name
    @staticmethod
    def _get_port(d,k):
        p = d.get(k,'')
        if p:
            port = ";".join(p)
            return port
        else:
            return

    @staticmethod
    def _filter_prefix(d,k):
        ip_pre = d.get(k,'')
        if ip_pre:
            return ip_pre
        else:
            return

    def get_hostname(self):
        # 如果不配置名字,使用默认名字VSR
        hostname = 'VSR'
        for line in self.data:
            if line[0] == "name" and len(line) == 2:
                hostname = line[1].strip("\"")
                break
        return hostname

    def get_mg_counter(self):
        # 统计内容:policy-rule-base,policy-rule,policy-rule-unit,charging-rule-unit,stat-rule-unit,sru-list,charging-group,app-group,application,entry
        prb = 0
        prb_list = []
        pr = 0
        pru = 0
        cru = 0
        sru = 0
        srul = 0
        chg = 0
        app_grp = 0
        app = 0
        entry = 0
        index = 0
        for line in self.data:
            if line[0] == "charging-group" and line[-1] == "create":
                chg = chg + 1
            if line[0] == "app-group" and line[-1] == "create":
                app_grp = app_grp + 1
            if line[0] == "application" and line[-1] == "create":
                app = app + 1
            if line[0] == "policy-rule-unit" and len(line) == 2:
                pru = pru + 1
            if line[0] == "charging-rule-unit" and len(line) == 2:
                cru = cru + 1
            if line[0] == "policy-rule" and len(line) >= 8:
                pr = pr + 1
            if line[0] == "stat-rule-unit" and len(line) == 2:
                pre_line = self.data[index-1]
                if pre_line[0] != "sru-list":
                    sru = sru + 1
            if line[0] == "sru-list" and len(line) == 2:
                srul = srul + 1
            if line[0] == "policy-rule-base" and len(line) == 2:
                prb_list.append(line[1].strip("\""))
            if line[0] == "entry" and len(line) == 3 and line[-1] == "create":
                next_line = self.data[index + 1]
                next_line2 = self.data[index + 2]
                if (next_line[0] != "match" and next_line[0] != "action") and (next_line2[0] != "match" and next_line2[0] != "action"):
                    entry = entry + 1
            index = index + 1

        prb = len(set(prb_list))
        return prb,pr,pru,cru,sru,srul,chg,app_grp,app,entry

    def output_free_entry(self, f_out):
        index = 0
        entry_list = []
        free_entry = []
        for line in self.data:
            if line[0] == "entry" and len(line) == 3 and line[2] == "create":
                next_line = self.data[index + 1]
                next_line2 = self.data[index + 2]
                if (next_line[0] != "match" and next_line[0] != "action") and (next_line2[0] != "match" and next_line2[0] != "action"):
                    entry_list.append(int(line[1]))
            index = index + 1

        for i in range(1, 65536):
            if i not in entry_list:
                free_entry.append(i)

        free_entry.sort()

        with open(f_out, 'w',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            header = ["Free Entry Id"]
            writer.writerow(header)
            for item in free_entry:
                writer.writerow([item])



    def get_app(self):
        # 获取applicaion信息,其中app-group为非必须关联项
        # 输出格式为{'APP_blbl_3GNET':{'application':'APP_blbl_3GNET','app_group':'default-app-group','chg_group':'CHG_blbl_3GNET'}}
        app_dict = {}
        keys = ['application','app_group','chg_group']
        flag = False
        for line in self.data:
            if line[0] == "application" and line[-1] == "create":
                app_name = line[1].strip("\"")
                app_item = {}.fromkeys(keys,'')
                app_item['application'] = app_name
                flag = True
            if flag and line[0] == "app-group":
                # 需要考虑app-group命名包含空格的情况
                if len(line) == 2:
                    app_item['app_group'] = line[1].strip("\"")
                if len(line) > 2:
                    app_item['app_group'] = ' '.join(line[1:]).strip("\"")
            if flag and line[0] == "charging-group" and len(line) == 2:
                app_item['chg_group'] = line[1].strip("\"")
            if flag and line[0] == "exit":
                app_dict.setdefault(app_name,app_item)
        return app_dict

    def get_cru(self):
        # cru: charging-rule-unit,只需要在SMF上配置,UPF不需要配置
        # sru,rele为可选配置
        # 输出格式: {'CRU_LL800DX1':{'rg':'1291846181','sru':'SRU_ll800dx1_L34_01','sid':'1291846181','rele':'service-id'}}
        cru_dict = {}
        flag = False
        keys = ['rg','sru','sid','rele']
        for line in self.data:
            if line[0] == "charging-rule-unit" and len(line) == 2:
                cru_name = line[1].strip("\"")
                cru_item = {}.fromkeys(keys,'')
                flag = True
            if flag and line[0] == "rating-group":
                # rating-group为必选配置
                cru_item['rg'] = line[1]
                # sru可选,当len(line)>2时,说明配置了sru
                if len(line) > 2:
                    cru_item['sru'] = line[3].strip("\"")
            if flag and line[0] == "service-identifier" and len(line) == 2:
                cru_item['sid'] = line[1]
            if flag and line[0] == "reporting-level" and len(line) == 2:
                cru_item['rele'] = line[1]
            if flag and line[0] == "exit":
                cru_dict.setdefault(cru_name,cru_item)
                flag = False
        return cru_dict

    def get_pr(self):
        # smf:pru,cru,qci,arp,precedence必选,qru,aru,tru可选
        # upf:pru,srul,precedence必选,qci,arp,qru,aru,tru可选
        # 对smf和upf来说,都必须有的是pru,precedence
        # 输出格式:{'PR_HTZQ_L34_01':{'pru':'PRU_HTZQ_L34_01','cru':'CRU_HTZQ','qci':'*','arp':'*' ...}}
        pr_dict = {}
        keys = ['pru','cru','qci','arp','pre','srul','qru','aru','tru']
        for line in self.data:
            if line[0] == "policy-rule" and len(line) >= 6:
                pr_name = line[line.index('policy-rule')+1].strip("\"")
                pr_item = {}.fromkeys(keys,'')
                pru = line[line.index('policy-rule-unit')+1].strip("\"")
                pre = line[line.index('precedence')+1]
                pr_item['pru'] = pru
                pr_item['pre'] = pre
                try:
                    pr_item['cru'] = line[line.index('charging-rule-unit')+1].strip("\"")
                except ValueError:
                    pass
                try:
                    pr_item['qci'] = line[line.index('qci')+1]
                except ValueError:
                    pass
                try:
                    pr_item['arp'] = line[line.index('arp')+1]
                except ValueError:
                    pass
                try:
                    pr_item['srul'] = line[line.index('stat-rule-unit-list')+1].strip("\"")
                except ValueError:
                    pass
                try:
                    pr_item['qru'] = line[line.index('qos-rule-unit')+1].strip("\"")
                except ValueError:
                    pass
                try:
                    pr_item['aru'] = line[line.index('action-rule-unit')+1].strip("\"")
                except ValueError:
                    pass
                try:
                    pr_item['tru'] = line[line.index('trigger-rule-unit')+1].strip("\"")
                except ValueError:
                    pass
                pr_dict.setdefault(pr_name,pr_item)
        return pr_dict

    def get_ip_prefix(self):
        # 目前配置未使用,后续商用会启用ip-prefix-list
        # 输出格式:{'IPL_pptv_00':['111.0.93.19/32','111.0.93.20/30'...]}
        # 该函数输出的ip-prefix-list可能会包含空的ip-prefix-list
        ip_prefix_dict = {}
        flag = False
        for line in self.data:
            if line[0] == "ip-prefix-list" and line[-1] == "create" and len(line) == 3:
                ip_prefix = line[1].strip("\"")
                if ip_prefix.startswith("IPL_"):
                    flag = True
                    prefix = []
            if flag and line[0] == "prefix" and len(line) == 2:
                prefix.append(line[1])
            if flag and line[0] == "exit" and prefix:
                ip_prefix_dict.setdefault(ip_prefix,prefix)
                flag = False
        return ip_prefix_dict

    def get_pru(self):
        # flow-description字段:remote-ip,protocol,remote-port,aa-charging-group 其中remote-port可以是eq一个特定的端口,也可以是range范围
        # pdr-id可选配置,有些PRU没有手动配置
        # 输出格式: {'PRU_GFZQ_L34_01': {
        #     'pdr-id':'1028',
        #     'fd_list': [
        #     {'fd':'1','remote-ip':'219.159.38.207/32','protocol':'','remote-port':'','aa-charging-group':''},
        #     {'fd':'2','remote-ip':'101.230.213.101/32','protocol':'6','remote-port':'3292','aa-charging-group':''},
        #     ...
        #     ]
        # }
        # }
        pru_dict = {}
        pru_flag = False
        fd_flag = False
        keys = ['fd','remote-ip','protocol','remote-port','aa-charging-group']
        for line in self.data:
            if line[0] == "policy-rule-unit" and len(line) == 2:
                pru_flag = True
                pru = line[1].strip("\"")
                fd_list = []
                pdr_id = ''
            if pru_flag and line[0] == "pdr-id" and len(line) == 2:
                pdr_id = line[1]
            if pru_flag and line[0] == "flow-description" and len(line) == 2:
                fd_item = {}.fromkeys(keys,'')
                fd_item['fd'] = line[1]
                fd_flag = True
            if pru_flag and fd_flag and line[0] == "remote-ip":
                fd_item['remote-ip'] = line[1]
            if pru_flag and fd_flag and line[0] == "protocol":
                fd_item['protocol'] = line[1]
            if pru_flag and fd_flag and line[0] == "aa-charging-group":
                fd_item['aa-charging-group'] = line[1].strip("\"")
            if pru_flag and fd_flag and line[0] == "remote-port":
                if line[1] == "range" and len(line) == 4:
                    fd_item['remote-port'] = line[2] + "_" + line[3]
                if line[1] == "eq" and len(line) == 3:
                    fd_item['remote-port'] = line[2]
            if pru_flag and fd_flag and line[0] == "exit":
                fd_flag = False
                fd_list.append(fd_item)
            if pru_flag and not fd_flag:
                pru_dict.setdefault(pru,{})['pdr_id'] = pdr_id
                pru_dict.setdefault(pru,{})['fd_list'] = fd_list
        return pru_dict

    def get_sru(self):
        # 输出格式: {'SRU_wsd_3GNET_02_L34_01':{'urr_id':'1196','urr_profile':'default-urr-profile'}}
        sru_dict = {}
        flag = False
        keys = ['urr_id','urr_profile']
        for line in self.data:
            if line[0] == "stat-rule-unit" and len(line) == 2:
                sru = line[1].strip("\"")
                sru_item = {}.fromkeys(keys,'')
                flag = True
            if flag and line[0] == "urr-id" and len(line) == 4:
                sru_item['urr_id'] = line[1]
                sru_item['urr_profile'] = line[3].strip("\"")
            if flag and line[0] == "exit":
                sru_dict.setdefault(sru,sru_item)
        return sru_dict

    def get_port_list(self):
        # 输出示例:{'PL_nmeedsga_05': ['52060-52062', '52064', '52066'], 'PL_tcp_pcc_r_01': ['80', '8080', '9200', '9201'], 'PL_ydcy_01': ['80', '443']}
        port_dict = {}
        flag = False
        for line in self.data:
            if line[0] == "port-list" and line[-1] == "create":
                pl_name = line[1].strip("\"")
                pl = []
                flag = True
            if flag and line[0] == "port" and line[1] == "range" and len(line) == 4:
                pl.append(line[2] + "-" + line[3])
            if flag and line[0] == "port" and len(line) == 2 and line[1].isdigit():
                pl.append(line[1])
            if flag and line[0] == "exit":
                port_dict.setdefault(pl_name,pl)
                flag = False
        return port_dict

    def get_dns_cache(self):
        # 示例输出: {'white-list':['*.3g.wxcs.cn','*.caiyun.feixin.10086.cn'...]}
        dns_cache_dict = {}
        flag = False
        for line in self.data:
            if line[0] == "dns-ip-cache" and line[-1] == "create":
                dns_cache = line[1].strip("\"")
                cache_list = []
                flag = True
            if flag and line[0] == "domain" and line[2] == "expression":
                cache = line[3].strip("\"").lstrip("^").rstrip("$")
                cache_list.append(cache)
            if flag and line[0] == "exit":
                dns_cache_dict.setdefault(dns_cache,cache_list)
                flag = False
        return dns_cache_dict

    def get_sru_list(self):
        # upf配置了sru_list,关联sru
        # 输出格式: {'zsxb_L7_01':{'sru':'SRU_zsxb_L7_01'}}
        srul_dict = {}
        flag = False
        for line in self.data:
            if line[0] == "sru-list" and len(line) == 2:
                srul = line[1].strip("\"")
                sru_item = {}.fromkeys(['sru'],'')
                flag = True
            if flag and line[0] == "stat-rule-unit" and len(line) == 2:
                sru_item['sru'] = line[1].strip("\"")
            if flag and line[0] == "exit":
                srul_dict.setdefault(srul,sru_item)
                flag = False
        return srul_dict


    def get_entry(self):
        entry_dict = {}
        index = 0
        flag = False
        keys = ['http-host', 'http-uri', 'application', 'ip-prefix-list', 'server-address', 'server-port','http-port', 'ip-protocol-num', 'protocol-aa', 'http-user-agent', 'tls-cert-subj-common-name','http-referer', 'status']
        for line in self.data:
            if line[0] == "entry" and line[-1] == "create":
                next_line = self.data[index+1]
                next_line2 = self.data[index+2]
                if (next_line[0] != "match" and next_line[0] != "action") and (next_line2[0] != "match" and next_line2[0] != "action"):
                    entry_id = line[1]
                    entry_item = {}.fromkeys(keys,'')
                    entry_item['entry_id'] = entry_id
                    flag = True
            if flag and line[0] == "expression" and line[2] == "http-host" and len(line) == 5:
                entry_item['http-host'] = line[4].strip("\"").lstrip("^").rstrip("$")
            if flag and line[0] == "expression" and line[2] == "http-uri" and len(line) == 5:
                entry_item['http-uri'] = line[4].strip("\"")
            if flag and line[0] == "application" and len(line) == 2:
                entry_item['application'] = line[1].strip("\"")
            if flag and line[0] == "http-port" and len(line) == 3:
                entry_item['http-port'] = line[2]
            if flag and line[0] == "ip-protocol-num" and line[1] == "eq" and len(line) == 3:
                entry_item['ip-protocol-num'] = line[2]
            if flag and line[0] == "server-address" and line[1] == "eq":
                if line[2] == "ip-prefix-list":
                    entry_item['ip-prefix-list'] = line[3].strip("\"")
                    entry_item['server-address'] = line[3].strip("\"")
                elif line[2] == "dns-ip-cache":
                    entry_item['server-address'] = line[3].strip("\"")
                else:
                    entry_item['server-address'] = line[2]
            if flag and line[0] == "server-port" and line[1] == "eq":
                if len(line) == 3:
                    entry_item['server-port'] = line[2]
                if line[2] == "range" and len(line) == 5:
                    entry_item['server-port'] = line[3] + "-" + line[4]
                if line[2] == "port-list" and len(line) == 4:
                    entry_item['server-port'] = line[3].strip("\"")
            if flag and line[0] == "protocol" and line[1] == "eq" and len(line) == 3:
                entry_item['protocol-aa'] = line[2].strip("\"")
            if flag and line[0] == "expression" and line[2] == "http-user-agent":
                entry_item['http-user-agent'] = line[4].strip("\"")
            if flag and line[0] == "expression" and line[2] == "tls-cert-subj-common-name":
                entry_item['tls-cert-subj-common-name'] = line[4].strip("\"").lstrip("^").rstrip("$")
            if flag and line[0] == "expression" and line[2] == "http-referer":
                entry_item['http-referer'] = line[4].strip("\"")
            if flag and 'shutdown' in line:
                if len(line) == 1:
                    entry_item['status'] = "shutdown"
                if len(line) == 2:
                    entry_item['status'] = "no shutdown"
            if flag and line[0] == "exit":
                entry_dict.setdefault(entry_id,entry_item)
                flag = False
            index = index + 1
        return entry_dict


    def output_all_config(self,f_out):
        pr_dict = self.get_pr()
        # smf配置cru,upf不配置cru,所以upf返回的cru_dict为{}
        cru_dict = self.get_cru()
        # sru-list只有upf配置,smf不配置
        srul_dict = self.get_sru_list()
        app_dict = self.get_app()
        pru_dict = self.get_pru()
        entry_dict = self.get_entry()
        port_dict = self.get_port_list()
        ip_prefix_dict = self.get_ip_prefix()
        sru_dict = self.get_sru()
        headers = [
            'policy-rule',
            'precedence',
            'qci',
            'arp',
            'stat-rule-unit-list',
            'qos-rule-unit',
            'action-rule-unit',
            'trigger-rule-unit',
            'rating-group',
            'service-id',
            'reporting-level',
            'stat-rule-unit',
            'urr-id',
            'policy-rule-unit',
            'pdr-id',
            'flow-description',
            'remote-ip',
            'protocol',
            'remote-port',
            'aa-charging-group',
            'entry',
            'application',
            'app-group',
            'http-host',
            'http-uri',
            'ip-prefix-list',
            'server-address',
            'server-port',
            'http-port',
            'ip-protocol-num',
            'protocol-aa',
            'http-user-agent',
            'tls-cert-subj-common-name',
            'http-referer',
            'status'
        ]
        with open(f_out,'w',encoding='utf-8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            pr_all = sorted(pr_dict.keys())
            for pr in pr_all:
                precedence = pr_dict.get(pr).get('pre')
                qci = pr_dict.get(pr).get('qci')
                arp = pr_dict.get(pr).get('arp')
                # srul只有upf配置
                srul = pr_dict.get(pr).get('srul')
                qru = pr_dict.get(pr).get('qru')
                aru = pr_dict.get(pr).get('aru')
                tru = pr_dict.get(pr).get('tru')
                pru = pr_dict.get(pr).get('pru')
                # cru只有smf配置
                cru = pr_dict.get(pr).get('cru')
                # print(cru)
                # print(cru_dict)
                # cru非空,说明是smf,根据cru拿到sru,但是cru中的sru是非必须项
                if cru:
                    rg = cru_dict.get(cru).get('rg','')
                    sid = cru_dict.get(cru).get('sid','')
                    rele = cru_dict.get(cru).get('rele','')
                    sru = cru_dict.get(cru).get('sru','')
                    if sru:
                        urr_id = sru_dict.get(sru).get('urr_id')
                    else:
                        urr_id = ''
                # srul非空,说明是upf,根据srul拿到sru
                if srul:
                    rg,sid,rele = ('','','')
                    sru = srul_dict.get(srul).get('sru')
                    urr_id = sru_dict.get(sru).get('urr_id')

                pdr_id = pru_dict.get(pru).get('pdr_id')
                fds = sorted(pru_dict.get(pru).get('fd_list'),key=lambda x:int(x.get('fd')))
                for fd in fds:
                    fd_id = fd.get('fd','')
                    remote_ip = fd.get('remote-ip','')
                    protocol = fd.get('protocol','')
                    remote_port = fd.get('remote-port','')
                    aa_chg_group = fd.get('aa-charging-group','')
                    # aa_chg_group为空,为三层规则,可以直接写入文件
                    if not aa_chg_group:
                        item = [pr,precedence,qci,arp,srul,qru,aru,tru,rg,sid,rele,sru,urr_id,pru,pdr_id,fd_id,remote_ip,protocol,remote_port,aa_chg_group]
                        writer.writerow(item)
                    else:
                        app_list = self._filter_app(app_dict,aa_chg_group)
                        if app_list:
                            for app in app_list:
                                application = app.get('application','')
                                app_group = app.get('app_group','')
                                entry_list = self._filter_entry(entry_dict,application)
                                if entry_list:
                                    for entry in entry_list:
                                        # print(entry)
                                        entry_id = entry.get('entry_id','')
                                        http_host = entry.get('http-port','')
                                        http_uri = entry.get('http-uri','')
                                        prefix = entry.get('ip-prefix-list','')
                                        server_address = entry.get('server-address','')
                                        server_port = entry.get('server-port','')
                                        http_port = entry.get('http-port','')
                                        ip_protocol_num = entry.get('ip-protocol-num','')
                                        protocol_aa = entry.get('protocol-aa','')
                                        http_user_agent = entry.get('http-user-agent','')
                                        tls_name = entry.get('tls-cert-subj-common-name','')
                                        http_refer = entry.get('http-referer','')
                                        status = entry.get('status','')
                                        if server_port in port_dict.keys():
                                            server_port = self._get_port(port_dict,server_port)
                                        if server_address in ip_prefix_dict.keys():
                                            ip_prefix_list = self._filter_prefix(ip_prefix_dict,server_address)
                                            for ip_prefix in ip_prefix_list:
                                                server_address = ip_prefix
                                                item = [pr,precedence,qci,arp,srul,qru,aru,tru,rg,sid,rele,sru,urr_id,pru,pdr_id,fd_id,remote_ip,protocol,remote_port,aa_chg_group,entry_id, application, app_group, http_host, http_uri, prefix,server_address, server_port, http_port, ip_protocol_num,protocol_aa, http_user_agent, tls_name, http_refer, status]
                                                writer.writerow(item)
                                        else:
                                            item = [pr,precedence,qci,arp,srul,qru,aru,tru,rg,sid,rele,sru,urr_id,pru,pdr_id,fd_id,remote_ip,protocol,remote_port,aa_chg_group,entry_id, application, app_group, http_host, http_uri, prefix,server_address, server_port, http_port, ip_protocol_num,protocol_aa, http_user_agent, tls_name, http_refer, status]
                                            writer.writerow(item)


    @staticmethod
    def get_diff_items(lst1,lst2):
        set1 = set(lst1)
        set2 = set(lst2)
        res = set1 ^ set2
        if res:
            return list(res)
        else:
            return

    def get_invalid_app(self):
        # 查找无效的application,查找方法如下:
        # 1.首先获取配置的所有application (get_app)
        # 2.获取所有的entry,并过滤entry中所有引用的application
        # 3.比较两个列表中的不同项,即为已配置但未关联的application,视为垃圾数据
        app_dict = self.get_app()
        entry_dict = self.get_entry()
        app_list = [r.get('application') for r in app_dict.values()]
        valid_app_list = set([r.get('application') for r in entry_dict.values()])
        res = self.get_diff_items(app_list,valid_app_list)
        if res:
            return res
        else:
            return

    def get_aa_chg_list(self):
        aa_chg_list = []
        for line in self.data:
            if line[0] == "charging-group" and len(line) == 3 and line[-1] == "create":
                aa_chg_list.append(line[1].strip("\""))
        return aa_chg_list

    def get_invalid_chg(self):
        # 查找没有关联application的charging-group,查找方法如下：
        # 1.获取所有配置的application，并提取charging-group(有效的charing-group)
        # 2.获取所有已配置的charging-group(配置的charging-group)
        # 3.取两个列表的差异项,即为无效的charging-group
        app_dict = self.get_app()
        aa_chg_list = self.get_aa_chg_list()
        valid_chg_list = [r.get('chg_group') for r in app_dict.values()]
        res = self.get_diff_items(aa_chg_list,valid_chg_list)
        if res:
            return res
        else:
            return

    @staticmethod
    def get_dup_items(lst):
        # 获取列表中的重复项
        res = []
        uniq_lst = list(set(lst))
        for item in uniq_lst:
            num = lst.count(item)
            if num > 1:
                res.append((item,num))
        return res

    def check_duplicate_cache(self):
        res = {}
        dns_cache_dict = self.get_dns_cache()
        for cache in dns_cache_dict:
            items = dns_cache_dict.get(cache)
            rr = self.get_dup_items(items)
            res.setdefault(cache,rr)
        return res














# log1 = "HA_ZZSMF01_NK.cfg"
# log2 = "HA_ZZUPF02_NK.cfg"
# log3 = "luysaegw32bnk_20200521.cfg"
# smf = PccTool(log1)
# upf = PccTool(log2)
# cmg = PccTool(log3)
# # print(smf.get_hostname())
# # print(upf.get_hostname())
#
# chg1 = smf.get_aa_chg_list()
# print(chg1)
# chg2 = upf.get_aa_chg_list()
# print(chg2)



# app1 = smf.get_app()
# # print(app1)
# # print(smf.filter_app(app1,'cg_ME_APP1'))
# app2 = upf.get_app()
# # print(len(app2))
# # for k,v in app2.items():
# #     print(k,v)
# print(upf.filter_app(app2,'CHG_zhgd_3GNET'))

# cru_dict = smf.get_cru()
# for k,v in cru_dict.items():
#     print(k,v)



# cru2 = upf.get_cru()
# print(cru2)
#
# pr1 = smf.get_pr()
# print(pr1.keys())
# print(sorted(pr1.keys()))
# for k,v in pr1.items():
#     print(k,v)
# pr2 = upf.get_pr()
# for k,v in pr2.items():
#     print(k,v)

# ip_prefix_dict = cmg.get_ip_prefix()
# for k,v in ip_prefix_dict.items():
#     print(k,v)

# pru_dict = smf.get_pru()
# print(len(pru_dict))
# for k,v in pru_dict.items():
#     print(k,v)
# print(pru_dict['pru1'])
# print(pru_dict['pru2'])
# fds = sorted(pru_dict.get('PRU_aqy_L34_03').get('fd_list'),key=lambda x:int(x.get('fd')))
# for fd in fds:
#     print(fd)

# print(pru_dict['PRU_wx_L7_01'])

# upf_pru = upf.get_pru()
# print(len(upf_pru))
# print(upf_pru['pru1'])
# print(upf_pru['pru2'])
# print(upf_pru['PRU_volteut'])
# print(upf_pru['PRU_wx_L7_01'])

# sru_smf = smf.get_sru()
# for k,v in sru_smf.items():
#     print(k,v)
# sru_upf = upf.get_sru()
# for k,v in sru_upf.items():
#     print(k,v)

# srul_smf = smf.get_sru_list()
# print(srul_smf)
# srul_upf = upf.get_sru_list()
# print(srul_upf)

# upf_entry = upf.get_entry()
# print(len(upf_entry))
# for k,v in upf_entry.items():
#     print(k,v)

# smf_entry = smf.get_entry()
# print(smf_entry)

# port_dict = cmg.get_port_list()
# print(port_dict)

# dns_cache = cmg.get_dns_cache()
# for k,v in dns_cache.items():
#     print(k,v)

# smf.output_all_config('smf.csv')
# upf.output_all_config('upf.csv')