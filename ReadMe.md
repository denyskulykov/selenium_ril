Utils for Dashboard
===================

This util is for testing Horizon and Opening Ilo page for RIL project.

How to start
===================

1) Clone it:
```bash
   # user@your-pc:~/# git clone https://github.com/dkulykovmirantis/selenium_ril.git
```

2) Go to the repo folder:
```bash
   # cd selenium_ril/
```

3) Create virtualenv and install requirements and package:
```bash
   # virtualenv --system-site-packages .venv
   # source .venv/bin/activate
   # pip install -r requirements.txt
```

4) Prepare config:
```bash
   # cp global_config.yaml.exampel global_config.yaml
   # vim global_config.yaml
```

5.1) Start tests (make sure you can open base_url or ilo):
```bash
   # python test_dashboard.py
```

6) Open screenshot:
```bash
   # display test_openstack_dashboard_name_test_data.png
```

5.2) For opening IlO page:

Open first node - start_ip and using param number_of_node
```bash
   # python open_ilo.py number
```
OR

Open pages From start_ip To end_ip
```bash
   # python open_ilo.py range
```
OR

Open only one page - start_ip
```bash
   # python open_ilo.py simple
```

