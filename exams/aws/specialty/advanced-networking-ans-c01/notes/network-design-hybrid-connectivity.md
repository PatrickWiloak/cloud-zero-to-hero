# Network Design and Hybrid Connectivity

## VPC Design and Architecture

### Multi-Tier VPC Architecture

**Reference Architecture**
```
VPC: 10.0.0.0/16

Availability Zone A (us-east-1a)
├── Public Subnet A: 10.0.1.0/24
│   ├── NAT Gateway A
│   ├── Application Load Balancer
│   └── Bastion Host
├── Private Subnet A (App): 10.0.10.0/24
│   ├── Application Servers
│   └── Auto Scaling Group
└── Private Subnet A (Data): 10.0.20.0/24
    ├── RDS Primary
    └── ElastiCache

Availability Zone B (us-east-1b)
├── Public Subnet B: 10.0.2.0/24
│   ├── NAT Gateway B
│   └── ALB (multi-AZ)
├── Private Subnet B (App): 10.0.11.0/24
│   ├── Application Servers
│   └── Auto Scaling Group
└── Private Subnet B (Data): 10.0.21.0/24
    ├── RDS Standby
    └── ElastiCache Replica
```

**CloudFormation VPC Template**
```yaml
Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: Production-VPC

  # Public Subnets
  PublicSubnetA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Public-Subnet-A

  PublicSubnetB:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: Public-Subnet-B

  # Private Subnets - Application Tier
  PrivateSubnetAppA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.10.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-App-Subnet-A

  PrivateSubnetAppB:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.11.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-App-Subnet-B

  # Private Subnets - Data Tier
  PrivateSubnetDataA:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.20.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-Data-Subnet-A

  PrivateSubnetDataB:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.21.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      Tags:
        - Key: Name
          Value: Private-Data-Subnet-B

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: Production-IGW

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # NAT Gateways
  NATGatewayAEIP:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc

  NATGatewayA:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGatewayAEIP.AllocationId
      SubnetId: !Ref PublicSubnetA
      Tags:
        - Key: Name
          Value: NAT-Gateway-A

  NATGatewayBEIP:
    Type: AWS::EC2::EIP
    DependsOn: AttachGateway
    Properties:
      Domain: vpc

  NATGatewayB:
    Type: AWS::EC2::NatGateway
    Properties:
      AllocationId: !GetAtt NATGatewayBEIP.AllocationId
      SubnetId: !Ref PublicSubnetB
      Tags:
        - Key: Name
          Value: NAT-Gateway-B

  # Route Tables
  PublicRouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Public-Route-Table

  PublicRoute:
    Type: AWS::EC2::Route
    DependsOn: AttachGateway
    Properties:
      RouteTableId: !Ref PublicRouteTable
      DestinationCidrBlock: 0.0.0.0/0
      GatewayId: !Ref InternetGateway

  PublicSubnetARouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetA
      RouteTableId: !Ref PublicRouteTable

  PublicSubnetBRouteTableAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref PublicSubnetB
      RouteTableId: !Ref PublicRouteTable

  # Private Route Table A
  PrivateRouteTableA:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Private-Route-Table-A

  PrivateRouteA:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTableA
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NATGatewayA

  # Private Route Table B
  PrivateRouteTableB:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags:
        - Key: Name
          Value: Private-Route-Table-B

  PrivateRouteB:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref PrivateRouteTableB
      DestinationCidrBlock: 0.0.0.0/0
      NatGatewayId: !Ref NATGatewayB
```

### IP Address Planning

**CIDR Block Sizing**
| Subnet Size | CIDR | Usable IPs | Use Case |
|------------|------|------------|----------|
| /28 | x.x.x.0/28 | 11 | Small services, endpoints |
| /27 | x.x.x.0/27 | 27 | Small workloads |
| /26 | x.x.x.0/26 | 59 | Medium workloads |
| /25 | x.x.x.0/25 | 123 | Large workloads |
| /24 | x.x.x.0/24 | 251 | Standard subnet |
| /23 | x.x.x.0/23 | 507 | Very large subnet |
| /22 | x.x.x.0/22 | 1019 | Extra large |
| /21 | x.x.x.0/21 | 2043 | Massive scale |

