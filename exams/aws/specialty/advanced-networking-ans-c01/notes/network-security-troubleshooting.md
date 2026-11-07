# Network Security and Troubleshooting

## Network Security

### Security Groups

**Characteristics**
- Stateful: Return traffic automatically allowed
- Allow rules only (implicit deny)
- Instance level security
- Evaluate all rules before deciding
- Separate rules for inbound and outbound

**Best Practices**
```yaml
Resources:
  WebServerSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Web server security group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        # HTTP from ALB only
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          SourceSecurityGroupId: !Ref ALBSecurityGroup
        # HTTPS from ALB only
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          SourceSecurityGroupId: !Ref ALBSecurityGroup
        # SSH from bastion only
        - IpProtocol: tcp
          FromPort: 22
          ToPort: 22
          SourceSecurityGroupId: !Ref BastionSecurityGroup
      SecurityGroupEgress:
        # Allow all outbound (default, but explicit)
        - IpProtocol: -1
          CidrIp: 0.0.0.0/0

  DatabaseSecurityGroup:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupDescription: Database security group
      VpcId: !Ref VPC
      SecurityGroupIngress:
        # MySQL from app servers only
        - IpProtocol: tcp
          FromPort: 3306
          ToPort: 3306
          SourceSecurityGroupId: !Ref WebServerSecurityGroup
      SecurityGroupEgress:
        # No outbound needed for RDS
        - IpProtocol: -1
          CidrIp: 127.0.0.1/32
```

### Network ACLs

**Characteristics**
- Stateless: Must allow return traffic explicitly  
- Allow and Deny rules
- Subnet level security
- Rules evaluated in number order
- Default NACL allows all traffic

**NACL Configuration**
```yaml
Resources:
  PublicNetworkAcl:
    Type: AWS::EC2::NetworkAcl
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Public-NACL

  # Inbound HTTP
  InboundHTTPRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 100
      Protocol: 6  # TCP
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 80
        To: 80

  # Inbound HTTPS
  InboundHTTPSRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 110
      Protocol: 6
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 443
        To: 443

  # Inbound ephemeral ports (for return traffic)
  InboundEphemeralRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 120
      Protocol: 6
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 1024
        To: 65535

  # Block specific IP
  BlockMaliciousIP:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 50
      Protocol: -1
      RuleAction: deny
      CidrBlock: 198.51.100.0/24

  # Outbound rules
  OutboundHTTPRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 100
      Protocol: 6
      Egress: true
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 80
        To: 80

  OutboundHTTPSRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 110
      Protocol: 6
      Egress: true
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 443
        To: 443

  OutboundEphemeralRule:
    Type: AWS::EC2::NetworkAclEntry
    Properties:
      NetworkAclId: !Ref PublicNetworkAcl
      RuleNumber: 120
      Protocol: 6
      Egress: true
      RuleAction: allow
      CidrBlock: 0.0.0.0/0
      PortRange:
        From: 1024
        To: 65535
```

### AWS Network Firewall

**Features**
- Stateful and stateless inspection
- Deep packet inspection
- Intrusion prevention (IPS)
- Domain filtering
- TLS inspection

**Network Firewall Configuration**
```yaml
Resources:
  NetworkFirewall:
    Type: AWS::NetworkFirewall::Firewall
    Properties:
      FirewallName: Production-Firewall
      VpcId: !Ref VPC
      SubnetMappings:
        - SubnetId: !Ref FirewallSubnetA
        - SubnetId: !Ref FirewallSubnetB
      FirewallPolicyArn: !Ref FirewallPolicy

  FirewallPolicy:
    Type: AWS::NetworkFirewall::FirewallPolicy
    Properties:
      FirewallPolicyName: Production-Policy
      FirewallPolicy:
        StatelessDefaultActions:
          - 'aws:forward_to_sfe'
        StatelessFragmentDefaultActions:
          - 'aws:forward_to_sfe'
        StatefulRuleGroupReferences:
          - ResourceArn: !Ref DomainFilterRuleGroup
          - ResourceArn: !Ref IPSRuleGroup

  DomainFilterRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: Domain-Filter
      Type: STATEFUL
      Capacity: 100
      RuleGroup:
        RulesSource:
          RulesSourceList:
            TargetTypes:
              - HTTP_HOST
              - TLS_SNI
            Targets:
              - .malicious-site.com
              - .phishing-site.com
            GeneratedRulesType: DENYLIST

  IPSRuleGroup:
    Type: AWS::NetworkFirewall::RuleGroup
    Properties:
      RuleGroupName: IPS-Rules
      Type: STATEFUL
      Capacity: 1000
      RuleGroup:
        RulesSource:
          RulesString: |
            alert tcp any any -> any 80 (msg:"Possible SQL Injection"; content:"SELECT"; nocase; sid:1000001;)
            drop tcp any any -> any any (msg:"Known malware C2"; content:"|deadbeef|"; sid:1000002;)
```

