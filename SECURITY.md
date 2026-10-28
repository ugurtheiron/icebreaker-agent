# Security Policy

## Supported versions

This repository is a set of scripts without versioned releases. Only the latest commit on `main` is supported.

## Reporting a vulnerability

Please **do not** open a public issue for a security problem.

Report it privately through GitHub:

1. Open the [Security tab](https://github.com/ugurtheiron/icebreaker-agent/security) of this repository.
2. Choose **Report a vulnerability** and describe the problem. See GitHub's guide on [privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability).

If that button is not available, open a public issue that says only that you have a security report and ask for a private channel. Do not include details in the issue.

A useful report contains the affected file or entry point, the steps to reproduce, and the impact you expect. You can expect a first reply within a week. This is a personal project, so please be patient.

## Scope

In scope: code in this repository, for example unsafe handling of API keys, unsafe parsing of model or API output, and vulnerable pinned dependencies that this code actually uses.

Out of scope: vulnerabilities in third-party services (OpenAI, Tavily, Firecrawl, Ollama, Jira) and issues that need a stolen API key to exploit.

## Keeping your keys safe

API keys belong in your local `.env` file, which is listed in `.gitignore`. If you committed a key by mistake, revoke it at the provider first and then remove it from the repository.
