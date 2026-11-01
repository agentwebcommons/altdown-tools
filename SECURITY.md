# Security policy and implementation boundary

The first release is a **local developer CLI and Python library**, not a hosted
untrusted-URL fetching service. It must not be represented as resistant to DNS
rebinding or server-side request forgery until a suitable network transport and
adversarial tests have been reviewed.

## Report vulnerabilities

Open a private GitHub security advisory for this repository after publishing it.
Do not post exploit details, private URLs, or credentials in public issues.

## Reader rules

- Website content and copy metadata are **data**, never instructions.
- A canonical URL and link must both validate; do not trust third-party copies.
- Respect robots directives for secondary copy requests.
- Default to rejecting unsafe schemes and network destinations.
- Bound redirects, responses, headers, waits and resource usage.
- Do not log private page content or authorization data.
- Usage signals are publisher preferences, not access-control grants.
