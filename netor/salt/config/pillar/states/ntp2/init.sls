ntp_servers_recipe:
  netconfig.managed:
    - template_name: salt://ntp2/templates/ntp.jinja
    - servers: {{ salt.pillar.get('ntp.servers') | json }}