**Multi-Region IP Planning**
```
Organization CIDR: 10.0.0.0/8

Region: us-east-1 (10.0.0.0/12)
├── Production VPC: 10.0.0.0/16
│   ├── Public: 10.0.0.0/20
│   ├── Private App: 10.0.16.0/20
│   └── Private Data: 10.0.32.0/20
├── Development VPC: 10.1.0.0/16
└── Test VPC: 10.2.0.0/16

Region: us-west-2 (10.16.0.0/12)
├── Production VPC: 10.16.0.0/16
├── Development VPC: 10.17.0.0/16
└── DR VPC: 10.18.0.0/16

Region: eu-west-1 (10.32.0.0/12)
└── Production VPC: 10.32.0.0/16
```

## AWS Direct Connect

### Direct Connect Architecture

**Components**
- Customer Router (on-premises)
- Direct Connect Location (AWS facility)
- Customer Cage/Cross-Connect
- AWS Direct Connect Router
- Virtual Interfaces (VIFs)
  - Private VIF: Access VPC
  - Public VIF: Access AWS public services
  - Transit VIF: Access Transit Gateway

**Connection Types**
| Type | Bandwidth | Provider | Use Case |
|------|-----------|----------|----------|
| Dedicated | 1 Gbps, 10 Gbps, 100 Gbps | AWS Direct | Consistent high bandwidth |
| Hosted | 50 Mbps to 10 Gbps | APN Partner | Flexible bandwidth, shared |

**High Availability Direct Connect**
```
On-Premises
    ├── Router A ─────────┐
    │                      │
    └── Router B ─────────┤
                          │
                          ▼
            Direct Connect Location 1
                ├── DX Connection 1 (Active)
                └── DX Connection 2 (Standby)
                          │
                          ▼
            Direct Connect Location 2
                ├── DX Connection 3 (Active)
                └── DX Connection 4 (Standby)
                          │
                          ▼
                    AWS Region
                    ├── VGW or TGW
                    └── VPC
```

### Virtual Interfaces (VIFs)

**Private VIF Configuration**
```bash
# Create private VIF
aws directconnect create-private-virtual-interface \
    --connection-id dxcon-xxxxxx \
    --new-private-virtual-interface \
        virtualInterfaceName=PrivateVIF-Production,\
        vlan=100,\
        asn=65000,\
        authKey=secret123,\
        amazonAddress=169.254.1.1/30,\
        customerAddress=169.254.1.2/30,\
        addressFamily=ipv4,\
        virtualGatewayId=vgw-xxxxxx,\
        tags=[{Key=Environment,Value=Production}]
```

**Public VIF for AWS Services**
```bash
# Create public VIF
aws directconnect create-public-virtual-interface \
    --connection-id dxcon-xxxxxx \
    --new-public-virtual-interface \
        virtualInterfaceName=PublicVIF-S3,\
        vlan=200,\
        asn=65000,\
        authKey=secret456,\
        amazonAddress=169.254.2.1/30,\
        customerAddress=169.254.2.2/30,\
        routeFilterPrefixes=[{cidr=0.0.0.0/0}]
```

**Transit VIF with Transit Gateway**
```yaml
Resources:
  TransitGateway:
    Type: AWS::EC2::TransitGateway
    Properties:
      Description: Central transit gateway
      DefaultRouteTableAssociation: enable
      DefaultRouteTablePropagation: enable
      DnsSupport: enable
      VpnEcmpSupport: enable

  DirectConnectGateway:
    Type: AWS::DirectConnect::Gateway
    Properties:
      AmazonSideAsn: 64512

  TransitGatewayAttachment:
    Type: AWS::EC2::TransitGatewayAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      VpcId: !Ref VPC
      SubnetIds:
        - !Ref PrivateSubnetA
        - !Ref PrivateSubnetB

  DXGatewayAssociation:
    Type: AWS::DirectConnect::GatewayAssociation
    Properties:
      DirectConnectGatewayId: !Ref DirectConnectGateway
      GatewayId: !Ref TransitGateway
```

