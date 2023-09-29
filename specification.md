# Specification

This specification provides a mechanism for projects to report information about their security in a machine-processable way. It is formatted as a YAML file to make it easy to read and edit by humans.

Values that are included within the specification may be required or optional. Optional values are reccommendations from the Open Source Security Foundation's _Identifying Security Threats Working Group_, but may not be prudent for all use cases.

Example implementations can be found on the specification's [GitHub repo](https://github.com/ossf/security-insights-spec/pull/37).

The following values are part of Security Insights Specification `v1.0.0`

## Header
Here is an example of the header section, which holds high-level information about the project and its security documentation.

```yaml
header:
  schema-version: 1.0.0
  parent-security-yaml: https://blah.com/ossf-security.yaml
  expiration-date: '2023-08-31T10:10:09.000Z'
  last-updated: '2021-09-01'
  last-reviewed: '2022-09-01'
  commit-hash: 4dbf78ebc006ee5f668c0a74876ef8d6db9485be
  project-url: https://github.com/foo/bar
  project-release: '1.2.0'
  changelog: https://github.com/foo/changelog.md
  license: https://git.foo/license
```

### Fields

- `schema-version` (Required)
  - **Description:** Provide the version of the specification that you are adhering to. This information is useful to validate the YAML according to the correct schema version.
  - **Type:** String. The version must match one of the values defined in the field `enum` of the schema.
