import typing

import crossplane


class NginxService:
    """
    Nginx config builder.
    Example:
        server {
            listen 80;
            server_name 192.0.2.0;

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            }
        }
    """


    @classmethod
    def build(cls, server_name: str, proxy_pass: str):
        config = {}
        server_block = cls._build_block(directive="http", additional_block=True)
        server_block["block"].append(
            cls._build_block(directive="server", additional_block=True)
        )
        server_block["block"][0]["block"].append(
            cls._build_block("80", directive="listen")
        )
        server_block["block"][0]["block"].append(
            cls._build_block(server_name, directive="server_name")
        )
        server_block["block"][0]["block"].append(
            cls._build_block("/", directive="location", additional_block=True)
        )
        server_block["block"][0]["block"][-1]["block"].append(
            cls._build_block(proxy_pass, directive="proxy_pass")
        )
        server_block["block"][0]["block"][-1]["block"].append(
            cls._build_block("Host", "$host", directive="proxy_set_header")
        )
        server_block["block"][0]["block"][-1]["block"].append(
            cls._build_block(
                "X-Forwarded-For",
                "$proxy_add_x_forwarded_for",
                directive="proxy_set_header",
            )
        )
        config.update(server_block)
        return config

    @classmethod
    def parse(cls, config):
        return crossplane.build(config)

    @classmethod
    def _build_block(self, *args, **kwargs):
        _block = {
            "directive": kwargs.get("directive"),
            "args": list(args),
        }
        if kwargs.get("additional_block", False):
            _block.update({"block": []})
        return _block
