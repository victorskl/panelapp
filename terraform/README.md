# Terraform Deployment

This directory contains terraform-driven deployments for PanelApp.

### Prerequisites

1. Create AWS S3 bucket and DynamoDB table for terraform remote state and locking. Refer `backend.conf.sample` for sample backend config.
    - Enable `Versioning` for S3 bucket
    - Use `LockID` as Primary key, String type for DynamoDB table
    - Then, initialize terraform with `-backend-config` flag:
    ```
    cp backend.conf.sample backend.conf
    terraform init -backend-config="backend.conf"
    ```
    
2. Create the following environment specific secret parameters in AWS Parameter Store. If you are planning for more than one environment, replicate more of these parameters with respective environment shorthand variables: `dev`, `staging`, `prod`
    ```
    /panelapp/dev/database/db_name              String
    /panelapp/dev/database/master_password      SecureString
    /panelapp/dev/database/master_username      String
    /panelapp/dev/django/secret_key             SecureString
    /panelapp/dev/email/host                    String
    /panelapp/dev/email/user                    SecureString
    /panelapp/dev/email/password                SecureString
    ```

3. Create AWS Route53 Hosted Zones for `app_domain_name` to be used in deployment. 

4. Terraform scripts are configured to use default values. To modify these variables, copy `terraform.tfvars.sample` to `terraform.tfvars` and configure there.

### SMTP Email

- This can be any SMTP Email provider, e.g. Sendgrid, Mailgun, etc. Tested with Amazon SES.
- Example SMTP Email setting:
    - Goto Amazon SES Console
    - Create My SMTP Credentials
    - Setup parameter store like:
    ```
    /panelapp/dev/email/host        email-smtp.us-east-1.amazonaws.com
    /panelapp/dev/email/user        (generated by AWS)
    /panelapp/dev/email/password    (generated by AWS)
    ```

### Domain Name

- A designated domain name or sub-domain name should be created.
- Then, prepare this designated domain name to be hosted at AWS Route53 Public Hosted Zone.
- Example
    - Goto AWS Route53 Console
    - Hosted zones > Create Hosted Zone > Type: `Public Hosted Zone` > Domain Name: `panelapp.example.com`
- Terraform stack will then auto populate any necessary DNS records (A, CNAME).

### Running Stacks

- Stacks directory contain different kind of deployable PanelApp stacks.
- Each stack can be isolated by deployment environment using terraform workspace. Terraform default workspace map to `dev`. And you can additionally use environments: `staging` and `prod`.
- To create minimal PanelApp stack that run on AWS with minimal resources possible
    ```
    cd terraform/stacks/aws_mini
    terraform init -backend-config="backend.conf"
    terraform plan
    terraform apply
    terraform show
    ```
- And, perform `terraform destroy` to destroy the stack created