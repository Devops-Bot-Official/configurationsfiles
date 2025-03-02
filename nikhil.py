class CodeEditor(QPlainTextEdit):
    """Custom editor widget with line numbers and syntax highlighting."""
 
    def __init__(self, file_path=None, content="", parent=None):
        super().__init__(parent)
        self.setPlainText(content)
        self.line_number_area = LineNumberArea(self)  # ✅ Fix: Now correctly initialized
        self.file_path = file_path
        self.setPlaceholderText("Start typing your screenplay...")
 
        # ✅ Enable syntax highlighting
        file_type = os.path.splitext(file_path)[1].lower() if file_path else ""
        self.highlighter = SyntaxHighlighter(self.document(), file_type)
 
        # ✅ Enable syntax highlighting
        self.highlighter = ScreenplayHighlighter(self.document())
 
        # ✅ Connect key press events for auto-completion
        self.textChanged.connect(self.handle_auto_completion)
        # ✅ Connect changes to update line numbers
        self.textChanged.connect(self.update_line_number_area)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
 
        self.update_line_number_area_width()
 
    def handle_auto_completion(self):
        """Detects predefined keywords and auto-fills content."""
        text = self.toPlainText()

        if text.endswith("# ec2") or text.endswith("// ec2"):
            # ✅ Auto-fill EC2 instance template
            ec2_template = """resources:
  ec2_instances:
    - name: "MyEC2Instance"
      region: "us-east-1"
      instance_type: "t3.micro"  # Replace with desired instance type
      ami_id: "ami-0123456789abcdef0"  # Replace with actual AMI ID
      key_name: "my-key-pair"  # Replace with your SSH key pair name
      security_group: "sg-abcdefgh"  # Replace with your security group ID
      count: 2  # Number of instances to create
      user_data: |
        #!/bin/bash
        echo "Hello, World!" > /var/www/html/index.html
      tags:
        Name: "MyEC2Instance"
        Environment: "Production"
"""
            self.insertPlainText("\n" + ec2_template)  # ✅ Insert template

        elif text.endswith("# user") or text.endswith("// user"):
            # ✅ Auto-fill user template
            user_template = """resources:
  users:
    - identifier: "server-01"
      username: "testuser"
      password: "securepassword123"  # Optional, can be generated if not provided
      permissions: "sudo"  # Optional user group assignment
      create_user_ssh_key: true  # Whether to generate an SSH key for the user
      category: "production"  # Optional, specify category for host lookup
"""
            self.insertPlainText("\n" + user_template)  # ✅ Insert template

        elif text.endswith("# dynamodb") or text.endswith("// dynamodb"):
            # ✅ Auto-fill DynamoDB table template
            dynamodb_template = """resources:
  dynamodb_tables:
    - name: "TestTable"
      region: "us-east-1"
      attribute_definitions:
        - AttributeName: "id"
          AttributeType: "S"
      key_schema:
        - AttributeName: "id"
          KeyType: "HASH"
      billing_mode: "PAY_PER_REQUEST"  # Options: PAY_PER_REQUEST or PROVISIONED
      provisioned_throughput:
        ReadCapacityUnits: 5  # Required only if billing_mode is PROVISIONED
        WriteCapacityUnits: 5
      tags:
        - Key: "Environment"
          Value: "Test"
        - Key: "Project"
          Value: "DevOps-Bot"
"""
            self.insertPlainText("\n" + dynamodb_template)  # ✅ Insert template

        elif text.endswith("# codebuild") or text.endswith("// codebuild"):
            # ✅ Auto-fill CodeBuild project template
            codebuild_template = """resources:
  codebuild_projects:
    - name: "MyCodeBuildProject"
      region: "us-east-1"
      source:
        type: "GITHUB"
        location: "https://github.com/myrepo/myproject.git"
      environment:
        type: "LINUX_CONTAINER"
        image: "aws/codebuild/standard:5.0"
        computeType: "BUILD_GENERAL1_SMALL"
        environmentVariables:
          - name: "ENV_VAR1"
            value: "value1"
          - name: "ENV_VAR2"
            value: "value2"
      service_role: "arn:aws:iam::123456789012:role/CodeBuildServiceRole"
      artifacts:
        type: "S3"
        location: "my-codebuild-bucket"
      tags:
        - Key: "Environment"
          Value: "Development"
        - Key: "Project"
          Value: "DevOps-Bot"
"""
            self.insertPlainText("\n" + codebuild_template)  # ✅ Insert template

        elif text.endswith("# codebuild_build") or text.endswith("// codebuild_build"):
            # ✅ Auto-fill CodeBuild build template
            codebuild_build_template = """resources:
  codebuild_builds:
    - project_name: "MyCodeBuildProject"
      region: "us-east-1"
      source_version: "main"  # Optional: Branch, tag, or commit
      environment_variables:
        - name: "BUILD_ENV"
          value: "production"
        - name: "DEBUG_MODE"
          value: "false"
      execution_id: "execution-12345"
"""
            self.insertPlainText("\n" + codebuild_build_template)  # ✅ Insert template

        elif text.endswith("# nat_gateway") or text.endswith("// nat_gateway"):
            # ✅ Auto-fill NAT Gateway template
            nat_gateway_template = """resources:
  nat_gateways:
    - name: "MyNatGateway"
      region: "us-east-1"
      subnet_id: "subnet-12345678"  # Replace with your actual subnet ID
      allocation_id: "eipalloc-87654321"  # Replace with your actual Elastic IP allocation ID
      tags:
        - Key: "Name"
          Value: "MyNatGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + nat_gateway_template)  # ✅ Insert template

        elif text.endswith("# target_registration") or text.endswith("// target_registration"):
            # ✅ Auto-fill target registration template
            target_registration_template = """resources:
  target_registrations:
    - target_group_arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/my-target-group/abcdef123456"
      region: "us-east-1"
      targets:
        - "i-0123456789abcdef0"  # Replace with actual EC2 instance ID
        - "i-0fedcba9876543210"
      execution_id: "execution-12345"
