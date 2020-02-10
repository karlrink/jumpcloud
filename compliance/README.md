
# Compliance


---
## SOC2
what does SOC 2 require? It’s considered a technical audit, but it goes beyond that: SOC 2 requires companies to establish and follow strict information security policies and procedures, encompassing the security, availability, processing, integrity, and confidentiality of customer data. SOC 2 ensures that a company’s information security measures are in line with the unique parameters of today’s cloud requirements. 

Achieving SOC 2 compliance means you have established a process and practices with required levels of oversight across your organization. Specifically, you are using a process for monitoring unusual system activity, authorized and unauthorized system configuration changes, and user access levels.

The SOC 2 reporting standard is defined by the AICPA (The American Institute of Certified Public Accountants).  All SOC 2 audits are signed by licensed CPAs . To achieve SOC 2 compliance, most companies spend anywhere from six months to a year on focused preparation. This includes identifying which systems are in scope for the audit, developing policies and procedures, and implementing now security controls to reduce risks.  When ready, an organization will hire a licensed CPA audit firm to conduct the audit.

## SOC 2 Type II
An audit conducted against the Trust Service Criteria standard over a period of time.  This period typically covers six months the first time, and then a year thereafter. In other words, this audit answers: Did the security controls that were in place from January 1 through July 31st operate effectively? (Note: SOC 2 audits are generally only considered valid for a year, so you must get into a rhythm of conducting them annually.) This means you’ll need a system of record.

  - A system of record is the authoritative data source for a given type of information
  - The SOC 2 report and Trust Services framework give companies external validation that they are managing risks appropriately

---
Because SOC 2 requires careful controls around your organization and management of employees, it’s a good idea to invest in a human resource information system (HRIS).  These systems track employee onboarding, key paperwork, policies, and other HR workflows.

A key part of security and compliance is documenting your internal processes. This documentation should be a living and breathing part of your organization. Therefore, it needs to be easy to create, edit, share, and navigate. 

Keeping track of controls is an ongoing effort that is typically managed by a CSO or compliance manager. 

Managing SOC 2 compliance requires that a number of annual, semi-annual, quarterly, and monthly controls “fire” on time and are sufficiently documented. 
example, 
Was that quarterly backup and recovery test actually conducted?
What were the results?
Were the results sufficiently documented?

---
### Logical and Physical Access Controls
  - Database Access Management
  - Security Monitoring and Management
  - Single Sign-On and Identity and Access Management
  - Password Management
  - Asset Management
  - Physical Access Controls

System Operations, Change Management

- evidence collected and shared to a Google Drive, accessible to the auditor
- you need to demonstrate that sufficient alerting procedures are in place, 
  so that if any unauthorized access to customer data occurs, you can demonstrate the ability to respond and take corrective action in time.

Specifically, SOC 2 requires companies to set up alerts for any activities that result in unauthorized:

    - Exposure or modification of data, controls, or configurations
    - File transfer activities
    - Privileged filesystem, account, or login access

To ensure that you are meeting SOC 2 requirements, you must receive alerts whenever unauthorized access to customer data occurs.

---

# Detailed Audit Trails
logging, alerts

# Actionable Forensics
host-based monitoring, network monitoring, embeded monitoring

---

choose tools and processes that facilitate compliance from the beginning. remember that people must use these tools and follow your controls.

---
# Incidents and Prevention
Any incident that threatens the security, availability, processing integrity, confidentiality, and/or privacy of customer data in the cloud is a big no-no from the SOC 2 perspective.  SOC 2 is designed to assure your customers that you are monitoring for suspicious activity and are able to take corrective action quickly if an incident takes place. 

# visibility
Prioritize gaining visibility at the host level.  SOC 2 compliance demands granular visibility into user activity, processes, network connections, and more. 

---

SOC 2 Compliance Playbook

---

  - amazon aws outbound email system is ses

---

```
./compliance.py
Usage: ./compliance.py [option]

    options:

        check app_offenses
        check username_policy
        check|send systems_root_ssh
        check|send fde

```



