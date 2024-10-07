# CP-Ansible

## Non-root cp-ansible deployments

This fork provides some preliminaries for non-root, no sudo deployments. 

this repo is based on: https://github.com/tpham305/nonroot-cp-ansible-7.5.2 and merged with `7.7.1-post`

Added:

* Scripts for Zookeeper deployments

### What works and what does not
What works out of the box:

* Basic setup and configuration of most Confluent Platform components (excluding Confluent Replicator)
* TLS Encryption
* SASL authentication

What should work but is not yet tested:

* Kerberos authentication
* Role-based Access Control (RBAC) (see: https://docs.confluent.io/platform/current/security/rbac/)
    * Refer to the section on [RBAC Setup](#rbac-setup)

What is not supported, or requires additional manual steps:

* Confluent Replicator

### Deployment in non-root environments

Deployment prerequisites are similar to that of regular `cp-ansible`. Please refer to the details to build and install this `ansible-galaxy` collection for an air-gapped environment at https://docs.confluent.io/ansible/current/ansible-airgap.html.

To deploy, use additional tags:

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.all --skip-tags privileged,package,systemd,sysctl,health_check
```

The above will prepare the files on the hosts for all the components.

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.create_service_script
```

The above will create start scripts that can be used to start the components.

To start components:

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.start_script
```

To stop components:

```
ansible-playbook -i hosts_example_nonroot.yml confluent.platform.stop_script
```

### RBAC Setup

The playbook tasks around RBAC require that the Kafka Brokers (specifically, the embedded REST proxy) are running before they can function.

To increase the number of retries around the task "Get Kafka Cluster ID from Embedded Rest Proxy", configure the parameter `mds_retries` in the hosts file.
Alternatively, the user can simply terminate the playbook (`Ctrl + C`), and restart the playbook with `--skip-tags zookeeper`.

High-level steps as follows:

* Create the start scripts for all components first:
    * `ansible-playbook -i hosts_example_nonroot.yml confluent.platform.confluent.platform.create_service_script`
* Run the playbook (see above) to set up Zookeeper, Kafka Brokers
* At the task "Get Kafka Cluster ID from Embedded Rest Proxy":
    * Manually start Zookeepers and Kafka Brokers or use the script:
        * `ansible-playbook -i hosts_example_nonroot.yml confluent.platform.start_script --tags zookeeper,kafka_broker`
* The playbook will continue to the end
* Start the remaining Confluent Platform components:
    * `ansible-playbook -i hosts_example_nonroot.yml confluent.platform.start_script --skip-tags zookeeper,kafka_broker`

## Introduction
## Description

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

## Requirements

Prerequisites for installing CP can be found at https://docs.confluent.io/ansible/current/ansible-requirements.html#general-requirements.


## Installation

You can install this collection from Ansible Automation Hub and Ansible Galaxy by following https://docs.confluent.io/ansible/current/ansible-download.html.

As an alternative to the recommended methods above, you can install the package directly from the source repository.

* Create a directory with the following structure:<br>
```mkdir -p <path_to_cp-ansible>/ansible_collections/confluent/```

  You can put <path_to_cp-ansible> anywhere in your directory structure, but the directory structure under <path_to_cp-ansible> should be set up exactly as specified above.

* Clone the Ansible Playbooks for Confluent Platform repo into the platform directory inside the directory you created in the previous step:<br>
```git clone https://github.com/confluentinc/cp-ansible <path_to_cp-ansible>/ansible_collections/confluent/platform```


## Use Cases

Ansible Playbooks for Confluent Platform (Confluent Ansible) offers a simplified way to configure and deploy Confluent Platform.


## Testing

CP-Ansible's tests use the [Molecule](https://ansible.readthedocs.io/projects/molecule/) framework, and it is strongly advised to test this way before submitting a Pull Request. Please refer to the [HOW_TO_TEST.md](docs/HOW_TO_TEST.md)


## Contributing

If you would like to contribute to the CP-Ansible project, please refer to the [CONTRIBUTE.md](docs/CONTRIBUTING.md)

## Support

For any support request, please reach out to [Confluent Support Portal](https://support.confluent.io/).

## Release Notes

This [page](https://docs.confluent.io/ansible/current/ansible-release-notes.html) summarizes the technical details of the Confluent releases.

## License

[Apache 2.0](LICENSE.md)