"""
            self.insertPlainText("\n" + target_registration_template)  # ✅ Insert template

        elif text.endswith("# internet_gateway") or text.endswith("// internet_gateway"):
            # ✅ Auto-fill Internet Gateway template
            internet_gateway_template = """resources:
  internet_gateways:
    - name: "MyInternetGateway"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      tags:
        - Key: "Name"
          Value: "MyInternetGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + internet_gateway_template)  # ✅ Insert template

        elif text.endswith("# vpc") or text.endswith("// vpc"):
            # ✅ Auto-fill VPC template
            vpc_template = """resources:
  vpcs:
    - vpc_name: "MyVPC"
      region: "us-east-1"
      cidr_block: "10.0.0.0/16"
      tags:
        - Key: "Name"
          Value: "MyVPC"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + vpc_template)  # ✅ Insert template

        elif text.endswith("# target_group") or text.endswith("// target_group"):
            # ✅ Auto-fill target group template
            target_group_template = """resources:
  target_groups:
    - name: "MyTargetGroup"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      protocol: "HTTP"  # Options: HTTP, HTTPS, TCP, TLS, UDP, TCP_UDP, GENEVE
      port: 80
      target_type: "instance"  # Options: instance, ip, lambda, alb
      health_check_protocol: "HTTP"
      health_check_port: "traffic-port"  # Use "traffic-port" or a specific port
      tags:
        - Key: "Name"
          Value: "MyTargetGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + target_group_template)  # ✅ Insert template

        elif text.endswith("# load_balancer") or text.endswith("// load_balancer"):
            # ✅ Auto-fill load balancer template
            load_balancer_template = """resources:
  load_balancers:
    - name: "MyLoadBalancer"
      region: "us-east-1"
      subnets:
        - "subnet-12345678"  # Replace with actual subnet ID
        - "subnet-87654321"
      security_groups:
        - "sg-abcdefgh"  # Replace with actual security group ID
      scheme: "internet-facing"  # Options: "internet-facing" or "internal"
      type: "application"  # Options: "application", "network", or "gateway"
      ip_address_type: "ipv4"  # Options: "ipv4" or "dualstack"
      tags:
        - Key: "Name"
          Value: "MyLoadBalancer"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + load_balancer_template)  # ✅ Insert template

        elif text.endswith("# listener") or text.endswith("// listener"):
            # ✅ Auto-fill listener template
            listener_template = """resources:
  listeners:
    - name: "MyListener"
      region: "us-east-1"
      load_balancer_arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/MyLoadBalancer/abcdef123456"
      protocol: "HTTPS"  # Options: "HTTP", "HTTPS", "TCP", "TLS"
      port: 443  # Example: 80 for HTTP, 443 for HTTPS
      action_type: "forward"  # Options: "forward", "redirect"
      target_group_arn: "arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/MyTargetGroup/abcdef123456"
      ssl_certificate_arn: "arn:aws:acm:us-east-1:123456789012:certificate/abcdef-1234-5678-90ab-cdefghijklmn"  # Required for HTTPS/TLS
