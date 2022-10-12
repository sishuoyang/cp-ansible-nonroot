
# CP-Ansible

## Non-root cp-ansible deployments

This fork provides some preliminaries for non-root, no sudo deployments. 

### What works and what does not
What works:

* Basic setup and configuration of most Confluent Platform components (excluding Confluent Replicator)
* TLS Encryption
* SASL authentication

What is not supported, or requires additional manual steps:

* Role-based Access Control
* Confluent Replicator

What should work but is not yet tested:

* Kerberos authentication

### Deployment in non-root environments

Deployment prerequisites are similar to that of regular `cp-ansible`. Please refer to the details to build and install this `ansible-galaxy` collection for an air-gapped environment at https://docs.confluent.io/ansible/current/ansible-airgap.html.

To deploy, use additional tags:

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.all --skip-tags privileged,package,systemd,sysctl,health_check
```

The above will prepare the files on the hosts and create start scripts that can be used to start the components.

To start components:

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.start_components_script
```

## Introduction

Ansible provides a simple way to deploy, manage, and configure the Confluent Platform services. This repository provides playbooks and templates to easily spin up a Confluent Platform installation. Specifically this repository:

* Installs Confluent Platform packages or archive.
* Starts services using systemd scripts.
* Provides configuration options for many security options including encryption, authentication, and authorization.

The services that can be installed from this repository are:

* ZooKeeper
* Kafka
* Schema Registry
* REST Proxy
* Confluent Control Center
* Kafka Connect (distributed mode)
* KSQL Server
* Replicator

## Documentation

You can find the documentation for running CP-Ansible at https://docs.confluent.io/current/installation/cp-ansible/index.html.

You can find supported configuration variables in [VARIABLES.md](docs/VARIABLES.md)

## Contributing


If you would like to contribute to the CP-Ansible project, please refer to the [CONTRIBUTE.md](docs/CONTRIBUTING.md)


## License

[Apache 2.0](docs/LICENSE.md)