- `parent-security-yaml`
  - **Description:** Provide the link to the last version of the `SECUIRTY-INSIGHT.yml`. This information can be helpful if the repository or project is mirrored.
  - **Type:** String. The provided URL must meet the IRI standard ([RFC 3987](https://www.ietf.org/rfc/rfc3987.txt)) and starts with `https://`.
- `expiration-date` (Required) 
  - **Description:** The date this file should no longer be considered valid, and it can be at most one year from the date it was last reviewed.
  - **Type:** String. The provided value must be a datetime.
- `last-updated`
  - **Description:** The date of the last update to `SECURITY-INSIGHTS.yml`, excluding the properties `commit-hash` and `last-reviewed`.
  - **Type:** String. The provided value must be a date.
- `last-reviewed`
  - **Description:** Date this file was last reviewed by a project maintainer to confirm holistic accuracy.
  - **Type:** String. The provided value must be a date.
- `commit-hash`
  - **Description:** The last commit to which the `SECURITY-INSIGHTS.yml` refers.
  - **Type:** String. The provided hash must match the regex `^\b[0-9a-f]{5,40}\b$`.
- `project-url` (Required)
  - **Description:** URI for the main project repository that this document refers to.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.
- `project-release`
  - **Description:** The release version or artifact version to which the `SECURITY-INSIGHTS.yml` refers.
  - **Type:** String.
- `changelog`
  - **Description:** URL to the project changelog.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.
- `license`
  - **Description:** URL to the project license.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.

## Project Lifecycle

The purpose of the project-lifecycle section is to describe support, maintenance, and fitness expectations for the consumer. For example, a project may be just getting started, be mature, be in "bugfix only" mode, or be completely abandoned. It helps clarify expectations all around.

```yaml
project-lifecycle:
  stage: active
  roadmap: https://foo.bar/roadmap.html
  bug-fixes-only: false
  core-maintainers:
  - https://github.com/github
  - joe.bob@email.com
  release-cycle: https://foo/release
  release-process: |
      foo bar
```

### Fields

- `bug-fixes-only` (Required)
  - **Description:** Provide the maintenance status of the project by specifying if the maintainers fix only bugs without providing new features.
  - **Type:** Boolean.
- `core-maintainers` (Conditional required)
  - **Description:** Provide the contacts of the project maintainers (emails, social profiles, websites, etc). This information can help consumers to contact the right people.
  - **Type:** Array. Elements of the array are strings.
  - **Condition:** This value is required if `bug-fixes-only` is `true` or if `stage` is `active`.
- `roadmap`
  - **Description:** URI to the project roadmap.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.
- `release-cycle`
  - **Description:** URI to the project release cycle.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.
- `release-process`
  - **Description:** Provide a short description for the release process of the process.
  - **Type:** String. At most 560 characters.
- `stage` (Required)
  - **Description:** Provide the status of the project, `active` or `inactive`. This information can help Security Insights consumers to know if a project is still actively maintained or not. 
  - **Type:** String. The value must match one of those defined in the field `enum` of the schema.

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
      foo bar
  contributing-policy: https://example.com/development-policy.html
  code-of-conduct: https://example.com/code-of-conduct.html
```

### Fields

- `accepts-pull-requests` (Required)
  - **Description:** Define if the maintainers accept pull-requests or not from external contributors.
  - **Type:** Boolean.
- `accepts-automated-pull-requests` (Required)
  - **Description:** Define if the maintainers accept pull-requests generated by bots or automated tools.
  - **Type:** Boolean.
- `automated-tools-list`
  - **Description:** List of allowed and denied automated tools and bots. This property can integrate the value `accepts-automated-pull-requests`, according to an automated tool is allowed or denied.
  - **Type:** Array.
  - `automated-tool` (Required)
    - **Description:** The name of the automated tool or bot.
    - **Type:** String.
  - `action` (Required)
    - **Description:** Define if automated actions from a specific tool are allowed or denied.
    - **Type:** String. The version must match one of the values defined in the field `enum` of the schema.
  - `path`
    - **Description:** Provide paths or sub-paths where the automated actions are allowed or denied.
    - **Type:** Array. Elements of the array are strings.
  - `comment`
    - **Description:** Provide additional context or comments.
    - **Type:** String. At most 560 characters.
- `contributing-policy`
  - **Description:** URI to the project contributing policy.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.
- `code-of-conduct`
  - **Description:** URI to the project code of conduct.
  - **Type:** String. The provided URL must meet the IRI standard (RFC 3987) and starts with `https://`.

## Documentation

The documentation section is simply a list of URIs to any security documentation you have provided for stakeholders.

```yaml
documentation:
  - http://foo.bar/wiki
```

### Fields

This section is not required. It is an array containing links to the project documentation (docs, wiki, etc.). Every item must be a string that meets the IRI standard (RFC 3987) and starts with `https://`.

## Distribution Points

Similar to the previous section in our YAML, the distribution-points section is simply a list of URIs. This list should include any locations that users can expect to safely retrieve your released software.

```yaml
distribution-points:
  - https://example.com/foo
  - pkg:npm/foobar
```

This section is not required. It is an array containing pURLs to the official releases, official released artifacts, or official packages of the project. Every item must be a string.

## Security Artifacts

The section `security-artifacts` allows you to share any additional security documentation that lives outside this document.

```yaml
security-artifacts:
  threat-model:
    threat-model-created: true
    evidence-url:
    - https://foo.com/model.html
    comment: |
      foo bar
  self-assessment:
    self-assessment-created: true
    evidence-url:
    - https://foo.com/assessment.html
    comment: |
      foo bar
  other-artifacts:
    - artifact-name: example-artifact
      artifact-created: true
      evidence-url:
        - https://foo.com/artifact.html
      comment: |
        foo bar
```

### Fields

- `threat-model`
  - `threat-model-created` (Required)
    - **Description:** Define if a threat model has been created for the project. A false value may be used to add comments regarding the status of the assessment.
    - **Type:** Boolean.
  - `evidence-url` (Conditional required)
    - **Description:** Evidence of the project threat model.
    - **Type:** Array. Every provided item must be a string that meets the IRI standard (RFC 3987) and starts with `https://`.
    - **Condition:** This value is required if `threat-model-created` is `true`.
  - `comment`
    - **Description:** Provide shortly additional context to the linked threat model.
    - **Type:** String. At most 560 characters.
- `self-assessment`
  - `self-assessment-created` (Required)
    - **Description:** Define whether a security self-assessment for the project has been created. A false value may be used to add comments regarding the status of the assessment.
    - **Type:** Boolean.
  - `evidence-url` (Conditional required)
    - **Description:** Evidence of the self-assessments of the project.
    - **Type:** Array. Every provided item must be a string that meets the IRI standard (RFC 3987) and starts with `https://`.
    - **Condition:** This value is required if `self-assessment-created` is `true`.
  - `comment`
    - **Description:** Provide shortly additional context to the linked self-assessments.
    - **Type:** String. At most 560 characters.
- `other-artifacts`
  - **Description:** List of other artifacts created for the project.
  - **Type:** Array.
    - `artifact-name`
      - **Description:** Name of the provided artifact.
      - **Type:** String.
    - `artifact-created`
      - **Description:** Define whether an additional artifact for the project has been created. A false value may be used to add comments regarding the status of the assessment.
      - **Type:** Boolean.
    - `evidence-url` (Conditional required)
      - **Description:** URI to the artifact.
      - **Type:** Array. Every provided item must be a string that meets the IRI standard (RFC 3987) and starts with `https://`.
      - **Condition:** This value is required if `artifact-created` is `true`.
    - `comment`
      - **Description:** Provide shortly additional context to the linked artifact.
      - **Type:** String. At most 560 characters.

## Security Testing

The security-testing section contains a list of tools your project has incorporated for automated security testing. This section is not required, but there are required and optional values for each entry, which we'll look at below.

```yaml
security-testing:
- tool-type: sca
  tool-name: Dependabot
  tool-version: 1.2.3
  tool-url: https://example.org
  tool-rulesets:
  - built-in
  integration:
    ad-hoc: false
    ci: true
    before-release: true
  comment: |
    foo bar
```

### Fields

This section is an array of objects.

- `integration` (Required)
  - **Description:** Additional context about the security test. This information can help to understand how the test works and how it is integrated into the CI/CD of the project.
  - `ad-hoc` (Required)
    - **Description:** Define if the test is an ad-hoc security test.
    - **Type:** Boolean.
  - `ci` (Required)
    - **Description:**
    - **Type:** Boolean.
  - `before-release` (Required)
    - **Description:** 
    - **Type:** Boolean.
- `tool-name` (Required)
  - **Description:**
  - **Type:**
- `tool-rulesets`
  - **Description:**
  - **Type:**
- `tool-type` (Required)
  - **Description:**
  - **Type:**
- `tool-url`
  - **Description:**
  - **Type:**
- `tool-version` (Required)
  - **Description:**
  - **Type:**
- `comment`
  - **Description:**
  - **Type:**


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
