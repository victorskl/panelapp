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
    ```
3. Terraform scripts are configured to use default values. To modify these variables, copy `terraform.tfvars.sample` to `terraform.tfvars` and configure there.

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
