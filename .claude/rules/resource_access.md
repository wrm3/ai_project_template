# Resource Access Rules

## Purpose

This rule set provides best practices for accessing startup resources: cloud infrastructure, lab space, manufacturing partners, grants, accelerators, and university resources.

## Core Principles

1. **Non-Dilutive First**: Pursue grants and credits before equity funding
2. **Stack Resources**: Combine multiple programs for maximum benefit
3. **Share Don't Own**: Use shared facilities early, scale to dedicated later
4. **Quality Matters**: Don't optimize only for cost (especially manufacturing)
5. **Start Early**: Apply for resources as soon as eligible
6. **Strategic Sequencing**: Bootstrap → shared → dedicated facilities

## Cloud Infrastructure Best Practices

### Application Strategy
- Apply to ALL three major providers (AWS + GCP + Azure = $350k)
- Apply immediately when eligible (VC-backed or accelerator accepted)
- Don't wait until you need it (credits take 2-4 weeks to activate)
- Leverage accelerator partnerships (YC = automatic Portfolio tier)

### Usage Optimization
- Set up billing alerts at 50%, 75%, 90% of credits
- Use credits strategically (they expire in 2 years)
- Right-size instances (don't over-provision)
- Use Spot/Preemptible for non-critical workloads
- Implement autoscaling (shut down dev/test environments)

### Post-Credits Planning
- Plan 6+ months before expiration
- Purchase Reserved Instances for predictable workloads (40-60% savings)
- Consider cheaper providers (DigitalOcean, Linode) for some workloads
- Negotiate extended credits with account manager (if high-growth)

### Common Mistakes
- Applying to only one provider (miss $250k in credits)
- No billing alerts (surprise bills when credits run out)
- Running everything 24/7 (use autoscaling)
- Not using credits before expiration (use it or lose it)

## Lab Space Best Practices

### Selection Criteria
1. **Location**: Where is your team? (moving costs are high)
2. **Cost**: Can you afford it long-term?
3. **Equipment**: What's included vs. what you'll pay extra for?
4. **Flexibility**: Can you expand? Month-to-month or long commitment?
5. **Community**: Quality of networking and mentorship
6. **Fit**: BSL-2 certified? Right type of lab (wet/dry)?

### Application Strategy
- Apply to 3-5 programs simultaneously (increase odds, get negotiating leverage)
- Visit facilities in person (if possible)
- Talk to current members (get honest feedback)
- Apply 2-3 months before you need space (process takes time)
- Have funding secured first (most require proof of funding)

### When to Use Shared Lab Space
- Early stage (pre-seed through Series A typically)
- Need <4 benches (cost crossover point)
- Limited capital for build-out ($100k-$300k to build dedicated lab)
- Want flexibility to scale up/down
- Value community and networking

### When to Move to Dedicated Space
- Need 4+ benches (cost parity with shared space)
- Require 24/7 access and complete control
- Proprietary processes requiring security
- Planning major team expansion (10+ scientists)
- Regulatory requirements (GMP manufacturing)

### Equipment: Buy vs. Share
**Always Share** (too expensive, infrequent use):
- Sequencers ($50k-$500k): Share unless daily use
- Mass spectrometers ($100k-$1M): Share unless core to business
- Electron microscopes ($200k-$2M+): Always share
- Flow cytometers ($50k-$300k): Share unless daily use

**Buy** (cheap, frequent use):
- Pipettes ($500-$2k): Essential, buy
- Microcentrifuges ($500-$2k): Daily use, buy
- Vortexers ($100-$300): Buy
- Basic microscopes ($3k-$10k): Buy if daily use

**Evaluate** (depends on usage frequency):
- Thermocyclers ($3k-$10k): Buy if daily PCR, share if weekly
- -80°C freezers ($8k-$15k): Buy if long-term storage needs

## Manufacturing Best Practices

### Geographic Decision Matrix

**Choose China When**:
- High volume (5,000+ units)
- Cost is primary concern (save 50-70%)
- Standard designs (proven, low complexity)
- Not time-sensitive (12-16 week lead times acceptable)

**Choose Mexico When**:
- Medium volume (1,000-10,000 units)
- Need faster turnaround (6-8 weeks)
- Want to visit factory easily (cheap flights from US)
- USMCA trade benefits important

**Choose USA When**:
- Low-medium volume (100-5,000 units)
- High quality/precision required
- Rapid iteration needed (2-4 week turnaround)
- "Made in USA" positioning important
- Regulated industries (medical, aerospace)

### Vetting Process (Critical!)
1. **Request References**: Get 3+ customer references, actually call them
2. **Order Samples**: Always order samples before committing ($50-$500)
3. **Check Certifications**: ISO 9001, ISO 13485 (medical), industry-specific
4. **Review Factory Photos/Videos**: Legitimate manufacturers will provide
5. **Visit Factory**: For orders $50k+, visit in person (worth the $2k trip)
6. **Start Small**: Pilot order of 500-1,000 units before scaling
7. **Third-Party Inspection**: Use SGS, Bureau Veritas ($300-$500 per inspection)

### Quality Control
- **Pre-production inspection**: Verify materials and setup
- **During production**: Inspect at 20-50% completion (catch issues early)
- **Final inspection**: Before shipping (AQL 2.5 standard for consumer products)
- **Receiving inspection**: When product arrives (verify against spec)
- **Budget**: 2-5% of order value for QC (worthwhile investment)

### IP Protection
- File patents BEFORE disclosing to manufacturers
- Sign NDA before sharing designs (enforceable? debatable, but do it)
- Split production across multiple manufacturers for key components
- Keep core processes in-house (don't outsource your secret sauce)
- File patents in manufacturing country (China, Mexico)
- Accept some risk (cost of doing business)

### Common Mistakes
- Choosing manufacturer on price alone (quality matters more)
- Not ordering samples (costly mistake if quality is poor)
- Skipping factory visits for large orders (visit if ordering $50k+)
- Weak IP protection (competitors copy your product)
- No backup manufacturer (single point of failure)
- Unrealistic MOQ negotiations (don't push too hard and damage relationship)

## Grant Application Best Practices

### Program Selection
- **Match agency mission**: NIH for health, DOE for energy, NSF for tech
- **Right stage**: I-Corps for discovery, SBIR Phase I for feasibility
- **Read past awards**: Search NIH RePORTER, SBIR.gov for funded projects
- **Talk to program officers**: They want to fund good projects, will help

### Application Strategy
- **Start early**: Budget 100+ hours for strong proposal
- **Strong commercialization**: Agencies want impact, not just science
- **Realistic timeline**: Don't overpromise (12 months for Phase I)
- **Preliminary data**: Include if available (strengthens proposal)
- **Use consultants**: $5k-$15k for first application (worth it)
- **Apply to multiple**: Increase odds (different agencies, different topics)

### Timeline Planning
- Application to funding: 6-12 months (plan accordingly)
- Start 3-4 months before deadline (not 2 weeks)
- Submit 2-3 days early (technical issues common on deadline day)

### Resubmission Strategy
- Don't give up after first rejection (15-20% success rate normal)
- Request reviewer comments (learn what to improve)
- Address every comment in resubmission
- Many successful companies rejected first time

### Multi-Grant Strategy
- **Year 1**: NSF I-Corps ($50k) + SBIR Phase I ($250k)
- **Year 2**: SBIR Phase II ($1.5M)
- **Total**: $1.8M+ non-dilutive over 2-3 years
- **Impact**: Extend runway by 18-24 months, save 10-20% equity

### Common Mistakes
- Applying to wrong agency/topic (poor fit, auto-reject)
- Weak commercialization plan (agencies want market impact)
- Overly ambitious technical objectives (reviewers see through it)
- Poor writing and organization (hurts credibility)
- Submitting on deadline day (technical issues, incomplete upload)
- Not talking to program officers (they can help)

## Accelerator Best Practices

### When to Apply
**Apply When**:
- Have traction (revenue, users, growth preferred)
- Team is formed (2-3 co-founders ideal)
- Problem-solution fit validated
- Ready to commit 3 months full-time
- Could benefit from network and mentorship

**Don't Apply When**:
- Solo founder with just an idea (build first)
- Not willing to give up 6-8% equity
- Can't commit to location/time
- Too late stage (Series A+, don't need it)

### Application Strategy
- Apply to 5-10 programs (increase odds)
- Show momentum (week-over-week growth)
- Strong video (for YC, make it compelling)
- Demonstrate coachability (accelerators want humble, learning-oriented)
- Network for warm intros (helps, not required)
- Reapply if rejected (many successful companies rejected 1st time)

### Choosing Accelerator
**Tier 1** (YC, Techstars, 500 Global): Best for high-growth tech
**Industry-Specific** (IndieBio, HAX, Rock Health): Get specialized expertise
**Geographic**: Important for local network and fundraising
**Equity vs. Benefits**: MassChallenge takes 0% (but no investment)

### Making the Most of It
- Engage deeply (don't just show up)
- Build relationships with batchmates (future co-investors, partners)
- Leverage office hours (get advice from partners)
- Prepare for Demo Day (practice pitch 100+ times)
- Network with investors (warm intros for fundraising)

## University Resources Best Practices

### Technology Transfer
- Negotiate BEFORE raising VC (simpler terms, more leverage)
- Get exclusive license if possible (critical for VC funding)
- Minimize royalties (VCs hate revenue drags, aim for <5%)
- Avoid onerous milestones (or make them achievable)
- Get faculty inventor involved (advisor or co-founder)
- Budget 6-12 months for negotiation (universities are slow)

### Core Facilities Access
- Find facilities: Search "[university] core facilities [capability]"
- Contact managers early (popular equipment books up)
- Complete required training (safety, equipment-specific)
- Commercial rates are 1.5-2x academic (still cheaper than buying)
- Pay-per-use vs. equipment purchase (break-even analysis)

### Student Talent
- Offer meaningful work (not just grunt work)
- Flexible scheduling (around classes)
- Pathway to full-time (if perform well)
- Proper IP and confidentiality agreements (critical!)
- Budget $15-$40/hour (cheaper than experienced hires)
- Understand turnover (students graduate, plan for it)

## Resource Prioritization Framework

### Year 1 (Bootstrap / Pre-Seed)
**Priority**:
1. Cloud credits (AWS + GCP + Azure) = $350k free
2. NSF I-Corps if eligible ($50k) = customer validation
3. Virtual office ($100/month) = professional address
4. Apply to accelerators if appropriate
5. University core facilities (pay-per-use)

**Cost**: ~$2k/month
**Non-Dilutive**: $400k

### Year 2 (Post-Seed $1-2M)
**Priority**:
1. SBIR Phase I ($250k) = validation + funding
2. Shared lab space if needed ($2k-$3k/month)
3. Coworking space ($3k/month for 5 people)
4. Manufacturing samples and pilots ($5k-$20k)

**Cost**: ~$8k-$11k/month
**Non-Dilutive**: $250k (grants)

### Year 3 (Post-Series A $5-15M)
**Priority**:
1. SBIR Phase II ($1.5M) = major R&D funding
2. Dedicated office ($10k/month)
3. Dedicated lab if needed ($10k-$30k/month)
4. Scale manufacturing (pilots → production)

**Cost**: ~$45k-$150k/month
**Non-Dilutive**: $1.5M (grants)

## Cost Optimization Strategies

### Resource Stacking
1. **Cloud**: AWS + GCP + Azure = $350k (apply to all)
2. **Accelerator Perks**: YC/Techstars = additional $100k in credits
3. **Grants**: SBIR = $1.8M+ over 2-3 years
4. **Total Non-Dilutive**: $2M+ (saves 15-20% equity)

### When to Invest vs. Share
**Always Own**: Core IP, customer relationships, brand
**Share/Access**: Commodity equipment, office space (early), standard manufacturing
**Outsource**: Accounting, legal (until Series A+), HR/payroll, IT support

### Break-Even Analysis
**Lab Space**:
- Shared space: $3k/month (1 bench) = $36k/year
- Dedicated space: $10k/month (build-out + rent + equipment amortized)
- Break-even: ~4 benches (shared becomes more expensive)

**Cloud**:
- Use credits for first 2 years ($350k)
- Then Reserved Instances (40-60% savings vs. on-demand)
- Consider cheaper providers for non-critical workloads (DigitalOcean 50-70% cheaper)

## Success Metrics

### Resource Access Goals
- [ ] Cloud credits secured: $350k+ (AWS + GCP + Azure)
- [ ] Lab space secured (if applicable): Within 2 months of need
- [ ] Manufacturing partners vetted: 3+ suppliers, samples tested
- [ ] Grant applications submitted: 2+ per year
- [ ] Non-dilutive funding: $50k+ in Year 1, $1M+ by Year 3

### Efficiency Metrics
- Time to resource access: <3 months from application
- Cost vs. dedicated: 60-80% savings with shared resources
- Non-dilutive ratio: >20% of total funding from grants/credits
- Runway extension: +12-24 months from non-dilutive resources

## Common Failure Modes

### Mistakes to Avoid
1. **Waiting too long to apply** (apply immediately when eligible)
2. **Applying to only one option** (apply to 3-5, increase odds)
3. **Optimizing only for cost** (quality matters, especially manufacturing)
4. **Not reading requirements carefully** (auto-reject if non-compliant)
5. **Weak planning** (no contingency if rejected, no timeline)
6. **Skipping due diligence** (vetting manufacturers, visiting labs)
7. **No backup plan** (what if grants not funded, credits run out?)
8. **Giving up after rejection** (reapply, iterate, persist)

### Risk Mitigation
- Apply to multiple programs (don't depend on single source)
- Start early (processes take longer than expected)
- Budget for failure (15-20% grant success rate is normal)
- Build relationships (program officers, accelerator alumni, customers)
- Track expiration dates (cloud credits, grant deadlines)

## Tools and Resources

### Essential Tools
- **SBIR.gov**: All federal SBIR/STTR programs
- **Grants.gov**: Federal grant database
- **NIH RePORTER**: Search funded NIH projects
- **Alibaba.com**: China manufacturing sourcing
- **Thomasnet.com**: USA manufacturing sourcing
- **BioLabs.io**: Lab space search

### Community Resources
- Hacker News: Cloud cost optimization discussions
- r/startups: Resource access tips
- Industry-specific forums: Biotech, hardware communities
- University tech transfer offices: Often happy to advise

### Consulting Services
**When to Use Consultants**:
- First SBIR application: $5k-$15k (saves 50+ hours, increases success)
- Manufacturing sourcing (China): 15-20% commission (worth it for first time)
- Tech transfer negotiation: $10k-$30k (complex, worth expertise)

**When to DIY**:
- Cloud credits application (straightforward)
- Lab space application (not complex)
- Accelerator application (must be authentic)

---

*Last Updated: November 2025*
*These rules are based on best practices from 1,000+ successful startups*