### AWS WAF

**Protection Types**
- SQL injection
- Cross-site scripting (XSS)
- Rate limiting
- Geo-blocking
- IP reputation lists
- Bot control

**WAF WebACL Configuration**
```json
{
  "Name": "ProductionWebACL",
  "Scope": "REGIONAL",
  "DefaultAction": {
    "Allow": {}
  },
  "Rules": [
    {
      "Name": "RateLimitRule",
      "Priority": 1,
      "Statement": {
        "RateBasedStatement": {
          "Limit": 2000,
          "AggregateKeyType": "IP"
        }
      },
      "Action": {
        "Block": {
          "CustomResponse": {
            "ResponseCode": 429
          }
        }
      },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "RateLimitRule"
      }
    },
    {
      "Name": "AWSManagedRulesCommonRuleSet",
      "Priority": 2,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesCommonRuleSet",
          "ExcludedRules": []
        }
      },
      "OverrideAction": {
        "None": {}
      },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "CommonRuleSet"
      }
    },
    {
      "Name": "SQLiProtection",
      "Priority": 3,
      "Statement": {
        "ManagedRuleGroupStatement": {
          "VendorName": "AWS",
          "Name": "AWSManagedRulesSQLiRuleSet"
        }
      },
      "OverrideAction": {
        "None": {}
      },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "SQLiProtection"
      }
    },
    {
      "Name": "GeoBlocking",
      "Priority": 4,
      "Statement": {
        "GeoMatchStatement": {
          "CountryCodes": ["CN", "RU", "KP"]
        }
      },
      "Action": {
        "Block": {}
      },
      "VisibilityConfig": {
        "SampledRequestsEnabled": true,
        "CloudWatchMetricsEnabled": true,
        "MetricName": "GeoBlocking"
      }
    }
  ]
}
```

### Shield and DDoS Protection

**AWS Shield Standard**
- Automatic protection (all AWS customers)
- Layer 3/4 DDoS protection
- No additional cost

**AWS Shield Advanced**
- Enhanced DDoS protection ($3,000/month)
- 24/7 DDoS Response Team (DRT)
- Cost protection (DDoS-related scaling costs)
- Real-time attack notifications
- Advanced attack analytics

```yaml
Resources:
  ShieldProtection:
    Type: AWS::Shield::Protection
    Properties:
      Name: ALB-Protection
      ResourceArn: !Ref ApplicationLoadBalancer

  DRTAccess:
    Type: AWS::Shield::DRTAccess
    Properties:
      RoleArn: !GetAtt DRTRole.Arn
      LogBucketList:
        - !Ref DDoSLogBucket
```

## VPC Flow Logs

### Flow Log Configuration

**Flow Log Formats**
```bash
# Default format
${version} ${account-id} ${interface-id} ${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status}

# Custom format with additional fields
${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${tcp-flags} ${type} ${pkt-srcaddr} ${pkt-dstaddr} ${action} ${log-status}
```

**CloudFormation Configuration**
```yaml
Resources:
  VPCFlowLogRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: vpc-flow-logs.amazonaws.com
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: CloudWatchLogPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'logs:CreateLogGroup'
                  - 'logs:CreateLogStream'
                  - 'logs:PutLogEvents'
                  - 'logs:DescribeLogGroups'
                  - 'logs:DescribeLogStreams'
                Resource: '*'

  FlowLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: /aws/vpc/flowlogs
      RetentionInDays: 7

  VPCFlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      ResourceType: VPC
      ResourceIds:
        - !Ref VPC
      TrafficType: ALL  # ACCEPT, REJECT, or ALL
      LogDestinationType: cloud-watch-logs
      LogGroupName: !Ref FlowLogGroup
      DeliverLogsPermissionArn: !GetAtt VPCFlowLogRole.Arn
      LogFormat: '${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${packets} ${bytes} ${start} ${end} ${action} ${log-status}'
      MaxAggregationInterval: 60

  # Flow logs to S3
  S3FlowLog:
    Type: AWS::EC2::FlowLog
    Properties:
      ResourceType: VPC
      ResourceIds:
        - !Ref VPC
      TrafficType: ALL
      LogDestinationType: s3
      LogDestination: !Sub 'arn:aws:s3:::${FlowLogBucket}'
      LogFormat: '${srcaddr} ${dstaddr} ${srcport} ${dstport} ${protocol} ${action}'
```

