# Computer Use Agent - Safety Guidelines

## Overview

The Computer Use Agent Skill provides powerful desktop automation capabilities, but with that power comes responsibility. This document provides comprehensive safety guidelines for using this skill safely and responsibly.

## Core Safety Principles

### 1. FAILSAFE is Mandatory
**The FAILSAFE feature MUST always be enabled.**

- **What it does**: Immediately aborts automation when mouse moves to upper-left corner
- **How to use**: Simply move mouse to the very top-left corner of your screen
- **When to use**: Anytime automation is doing something unexpected or dangerous
- **Configuration**: Always verify FAILSAFE is enabled before starting automation

**Never disable FAILSAFE** unless you have a specific, well-understood reason.

### 2. Start Simple, Build Confidence
**Always test with simple, low-risk tasks first.**

**Progression:**
1. **Day 1**: Single-click actions in test applications
2. **Day 2**: Multi-step workflows in test applications
3. **Day 3**: Simple production tasks with monitoring
4. **Week 2+**: Complex production workflows

**Never jump straight to complex or critical tasks.**

### 3. Monitor First Runs Closely
**Watch all automation closely, especially first runs.**

- Keep your eyes on the screen
- Have hand ready to trigger FAILSAFE
- Use confirmation mode for first run of each workflow
- Don't leave computer unattended during automation
- Review screenshot logs after completion

### 4. Use Appropriate Safety Settings
**Configure safety settings based on task risk and complexity.**

**Low Risk Tasks** (viewing, reading, navigation):
```yaml
failsafe_enabled: true
action_delay: 0.5
max_steps: 20
confirmation_mode: false
screenshot_logging: true
```

**Medium Risk Tasks** (form filling, data entry):
```yaml
failsafe_enabled: true
action_delay: 1.0
max_steps: 50
confirmation_mode: true  # First run only
screenshot_logging: true
```

**High Risk Tasks** (file operations, configuration changes):
```yaml
failsafe_enabled: true
action_delay: 2.0
max_steps: 30
confirmation_mode: true  # Always
screenshot_logging: true
```

### 5. Never Automate Sensitive Operations
**Some operations should NEVER be automated.**

**Absolutely Prohibited:**
- ❌ Password entry
- ❌ Banking or financial transactions
- ❌ Credit card information
- ❌ Social security numbers
- ❌ Personal health information
- ❌ Authentication codes (2FA, OTP)

**Require Explicit Permission:**
- ⚠️ File deletion
- ⚠️ Data modification
- ⚠️ Email sending
- ⚠️ Social media posting
- ⚠️ System configuration changes
- ⚠️ Software installation

## Risk Assessment Framework

### Low Risk (✅ Safe to Automate)

**Characteristics:**
- Read-only operations
- Test/sandbox environments
- Easily reversible actions
- No sensitive data involved
- No external communications

**Examples:**
- Reading content from applications
- Navigating menus
- Taking screenshots
- Opening applications
- Scrolling pages
- Copying test data

**Safety Settings:**
- Standard delay (0.5s)
- Standard max steps (20-50)
- Logging enabled
- Confirmation optional

### Medium Risk (⚠️ Requires Caution)

**Characteristics:**
- Modifies non-critical data
- Production environments
- Reversible with effort
- Limited external impact
- Professional data (non-sensitive)

**Examples:**
- Filling out forms
- Creating documents
- Moving files
- Updating records
- Downloading files
- Application configuration

**Safety Settings:**
- Slower delay (1.0s)
- Conservative max steps (30-50)
- Logging enabled
- Confirmation for first run
- Regular monitoring

### High Risk (🛑 Extreme Caution)

**Characteristics:**
- Deletes or overwrites data
- Difficult to reverse
- External communications
- System-level changes
- Impacts multiple users

**Examples:**
- Deleting files/folders
- Modifying databases
- Changing system settings
- Sending emails/messages
- Publishing content
- Installing software

**Safety Settings:**
- Very slow delay (2.0s+)
- Low max steps (10-20)
- Logging enabled
- Always require confirmation
- Continuous monitoring
- Backup before execution

### Prohibited (❌ Never Automate)

**Characteristics:**
- Involves credentials or secrets
- Financial transactions
- Sensitive personal data
- Irreversible consequences
- Legal/compliance implications

**Examples:**
- Password entry
- Banking operations
- Credit card transactions
- Medical record access
- Legal document signing
- HR/payroll operations

**Alternative:** Manual operation or specialized secure automation tools

## Safety Features

### FAILSAFE Mode