"""
            self.insertPlainText("\n" + listener_template)  # ✅ Insert template

        elif text.endswith("# rds_subnet_group") or text.endswith("// rds_subnet_group"):
            # ✅ Auto-fill RDS subnet group template
            rds_subnet_group_template = """resources:
  rds_subnet_groups:
    - name: "MyRDSSubnetGroup"
      region: "us-east-1"
      description: "Subnet group for RDS instances"
      subnets:
        - "subnet-12345678"  # Replace with actual subnet ID
        - "subnet-87654321"
      tags:
        - Key: "Name"
          Value: "MyRDSSubnetGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + rds_subnet_group_template)  # ✅ Insert template

        elif text.endswith("# subnet") or text.endswith("// subnet"):
            # ✅ Auto-fill subnet template
            subnet_template = """resources:
  subnets:
    - name: "MySubnet"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      cidr_block: "10.0.1.0/24"
      availability_zone: "us-east-1a"
      depends_on: ["vpc-12345678"]  # Optional dependencies (e.g., VPC creation)
      tags:
        - Key: "Name"
          Value: "MySubnet"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + subnet_template)  # ✅ Insert template

        elif text.endswith("# eks_nodegroup") or text.endswith("// eks_nodegroup"):
            # ✅ Auto-fill EKS node group template
            eks_nodegroup_template = """resources:
  eks_nodegroups:
    - name: "MyNodeGroup"
      region: "us-east-1"
      clusterName: "MyEKSCluster"
      nodeRole: "arn:aws:iam::123456789012:role/EKSNodeGroupRole"
      subnets:
        - "subnet-12345678"  # Replace with actual subnet IDs
        - "subnet-87654321"
      scalingConfig:
        minSize: 2
        maxSize: 5
        desiredSize: 3
      instanceTypes:
        - "t3.medium"  # Replace with desired instance types
      tags:
        - Key: "Name"
          Value: "MyNodeGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + eks_nodegroup_template)  # ✅ Insert template

        elif text.endswith("# eks_cluster") or text.endswith("// eks_cluster"):
            # ✅ Auto-fill EKS cluster template
            eks_cluster_template = """resources:
  eks_clusters:
    - name: "MyEKSCluster"
      region: "us-east-1"
      version: "1.24"  # Replace with the desired Kubernetes version
      role_arn: "arn:aws:iam::123456789012:role/EKSClusterRole"
      resources_vpc_config:
        subnetIds:
          - "subnet-12345678"  # Replace with actual subnet IDs
          - "subnet-87654321"
        securityGroupIds:
          - "sg-abcdefgh"  # Replace with actual security group IDs
        endpointPublicAccess: true
        endpointPrivateAccess: false
"""
            self.insertPlainText("\n" + eks_cluster_template)  # ✅ Insert template

        elif text.endswith("# elastic_ip") or text.endswith("// elastic_ip"):
            # ✅ Auto-fill Elastic IP template
            elastic_ip_template = """resources:
  elastic_ips:
    - name: "MyElasticIP"
      region: "us-east-1"
      domain: "vpc"  # Options: "vpc" (default), "standard" (EC2-Classic)
      instance_id: "i-0123456789abcdef0"  # Optional: Replace with an actual EC2 instance ID
      tags:
        - Key: "Name"
          Value: "MyElasticIP"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + elastic_ip_template)  # ✅ Insert template

        elif text.endswith("# security_group") or text.endswith("// security_group"):
            # ✅ Auto-fill security group template
            security_group_template = """resources:
  security_groups:
    - name: "MySecurityGroup"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      description: "Security group for web application"
      inbound_rules:
        - protocol: "tcp"
          port_range: "80"  # Allow HTTP traffic
          cidr_blocks: "0.0.0.0/0"
        - protocol: "tcp"
          port_range: "443"  # Allow HTTPS traffic
          cidr_blocks: "0.0.0.0/0"
        - protocol: "tcp"
          port_range: "22"  # Allow SSH access
          cidr_blocks: "192.168.1.0/24"  # Restrict SSH access to internal network
      tags:
        - Key: "Name"
          Value: "MySecurityGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + security_group_template)  # ✅ Insert template

        elif text.endswith("# route_table") or text.endswith("// route_table"):
            # ✅ Auto-fill route table template
            route_table_template = """resources:
  route_tables:
    - name: "MyRouteTable"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      tags:
        - Key: "Name"
          Value: "MyRouteTable"
        - Key: "Environment"
          Value: "Production"
      routes:
        - destination_cidr_block: "0.0.0.0/0"  # Default route for internet access
          gateway_id: "igw-abcdefgh"  # Replace with the actual Internet Gateway ID
"""
            self.insertPlainText("\n" + route_table_template)  # ✅ Insert template

        elif text.endswith("# network_interface") or text.endswith("// network_interface"):
            # ✅ Auto-fill network interface template
            network_interface_template = """resources:
  network_interfaces:
    - name: "MyNetworkInterface"
      region: "us-east-1"
      subnet_id: "subnet-12345678"  # Replace with your actual subnet ID
      description: "Primary network interface for application"
      groups:
        - "sg-abcdefgh"  # Replace with actual security group IDs
      tags:
        - Key: "Name"
          Value: "MyNetworkInterface"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + network_interface_template)  # ✅ Insert template

        elif text.endswith("# ssl_certificate") or text.endswith("// ssl_certificate"):
            # ✅ Auto-fill SSL certificate template
            ssl_certificate_template = """resources:
  ssl_certificates:
    - domain_name: "example.com"
      region: "us-east-1"
      validation_method: "DNS"  # Options: "DNS" or "EMAIL"
      subject_alternative_names:
        - "www.example.com"
        - "api.example.com"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Owner"
          Value: "DevOps Team"