### Flow Log Analysis

**Athena Queries for Flow Logs**
```sql
-- Create table for S3-based flow logs
CREATE EXTERNAL TABLE IF NOT EXISTS vpc_flow_logs (
  version int,
  account string,
  interfaceid string,
  sourceaddress string,
  destinationaddress string,
  sourceport int,
  destinationport int,
  protocol int,
  numpackets int,
  numbytes bigint,
  starttime int,
  endtime int,
  action string,
  logstatus string
)
PARTITIONED BY (dt string)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ' '
LOCATION 's3://your-bucket/prefix/AWSLogs/{account_id}/vpcflowlogs/{region}/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Find top talkers
SELECT sourceaddress, destinationaddress, SUM(numbytes) as total_bytes
FROM vpc_flow_logs
WHERE dt = '2024-01-01'
GROUP BY sourceaddress, destinationaddress
ORDER BY total_bytes DESC
LIMIT 20;

-- Find rejected connections
SELECT sourceaddress, destinationaddress, sourceport, destinationport, protocol, COUNT(*) as reject_count
FROM vpc_flow_logs
WHERE action = 'REJECT' AND dt = '2024-01-01'
GROUP BY sourceaddress, destinationaddress, sourceport, destinationport, protocol
ORDER BY reject_count DESC;

-- Detect port scanning
SELECT sourceaddress, COUNT(DISTINCT destinationport) as unique_ports, COUNT(*) as attempts
FROM vpc_flow_logs
WHERE dt = '2024-01-01'
GROUP BY sourceaddress
HAVING COUNT(DISTINCT destinationport) > 100
ORDER BY unique_ports DESC;

-- Traffic to specific ports
SELECT sourceaddress, COUNT(*) as attempts
FROM vpc_flow_logs
WHERE destinationport = 22 AND action = 'REJECT' AND dt = '2024-01-01'
GROUP BY sourceaddress
ORDER BY attempts DESC;
```

## Network Troubleshooting

### Common Connectivity Issues

**Issue: Cannot connect to EC2 instance**

Troubleshooting steps:
1. Check security group inbound rules
2. Check NACL rules (both inbound and outbound)
3. Check route table for correct routes
4. Verify instance is running
5. Check instance has public/Elastic IP (if accessing from internet)
6. Verify VPC has Internet Gateway attached
7. Check OS-level firewall (iptables, Windows Firewall)

**Issue: Instances cannot access internet**

Troubleshooting steps:
1. Check route table has route to IGW (0.0.0.0/0 -> igw-xxx)
2. Verify NACL allows outbound traffic
3. Check security group allows outbound traffic
4. For private subnets, verify NAT Gateway exists and is healthy
5. Check NAT Gateway route (0.0.0.0/0 -> nat-xxx)
6. Verify NAT Gateway has Elastic IP
7. Check DNS resolution (VPC DNS settings)

**Issue: VPN tunnel down**

Troubleshooting steps:
1. Check customer gateway configuration
2. Verify IPsec parameters match (encryption, authentication)
3. Check pre-shared key
4. Verify BGP configuration (if using dynamic routing)
5. Check firewall allows UDP 500, UDP 4500
6. Verify routes are propagated
7. Check tunnel status in AWS Console
8. Review CloudWatch metrics for VPN

### VPC Reachability Analyzer

**Analyze Network Path**
```bash
# Create reachability analysis
aws ec2 create-network-insights-path \
    --source i-1234567890abcdef0 \
    --destination i-0987654321fedcba0 \
    --destination-port 443 \
    --protocol tcp

# Start analysis
aws ec2 start-network-insights-analysis \
    --network-insights-path-id nip-xxxxx

# Get results
aws ec2 describe-network-insights-analyses \
    --network-insights-analysis-ids nia-xxxxx
```