### LAG (Link Aggregation Groups)

**Benefits**
- Increased bandwidth (up to 4 connections)
- Automatic failover
- Single logical connection
- Consistent routing

```bash
# Create LAG
aws directconnect create-lag \
    --location EqDC2 \
    --number-of-connections 4 \
    --connections-bandwidth 10Gbps \
    --lag-name Production-LAG

# Associate existing connection with LAG
aws directconnect associate-connection-with-lag \
    --connection-id dxcon-xxxxxx \
    --lag-id dxlag-yyyyyy
```

## Site-to-Site VPN

### VPN Architecture

**VPN Components**
- Customer Gateway (CGW): On-premises VPN device
- Virtual Private Gateway (VGW): AWS VPN concentrator
- VPN Connection: IPsec tunnels (2 tunnels for HA)
- Transit Gateway: Central hub for multiple VPNs

**Static vs Dynamic Routing**
| Type | Protocol | Use Case | Complexity |
|------|----------|----------|------------|
| Static | N/A | Simple, few routes | Low |
| Dynamic | BGP | Many routes, automatic failover | Medium |

**VPN CloudFormation**
```yaml
Resources:
  CustomerGateway:
    Type: AWS::EC2::CustomerGateway
    Properties:
      Type: ipsec.1
      BgpAsn: 65000
      IpAddress: 203.0.113.1  # Public IP of on-prem device
      Tags:
        - Key: Name
          Value: OnPremises-CGW

  VPNGateway:
    Type: AWS::EC2::VPNGateway
    Properties:
      Type: ipsec.1
      AmazonSideAsn: 64512
      Tags:
        - Key: Name
          Value: Production-VGW

  VPNGatewayAttachment:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      VpnGatewayId: !Ref VPNGateway

  VPNConnection:
    Type: AWS::EC2::VPNConnection
    Properties:
      Type: ipsec.1
      StaticRoutesOnly: false  # Use BGP
      CustomerGatewayId: !Ref CustomerGateway
      VpnGatewayId: !Ref VPNGateway
      VpnTunnelOptionsSpecifications:
        - TunnelInsideCidr: 169.254.10.0/30
          PreSharedKey: !Ref VPNTunnel1PSK
        - TunnelInsideCidr: 169.254.10.4/30
          PreSharedKey: !Ref VPNTunnel2PSK
      Tags:
        - Key: Name
          Value: Production-VPN

  # Enable route propagation
  VPNRoutePropagation:
    Type: AWS::EC2::VPNGatewayRoutePropagation
    DependsOn: VPNGatewayAttachment
    Properties:
      RouteTableIds:
        - !Ref PrivateRouteTableA
        - !Ref PrivateRouteTableB
      VpnGatewayId: !Ref VPNGateway
```

### Accelerated Site-to-Site VPN

**Benefits**
- Uses AWS Global Accelerator
- Improved performance (up to 60% latency reduction)
- Better throughput for long-distance connections

```bash
# Create accelerated VPN
aws ec2 create-vpn-connection \
    --type ipsec.1 \
    --customer-gateway-id cgw-xxxxxx \
    --vpn-gateway-id vgw-yyyyyy \
    --options "EnableAcceleration=true,TunnelOptions=[{TunnelInsideCidr=169.254.10.0/30},{TunnelInsideCidr=169.254.10.4/30}]"
```

## Transit Gateway

### Transit Gateway Architecture