**How It Works:**
1. PyAutoGUI monitors mouse position constantly
2. If mouse reaches screen corners (configurable), automation STOPS immediately
3. All pending actions are cancelled
4. Control returns to user

**Default FAILSAFE Locations:**
- Upper-left corner (0, 0)
- Can be configured to other corners if needed

**Using FAILSAFE:**
1. Keep mouse away from corners during setup
2. Move mouse to corner quickly if automation goes wrong
3. Automation stops within milliseconds
4. No confirmation required - instant stop

**Testing FAILSAFE:**
Before first use, test that FAILSAFE works:
1. Start simple automation
2. Move mouse to upper-left corner
3. Verify automation stops immediately
4. Confirm you can regain control

### Action Delays

**Purpose:** Give applications time to respond between actions

**Recommended Delays:**
- **0.3s**: Very fast UIs (games, real-time apps)
- **0.5s**: Standard UIs (most applications)
- **1.0s**: Complex UIs (multi-step animations)
- **2.0s**: Slow UIs (heavy applications, network calls)
- **5.0s+**: Very slow UIs (startup, large data loads)

**When to Increase Delay:**
- Actions missing targets
- UI not ready for next action
- Animations not completing
- Network requests pending
- Application under heavy load

### Step Limits

**Purpose:** Prevent infinite loops and runaway automation

**Recommended Limits:**
- **10-20 steps**: Simple tasks (form filling, menu navigation)
- **20-50 steps**: Medium tasks (multi-form workflows)
- **50-100 steps**: Complex tasks (multi-application workflows)

**What Happens at Limit:**
- Automation stops automatically
- Current state saved
- Screenshot captured
- User notified
- Option to continue with higher limit

**Setting Step Limits:**
- Estimate task complexity
- Add 50% buffer for unexpected steps
- Start conservative, increase if needed
- Monitor actual steps used
- Adjust for future runs

### Confirmation Mode

**Purpose:** Require user approval before executing actions

**Levels:**
1. **No Confirmation**: Automation runs fully automatically
2. **First Action**: Confirm before starting, then run
3. **Critical Actions**: Confirm destructive actions only
4. **Every Action**: Confirm each action (debugging/learning)

**When to Use:**
- ✅ First run of new workflow
- ✅ High-risk operations
- ✅ Production environments
- ✅ Learning/debugging
- ❌ Tested, low-risk workflows
- ❌ Batch operations (too many confirmations)

### Screenshot Logging

**Purpose:** Create audit trail of automation activities

**What Gets Logged:**
- Screenshot before each action
- Screenshot after each action
- Screenshot of errors or unexpected states
- Screenshot at task completion
- Metadata (timestamp, action type, coordinates)

**Storage:**
- Default: `~/.claude/computer-use-logs/YYYYMMDD_HHMMSS/`
- Organized by task run
- Includes metadata JSON
- Automatically cleaned up after 30 days (configurable)

**Using Logs:**
- Review what automation did
- Debug failed workflows
- Verify correct operation
- Compliance/audit requirements
- Training data for improvements

## Safe Automation Practices

### Before Starting

**Pre-Flight Checklist:**
- [ ] Understand what task will do
- [ ] Verify applications are in correct state
- [ ] Close unnecessary windows
- [ ] Backup important data if applicable
- [ ] Test FAILSAFE is working
- [ ] Review safety settings
- [ ] Clear screen of sensitive information
- [ ] Be ready to monitor closely

### During Automation

**Monitoring Checklist:**
- [ ] Watch screen continuously
- [ ] Keep hand near mouse for FAILSAFE
- [ ] Verify actions are correct
- [ ] Watch for unexpected dialogs
- [ ] Monitor for errors
- [ ] Check application responsiveness
- [ ] Abort if anything looks wrong

**Red Flags - Stop Immediately:**
- 🚩 Wrong application has focus
- 🚩 Unexpected dialog appears
- 🚩 Actions going to wrong location
- 🚩 Sensitive information on screen
- 🚩 Application crashed or froze
- 🚩 Infinite loop detected
- 🚩 Unintended consequences observed

### After Completion

**Post-Run Checklist:**
- [ ] Verify task completed correctly
- [ ] Check for errors or warnings
- [ ] Review screenshot logs
- [ ] Verify data integrity
- [ ] Close temporary windows
- [ ] Clean up temporary files
- [ ] Document any issues
- [ ] Update workflow if needed

## Environment Safety

### Test Environments

**Always test in safe environments first:**
- ✅ Local development machines
- ✅ Test/staging servers
- ✅ Sandbox accounts
- ✅ Virtual machines
- ✅ Test databases
- ❌ Production environments (until tested)
- ❌ Live customer data
- ❌ Shared/critical systems

