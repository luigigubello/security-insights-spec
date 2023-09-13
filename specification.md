# Specification

The following values are part of Security Insights Specification `v1.0.0`

## Header
Here is an example of the header section, which holds high-level information about the project and its security documentation.

```yaml
header:
  schema-version: 1.0.0
  last-updated: '2021-09-01'
  last-reviewed: '2022-09-01'
  expiration-date: '2023-08-31T10:10:09.000Z'
  project-url: https://github.com/foo/bar
  commit-hash: 4dbf78ebc006ee5f668c0a74876ef8d6db9485be
  project-release: '1.2.0'
  changelog: https://github.com/foo/changelog.md
  license: https://git.foo/license
  parent-security-yaml: https://blah.com/ossf-security.yaml
```

Now let’s break that down:
- `schema-version` (Required): Provide the version of the specification that you are adhering to.
  - **String**
- `last-updated` (Required): Date of the most recent change to this file.
  - **Date**
- `last-reviewed` (Required): Date this file was last reviewed to confirm holistic accuracy.
  - **Date**
- `expiration-date` (Required): Date this file should no longer be considered valid. Maximum one year from the date it was last reviewed.
  - **Date-time**
- `project-url` (Required): URI for the project repository that this document pertains to.
  - **String** beginning with **https://**
- `commit-hash` (Required): The last commit on the repository that this document pertains to.
  - **String** matching the git SHA format
- `changelog`: URI for the changelog for the project.
  - **String** beginning with **https://**
- `license`: URI for the license for the corresponding version of the project.
  - **String** beginning with **https://**
- `parent-security-yaml`: If the document is mirrored from another, give a URI pointing to the original.
  - **String** beginning with **https://**

## Project Lifecycle
The project-lifecycle section contains information about how the project is maintained. This is the first of many places where we’ll see conditional requirements in the schema.

```yaml
project-lifecycle:
  stage: active
  roadmap: https://foo.bar/roadmap.html
  bug-fixes-only: false
  core-maintainers:
    - https://github.com/scovetta
    - joe.bob@email.com
```

Note that the last value on this list is a conditional requirement, making it optional if the project is no longer being maintained. We’ll see more values like this in the following sections.
- `stage` (Required): The project’s maintenance stage.
  - **String**. Values may be active or inactive.
- `roadmap`: URI to information about the project’s roadmap.
  - **String** beginning with **https://**
- `bug-fixes-only`: Is the project active, but only accepting bugfix changes?
  - **Boolean**
- `core-maintainers`: Required if bug-fixes-only is true or stage is active. Contact information for the project’s maintainers, such as email or URI.
  - **List** of **String** entries

## Contribution Policy
The contribution-policy section describes the decisions made by the project regarding when and how to accept contributions.

```yaml
contribution-policy:
  accepts-pull-requests: true
  accepts-automated-pull-requests: true
  automated-tools-list:
    - automated-tool: example/security-research
      action: denied
      path:
        - main/foo/bar
        - main/examples
      comment: |
        Lorem ipsum dolor sit amet, consectetur adipisci elit,
        sed do eiusmod tempor incidunt ut labore et dolore magna aliqua.
  contributing-policy: https://example.com/development-policy.html
  code-of-conduct: https://example.com/code-of-conduct.html
```

- `accepts-pull-requests` (Required): Does your project accept PRs from non-maintainers?
  - **Boolean**
- `accepts-automated-pull-requests` (Required): Does your project accept PRs from bots or automated tools?
  - **Boolean**
- `automated-tools-list`: If you have exceptions to accepts-automated-pull-requests, such as allowing select tools or blocking select tools, review the specification for more information about how to list those exceptions here.
  - **List** of **Objects**
- `contributing-policy`: URI to your project’s detailed contribution policy.
  - **String** beginning with **https://**
- `code-of-conduct`: URI to your project’s code of conduct.
  - **String** beginning with **https://**

## Documentation
The documentation section is simply a list of URIs to any security documentation you have provided for stakeholders.

```yaml
documentation:
  - http://foo.bar/wiki
```

This section is not required. Each entry to the list must be a **String** beginning with **https://**.

## Distribution Points
Similar to the previous section in our YAML, the distribution-points section is simply a list of URIs. This list should include any locations that users can expect to safely retrieve your released software.

```yaml
distribution-points:
  - https://example.com/foo
  - pkg:npm/foobar
```

This section is not required. Any entry to the list must be a **String**.

## Security Artifacts
The security-artifacts section allows you to share any additional security documentation that lives outside this document.

```yaml
security-artifacts:
  threat-model:
    threat-model-created: true
    evidence-url:
    - https://foo.com/model.html
    comment: |
      Lorem ipsum dolor sit amet, consectetur adipisci elit,
      sed do eiusmod tempor incidunt ut labore et dolore magna aliqua.
```

This section is not required. If threat-model-created is true, then evidence-url must contain at least one **String** beginning with **https://**.

## Security Testing
The security-testing section contains a list of tools your project has incorporated for automated security testing. This section is not required, but there are required and optional values for each entry, which we’ll look at below.

- `tool-name` (Required): **String**
- `tool-type` (Required): **String**, values may be sast, dast, iast, fuzzer
- `tool-version` (Required): **String**
- `tool-url`: **String** beginning with **https://**
- `integration` (Required)
    - `ad-hoc` (Required): Is the tool used manually on an ad-hoc basis?
    - **Boolean**
    - `before-release` (Required): Does the tool run automatically before every release?
    - **Boolean**
    - `ci` (Required): Does the tool run as part of continuous integration tests?
    - **Boolean**
    - `tool-rulesets`: Are any premade rulesets used from this tool?
    - **List** of **String** entries