**Hub-and-Spoke Model**
```
                Transit Gateway
                      │
        ┌─────────────┼─────────────┐
        │             │             │
    VPC-Prod      VPC-Dev      VPC-Shared
        │             │             │
    10.0.0.0/16   10.1.0.0/16   10.2.0.0/16

    VPN Connection (On-Premises)
        │
    192.168.0.0/16

    Direct Connect Gateway
        │
    172.16.0.0/12
```

**Transit Gateway Configuration**
```yaml
Resources:
  TransitGateway:
    Type: AWS::EC2::TransitGateway
    Properties:
      Description: Central hub for all VPCs and on-premises
      AmazonSideAsn: 64512
      DefaultRouteTableAssociation: enable
      DefaultRouteTablePropagation: enable
      DnsSupport: enable
      VpnEcmpSupport: enable
      MulticastSupport: disable
      Tags:
        - Key: Name
          Value: Central-TGW

  # Attach Production VPC
  TGWAttachmentProd:
    Type: AWS::EC2::TransitGatewayAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      VpcId: !Ref ProductionVPC
      SubnetIds:
        - !Ref ProdSubnetA
        - !Ref ProdSubnetB
      Tags:
        - Key: Name
          Value: TGW-Attach-Production

  # Attach Development VPC
  TGWAttachmentDev:
    Type: AWS::EC2::TransitGatewayAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      VpcId: !Ref DevelopmentVPC
      SubnetIds:
        - !Ref DevSubnetA
        - !Ref DevSubnetB

  # VPN Attachment
  TGWVPNAttachment:
    Type: AWS::EC2::TransitGatewayAttachment
    Properties:
      TransitGatewayId: !Ref TransitGateway
      VpnConnectionId: !Ref VPNConnection
```

### Transit Gateway Route Tables

**Isolated Routing Tables**
```yaml
Resources:
  # Production Route Table
  TGWRouteTableProd:
    Type: AWS::EC2::TransitGatewayRouteTable
    Properties:
      TransitGatewayId: !Ref TransitGateway
      Tags:
        - Key: Name
          Value: Production-Routes

  # Development Route Table
  TGWRouteTableDev:
    Type: AWS::EC2::TransitGatewayRouteTable
    Properties:
      TransitGatewayId: !Ref TransitGateway
      Tags:
        - Key: Name
          Value: Development-Routes

  # Shared Services Route Table
  TGWRouteTableShared:
    Type: AWS::EC2::TransitGatewayRouteTable
    Properties:
      TransitGatewayId: !Ref TransitGateway
      Tags:
        - Key: Name
          Value: Shared-Services-Routes

  # Associate Production VPC with Production Route Table
  TGWRouteTableAssociationProd:
    Type: AWS::EC2::TransitGatewayRouteTableAssociation
    Properties:
      TransitGatewayAttachmentId: !Ref TGWAttachmentProd
      TransitGatewayRouteTableId: !Ref TGWRouteTableProd

  # Production can access Shared Services
  TGWRouteProdToShared:
    Type: AWS::EC2::TransitGatewayRoute
    Properties:
      TransitGatewayRouteTableId: !Ref TGWRouteTableProd
      DestinationCidrBlock: 10.2.0.0/16
      TransitGatewayAttachmentId: !Ref TGWAttachmentShared

  # Production can access On-Premises
  TGWRouteProdToOnPrem:
    Type: AWS::EC2::TransitGatewayRoute
    Properties:
      TransitGatewayRouteTableId: !Ref TGWRouteTableProd
      DestinationCidrBlock: 192.168.0.0/16
      TransitGatewayAttachmentId: !Ref TGWVPNAttachment
```

### Transit Gateway Peering