**Common Analysis Results**
- Security group blocking traffic
- NACL denying traffic
- No route to destination
- IGW not attached
- Instance not in running state

### Packet Capture

**Using VPC Traffic Mirroring**
```yaml
Resources:
  # Mirror target (Network Load Balancer)
  MirrorTargetNLB:
    Type: AWS::EC2::TrafficMirrorTarget
    Properties:
      NetworkLoadBalancerArn: !Ref AnalysisNLB
      Description: Traffic analysis NLB

  # Mirror filter
  MirrorFilter:
    Type: AWS::EC2::TrafficMirrorFilter
    Properties:
      Description: Capture all traffic
      NetworkServices:
        - amazon-dns

  # Ingress rule
  MirrorFilterIngressRule:
    Type: AWS::EC2::TrafficMirrorFilterRule
    Properties:
      TrafficMirrorFilterId: !Ref MirrorFilter
      TrafficDirection: ingress
      RuleNumber: 100
      RuleAction: accept
      Protocol: -1
      SourceCidrBlock: 0.0.0.0/0
      DestinationCidrBlock: 0.0.0.0/0

  # Egress rule
  MirrorFilterEgressRule:
    Type: AWS::EC2::TrafficMirrorFilterRule
    Properties:
      TrafficMirrorFilterId: !Ref MirrorFilter
      TrafficDirection: egress
      RuleNumber: 100
      RuleAction: accept
      Protocol: -1
      SourceCidrBlock: 0.0.0.0/0
      DestinationCidrBlock: 0.0.0.0/0

  # Mirror session
  MirrorSession:
    Type: AWS::EC2::TrafficMirrorSession
    Properties:
      NetworkInterfaceId: !Ref SourceENI
      TrafficMirrorTargetId: !Ref MirrorTargetNLB
      TrafficMirrorFilterId: !Ref MirrorFilter
      SessionNumber: 1
      PacketLength: 65535
      VirtualNetworkId: 12345
```

### DNS Troubleshooting

**Route 53 Resolver**
```bash
# Query DNS from within VPC
dig @169.254.169.253 example.com

# Test specific nameserver
dig @8.8.8.8 example.com

# Get all DNS records
dig example.com ANY

# Check DNS propagation
dig +trace example.com
```

**Route 53 Resolver Endpoints**
```yaml
Resources:
  # Inbound endpoint (for on-premises to query AWS)
  InboundResolverEndpoint:
    Type: AWS::Route53Resolver::ResolverEndpoint
    Properties:
      Direction: INBOUND
      IpAddresses:
        - SubnetId: !Ref PrivateSubnetA
        - SubnetId: !Ref PrivateSubnetB
      SecurityGroupIds:
        - !Ref ResolverSecurityGroup
      Name: Inbound-Resolver

  # Outbound endpoint (for AWS to query on-premises)
  OutboundResolverEndpoint:
    Type: AWS::Route53Resolver::ResolverEndpoint
    Properties:
      Direction: OUTBOUND
      IpAddresses:
        - SubnetId: !Ref PrivateSubnetA
        - SubnetId: !Ref PrivateSubnetB
      SecurityGroupIds:
        - !Ref ResolverSecurityGroup
      Name: Outbound-Resolver

  # Forwarding rule for on-premises domain
  ResolverRule:
    Type: AWS::Route53Resolver::ResolverRule
    Properties:
      DomainName: onprem.example.com
      RuleType: FORWARD
      ResolverEndpointId: !Ref OutboundResolverEndpoint
      TargetIps:
        - Ip: 192.168.1.10
          Port: 53
        - Ip: 192.168.1.11
          Port: 53

  # Associate rule with VPC
  ResolverRuleAssociation:
    Type: AWS::Route53Resolver::ResolverRuleAssociation
    Properties:
      ResolverRuleId: !Ref ResolverRule
      VPCId: !Ref VPC
```

## Performance Optimization

### Enhanced Networking

**Instance Types with Enhanced Networking**
- ENA (Elastic Network Adapter): Up to 100 Gbps
- Intel 82599 VF: Up to 10 Gbps (older instances)