### Data Safety

**Protect your data:**
1. **Backup**: Always backup before automating file operations
2. **Test Data**: Use test data for initial runs
3. **Staging**: Test in staging before production
4. **Rollback**: Have rollback plan for failures
5. **Monitoring**: Monitor data integrity after automation

### System Safety

**Protect your system:**
1. **Permissions**: Run with minimal required permissions
2. **Isolation**: Use VMs or containers when possible
3. **Monitoring**: Watch system resources
4. **Limits**: Set appropriate resource limits
5. **Recovery**: Have system restore point before major automations

## Privacy and Security

### Screen Content

**Be aware of what's on screen:**
- Screenshots may capture sensitive information
- Vision AI analyzes everything visible
- Logs may contain sensitive data
- Consider using on dedicated/isolated displays

**Protecting Privacy:**
- Close sensitive windows before automation
- Use privacy filters on monitors
- Review screenshot logs for sensitive data
- Configure log retention appropriately
- Encrypt logs if they contain sensitive information

### API Keys and Credentials

**Vision AI requires API access:**
- OpenAI API key needed for vision analysis
- API calls include screenshot data
- Screenshots processed by external service
- Review OpenAI's privacy policy
- Consider data residency requirements

**Best Practices:**
- Use API keys with minimal required permissions
- Rotate API keys regularly
- Monitor API usage for anomalies
- Review API provider's security practices
- Consider self-hosted alternatives for sensitive environments

### Compliance Considerations

**Regulatory compliance:**
- **GDPR**: Be careful with EU personal data
- **HIPAA**: Don't automate healthcare data operations
- **PCI-DSS**: Never automate payment card operations
- **SOX**: Consider audit trail requirements
- **Industry-Specific**: Check your industry regulations

## Incident Response

### If Automation Goes Wrong

**Immediate Actions:**
1. **STOP**: Trigger FAILSAFE immediately (move mouse to corner)
2. **ASSESS**: Determine what went wrong
3. **DOCUMENT**: Take notes, screenshots of error state
4. **RECOVER**: Restore to known good state if needed
5. **REPORT**: Document incident for review

**Recovery Steps:**
1. Close affected applications
2. Check for partial data changes
3. Restore from backup if necessary
4. Verify system integrity
5. Review logs to understand failure
6. Update workflow to prevent recurrence

### If Sensitive Data Exposed

**Immediate Actions:**
1. **STOP**: Stop automation immediately
2. **SECURE**: Close or minimize sensitive windows
3. **LOGS**: Review and secure any logs containing sensitive data
4. **REPORT**: Follow your organization's data breach procedures
5. **REVIEW**: Determine how exposure occurred

**Prevention:**
- Always clear sensitive data from screen before automation
- Use privacy filters
- Configure logging to exclude sensitive areas
- Review security practices regularly

## Training and Competency

### Skill Development Path

**Level 1: Beginner** (Week 1)
- Learn FAILSAFE usage
- Practice single-action tasks
- Understand safety settings
- Use test environments only

**Level 2: Intermediate** (Week 2-4)
- Multi-step workflows
- Error handling
- Production tasks (low-risk)
- Workflow optimization

**Level 3: Advanced** (Month 2+)
- Complex multi-application workflows
- Custom safety configurations
- Troubleshooting and debugging
- Workflow development

**Never skip levels.** Build competency gradually.

### Documentation

**Document your workflows:**
1. Task description
2. Prerequisites and setup
3. Step-by-step procedure
4. Safety settings used
5. Known issues and workarounds
6. Recovery procedures
7. Testing and validation results

**Why Document:**
- Knowledge sharing
- Consistency
- Troubleshooting reference
- Compliance requirements
- Continuous improvement

## Summary

**Core Safety Rules:**
1. ✅ Always enable FAILSAFE
2. ✅ Start simple, build confidence
3. ✅ Monitor closely, especially first runs
4. ✅ Use appropriate safety settings
5. ✅ Never automate sensitive operations
6. ✅ Test in safe environments first
7. ✅ Enable screenshot logging
8. ✅ Have hand ready to abort
9. ✅ Backup before file operations
10. ✅ Document workflows and incidents

**Remember:**
- This tool controls your actual computer
- Safety must always be the top priority
- When in doubt, stop and assess
- Better to be overcautious than to cause problems
- Learn gradually, test thoroughly, document well

---

**Questions or Concerns?**
If you're unsure about the safety of an automation task, STOP and consult with experienced users or administrators before proceeding.
