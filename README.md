# AI Coding and Reviewer Agents

## Usage

## Project Settings

### Settings -> Actions -> General -> Workflow permissions

* Read and write permissions
* ✔ Allow GitHub Actions to create and approve pull requests

![image](https://github.com/user-attachments/assets/e78e60d0-9e16-425e-bcad-264c8f81b878)

### Settings -> Secrets and variables -> Actions -> Secrets

Set `MODEL_API_KEY` and `MODEL_ID`

## Workflow Configuration

Create a file `.github/workflows/ai-agent.yaml`:

```yaml
name: AI Agent Workflow

on:
  issues:
    types: [opened]
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]

jobs:
  ai-agents:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Coding Agent (start new task)
        if: github.event_name == 'issues'
        uses: Addefan/coding-agent-megaschool-2026@v1.0.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "coder"
          issue_number: ${{ github.event.issue.number }}

      - name: Reviewer Agent (review PR)
        if: github.event_name == 'pull_request'
        uses: Addefan/coding-agent-megaschool-2026@v1.0.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "reviewer"
          pr_number: ${{ github.event.pull_request.number }}
      
      - name: Coding Agent (fix after review)
        if: github.event_name == 'issue_comment' && github.issue.pull_request
        uses: Addefan/coding-agent-megaschool-2026@v1.0.0
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model_api_key: ${{ secrets.MODEL_API_KEY }}
          model_id: ${{ secrets.MODEL_ID }}
          mode: "coder"
          pr_number: ${{ github.event.issue.number }}
```
