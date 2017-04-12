import paramiko
import time

from monitor.monasca.manager import MonascaMonitor
from monitor.plugins.base import Plugin


class WebAppMonitor(Plugin):

    def __init__(self, app_id, info_plugin, collect_period, keypair, retries=60):
        Plugin.__init__(self, collect_period, retries=retries)
        self.app_id = app_id
        self.host_ip = info_plugin['host_ip']
        self.keypair_path = keypair
        self.host_username = info_plugin['host_username']
        self.log_path = info_plugin['log_path']
        self.dimensions = {}
        self.last_checked = ''
        self.monasca = MonascaMonitor()

    def _get_metric_value(self, log):
        value = None
        for i in range(len(log) - 1, 0, -1):
            if log[i] == '#':
                value = float(log[i + 1:-1])
        return value

    def _get_ssh_connection(self):
        keypair = paramiko.RSAKey.from_private_key_file(self.keypair_path)
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        conn.connect(hostname=self.host_ip, username=self.host_username, pkey=keypair)
        return conn

    def _publish_metrics(self, last_log):
        metric = {}
        print last_log
        # Check if this log line contains a new metric measurement
        if '[Random]' in last_log and self.last_checked != last_log:
            self.last_checked = last_log
            # Add to metric_info values for this measurement:
            # value and timestamp
            value = self._get_metric_value(last_log)
            metric['name'] = 'web_app.random'
            metric['value'] = value
            metric['timestamp'] = time.time() * 1000
            metric['dimensions'] = {"app_id": self.app_id,
                                    "host": self.host_ip}
            # Sending the metric to Monasca
            print value
            self.monasca.send_metrics([metric])
            print "WebApp metric published: %i" % (value)

        # Flag that checks if the log capture is ended
        elif '[END]' in last_log:
            self.running = False

    def monitoring_application(self, dimensions, app_id):
        try:

            conn = self._get_ssh_connection()
            stdin , stdout, stderr = conn.exec_command("sudo tail -1 %s" % self.log_path)
            self._publish_metrics(stdout.read())

            # metric = {}
            # last_log = stdout.read()
            # print last_log
            # # Check if this log line contains a new metric measurement
            # if '[Random]' in last_log and self.last_checked != last_log:
            #     self.last_checked = last_log
            #     # Add to metric_info values for this measurement:
            #     # value and timestamp
            #     value = self._get_metric_value(last_log)
            #     metric['name'] = 'web_app.random'
            #     metric['value'] = value
            #     metric['timestamp'] = time.time() * 1000
            #     metric['dimensions'] = {"app_id": self.app_id,
            #                                  "host": self.host_ip}
            #     # Sending the metric to Monasca
            #     print value
            #     self.monasca.send_metrics([metric])
            #     print "WebApp metric published: %i" % (value)
            #
            # # Flag that checks if the log capture is ended
            # elif '[END]' in last_log:
            #     self.running = False

        except Exception as ex:
            print "Monitoring %s is not possible. \nError: %s. %s remaining attempts" % (self.app_id, ex.message, self.attempts)
            raise ex