"""
            self.insertPlainText("\n" + ssl_certificate_template)  # ✅ Insert template

        elif text.endswith("# transit_gateway") or text.endswith("// transit_gateway"):
            # ✅ Auto-fill transit gateway template
            transit_gateway_template = """resources:
  transit_gateways:
    - name: "MyTransitGateway"
      region: "us-east-1"
      description: "Primary Transit Gateway for cross-region networking"
      options:
        AmazonSideAsn: 64512  # Replace with your ASN if needed
        AutoAcceptSharedAttachments: "disable"  # Options: "enable" or "disable"
        DefaultRouteTableAssociation: "enable"  # Options: "enable" or "disable"
        DefaultRouteTablePropagation: "enable"  # Options: "enable" or "disable"
      tags:
        - Key: "Name"
          Value: "MyTransitGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + transit_gateway_template)  # ✅ Insert template

        elif text.endswith("# transit_gateway_attachment") or text.endswith("// transit_gateway_attachment"):
            # ✅ Auto-fill transit gateway attachment template
            transit_gateway_attachment_template = """resources:
  transit_gateway_attachments:
    - name: "MyTransitGatewayAttachment"
      region: "us-east-1"
      transit_gateway_id: "tgw-12345678"  # Replace with your actual Transit Gateway ID
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      subnet_ids:
        - "subnet-12345678"  # Replace with actual subnet IDs
        - "subnet-87654321"
      tags:
        - Key: "Name"
          Value: "MyTransitGatewayAttachment"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + transit_gateway_attachment_template)  # ✅ Insert template

        elif text.endswith("# transit_gateway_policy_table") or text.endswith("// transit_gateway_policy_table"):
            # ✅ Auto-fill transit gateway policy table template
            transit_gateway_policy_table_template = """resources:
  transit_gateway_policy_tables:
    - name: "MyTransitGatewayPolicyTable"
      region: "us-east-1"
      transit_gateway_id: "tgw-12345678"  # Replace with your actual Transit Gateway ID
      policy_rules:
        - source_cidr: "10.0.0.0/16"
          destination_cidr: "192.168.1.0/24"
          action: "allow"
        - source_cidr: "10.0.1.0/24"
          destination_cidr: "172.16.0.0/12"
          action: "deny"
      tags:
        - Key: "Name"
          Value: "MyTransitGatewayPolicyTable"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + transit_gateway_policy_table_template)  # ✅ Insert template
        elif text.endswith("# transit_gateway_route_table") or text.endswith("// transit_gateway_route_table"):
            # ✅ Auto-fill transit gateway route table template
            transit_gateway_route_table_template = """resources:
  transit_gateway_route_tables:
    - name: "MyTGWRouteTable"
      region: "us-east-1"
      transit_gateway_id: "tgw-12345678"  # Replace with your actual Transit Gateway ID
      tags:
        - Key: "Name"
          Value: "MyTGWRouteTable"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + transit_gateway_route_table_template)  # ✅ Insert template

        elif text.endswith("# transit_gateway_multicast") or text.endswith("// transit_gateway_multicast"):
            # ✅ Auto-fill transit gateway multicast domain template
            transit_gateway_multicast_template = """resources:
  transit_gateway_multicasts:
    - name: "MyTGWMulticastDomain"
      region: "us-east-1"
      transit_gateway_id: "tgw-12345678"  # Replace with your actual Transit Gateway ID
      tags:
        - Key: "Name"
          Value: "MyTGWMulticastDomain"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + transit_gateway_multicast_template)  # ✅ Insert template

        elif text.endswith("# customer_gateway") or text.endswith("// customer_gateway"):
            # ✅ Auto-fill customer gateway template
            customer_gateway_template = """resources:
  customer_gateways:
    - name: "MyCustomerGateway"
      region: "us-east-1"
      bgp_asn: 65000  # Replace with your actual BGP ASN
      ip_address: "203.0.113.1"  # Replace with your actual public IP address
      type: "ipsec.1"  # Default type for AWS VPN connections
      tags:
        - Key: "Name"
          Value: "MyCustomerGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + customer_gateway_template)  # ✅ Insert template

        elif text.endswith("# virtual_private_gateway") or text.endswith("// virtual_private_gateway"):
            # ✅ Auto-fill virtual private gateway template
            virtual_private_gateway_template = """resources:
  virtual_private_gateways:
    - name: "MyVPGateway"
      region: "us-east-1"
      amazon_side_asn: 64512  # Default ASN for AWS
      tags:
        - Key: "Name"
          Value: "MyVPGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + virtual_private_gateway_template)  # ✅ Insert template

        elif text.endswith("# vpn_connection") or text.endswith("// vpn_connection"):
            # ✅ Auto-fill VPN connection template
            vpn_connection_template = """resources:
  vpn_connections:
    - name: "MyVPNConnection"
      region: "us-east-1"
      customer_gateway_id: "cgw-12345678"  # Replace with your actual Customer Gateway ID
      vpn_gateway_id: "vgw-87654321"  # Replace with your VPN Gateway ID (if applicable)
      # transit_gateway_id: "tgw-abcdefgh"  # Uncomment if using a Transit Gateway instead
      tags:
        - Key: "Name"
          Value: "MyVPNConnection"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + vpn_connection_template)  # ✅ Insert template

        elif text.endswith("# client_vpn_endpoint") or text.endswith("// client_vpn_endpoint"):
            # ✅ Auto-fill client VPN endpoint template
            client_vpn_endpoint_template = """resources:
  client_vpn_endpoints:
    - name: "MyClientVPN"
      region: "us-east-1"
      client_cidr_block: "10.0.0.0/22"  # Replace with your CIDR block
      server_certificate_arn: "arn:aws:acm:us-east-1:123456789012:certificate/abcdef12-3456-7890-abcd-ef1234567890"
      authentication_options:
        - Type: "certificate-authentication"
          MutualAuthentication:
            ClientRootCertificateChainArn: "arn:aws:acm:us-east-1:123456789012:certificate/abcdef12-3456-7890-abcd-ef1234567890"
      connection_log_options:
        Enabled: true
        CloudwatchLogGroup: "/aws/client-vpn/logs"
        CloudwatchLogStream: "client-vpn-stream"
      tags:
        - Key: "Name"
          Value: "MyClientVPN"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + client_vpn_endpoint_template)  # ✅ Insert template

        elif text.endswith("# lattice_service") or text.endswith("// lattice_service"):
            # ✅ Auto-fill lattice service template
            lattice_service_template = """resources:
  lattice_services:
    - name: "MyLatticeService"
      region: "us-east-1"
      auth_type: "NONE"  # Options: "NONE" or other applicable auth types
      tags:
        - Key: "Name"
          Value: "MyLatticeService"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + lattice_service_template)  # ✅ Insert template

        elif text.endswith("# resource_configuration") or text.endswith("// resource_configuration"):
            # ✅ Auto-fill resource configuration template
            resource_configuration_template = """resources:
  resource_configurations:
    - name: "MyResourceConfig"
      region: "us-east-1"
      config_type: "AggregatorConfig"  # Name of the Configuration Aggregator
      target_resource: "123456789012"  # AWS Account ID to aggregate resources from
      all_aws_regions: true  # Whether to aggregate from all AWS regions
      tags:
        - Key: "Name"
          Value: "MyResourceConfig"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + resource_configuration_template)  # ✅ Insert template

        elif text.endswith("# resource_gateway") or text.endswith("// resource_gateway"):
            # ✅ Auto-fill resource gateway template
            resource_gateway_template = """resources:
  resource_gateways:
    - name: "MyResourceGateway"
      region: "us-east-1"
      description: "API Gateway for managing internal APIs"
      tags:
        - Key: "Name"
          Value: "MyResourceGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + resource_gateway_template)  # ✅ Insert template

        elif text.endswith("# vpc_endpoint") or text.endswith("// vpc_endpoint"):
            # ✅ Auto-fill VPC endpoint template
            vpc_endpoint_template = """resources:
  vpc_endpoints:
    - name: "MyVPCEndpoint"
      region: "us-east-1"
      vpc_id: "vpc-12345678"  # Replace with your actual VPC ID
      service_name: "com.amazonaws.us-east-1.s3"  # Example for S3, replace as needed
      tags:
        - Key: "Name"
          Value: "MyVPCEndpoint"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + vpc_endpoint_template)  # ✅ Insert template

        elif text.endswith("# vpc_endpoint_service") or text.endswith("// vpc_endpoint_service"):
            # ✅ Auto-fill VPC endpoint service template
            vpc_endpoint_service_template = """resources:
  vpc_endpoint_services:
    - name: "MyVPCEndpointService"
      region: "us-east-1"
      nlb_arns:
        - "arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/net/MyNLB/abcdef1234567890"  # Replace with your actual NLB ARN
      tags:
        - Key: "Name"
          Value: "MyVPCEndpointService"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + vpc_endpoint_service_template)  # ✅ Insert template

        elif text.endswith("# service_network") or text.endswith("// service_network"):
            # ✅ Auto-fill service network template
            service_network_template = """resources:
  service_networks:
    - name: "MyServiceNetwork"
      region: "us-east-1"
      tags:
        - Key: "Name"
          Value: "MyServiceNetwork"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + service_network_template)  # ✅ Insert template
        elif text.endswith("# lattice_service") or text.endswith("// lattice_service"):
            # ✅ Auto-fill lattice service template
            lattice_service_template = """resources:
  lattice_services:
    - name: "MyLatticeService"
      region: "us-east-1"
      tags:
        - Key: "Name"
          Value: "MyLatticeService"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + lattice_service_template)  # ✅ Insert template

        elif text.endswith("# resource_gateway") or text.endswith("// resource_gateway"):
            # ✅ Auto-fill resource gateway template
            resource_gateway_template = """resources:
  resource_gateways:
    - name: "MyResourceGateway"
      region: "us-east-1"
      description: "API Gateway for managing internal APIs"
      tags:
        - Key: "Name"
          Value: "MyResourceGateway"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + resource_gateway_template)  # ✅ Insert template

        elif text.endswith("# resource_configuration") or text.endswith("// resource_configuration"):
            # ✅ Auto-fill resource configuration template
            resource_configuration_template = """resources:
  resource_configurations:
    - name: "MyResourceConfig"
      region: "us-east-1"
      config_type: "AggregatorConfig"  # Name of the Configuration Aggregator
      target_resource: "123456789012"  # AWS Account ID to aggregate resources from
      all_aws_regions: true  # Whether to aggregate from all AWS regions
      tags:
        - Key: "Name"
          Value: "MyResourceConfig"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + resource_configuration_template)  # ✅ Insert template

        elif text.endswith("# firewall_policy") or text.endswith("// firewall_policy"):
            # ✅ Auto-fill firewall policy template
            firewall_policy_template = """resources:
  firewall_policies:
    - name: "MyFirewallPolicy"
      region: "us-east-1"
      description: "Firewall policy for controlling traffic"
      stateful_rule_group_arns:
        - "arn:aws:network-firewall:us-east-1:123456789012:stateful-rulegroup/MyStatefulRuleGroup"
      stateless_default_actions:
        - "aws:pass"
      stateless_fragment_default_actions:
        - "aws:drop"
      stateless_custom_actions:
        - Name: "CustomAction"
          ActionDefinition:
            PublishMetricAction:
              Dimensions:
                - Value: "CustomMetric"
      tags:
        - Key: "Name"
          Value: "MyFirewallPolicy"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + firewall_policy_template)  # ✅ Insert template

        elif text.endswith("# rule_group") or text.endswith("// rule_group"):
            # ✅ Auto-fill rule group template
            rule_group_template = """resources:
  rule_groups:
    - name: "MyRuleGroup"
      region: "us-east-1"
      capacity: 100  # Number of rules the rule group can support
      rule_group_type: "STATEFUL"  # Options: "STATEFUL" or "STATELESS"
      description: "Stateful rule group for traffic filtering"
      rules:
        - "pass tcp any any -> any any (msg:\"Allow TCP\"; sid:1000001;)"
        - "drop udp any any -> any any (msg:\"Drop UDP\"; sid:1000002;)"
      tags:
        - Key: "Name"
          Value: "MyRuleGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + rule_group_template)  # ✅ Insert template

        elif text.endswith("# tls_inspection_configuration") or text.endswith("// tls_inspection_configuration"):
            # ✅ Auto-fill TLS inspection configuration template
            tls_inspection_configuration_template = """resources:
  tls_inspection_configurations:
    - name: "MyTLSInspectionConfig"
      region: "us-east-1"
      inspection_certificate_arn: "arn:aws:acm:us-east-1:123456789012:certificate/abcdef12-3456-7890-abcd-ef1234567890"
      description: "TLS Inspection configuration for monitoring encrypted traffic"
      tags:
        - Key: "Name"
          Value: "MyTLSInspectionConfig"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + tls_inspection_configuration_template)  # ✅ Insert template

        elif text.endswith("# resource_group") or text.endswith("// resource_group"):
            # ✅ Auto-fill resource group template
            resource_group_template = """resources:
  resource_groups:
    - name: "MyResourceGroup"
      region: "us-east-1"
      resource_type: "AWS::EC2::Instance"  # Replace with the appropriate AWS resource type
      resource_arns:
        - "arn:aws:ec2:us-east-1:123456789012:instance/i-abcdef1234567890"  # Replace with actual resource ARNs
        - "arn:aws:ec2:us-east-1:123456789012:instance/i-0987654321fedcba"
      tags:
        - Key: "Name"
          Value: "MyResourceGroup"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + resource_group_template)  # ✅ Insert template

        elif text.endswith("# user_group") or text.endswith("// user_group"):
            # ✅ Auto-fill user group template
            user_group_template = """resources:
  user_groups:
    - name: "Developers"
      region: "us-east-1"
      path: "/engineering/"  # Optional IAM path
      tags:
        - Key: "Department"
          Value: "Engineering"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + user_group_template)  # ✅ Insert template

        elif text.endswith("# iam_user") or text.endswith("// iam_user"):
            # ✅ Auto-fill IAM user template
            iam_user_template = """resources:
  iam_users:
    - name: "john.doe"
      region: "us-east-1"
      path: "/engineering/"  # Optional IAM path
      groups:
        - "Developers"  # List of groups to add the user to
        - "Admins"
      tags:
        - Key: "Department"
          Value: "Engineering"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + iam_user_template)  # ✅ Insert template

        elif text.endswith("# iam_role") or text.endswith("// iam_role"):
            # ✅ Auto-fill IAM role template
            iam_role_template = """resources:
  iam_roles:
    - name: "EC2AccessRole"
      region: "us-east-1"
      path: "/service-role/"  # Optional IAM path
      assume_role_policy_document:
        Version: "2012-10-17"
        Statement:
          - Effect: "Allow"
            Principal:
              Service: "ec2.amazonaws.com"
            Action: "sts:AssumeRole"
      tags:
        - Key: "Name"
          Value: "EC2AccessRole"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + iam_role_template)  # ✅ Insert template

        elif text.endswith("# identity_provider") or text.endswith("// identity_provider"):
            # ✅ Auto-fill identity provider template
            identity_provider_template = """resources:
  identity_providers:
    - name: "MySAMLProvider"
      region: "us-east-1"
      type: "SAML"
      metadata_document: "<SAML_METADATA_XML>"  # Replace with actual SAML metadata XML
      tags:
        - Key: "Name"
          Value: "MySAMLProvider"
        - Key: "Environment"
          Value: "Production"

    - name: "MyOIDCProvider"
      region: "us-east-1"
      type: "OIDC"
      url: "https://oidc.example.com"
      client_id_list:
        - "my-client-id"
      thumbprint_list:
        - "9e99a48a9960b14926bb7f3b02e22da5b2b6c68d"  # Replace with the actual OIDC thumbprint
      tags:
        - Key: "Name"
          Value: "MyOIDCProvider"
        - Key: "Environment"
          Value: "Production"
"""
            self.insertPlainText("\n" + identity_provider_template)  # ✅ Insert template

        elif text.endswith("# account_settings") or text.endswith("// account_settings"):
            # ✅ Auto-fill account settings template
            account_settings_template = """resources:
  account_settings:
    - region: "us-east-1"
      password_policy:
        minimum_length: 12
        require_symbols: true
        require_numbers: true
        require_uppercase: true
        require_lowercase: true
        allow_user_change: true
        max_password_age: 90
        password_reuse_prevention: 24
        hard_expiry: false

    - region: "us-east-1"
      account_alias: "my-organization-alias"
"""
            self.insertPlainText("\n" + account_settings_template)  # ✅ Insert template

        elif text.endswith("# root_access_management") or text.endswith("// root_access_management"):
            # ✅ Auto-fill root access management template
            root_access_management_template = """resources:
  root_access_management:
    - region: "us-east-1"
      enforce_mfa: true  # Ensure root MFA is enabled
      remove_access_keys: true  # Ensure root access keys are removed
"""
            self.insertPlainText("\n" + root_access_management_template)  # ✅ Insert template

        elif text.endswith("# access_analyzer") or text.endswith("// access_analyzer"):
            # ✅ Auto-fill access analyzer template
            access_analyzer_template = """resources:
  access_analyzers:
    - name: "MyAccessAnalyzer"
      region: "us-east-1"
      type: "ACCOUNT"  # Options: "ACCOUNT" or "ORGANIZATION"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "Security"
      archive_rules:
        - RuleName: "ExcludeService1"
          RuleType: "EXCLUDE"
          Filter:
            - "service": "s3"
        - RuleName: "IncludeService2"
          RuleType: "INCLUDE"
          Filter:
            - "service": "ec2"
"""
            self.insertPlainText("\n" + access_analyzer_template)  # ✅ Insert template

        elif text.endswith("# memorydb_cluster") or text.endswith("// memorydb_cluster"):
            # ✅ Auto-fill MemoryDB cluster template
            memorydb_cluster_template = """resources:
  memorydb_clusters:
    - name: "MyMemoryDBCluster"
      region: "us-east-1"
      node_type: "db.r5.large"  # MemoryDB node type
      engine_version: "7.0"  # Optional: specify the engine version, or leave out to use the default
      acl_name: "open-access"  # Access control list
      subnet_group_name: "my-subnet-group"  # Name of the subnet group
      security_group_ids:
        - "sg-0123456789abcdef0"  # Optional: security group IDs
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "IT"
"""
            self.insertPlainText("\n" + memorydb_cluster_template)  # ✅ Insert template

        elif text.endswith("# global_datastore") or text.endswith("// global_datastore"):
            # ✅ Auto-fill global datastore template
            global_datastore_template = """resources:
  global_datastores:
    - global_datastore_id: "MyGlobalDatastore"
      region: "us-east-1"
      primary_replication_group_id: "primary-replication-group-id"
      replica_regions:
        - "us-west-2"
        - "eu-west-1"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "Database"
"""
            self.insertPlainText("\n" + global_datastore_template)  # ✅ Insert template

        elif text.endswith("# reserved_node") or text.endswith("// reserved_node"):
            # ✅ Auto-fill reserved nodes template
            reserved_nodes_template = """resources:
  reserved_nodes:
    - offering_id: "offering-id-123456"
      region: "us-east-1"
      cache_node_count: 3  # Optional: number of nodes to reserve
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "Database"
"""
            self.insertPlainText("\n" + reserved_nodes_template)  # ✅ Insert template

        elif text.endswith("# elasticache_backup") or text.endswith("// elasticache_backup"):
            # ✅ Auto-fill ElastiCache backup template
            elasticache_backup_template = """resources:
  elasticache_backups:
    - snapshot_name: "my-backup-snapshot"
      region: "us-east-1"
      source: "my-cluster-id"  # The ID of the cache cluster or replication group
      source_type: "cluster"  # Options: "replication_group" or "cluster"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "Database"
"""
            self.insertPlainText("\n" + elasticache_backup_template)  # ✅ Insert template

        elif text.endswith("# elasticache_configuration") or text.endswith("// elasticache_configuration"):
            # ✅ Auto-fill ElastiCache configuration template
            elasticache_configuration_template = """resources:
  elasticache_configurations:
    - name: "MyElastiCacheConfig"
      region: "us-east-1"
      replication_group_id: "my-replication-group-id"  # Optional, based on your config change needs
      cache_cluster_id: "my-cluster-id"  # Optional, depending on the configuration type
      parameters:
        - ParameterName: "maxmemory-policy"
          ParameterValue: "allkeys-lru"
        - ParameterName: "notify-keyspace-events"
          ParameterValue: "A"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Department"
          Value: "Cache"
"""
            self.insertPlainText("\n" + elasticache_configuration_template)  # ✅ Insert template

        elif text.endswith("# service_update") or text.endswith("// service_update"):
            # ✅ Auto-fill service updates template
            service_updates_template = """resources:
  service_updates:
    - service_update_name: "MyServiceUpdate"
      region: "us-east-1"
      replication_group_ids:
        - "my-replication-group-id-1"
        - "my-replication-group-id-2"
      cache_cluster_ids:
        - "my-cache-cluster-id-1"
        - "my-cache-cluster-id-2"
      service_update_type: "immediate"  # Optional: 'immediate' or 'replica'
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + service_updates_template)  # ✅ Insert template

        elif text.endswith("# redis_replication_group") or text.endswith("// redis_replication_group"):
            # ✅ Auto-fill Redis replication group template
            redis_replication_group_template = """resources:
  redis_replication_groups:
    - replication_group_id: "my-redis-replication-group"
      region: "us-east-1"
      description: "Redis Replication Group for caching"
      cache_node_type: "cache.m5.large"
      num_node_groups: 2  # Number of node groups for cluster mode
      automatic_failover: true  # Enable automatic failover
      security_group_ids:
        - "sg-0123456789abcdef0"  # Optional: security group IDs
      subnet_group_name: "my-redis-subnet-group"  # Optional: subnet group name
      parameter_group_name: "default.redis5.0"  # Optional: parameter group name
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "RedisCache"
"""
            self.insertPlainText("\n" + redis_replication_group_template)  # ✅ Insert template

        elif text.endswith("# subnet_group") or text.endswith("// subnet_group"):
            # ✅ Auto-fill ElastiCache subnet group template
            subnet_group_template = """resources:
  subnet_groups:
    - name: "my-elasticache-subnet-group"
      region: "us-east-1"
      description: "Subnet group for Redis cache"
      subnet_ids:
        - "subnet-0123456789abcdef0"
        - "subnet-0987654321abcdef0"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + subnet_group_template)  # ✅ Insert template

        elif text.endswith("# parameter_group") or text.endswith("// parameter_group"):
            # ✅ Auto-fill ElastiCache parameter group template
            parameter_group_template = """resources:
  parameter_groups:
    - name: "my-elasticache-parameter-group"
      region: "us-east-1"
      family: "redis5.0"
      description: "Custom parameter group for Redis 5.0"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + parameter_group_template)  # ✅ Insert template

        elif text.endswith("# cache_user") or text.endswith("// cache_user"):
            # ✅ Auto-fill ElastiCache cache user template
            cache_user_template = """resources:
  cache_users:
    - user_id: "my-cache-user"
      region: "us-east-1"
      user_name: "myuser"
      engine: "redis"  # Optional: e.g., redis or memcached
      access_string: "on ~* +@all"
      no_password_required: false  # Optional: set to true if no password is required
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + cache_user_template)  # ✅ Insert template
        elif text.endswith("# elasticache_client") or text.endswith("// elasticache_client"):
            # ✅ Auto-fill ElastiCache client template
            elasticache_client_template = """resources:
  elasticache_clients:
    - name: "redis-client"
      region: "us-east-1"
      version: "6.0"
      client_type: "redis"  # Options: redis or memcached
      installation_method: "yum"  # Optional: e.g., 'yum', 'docker', 'ansible', etc.
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + elasticache_client_template)  # ✅ Insert template

        elif text.endswith("# cloudfront_distribution") or text.endswith("// cloudfront_distribution"):
            # ✅ Auto-fill CloudFront distribution template
            cloudfront_distribution_template = """resources:
  cloudfront_distributions:
    - name: "my-cloudfront-distribution"
      region: "us-east-1"
      origins:
        - DomainName: "my-bucket.s3.amazonaws.com"
          Id: "S3-my-bucket"
          S3OriginConfig:
            OriginAccessIdentity: ""
      default_cache_behavior:
        TargetOriginId: "S3-my-bucket"
        ViewerProtocolPolicy: "allow-all"
        AllowedMethods:
          Quantity: 3
          Items:
            - "GET"
            - "HEAD"
            - "OPTIONS"
        CachedMethods:
          Quantity: 2
          Items:
            - "GET"
            - "HEAD"
      price_class: "PriceClass_100"  # Optional: Price class for the distribution
      enabled: true  # Optional: whether the distribution should be enabled
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "CloudFront"
"""
            self.insertPlainText("\n" + cloudfront_distribution_template)  # ✅ Insert template

        elif text.endswith("# cloudfront_function") or text.endswith("// cloudfront_function"):
            # ✅ Auto-fill CloudFront function template
            cloudfront_function_template = """resources:
  cloudfront_functions:
    - name: "my-cloudfront-function"
      region: "us-east-1"
      runtime: "cloudfront-js-1.0"  # e.g., "cloudfront-js-1.0" or another supported runtime
      function_code: |
        function handler(event) {
            var request = event.request;
            // Custom logic here
            return request;
        }
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "CloudFront"
"""
            self.insertPlainText("\n" + cloudfront_function_template)  # ✅ Insert template

        elif text.endswith("# oai") or text.endswith("// oai"):
            # ✅ Auto-fill CloudFront OAI template
            oai_template = """resources:
  oais:
    - comment: "My CloudFront OAI"
      region: "us-east-1"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "CloudFront"
