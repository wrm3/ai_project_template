# Multi-Agent Workflow Example with File-Based Prompts

This document demonstrates how to use the enhanced `plan_exec_llm.py` script with file-based prompts in a multi-agent workflow.

## Step 1: Create a Detailed Prompt File

Create a file named `unix_timestamp_migration_plan.txt` with a detailed prompt:

```
We need to develop a comprehensive plan to migrate the trading bot to use Unix timestamps as the source of truth for all time-related operations. The bot crashed during the spring forward daylight savings transition, and we've identified that the current approach of deriving _unix values from _dttm values in database triggers is problematic.

Specific issues to address:
1. Reverse the dependency in database triggers to make _dttm columns derive from _unix columns
2. Update all code to prioritize Unix timestamps for calculations
3. Create a safe migration plan for the live database
4. Develop comprehensive tests for DST transition scenarios

Please provide a detailed plan with the following sections:
1. Database migration strategy (with backup procedures)
2. Code refactoring approach (prioritized by component)
3. Testing methodology
4. Rollout and monitoring plan
```

## Step 2: Invoke the Planner with the File-Based Prompt

As the Executor, you would run:

```bash
py -3 hanx_tools/plan_exec_llm.py --prompt-file unix_timestamp_migration_plan.txt --file hanx_plan.md
```

## Step 3: Update the Plan Based on the Planner's Response

After receiving the Planner's response, update the `hanx_plan.md` file with the suggested changes.

## Step 4: Execute the Plan

As the Executor, read the updated plan and execute the tasks outlined by the Planner.

## Step 5: Report Progress and Request Further Guidance

After completing some tasks or encountering issues, update the "Current Status / Progress Tracking" and "Executor's Feedback or Assistance Requests" sections in `hanx_plan.md`.

## Step 6: Request Further Planning

For complex next steps, create another detailed prompt file and invoke the Planner again:

```bash
py -3 hanx_tools/plan_exec_llm.py --prompt-file database_migration_details.txt --file hanx_plan.md
```

## Benefits of File-Based Prompts

1. **Handles Complex Prompts**: Can include detailed requirements, context, and specific questions
2. **Reusable**: Prompt files can be saved, versioned, and reused
3. **Editable**: Easier to refine and improve prompts over time
4. **Documented**: Provides a record of the planning process 