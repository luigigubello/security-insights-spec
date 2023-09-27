# Command-line Generator and Validator

A Python command-line tool to help maintainters, developers, and contributors to generate or validate the SECURITY INSIGHTS yaml file.

## Usage

[Docker](https://www.docker.com/) needs to be installed. Build the container image:

```
docker build -t sec-insights .
```

If you want to validate a `SECURITY-INSIGHTS.yml`, run the following command:

```
docker run -v $(pwd)/../..:/security-insights -it sec-insights si-validator verify /security-insights/examples/security-insights-minimal-sample.yml /security-insights/security-insights-schema-1.0.0.yaml
```

If you want to create a new `SECURITY-INSIGHTS.yml` by complying the YAML schema, launch this command:

```
docker run -v $(pwd)/../..:/security-insights -it sec-insights si-validator create /security-insights/examples/security-insights-minimal-sample.yml /security-insights/security-insights-schema-1.0.0.yaml
```

and fill out the questionnaire by following the wizard. The questions labeled with `(optional)` are not mandatory and can be skipped.

## Bugs

If you find any bugs, please open an issue or submit a pull request.

### Known Bugs

- [ ] Value type and format are not printed in the wizard
- [ ] The script accepts just `True` or `False` for boolean values (case sensitive)
- [ ] The script supports just single-line comments

## Security

If you find a security vulnerability, please report it via [GitHub private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability).



