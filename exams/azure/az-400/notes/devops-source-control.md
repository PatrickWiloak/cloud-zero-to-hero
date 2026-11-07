# DevOps Source Control and Collaboration

## Overview
Effective source control and collaboration are fundamental to DevOps practices. This covers Git workflows, branching strategies, repository management, and team collaboration using Azure Repos and GitHub.

## Source Control Strategy

### Version Control Systems

#### Git Fundamentals
- **Distributed version control system**
- **Local repository:** Full history on each machine
- **Remote repository:** Centralized collaboration (Azure Repos, GitHub)
- **Key concepts:**
  - Commits: Snapshots of code
  - Branches: Parallel development lines
  - Merges: Combining branches
  - Pull requests: Code review and collaboration

#### Git vs Centralized VCS
| Feature | Git (Distributed) | TFVC (Centralized) |
|---------|------------------|-------------------|
| Repository | Full copy locally | Partial working copy |
| Offline work | Yes | Limited |
| Branching | Lightweight, fast | Heavier |
| Merging | Powerful, automated | More manual |
| Performance | Fast | Depends on server |

### Authentication Strategies

#### Personal Access Tokens (PATs)
- **Use case:** Automated scripts, CI/CD, Git operations
- **Benefits:**
  - Scoped permissions
  - Revocable
  - Expiration dates
- **Security:** Store in Key Vault, never commit to code

#### SSH Keys
- **Use case:** Git operations without passwords
- **Setup:**
  ```bash
  # Generate SSH key
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  
  # Add to ssh-agent
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa
  
  # Add public key to Azure DevOps/GitHub
  cat ~/.ssh/id_rsa.pub
  ```

#### OAuth/Azure AD Integration
- **Use case:** Web applications, automated services
- **Benefits:**
  - No password storage
  - Token-based authentication
  - Azure AD integration
  - Conditional Access support

### Managing Large Files

#### Git LFS (Large File Storage)
- **Purpose:** Handle large binary files efficiently
- **How it works:**
  - Stores pointer in Git
  - Actual file in LFS storage
  - Downloads on checkout

```bash
# Install Git LFS
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.mp4"

# Commit .gitattributes
git add .gitattributes
git commit -m "Track large files with LFS"
```

#### Repository Size Management
- **Strategies:**
  - Use .gitignore for build artifacts
  - Avoid committing binaries
  - Use package management for dependencies
  - Clean up history if needed (carefully)
  - Archive old branches

## Branching Strategies

### Git Flow

