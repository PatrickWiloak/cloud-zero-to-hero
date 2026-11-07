# Capabilities of Power Automate and Power Virtual Agents

## Overview
This domain covers Power Automate flow types, automation capabilities, Power Virtual Agents chatbot creation, and integration scenarios. Together these topics represent 20-30% of the exam and focus on process automation and conversational AI.

## Key Topics

### Power Automate Types
- Cloud flows: Automated (event-triggered)
- Cloud flows: Instant (manually triggered)
- Cloud flows: Scheduled (time-based)
- Desktop flows (Robotic Process Automation - RPA)
- Business process flows (guided processes)

### Building Flows
- Creating flows from templates
- Using triggers (When, How, What)
- Using actions (Create, Update, Send, etc.)
- Flow control (conditions, loops, parallel branches)
- Flow sharing and management
- Error handling and retry logic

### Power Automate Integration
- Integration with Power Apps and Power BI
- Approval workflows
- Document generation and processing
- Email and notification automation
- Data synchronization between systems

### Power Virtual Agents Capabilities
- Creating chatbots without code
- Publishing bots to multiple channels (Teams, website, Facebook)
- Bot analytics and performance monitoring
- AI-powered natural language understanding

### Building Chatbots
- Topics and trigger phrases configuration
- Conversation flow design with nodes
- Using entities for information extraction
- Variables for maintaining context
- Integration with Power Automate flows
- Integration with other Power Platform components

## Services Reference

### Power Automate Components
- Power Automate cloud flows
- Power Automate Desktop (RPA)
- AI Builder (for intelligent automation)
- Approvals center
- Process advisor

### Power Virtual Agents Components
- Bot creation canvas
- Topics and entities
- Analytics dashboard
- Bot channels (Teams, Web, etc.)
- Pre-built content from templates

### Integration Points
- 350+ connectors
- Custom connectors
- HTTP requests
- Azure services
- Microsoft 365 services

## Best Practices

### Flow Design
- Use meaningful names for flows and actions
- Implement error handling with scope and try-catch
- Add comments for complex logic
- Use variables to make flows maintainable
- Test flows thoroughly before deployment
- Monitor flow run history regularly

### Approval Workflows
- Clearly define approval criteria
- Set appropriate timeouts
- Include relevant information in approval requests
- Implement escalation paths
- Send notifications for status changes
- Track approval history

### RPA Best Practices
- Start with simple, repetitive tasks
- Document manual process steps first
- Use UI selectors carefully
- Implement error recovery
- Use attended vs unattended appropriately
- Monitor desktop flow execution

### Chatbot Design
- Start with FAQ topics from existing documentation
- Use clear, conversational language
- Implement fallback topics for unknown questions
- Test with real user questions
- Monitor conversation analytics
- Iterate based on user feedback

## Common Scenarios

### Power Automate Use Cases
- Approval workflow for expense reports
- Daily summary email from SharePoint list
- Social media post monitoring and response
- File synchronization between systems
- Lead notification from forms
- Invoice processing automation

### Desktop Flow (RPA) Use Cases
- Data entry from email to ERP system
- Legacy application automation
- Report generation from multiple systems
- Screen scraping for data extraction
- File processing and organization

### Power Virtual Agents Use Cases
- IT help desk support bot
- FAQ automation for customer service
- Employee onboarding assistant
- HR policy information bot
- Store locator and hours bot
- Order status inquiry bot

### Integration Scenarios
- Power App triggering approval flow
- Chatbot calling Power Automate for data
- Flow updating Power BI dataset
- Approval notification in Teams
- Form submission triggering email
- Dataverse update triggering notification

## Study Tips

- Understand the three types of cloud flows and when to use each
- Practice creating flows from templates
- Learn common triggers and actions
- Understand approval flow configuration
- Study condition and loop controls
- Learn about desktop flows and RPA concepts
- Practice creating chatbot topics
- Understand entities and their role in chatbots
- Study bot analytics and monitoring
- Learn how Power Virtual Agents integrates with Power Automate

## Key terms

- **Cloud flow** - a Power Automate flow that runs in the cloud and is started by an automatic, instant or scheduled trigger.
- **Automated flow** - a cloud flow that starts when an event occurs, such as a new email arriving.
- **Instant flow** - a cloud flow that a user starts manually, for example with a button.
- **Scheduled flow** - a cloud flow that runs at set times or intervals.
- **Desktop flow** - a Power Automate flow that automates actions in desktop applications, known as robotic process automation.
- **Connector** - a wrapper around a service's API that lets apps and flows work with that service.
- **Premium connector** - a connector that needs a paid Power Platform licence rather than one included with Microsoft 365.
- **AI Builder** - a Power Platform capability that adds AI models, such as form processing, to apps and flows.