**Enable ENA**
```bash
# Check if ENA is enabled
aws ec2 describe-instances \
    --instance-ids i-1234567890abcdef0 \
    --query 'Reservations[].Instances[].EnaSupport'

# Modify instance attribute
aws ec2 modify-instance-attribute \
    --instance-id i-1234567890abcdef0 \
    --ena-support
```

### Placement Groups

**Types**
- **Cluster**: Low latency, high throughput (same AZ)
- **Partition**: Isolated hardware failures (multi-AZ)
- **Spread**: Strict instance placement (max 7 per AZ)

```yaml
Resources:
  ClusterPlacementGroup:
    Type: AWS::EC2::PlacementGroup
    Properties:
      Strategy: cluster

  SpreadPlacementGroup:
    Type: AWS::EC2::PlacementGroup
    Properties:
      Strategy: spread

  Instance:
    Type: AWS::EC2::Instance
    Properties:
      PlacementGroupName: !Ref ClusterPlacementGroup
      InstanceType: c5n.18xlarge  # Network-optimized
```

### Jumbo Frames (MTU)

**MTU Sizes**
- Default: 1500 bytes
- Jumbo frames: 9001 bytes (within VPC)
- Internet: 1500 bytes max

**Test MTU**
```bash
# Test with 8972 bytes (9000 - 28 header)
ping -M do -s 8972 10.0.1.100

# Check MTU on interface
ip link show eth0
```

## Monitoring and Metrics

### VPC Metrics to Monitor

**CloudWatch Metrics**
```python
import boto3

cloudwatch = boto3.client('cloudwatch')

# VPN tunnel status
cloudwatch.put_metric_alarm(
    AlarmName='VPN-Tunnel-Down',
    MetricName='TunnelState',
    Namespace='AWS/VPN',
    Statistic='Maximum',
    Period=60,
    EvaluationPeriods=2,
    Threshold=0,
    ComparisonOperator='LessThanThreshold',
    Dimensions=[
        {'Name': 'VpnId', 'Value': 'vpn-xxxxx'},
        {'Name': 'TunnelIpAddress', 'Value': '52.1.2.3'}
    ]
)

# NAT Gateway packet drop
cloudwatch.put_metric_alarm(
    AlarmName='NAT-Gateway-PacketDrop',
    MetricName='PacketsDropCount',
    Namespace='AWS/NATGateway',
    Statistic='Sum',
    Period=300,
    EvaluationPeriods=1,
    Threshold=1000,
    ComparisonOperator='GreaterThanThreshold',
    Dimensions=[
        {'Name': 'NatGatewayId', 'Value': 'nat-xxxxx'}
    ]
)
```

## Exam Tips

### Security Concepts
- Security Groups: Stateful, allow only, instance-level
- NACLs: Stateless, allow/deny, subnet-level
- Network Firewall: Deep packet inspection, IPS
- WAF: Application layer protection
- Shield: DDoS protection

### Troubleshooting Approach
1. Check security groups and NACLs
2. Verify route tables
3. Check gateway attachments (IGW, NAT, VGW)
4. Review VPC Flow Logs
5. Use Reachability Analyzer
6. Check DNS configuration
7. Verify instance-level settings

### Common Scenarios
- No internet access: Check IGW, route table, NAT Gateway
- Cannot SSH: Security group, NACL, key pair
- VPN issues: IPsec config, routing, firewall
- Slow performance: Enhanced networking, placement groups, MTU
- DNS resolution: Route 53 Resolver, VPC DNS settings

### Best Practices
- Use security groups as primary firewall
- NACLs for additional subnet-level protection
- Enable VPC Flow Logs for all VPCs
- Monitor with CloudWatch alarms
- Use WAF for web applications
- Enable Shield Advanced for critical resources
- Regular security audits
- Document network architecture

## Key terms

- **Network ACL** - a stateless, subnet-level firewall with numbered allow and deny rules.
- **Security group** - a stateful, instance-level firewall that supports allow rules only.
- **VPC Flow Logs** - a feature that records IP traffic metadata for network interfaces, subnets or VPCs.
- **Reachability Analyzer** - a tool that tests whether a path between two resources is reachable and finds the blocking component.
- **AWS Network Firewall** - a managed, stateful network firewall and intrusion prevention service for VPCs.
- **Traffic Mirroring** - a feature that copies network traffic from an elastic network interface to a monitoring appliance.
