# Product Development Rules

> **Best practices for startup product development across all industries**

## When to Use Product Development Skill

### Automatic Triggers
Invoke the `startup-product-development` skill when user mentions:
- "product roadmap"
- "MVP" or "minimum viable product"
- "what should I build first"
- "technology stack" or "tech stack"
- "product development plan"
- "product-market fit"
- Industry-specific: "prototype", "manufacturing", "clinical trials"

### Manual Invocation
- User explicitly asks for product development guidance
- User needs help defining MVP scope
- User wants to create a product roadmap
- User needs technology selection recommendations

## MVP Definition Best Practices

### DO:
- Focus on ONE core problem
- Define success metrics before building
- Use MoSCoW prioritization (Must/Should/Could/Won't)
- Target 5-10 features maximum for MVP
- Plan for 8-12 weeks to launch (software)
- Validate with users before and during development
- Build for 10x scale, not 1000x

### DON'T:
- Add "just one more feature" (scope creep)
- Build for edge cases in MVP
- Perfect UI before validating core value
- Skip user testing
- Build features without user validation
- Ignore quality ("it's just an MVP")
- Optimize for scale before validation

## Product Roadmap Planning

### DO:
- Start with Vision → Strategy → Roadmap → Backlog
- Use quarterly themes (not detailed feature lists)
- Prioritize using RICE or MoSCoW
- Allocate 20-30% capacity for technical debt
- Review and adjust quarterly
- Communicate roadmap to stakeholders
- Build in flexibility for pivots

### DON'T:
- Commit to specific dates publicly
- Ignore technical debt indefinitely
- Change priorities mid-sprint
- Build features without strategy alignment
- Skip stakeholder input
- Create 2-year detailed roadmap (too rigid)

## Technology Stack Selection

### DO:
- Choose technologies team already knows
- Bias toward proven, mature technologies
- Consider hiring market for chosen stack
- Use managed services (auth, payments, email)
- Document decision rationale
- Plan migration paths for vendor lock-in risks
- Start simple, upgrade when needed

### DON'T:
- Choose trendy tech without justification
- Over-engineer for hypothetical scale
- Build commodity features (auth, payments)
- Ignore team expertise in selection
- Skip security considerations
- Commit to bleeding-edge untested tech
- Optimize prematurely

## Industry-Specific Rules

### Software/SaaS
- Use Agile/Scrum with 2-week sprints
- Implement CI/CD from day 1
- Write tests for critical business logic
- Deploy to staging before production
- Monitor error rates and performance
- Iterate based on user feedback

### Hardware
- Plan for 6-12 month development cycles
- Order long-lead components early
- Budget for certifications (FCC, CE, UL)
- Start with breadboard, not PCB
- Design for manufacturing from prototype stage
- Build in test points for debugging

### Biotech/Pharma
- Engage FDA/regulators early
- Budget 50% more time than estimated
- Plan clinical trials with statistician
- Implement ISO 13485 quality systems
- Protect IP with provisional patents
- Build GMP processes from day 1

### Consumer Products
- Validate demand before manufacturing MOQ
- Design for 3-5x manufacturing cost (retail pricing)
- Test with target users extensively
- Plan for seasonal cycles (Q4 critical)
- Source multiple suppliers for key components

## Build vs Buy Decisions

### Build When:
- Core competitive differentiator
- Specific requirements not met by SaaS
- Long-term cost savings justify investment
- Need full control over data and roadmap

### Buy/SaaS When:
- Commodity functionality (auth, payments, email)
- Not core to value proposition
- Faster time to market critical
- Maintenance burden too high to justify building

## Quality Assurance

### DO:
- Write tests for critical business logic (70-80% coverage)
- Test on staging before production
- Monitor error rates and user feedback
- Implement beta testing program
- Fix critical bugs before new features
- Track and trend defect metrics

### DON'T:
- Skip testing to save time (false economy)
- Test only happy paths
- Ignore user-reported bugs
- Deploy on Fridays without monitoring
- Neglect security testing
- Ship known critical bugs

## Product-Market Fit Assessment

### Indicators of PMF:
- Users actively seeking your product (organic demand)
- 40%+ Day 30 retention
- NPS > 50
- Sean Ellis test: >40% "very disappointed" if product disappeared
- Scaling challenges (demand exceeds capacity)
- Word-of-mouth growth

### No PMF Yet:
- High churn (>10% monthly)
- Low engagement (< 5 min sessions)
- NPS < 10
- Unclear value proposition to users
- **Action**: Focus on iteration, user interviews, consider pivot

## Revolutionary Concepts

### DO:
- Apply first principles thinking
- Validate technical feasibility early
- Build proof of concept before full product
- Test with target users frequently
- Protect IP with provisional patents
- Assess competitive moat

### DON'T:
- Build in isolation without user feedback
- Assume "if you build it, they will come"
- Skip market validation
- Ignore existing solutions without reason
- Underestimate development timeline
- Neglect business model validation

## Integration with Other Skills

### Use With:
- **Research & Validation Skill**: Market research before roadmap
- **Patent Filing Skill**: Protect innovative product features
- **VC Fundraising Skill**: Product roadmap critical for pitch deck
- **full-stack-developer SubAgent**: Implement software products
- **devops-engineer SubAgent**: Set up infrastructure
- **qa-engineer SubAgent**: Execute testing strategy

## Success Metrics

### Process Metrics:
- MVP launched within timeline (±20%)
- Roadmap reviews conducted quarterly
- Team velocity predictable (±15%)
- Technical debt <30% of backlog
- Code review turnaround <24 hours

### Product Metrics:
- User retention trending up
- NPS improving quarter over quarter
- Feature adoption >40% of users
- Production incidents <5 per month
- Customer satisfaction (CSAT) >4/5

## Common Mistakes to Avoid

1. **Scope Creep**: Adding features mid-MVP development
2. **Over-Engineering**: Building for scale before validation
3. **Ignoring Users**: Building without user feedback
4. **Technology Choices**: Choosing unfamiliar or untested tech
5. **Skipping Testing**: Shipping bugs to save time
6. **Rigid Roadmaps**: Inability to pivot with new data
7. **Technical Debt**: Ignoring refactoring until system breaks
8. **Premature Optimization**: Optimizing before identifying bottlenecks

## Checklists

### MVP Launch Checklist
- [ ] Core workflow works end-to-end
- [ ] 5-10 target users tested successfully
- [ ] Success metrics tracking implemented
- [ ] Critical bugs resolved
- [ ] Beta user list ready (10-50 users)
- [ ] Support process defined
- [ ] Monitoring and error tracking active
- [ ] Rollback plan documented

### Quarterly Roadmap Review Checklist
- [ ] Previous quarter results analyzed
- [ ] Stakeholder input gathered
- [ ] Capacity and resources assessed
- [ ] RICE scores calculated for features
- [ ] Technical debt time allocated (20-30%)
- [ ] Success metrics defined
- [ ] Team aligned on priorities
- [ ] Roadmap communicated to stakeholders

### Technology Stack Decision Checklist
- [ ] Team expertise considered
- [ ] Time to market feasible
- [ ] Scalability to 10x validated
- [ ] Budget aligned with projections
- [ ] Hiring market checked
- [ ] Ecosystem maturity verified
- [ ] Migration path exists for vendor lock-in
- [ ] Security requirements met
- [ ] Decision rationale documented

---

**Rule Type**: Best Practices
**Applies To**: All product development activities
**Priority**: High
**Last Updated**: 2025-11-02