#### Overview
- **Best for:** Release-based software development
- **Branches:**
  - **main/master:** Production-ready code
  - **develop:** Integration branch
  - **feature/*:** New features
  - **release/*:** Release preparation
  - **hotfix/*:** Emergency production fixes

#### Workflow
```bash
# Create feature branch
git checkout -b feature/user-authentication develop

# Work on feature, commit changes
git add .
git commit -m "Add user authentication"

# Merge back to develop
git checkout develop
git merge --no-ff feature/user-authentication

# Create release branch
git checkout -b release/1.0.0 develop

# Merge release to main and develop
git checkout main
git merge --no-ff release/1.0.0
git tag -a v1.0.0

git checkout develop
git merge --no-ff release/1.0.0
```

#### Pros and Cons
**Pros:**
- Clear separation of concerns
- Good for versioned releases
- Supports parallel development

**Cons:**
- Complex for continuous deployment
- More branches to manage
- Merge overhead

### GitHub Flow

#### Overview
- **Best for:** Continuous deployment
- **Simpler than Git Flow**
- **Branches:**
  - **main:** Always deployable
  - **feature branches:** All work done here

#### Workflow
```bash
# Create feature branch
git checkout -b add-payment-gateway main

# Work and commit
git add .
git commit -m "Implement payment gateway"

# Push and create pull request
git push origin add-payment-gateway

# After PR review and approval, merge to main
# Deploy from main (automated)
```

#### Pros and Cons
**Pros:**
- Simple and straightforward
- Perfect for CD
- Fewer branches to manage

**Cons:**
- Less suitable for versioned releases
- Main must always be deployable

### Trunk-Based Development

#### Overview
- **Philosophy:** Everyone commits to trunk (main) frequently
- **Short-lived branches:** Hours to 1-2 days max
- **Feature flags:** Control feature rollout

#### Implementation
```bash
# Work directly on main or very short-lived branches
git checkout main
git pull

# Make small changes
git add .
git commit -m "Small incremental change"
git push

# Or short-lived branch
git checkout -b quick-fix main
# Work (< 1 day)
git push
# Create PR, merge same day
```

#### Pros and Cons
**Pros:**
- Reduces merge conflicts
- Faster integration
- Encourages small commits
- Good for CI/CD

**Cons:**
- Requires discipline
- Needs feature flags
- Requires good testing

### Release Flow (Microsoft)

#### Overview
- **Used by:** Microsoft for Azure DevOps
- **Combines:** Trunk-based + release branches

#### Branches
- **main:** Development happens here
- **release/*:** Created for releases
- **topic branches:** Short-lived feature branches

## Pull Request Guidelines

### PR Best Practices

#### Creating Effective PRs
1. **Small and focused:** One logical change
2. **Descriptive title:** Clear purpose
3. **Detailed description:**
   - What changed and why
   - Related work items
   - Testing performed
4. **Link work items:** Traceability
5. **Self-review:** Check your own code first

#### PR Template Example
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Work Items
- Fixes #123
- Related to #456

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No new warnings generated
```

### Branch Policies

#### Required Reviewers
```yaml
# Azure DevOps branch policy
- Minimum number of reviewers: 2
- Allow requestors to approve own changes: No
- Require specific reviewers:
  - Security team for /security/*
  - Platform team for /infrastructure/*
```

#### Build Validation
- **Require successful build** before merge
- **Build definition:** CI pipeline
- **Policy:** Block if build fails

#### Status Checks
- **Required:** All status checks must pass
- **Examples:**
  - Unit tests
  - Code coverage
  - Security scanning
  - Linting

#### Comment Requirements
- **Resolve all comments:** Before merge
- **Required approvals:** At least N approvals
- **Block with rejection:** Any reviewer can block

### Code Review Guidelines

#### Reviewer Responsibilities
1. **Understand the change:** Read description and code
2. **Check logic:** Does it work correctly?
3. **Check tests:** Adequate test coverage?
4. **Check style:** Follows coding standards?
5. **Check security:** Any security concerns?
6. **Provide feedback:** Constructive comments
7. **Timely response:** Within agreed SLA

#### Comment Types
- **Must fix:** Blocking issues
- **Should fix:** Important improvements
- **Consider:** Suggestions
- **Question:** Need clarification
- **Praise:** Acknowledge good work

## Repository Configuration

### Repository Permissions

#### Azure Repos Permissions
- **Readers:** Read only
- **Contributors:** Read, commit, create branches
- **Build Administrators:** Manage build definitions
- **Project Administrators:** Full control

#### Branch Permissions
- **main/master:**
  - Deny direct pushes
  - Require PR
  - Limit who can approve
- **develop:**
  - Allow direct push for small fixes
  - Encourage PRs
- **feature/*:**
  - Open to all contributors

### Git Hooks

#### Client-Side Hooks
```bash
# pre-commit hook (.git/hooks/pre-commit)
#!/bin/sh
# Run linter before commit
npm run lint
if [ $? -ne 0 ]; then
    echo "Linting failed. Commit aborted."
    exit 1
fi

# Run tests
npm test
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

#### Server-Side Hooks (Azure DevOps)
- **Pre-receive:** Validate before accepting push
- **Post-receive:** Trigger builds, notifications
- **Update:** Validate individual branch updates

### Workflow Hooks

#### Azure DevOps Service Hooks
```json
{
  "publisherId": "tfs",
  "eventType": "git.push",
  "resourceVersion": "1.0",
  "consumerId": "webHooks",
  "consumerActionId": "httpRequest",
  "publisherInputs": {
    "repository": "MyRepo",
    "branch": "refs/heads/main"
  },
  "consumerInputs": {
    "url": "https://myservice.com/webhook"
  }
}
```

**Common use cases:**
- Trigger external CI/CD
- Send notifications (Slack, Teams)
- Update external tracking systems
- Trigger security scans

## Monorepo vs Multi-Repo

### Monorepo Strategy

#### Characteristics
- **Single repository** for multiple projects
- **Shared code:** Easy to share and refactor
- **Atomic changes:** Change multiple projects together
- **Single version:** All code at same version

#### Pros
- Easy refactoring across projects
- Simplified dependency management
- Code reuse
- Single source of truth

#### Cons
- Large repository size
- Build complexity
- Access control challenges
- Clone time

#### When to Use
- Tightly coupled microservices
- Shared libraries across projects
- Need atomic changes across components

### Multi-Repo Strategy

#### Characteristics
- **Separate repositories** for each project
- **Independent versioning**
- **Clear ownership**
- **Smaller repositories**

#### Pros
- Clear boundaries
- Independent release cycles
- Easier access control
- Smaller clones

#### Cons
- Dependency management complexity
- Harder to make cross-repo changes
- Code duplication risk

#### When to Use
- Independent services
- Different teams/organizations
- Different release schedules
- Need strict access control

## Best Practices

### Commit Practices
1. **Frequent commits:** Integrate often
2. **Atomic commits:** One logical change per commit
3. **Good commit messages:** Descriptive and clear
4. **Never commit secrets:** Use Key Vault
5. **Keep main/master stable:** Always deployable

### Branch Management
1. **Delete merged branches:** Keep repository clean
2. **Protect important branches:** Branch policies
3. **Short-lived branches:** Merge within days
4. **Descriptive branch names:** feature/description-of-work
5. **Sync regularly:** Pull from main frequently

### Collaboration
1. **Small pull requests:** Easier to review
2. **Request reviews promptly:** Don't delay
3. **Respond to feedback:** Timely and respectfully
4. **Link work items:** Maintain traceability
5. **Document decisions:** In PR descriptions

### Security
1. **Use .gitignore:** Prevent sensitive files
2. **Scan for secrets:** Pre-commit hooks
3. **Use PATs with expiration:** Regular rotation
4. **Limit repository access:** Least privilege
5. **Enable security scanning:** Dependabot, CodeQL

## Study Tips

### Key Concepts
- Git flow vs GitHub flow vs Trunk-based development
- Branch policies and their purposes
- Pull request workflow and best practices
- Authentication methods (PAT, SSH, OAuth)
- Git hooks for automation

### Common Scenarios
1. **Versioned releases** → Git Flow
2. **Continuous deployment** → GitHub Flow or Trunk-based
3. **Large binary files** → Git LFS
4. **Code quality enforcement** → Branch policies + PR requirements
5. **Automated validation** → Build policies + git hooks

### Exam Focus
- Branching strategies and when to use each
- Configuring branch policies
- PR workflows and best practices
- Repository permission models
- Git hooks and service hooks

### Remember
- Git Flow = Complex, release-based
- GitHub Flow = Simple, continuous deployment
- Trunk-based = Frequent integration, feature flags
- Branch policies enforce quality
- PRs enable collaboration and review
- Protect main/master branch always

## Key terms

- **Branch policy** - a rule on a branch, such as required reviewers or a passing build, that must be met before a pull request can complete.
- **Trunk-based development** - a branching strategy where developers merge small changes into one main branch frequently.
- **Squash merge** - a merge that combines all commits of a branch into a single commit on the target branch.
- **Git LFS** - an extension that stores large binary files outside the repository and keeps pointers in Git.