"""
            self.insertPlainText("\n" + oai_template)  # ✅ Insert template

        elif text.endswith("# vpc_origin") or text.endswith("// vpc_origin"):
            # ✅ Auto-fill VPC origin template
            vpc_origin_template = """resources:
  vpc_origins:
    - name: "my-vpc-origin"
      region: "us-east-1"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "CloudFront"
"""
            self.insertPlainText("\n" + vpc_origin_template)  # ✅ Insert template

        elif text.endswith("# ecr_private_repository") or text.endswith("// ecr_private_repository"):
            # ✅ Auto-fill ECR private repository template
            ecr_private_repository_template = """resources:
  ecr_private_repositories:
    - name: "my-private-repo"
      region: "us-east-1"
      image_scan_on_push: true  # Optional: Whether to scan images on push
      lifecycle_policy:
        rules:
          - rulePriority: 1
            description: "Expire images older than 30 days"
            action:
              type: "expire"
            filter:
              tagStatus: "any"
              tagPrefixList:
                - "v1"
            expiration:
              days: 30
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ECR"
"""
            self.insertPlainText("\n" + ecr_private_repository_template)  # ✅ Insert template

        elif text.endswith("# ecr_public_repository") or text.endswith("// ecr_public_repository"):
            # ✅ Auto-fill ECR public repository template
            ecr_public_repository_template = """resources:
  ecr_public_repositories:
    - name: "my-public-repo"
      region: "us-east-1"
      repository_policy:
        statements:
          - Effect: "Allow"
            Action: "ecr:BatchCheckLayerAvailability"
            Resource: "*"
            Principal: "*"
      tags:
        - Key: "Environment"
          Value: "Public"
        - Key: "Service"
          Value: "ECR"
