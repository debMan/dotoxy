from os import path, getenv
import yaml


class Config:

    """
    A simple handler for configurations. The methods of this are used to handle
    config properties used to configure dotoxy
    """

    def __init__(self, config_file="config.yml"):
        """
        :type config_file: str
        :arg config_file:
            Containing the file path to config file
        """
        # Default values
        upstream = {
            "host": "1.1.1.1",
            "port": 853,
            "cn": "cloudflare-dns.com",
            "ca-file": None,
        }
        server = {
            "mode": "tcp",
            "bind-address": "0.0.0.0",
            "bind-port": 53,
        }

        # The configuration is set in a yml file.
        dirname = path.dirname(path.abspath(__file__))
        absolute_path = str(dirname + "/" + config_file)
        self.config_file = getenv("CONFIG_ADDRESS", absolute_path)
        with open(self.config_file, "r") as ymlfile:
            config = yaml.safe_load(ymlfile)
        upstream_configfile = config.get("upstream", {})
        if upstream_configfile is None:
            upstream_configfile = {}
        server_configfile = config.get("server", {})
        if server_configfile is None:
            server_configfile = {}

        # Merge config file and default configs
        upstream.update(upstream_configfile)
        server.update(server_configfile)

        # The configuration is set in environment variables
        upstream_envs = {
            "host": getenv("UPSTREAM__HOST", upstream['host']),
            "port": getenv("UPSTREAM__PORT", upstream['port']),
            "cn": getenv("UPSTREAM__CN", upstream['cn']),
            "ca-file": getenv("UPSTREAM__CA_FILE", upstream['ca-file']),
        }
        server_envs = {
            "mode": getenv("SERVER__MODE", server['mode']),
            "bind-address": getenv(
                "SERVER__BIND_ADDRESS", server['bind-address']
            ),
            "bind-port": getenv("SERVER__BIND_PORT", server['bind-port']),
        }

        # Merge all configs
        upstream.update(upstream_envs)
        server.update(server_envs)

        self.upstream = upstream
        self.server = server
