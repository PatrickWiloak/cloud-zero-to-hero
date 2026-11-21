# HashiCorp Packer Study Track

## About this track

> **This is a self-directed study track, not a certification guide.** HashiCorp's [certifications page](https://developer.hashicorp.com/certifications) (checked 2026-11-21) lists no Packer exam, only Terraform and Vault exams. Earlier versions of this guide quoted a cost, question count, passing score and domain weights for a "Packer Associate" exam; none of those had a vendor source, so they are removed. The notes, scenarios and labs still teach Packer as it is used in practice.

This track builds foundational knowledge and practical skills for building machine images with HashiCorp Packer. It is aimed at operators, platform engineers, and build engineers who produce immutable images (AMIs, Azure images, GCP images, Docker containers, vSphere templates, and more) as part of a CI/CD or release pipeline.

Packer is the HashiCorp tool for creating identical machine images for multiple platforms from a single source configuration.

## Who this is for

- Build and release engineers producing AMIs or other cloud images
- Platform engineers standardizing golden images for internal consumers
- DevOps engineers integrating Packer into CI pipelines
- Infrastructure operators migrating from manual image creation to repeatable, codified builds

## Topic areas

1. Understand Packer fundamentals
2. Understand and use Packer plugins (builders, provisioners, post-processors)
3. Author and debug HCL2 configuration
4. Integrate Packer with HCP Packer and artifact management
5. Use Packer in CI/CD and multi-cloud workflows
6. Secure images and manage credentials

See `fact-sheet.md` for detailed topics.

## Prerequisites and Recommended Experience

- Comfortable with one of the major clouds. You should know what an AMI is, what regions and AZs are, how security groups and key pairs work.
- Command-line fluency: Bash or PowerShell
- Basic shell scripting for provisioners
- Familiarity with at least one of: Ansible, Chef, Puppet, Shell provisioners
- Working knowledge of HCL (Terraform background helps enormously)
- Understanding of Git and CI/CD pipelines

## Study Path

1. Read `fact-sheet.md` for the topic map.
2. Work through the six notes files in `notes/` sequentially.
3. Follow the week-by-week schedule in `practice-plan.md`.
4. Review `scenarios.md` for real-world decision points.
5. Use `strategy.md` for the common traps.

## Hands-on Lab Requirements

Theoretical understanding is not enough. You need to build real images.

- Packer 1.10 or newer (1.11+ recommended)
- AWS free-tier account (AMI builds on free-tier EC2 work fine)
- Optionally: Azure or GCP sandbox for multi-cloud practice
- Docker Desktop or Docker Engine for container builder practice
- Text editor with HCL syntax support (VS Code + HashiCorp extension)

## Official Resources

- Packer documentation: https://developer.hashicorp.com/packer/docs
- Packer tutorials: https://developer.hashicorp.com/packer/tutorials
- HCP Packer documentation: https://developer.hashicorp.com/hcp/docs/packer
- Packer plugin registry: https://developer.hashicorp.com/packer/integrations

## Recommended Supplementary Resources

- HashiCorp Learn tutorials on building AWS AMIs and Docker images
- Example Packer templates in the `hashicorp/packer-examples` repository
- Packer GitHub repo for release notes and issue tracker
- Ansible documentation for the `ansible` provisioner

## Common Pitfalls to Avoid

- Studying the legacy JSON template format. HCL2 is the current format.
- Assuming Packer and Terraform are interchangeable. They solve different problems.
- Skipping the HCP Packer portion. It is how teams track and promote images.
- Ignoring post-processors. They shape the final artifact.
- Not practicing real builds. Reading docs does not build muscle memory.

## Time Investment Estimate

- 40 to 50 hours total
- 2 to 3 weeks of focused part-time study
- At least 10 hours of hands-on labs (can be compressed into a weekend)

## Cost Awareness

Practice builds create real cloud resources. Packer usually destroys the builder instance after the image is captured, but orphaned EBS snapshots, unregistered AMIs, and AWS Image Builder pipelines can accumulate. Budget alerts at $10 to $20 are adequate for practice.
