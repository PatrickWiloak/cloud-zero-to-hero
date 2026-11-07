# Capabilities of Power Apps

## Overview
This domain covers Power Apps types, building applications, and integration capabilities. It represents 25-30% of the exam and focuses on understanding how to create custom business applications with low-code/no-code development.

## Key Topics

### Power Apps Types
- Canvas apps (pixel-perfect, flexible design)
- Model-driven apps (data-centric, form-based)
- Power Apps portals (external-facing websites)
- Differences and appropriate use cases for each type

### Building Power Apps
- Creating canvas apps from templates
- Creating canvas apps from data sources
- Creating canvas apps from blank
- Creating model-driven apps from Dataverse
- Sharing and publishing applications
- App versioning and updates

### Power Apps Integration
- Connecting to data sources (Dataverse, SharePoint, SQL, etc.)
- Using Power Apps with other Power Platform components
- Common connectors (Office 365, SharePoint, OneDrive)
- Custom connectors for proprietary systems
- Power Apps in Microsoft Teams
- Offline capabilities for mobile apps

## Services Reference

### Core Components
- Power Apps Studio (canvas app designer)
- Model-driven app designer
- Power Apps Mobile (iOS and Android)
- Power Apps portals
- Dataverse (underlying data platform)

### Data Sources and Connectors
- Microsoft Dataverse
- SharePoint
- SQL Server and Azure SQL
- Excel and OneDrive
- Dynamics 365
- 350+ standard connectors
- Custom connectors

## Best Practices

### Canvas App Design
- Design for the target device (phone, tablet, desktop)
- Use consistent navigation patterns
- Implement responsive design principles
- Follow accessibility guidelines
- Keep formulas simple and maintainable
- Use components for reusability

### Model-Driven App Design
- Start with Dataverse tables and relationships
- Use business process flows for guided experiences
- Configure forms for optimal user experience
- Create views for different user roles
- Implement business rules for validation
- Use security roles for access control

### Data Integration
- Choose the right connector for data source
- Implement data validation
- Handle errors gracefully
- Use collections for performance
- Cache data when appropriate
- Implement proper authentication

### Performance Optimization
- Minimize data calls in app startup
- Use delegation for large datasets
- Optimize gallery and collection usage
- Reduce number of controls on screens
- Use concurrent function for parallel calls
- Monitor app performance and errors

## Common Scenarios

### Canvas App Use Cases
- Expense report submission
- Field service inspection forms
- Asset tracking and inventory
- Time and attendance tracking
- Customer feedback collection
- Mobile order entry

### Model-Driven App Use Cases
- CRM for sales management
- Project management system
- Help desk ticketing system
- Event registration and management
- Contract lifecycle management
- Vendor management portal

### Portal Use Cases
- Customer self-service portal
- Partner collaboration platform
- Community forum
- Job application portal
- Knowledge base website
- Event registration site

### Integration Scenarios
- Approval workflow with Power Automate
- Data visualization with Power BI
- SharePoint list as data source
- Teams integration for collaboration
- SQL Server data access
- Dynamics 365 extension

## Study Tips

- Understand when to use canvas vs model-driven apps
- Practice creating apps from templates
- Learn common formulas (Filter, Lookup, Patch, Navigate)
- Understand gallery controls and data binding
- Study Dataverse table creation and relationships
- Learn about delegation and its limitations
- Practice connecting to SharePoint lists
- Understand app sharing and permissions
- Study form types and their purposes
- Learn about business process flows in model-driven apps

## Key terms

- **Power Platform** - the Microsoft low-code platform made up of Power Apps, Power Automate, Power BI and Power Pages.
- **Canvas app** - a Power Apps app where the maker designs the screen layout freely and connects it to data.
- **Model-driven app** - a Power Apps app whose layout is generated from the data model and business processes in Dataverse.
- **Dataverse** - the Microsoft data platform that stores and manages data for Power Platform apps in tables.
- **Table** - the Dataverse structure, formerly called an entity, that holds rows of data in columns.
- **Business rule** - a no-code rule in Dataverse that applies validation or logic to a table.
- **Environment** - a space that holds a set of Power Platform resources, such as apps and flows, and separates them from other sets.