**Cross-Region Connectivity**
```yaml
Resources:
  # Transit Gateway in us-east-1 (already exists)
  TGWEast:
    Type: AWS::EC2::TransitGateway
    Properties:
      AmazonSideAsn: 64512

  # Transit Gateway in us-west-2
  TGWWest:
    Type: AWS::EC2::TransitGateway
    Properties:
      AmazonSideAsn: 64513

  # Peering Attachment
  TGWPeeringAttachment:
    Type: AWS::EC2::TransitGatewayPeeringAttachment
    Properties:
      TransitGatewayId: !Ref TGWEast
      PeerTransitGatewayId: !Ref TGWWest
      PeerAccountId: !Ref AWS::AccountId
      PeerRegion: us-west-2
      Tags:
        - Key: Name
          Value: East-West-Peering

  # Add route in East pointing to West
  TGWRouteEastToWest:
    Type: AWS::EC2::TransitGatewayRoute
    DependsOn: TGWPeeringAttachment
    Properties:
      TransitGatewayRouteTableId: !Ref TGWRouteTableEast
      DestinationCidrBlock: 10.16.0.0/12  # West region CIDR
      TransitGatewayAttachmentId: !Ref TGWPeeringAttachment
```

## VPC Peering

### VPC Peering Limitations
- No transitive peering
- Non-overlapping CIDR blocks
- Cannot peer with IPv6 only
- 125 peering connections per VPC limit

**VPC Peering Configuration**
```yaml
Resources:
  VPCPeeringConnection:
    Type: AWS::EC2::VPCPeeringConnection
    Properties:
      VpcId: !Ref VPCRequester
      PeerVpcId: !Ref VPCAccepter
      PeerOwnerId: !Ref AWS::AccountId
      PeerRegion: !Ref AWS::Region
      Tags:
        - Key: Name
          Value: Prod-to-Shared-Peering

  # Update route tables
  RouteRequester:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref RequesterRouteTable
      DestinationCidrBlock: 10.2.0.0/16
      VpcPeeringConnectionId: !Ref VPCPeeringConnection

  RouteAccepter:
    Type: AWS::EC2::Route
    Properties:
      RouteTableId: !Ref AccepterRouteTable
      DestinationCidrBlock: 10.0.0.0/16
      VpcPeeringConnectionId: !Ref VPCPeeringConnection
```

## Exam Tips

### Key Concepts
- VPC: Isolated virtual network
- Direct Connect: Dedicated physical connection
- VPN: Encrypted tunnel over internet
- Transit Gateway: Hub for VPC and on-premises connectivity
- VPC Peering: Direct VPC-to-VPC connection

### Design Decisions
- **Need high bandwidth, low latency**: Direct Connect
- **Quick setup, encrypted**: Site-to-Site VPN
- **Many VPCs, hub-spoke**: Transit Gateway
- **Simple VPC-to-VPC**: VPC Peering
- **Redundancy**: Multiple DX connections, VPN backup

### Best Practices
- Plan IP addressing carefully (no overlaps)
- Use multiple AZs for high availability
- Implement redundant connections
- Use BGP for dynamic routing
- Monitor connection health
- Document network architecture
- Use Transit Gateway for complex topologies
- VPN as backup for Direct Connect

## Key terms

- **Transit Gateway** - a regional hub that connects VPCs and on-premises networks through attachments and route tables.
- **Direct Connect gateway** - a global resource that connects a Direct Connect connection to VPCs or transit gateways in multiple Regions.
- **Virtual interface (VIF)** - a Direct Connect logical interface; private reaches VPCs, public reaches AWS public services, and transit reaches transit gateways.
- **Site-to-Site VPN** - an IPsec connection between your network and AWS, with two tunnels per connection for redundancy.
- **VPC peering** - a one-to-one private connection between two VPCs that does not support transitive routing.
- **Gateway Load Balancer** - a load balancer that distributes traffic to virtual appliances such as firewalls, using GENEVE encapsulation.
- **AWS Cloud WAN** - a managed service that builds a global network with a core network policy and segments.
- **Route 53 Resolver endpoint** - an inbound or outbound endpoint that forwards DNS queries between a VPC and an on-premises network.
- **PrivateLink** - a service that exposes a service privately to other VPCs through interface endpoints, without internet access or peering.