"""
            self.insertPlainText("\n" + ecr_public_repository_template)  # ✅ Insert template

        elif text.endswith("# valkey_cache") or text.endswith("// valkey_cache"):
            # ✅ Auto-fill Valkey cache template
            valkey_cache_template = """resources:
  valkey_caches:
    - name: "my-valkey-cache"
      region: "us-east-1"
      engine_version: "8.0"  # Optional: specify the engine version, defaults to '8.0'
      description: "A serverless Redis cache for my application."
      security_group_ids:
        - "sg-12345678"
      subnet_ids:
        - "subnet-12345678"
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "Redis"
"""
            self.insertPlainText("\n" + valkey_cache_template)  # ✅ Insert template

        elif text.endswith("# event_subscription") or text.endswith("// event_subscription"):
            # ✅ Auto-fill ElastiCache event subscription template
            event_subscription_template = """resources:
  event_subscriptions:
    - subscription_name: "my-elasticache-event-subscription"
      region: "us-east-1"
      sns_topic_arn: "arn:aws:sns:us-east-1:123456789012:MySNSTopic"
      source_type: "cache-cluster"  # Optional: e.g., 'cache-cluster', 'cache-parameter-group', etc.
      source_ids:
        - "my-cache-cluster-id"  # Optional: list of specific source IDs to filter by
      event_categories:
        - "availability"
        - "creation"  # Optional: list of event categories to filter by
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + event_subscription_template)  # ✅ Insert template

        elif text.endswith("# cache_user_group") or text.endswith("// cache_user_group"):
            # ✅ Auto-fill ElastiCache cache user group template
            cache_user_group_template = """resources:
  cache_user_groups:
    - user_group_id: "my-cache-user-group"
      region: "us-east-1"
      engine: "redis"  # Optional: engine type (e.g., redis or memcached)
      user_ids:
        - "my-cache-user-id"  # List of user IDs to associate with this user group
      tags:
        - Key: "Environment"
          Value: "Production"
        - Key: "Service"
          Value: "ElastiCache"
"""
            self.insertPlainText("\n" + cache_user_group_template)  # ✅ Insert template
        
        elif text.endswith("# s3_b") or text.endswith("// s3_bucket"):
        # ✅ Auto-fill EC2 instance template
          s3_template = """resources:
s3_buckets:
- name: "my-s3-bucket"
  region: "us-east-1"
  public_access_block: true  # Block public access to the bucket
  versioning: true  # Enable versioning
  lifecycle_rules:
    - id: "ExpireOldObjects"
      prefix: "logs/"
      status: "Enabled"
      expiration_in_days: 30  # Automatically delete objects older than 30 days
  logging:
    TargetBucket: "my-logging-bucket"
    TargetPrefix: "logs/"
  encryption:
    SSEAlgorithm: "AES256"  # Server-side encryption using AES-256

"""
        self.insertPlainText("\n" + s3_template)  # ✅ Insert template

    # ...existing code...